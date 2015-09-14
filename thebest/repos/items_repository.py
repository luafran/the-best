from tornado import gen
from tornado_elasticsearch import AsyncElasticsearch

ITEMS = {
    'car': 'Fiat 128',
    'wine': 'Toro',
    'beer': 'Imperial',
    'movie': 'Back to the future',
    'actor': 'Richard Dean Anderson'
}


@gen.coroutine
def get_items():
    elastic_search = AsyncElasticsearch()
    result = yield elastic_search.search(index='the-best-test')
    hits = result.get('hits').get('hits')
    result = [hit.get('_source').get('name') for hit in hits]
    # raise gen.Return(ITEMS.keys())
    raise gen.Return(result)


@gen.coroutine
def get_item_answer(item):
    raise gen.Return(ITEMS[item])


@gen.coroutine
def get_category_suggestions(prefix):
    elastic_search = AsyncElasticsearch()
    body = {
        'query': {
            'prefix': {
                'name': prefix
            }
        }
    }

    result = yield elastic_search.search(index='the-best-test', doc_type='category', body=body)
    hits = result.get('hits').get('hits')
    result = [hit.get('_source').get('name') for hit in hits]

    raise gen.Return(result)
