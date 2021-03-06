from itertools import groupby
import uuid
from tornado import gen
from tornado_elasticsearch import AsyncElasticsearch
import elasticsearch.exceptions

from thebest.common import exceptions

ID_TAG = '_id'
HITS_TAG = 'hits'
TOTAL_TAG = 'total'
SOURCE_TAG = '_source'
CREATED_TAG = 'created'
QUESTION_TAG = 'q'
ANSWER_TAG = 'a'
TEXT_TAG = 'text'
VOTES_TAG = 'votes'


ELASTIC_SEARCH_ENDPOINT = '52.88.14.176'


@gen.coroutine
def get_question_suggestions2(text):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    params = {
        'search_type': 'count'
    }

    body = {
        "query": {
            "prefix": {
                QUESTION_TAG: text
            }
        },
        "aggs": {
            "questions": {
                "terms": {
                    "field": QUESTION_TAG
                }
            }
        }
    }

    result = yield elastic_search.search(index='the-best-test',
                                         doc_type='item',
                                         body=body,
                                         params=params)
    buckets = result.get('aggregations').get('questions').get('buckets')
    result = [bucket.get('key') for bucket in buckets]
    raise gen.Return(result)


@gen.coroutine
def get_question_suggestions(text):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)
    body = {
        'query': {
            'prefix': {
                QUESTION_TAG: text.lower()
            }
        }
    }

    try:
        result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
        hits = result.get(HITS_TAG).get(HITS_TAG)
        result = [hit.get(SOURCE_TAG).get(QUESTION_TAG)
                  for hit in sorted(hits, key=lambda x: x.get(SOURCE_TAG).get(QUESTION_TAG))]
        # Remove duplicates
        result = [key for key, _ in groupby(result, lambda x: x)]
    except elasticsearch.exceptions.ElasticsearchException as ex:
        raise exceptions.DatabaseOperationError('{0}'.format(ex.message))

    raise gen.Return(result)


@gen.coroutine
def get_answer_suggestions(question, text):  # pylint: disable=unused-argument

    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    query = {
        "bool": {
            "must": [
                {
                    "match_phrase": {
                        QUESTION_TAG: question
                    }
                },
                {
                    "prefix": {
                        ANSWER_TAG: text.lower()
                    }
                }
            ]
        }
    }

    body = {
        'query': query
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)

    hits = result.get(HITS_TAG).get(HITS_TAG)
    result = [hit.get(SOURCE_TAG).get(ANSWER_TAG) for hit in hits]

    raise gen.Return(result)


@gen.coroutine
def get_system_questions():
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    query = {
        "filtered": {
            "filter": {
                "missing": {
                    "field": ANSWER_TAG
                }
            }
        }
    }

    body = {
        "query": query
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get(HITS_TAG)
    total = hits.get('total')
    if total == 0:
        print "No item without answer"
        hits = yield _get_all_items()

    items = []
    for hit in hits.get('hits'):
        question = hit.get('_source').get(QUESTION_TAG)
        item = {QUESTION_TAG: question}
        items.append(item)

    raise gen.Return(items)


@gen.coroutine
def get_best_answers(question):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    query = {
        "filtered": {
            "filter": {
                "exists": {
                    "field": ANSWER_TAG
                }
            },
            "query": {
                "match": {
                    QUESTION_TAG: question
                }
            }
        }
    }

    body = {
        "query": query,
        "sort": {"votes": {"order": "desc"}}
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    total = result.get(HITS_TAG).get('total')
    if total == 0:
        result = yield _get_items_with_q_and_no_a(question)

    hits = result.get(HITS_TAG).get(HITS_TAG)

    items = []
    for hit in hits:
        source = hit.get(SOURCE_TAG)
        item = {
            ANSWER_TAG: source.get(ANSWER_TAG)
        }
        items.append(item)

    raise gen.Return(items)


@gen.coroutine
def add_question(question):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    item_id = str(uuid.uuid4())
    body = {
        QUESTION_TAG: question,
        'suggest': {
            'input': question,
            'output': question,
            'payload': {
                'item_id': item_id
            },
            'weight': 1
        }
    }

    # Two yields? yes!
    result = yield elastic_search.create(index='the-best-test', doc_type='item', id=item_id, body=body)
    result = yield result

    raise gen.Return(result)


@gen.coroutine
def add_answer(question, answer):

    hits = yield _get_items_with_q_and_no_a(question)
    hits = hits.get(HITS_TAG)
    total = hits.get('total')
    if total > 0:
        # We have an item with this question and no answer
        # This is a rae condition!!! Another instance may be updating this item at the same time
        print "Add answer to question"
        hit = hits.get(HITS_TAG)[0]
        item_id = hit.get(ID_TAG)
        item = hit.get(SOURCE_TAG)
        item[ANSWER_TAG] = answer
        yield _update_item(item_id, item)
    else:
        # Do we have this items?
        hits = yield _get_items_with_q_and_a(question, answer)
        total = hits.get('total')
        if total > 0:
            # Yes, we have to add a vote
            # This is a rae condition!!! Another instance may be updating this item at the same time
            hit = hits.get(HITS_TAG)[0]
            item_id = hit.get(ID_TAG)
            item = hit.get(SOURCE_TAG)
            item[VOTES_TAG] = item.get(VOTES_TAG, 0) + 1
            yield _update_item(item_id, item)
        else:
            # No, we have to add a new item with this q and a
            yield _add_item(question, answer)

    raise gen.Return(None)


@gen.coroutine
def _get_items_with_q_and_a(question, answer):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    query = {
        "bool": {
            "must": [
                {
                    "match_phrase": {
                        QUESTION_TAG: question
                    }
                },
                {
                    "match_phrase": {
                        ANSWER_TAG: answer
                    }
                }
            ]
        }
    }

    body = {
        "query": query
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get(HITS_TAG)
    raise gen.Return(hits)


@gen.coroutine
def _get_items_with_q_and_no_a(question):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    query = {
        "match_phrase": {
            QUESTION_TAG: question
        }
    }

    query_filter = {
        "missing": {
            "field": ANSWER_TAG
        }
    }

    body = {
        "query": {
            "filtered": {
                "query": query,
                "filter": query_filter
            }
        }
    }

    hits = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    raise gen.Return(hits)


@gen.coroutine
def _get_items_with_question(question):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    params = {
        QUESTION_TAG: QUESTION_TAG + ':' + question
    }

    hits = yield elastic_search.search(index='the-best-test', doc_type='item', params=params)

    raise gen.Return(hits)


@gen.coroutine
def _get_all_items():
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    result = yield elastic_search.search(index='the-best-test',
                                         doc_type='item')
    hits = result.get(HITS_TAG)
    raise gen.Return(hits)


@gen.coroutine
def _get_item(item_id):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    try:
        item = yield elastic_search.get(index='the-best-test', doc_type='item', id=item_id)
    except elasticsearch.exceptions.NotFoundError:
        raise exceptions.NotFound('item id {0}'.format(item_id))
    except elasticsearch.exceptions.ElasticsearchException as ex:
        raise exceptions.DatabaseOperationError('ex: {0}'.format(ex.message))

    raise gen.Return(item)


@gen.coroutine
def _add_item(question, answer):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    item_id = str(uuid.uuid4())
    body = {
        QUESTION_TAG: question,
        ANSWER_TAG: answer,
        'suggest': {
            'input': question,
            'output': question,
            'payload': {
                'item_id': item_id
            },
            'weight': 1
        }
    }

    # Two yields? yes!
    result = yield elastic_search.create(index='the-best-test', doc_type='item', id=item_id, body=body)
    result = yield result

    raise gen.Return(result)


@gen.coroutine
def _update_item(item_id, item):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    try:
        result = yield elastic_search.index(index='the-best-test', doc_type='item', id=item_id, body=item)
        raise gen.Return(result)
    except elasticsearch.exceptions.NotFoundError:
        raise gen.Return(exceptions.NotFound('item id {0}'.format(item_id)))
    except elasticsearch.exceptions.ElasticsearchException as ex:
        raise gen.Return(exceptions.DatabaseOperationError('ex: {0}'.format(ex.message)))
