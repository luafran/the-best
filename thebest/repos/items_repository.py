import uuid
from tornado import gen
from tornado_elasticsearch import AsyncElasticsearch

ID_TAG = '_id'
HITS_TAG = 'hits'
SOURCE_TAG = '_source'
QUESTION_TAG = 'q'
ANSWER_TAG = 'a'
TEXT_TAG = 'text'


ELASTIC_SEARCH_ENDPOINT = '52.88.14.176'


@gen.coroutine
def get_question_suggestions(text):
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
def get_question_suggestions2(text):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)
    body = {
        'item-suggest': {
            TEXT_TAG: text,
            'completion': {
                'field': 'suggest'
            }
        }
    }

    result = yield elastic_search.suggest(index='the-best-test', body=body)
    options = result.get('item-suggest')[0].get('options')
    result = [option.get(TEXT_TAG) for option in options]

    raise gen.Return(result)


@gen.coroutine
def get_answer_suggestions(text):

    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)
    body = {
        'query': {
            'prefix': {
                ANSWER_TAG: text.lower()
            }
        }
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)

    hits = result.get(HITS_TAG).get(HITS_TAG)
    result = [hit.get(SOURCE_TAG).get(ANSWER_TAG) for hit in hits]

    raise gen.Return(result)


@gen.coroutine
def get_items_without_answer():
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

    raise gen.Return(hits)


@gen.coroutine
def get_best_answer(question):
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
        "query": query
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get(HITS_TAG)
    raise gen.Return(hits)


@gen.coroutine
def get_items_q_a(question, answer):
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
def get_items_q(question):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    params = {
        QUESTION_TAG: QUESTION_TAG + ':' + question
    }

    results = yield elastic_search.search(index='the-best-test',
                                          doc_type='item',
                                          params=params)
    hits = results.get(HITS_TAG)
    raise gen.Return(hits)


@gen.coroutine
def get_items():
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    result = yield elastic_search.search(index='the-best-test',
                                         doc_type='item')
    hits = result.get(HITS_TAG)
    raise gen.Return(hits)


@gen.coroutine
def add_item(question, answer):
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

    elastic_search.create(index='the-best-test', doc_type='item', id=item_id, body=body)

    raise gen.Return(None)


@gen.coroutine
def update_item_answer(item_id, answer):
    elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

    item = yield elastic_search.get(index='the-best-test', doc_type='item', id=item_id)
    item[SOURCE_TAG][ANSWER_TAG] = answer

    elastic_search.index(index='the-best-test', doc_type='item', id=item_id, body=item[SOURCE_TAG])
