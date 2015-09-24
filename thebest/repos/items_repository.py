import uuid
from tornado import gen
from tornado_elasticsearch import AsyncElasticsearch

QUESTION_TAG = 'q'
ANSWER_TAG = 'a'
TEXT_TAG = 'text'


@gen.coroutine
def get_question_suggestions(text):
    elastic_search = AsyncElasticsearch()
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
def get_question_suggestions2(text):
    elastic_search = AsyncElasticsearch()

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
def get_answer_suggestions(text):

    elastic_search = AsyncElasticsearch()
    body = {
        'query': {
            'prefix': {
                ANSWER_TAG: text.lower()
            }
        }
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)

    print 'result', result
    hits = result.get('hits').get('hits')
    result = [hit.get('_source').get(ANSWER_TAG) for hit in hits]

    raise gen.Return(result)


@gen.coroutine
def get_question_for_user2():
    elastic_search = AsyncElasticsearch()
    body = {
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source').get(QUESTION_TAG) for hit in hits]
    item = {QUESTION_TAG: result[0]} if result else None
    raise gen.Return(item)


@gen.coroutine
def get_question_for_user():
    elastic_search = AsyncElasticsearch()

    query = {
        "filtered": {
            "filter": {
                "missing": {
                    "field": "a"
                }
            }
        }
    }

    body = {
        "query": query
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source') for hit in hits]

    item = {
        QUESTION_TAG: result[0].get(QUESTION_TAG)
    } if result else None

    raise gen.Return(item)


@gen.coroutine
def get_best_answer2(question):
    elastic_search = AsyncElasticsearch()
    params = {
        'q': QUESTION_TAG + ':' + question
    }
    result = yield elastic_search.search(index='the-best-test',
                                         doc_type='item',
                                         params=params)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source') for hit in hits]

    item = {
        QUESTION_TAG: result[0].get(QUESTION_TAG),
        ANSWER_TAG: result[0].get(ANSWER_TAG)
    } if result else None
    raise gen.Return(item)


@gen.coroutine
def get_best_answer(question):
    elastic_search = AsyncElasticsearch()

    query = {
        "filtered": {
            "filter": {
                "exists": {
                    "field": "a"
                }
            },
            "query": {
                "match": {
                    "q": question
                }
            }
        }
    }

    body = {
        "query": query
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source') for hit in hits]

    item = {
        QUESTION_TAG: result[0].get(QUESTION_TAG),
        ANSWER_TAG: result[0].get(ANSWER_TAG)
    } if result else None

    raise gen.Return(item)


@gen.coroutine
def get_items_q_a(question, answer):
    elastic_search = AsyncElasticsearch()

    query = {
        "bool": {
            "must": [
                {
                    "match": {
                        QUESTION_TAG: question
                    }
                },
                {
                    "match": {
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
    hits = result.get('hits').get('hits')
    items = [hit.get('_source') for hit in hits]
    raise gen.Return(items)


@gen.coroutine
def get_items_q(question):
    elastic_search = AsyncElasticsearch()
    params = {
        'q': QUESTION_TAG + ':' + question
    }
    result = yield elastic_search.search(index='the-best-test',
                                         doc_type='item',
                                         params=params)
    hits = result.get('hits').get('hits')

    items = [hit.get('_source') for hit in hits]

    raise gen.Return(items)


@gen.coroutine
def add_item(question, answer):
    elastic_search = AsyncElasticsearch()

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

    elastic_search.index(index='the-best-test', doc_type='item', body=body, id=item_id)

    raise gen.Return(None)
