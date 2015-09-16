from tornado import gen
from tornado_elasticsearch import AsyncElasticsearch


@gen.coroutine
def get_category_suggestions(prefix):
    elastic_search = AsyncElasticsearch()
    body = {
        'item-suggest': {
            'text': prefix,
            'completion': {
                'field': 'suggest'
            }
        }
    }

    result = yield elastic_search.suggest(index='the-best-test', body=body)
    options = result.get('item-suggest')[0].get('options')
    result = [option.get('text') for option in options]

    raise gen.Return(result)


@gen.coroutine
def get_category_for_user_question():
    elastic_search = AsyncElasticsearch()
    body = {
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='item', body=body)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source').get('category') for hit in hits]
    selected_answer = result[0]
    raise gen.Return(selected_answer)


@gen.coroutine
def get_category_answer(category):
    elastic_search = AsyncElasticsearch()
    params = {
        'q': 'category:' + category
    }
    result = yield elastic_search.search(index='the-best-test', doc_type='item', params=params)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source').get('answer') for hit in hits]
    selected_answer = result[0]
    raise gen.Return(selected_answer)

