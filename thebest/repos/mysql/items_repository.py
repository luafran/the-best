from tornado import gen
import tormysql
from thebest.common import settings


class TheBestRepository(object):
    def __init__(self):
        self.pool = tormysql.ConnectionPool(
            max_connections=settings.MYSQL_MAX_CONNECTIONS,
            idle_seconds=settings.MYSQL_IDLE_SECONDS,
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            db=settings.MYSQL_DB,
            charset=settings.MYSQL_CHARSET
        )

    @gen.coroutine
    def get_question_suggestions(self, text):
        result = []
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = "SELECT question " \
                                "  FROM questions " \
                                " WHERE MATCH(question) AGAINST('+{0}*' IN BOOLEAN MODE);"\
                        .format(text)
                    yield cursor.execute(statement)
                    for row in cursor:
                        result.append(row[0])
        raise gen.Return(result)

    @gen.coroutine
    def get_answer_suggestions(self, question, text):
        result = []
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = "SELECT answer " \
                                "  FROM answers " \
                                " WHERE question_id = sha1('{0}') " \
                                "   AND MATCH(answer) AGAINST('+{1}*' IN BOOLEAN MODE);"\
                        .format(question, text)
                    yield cursor.execute(statement)
                    for row in cursor:
                        result.append(row[0])
        raise gen.Return(result)

"""
    @gen.coroutine
    def get_system_questions(): # change to get_questions_for_user
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
    def get_best_answer(question): # return item array list (sorted by relevance)
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
    def get_items_q_a(question, answer): #?????
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
    def get_items_q(question): #????
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
    def get_items(): # ????
        elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

        result = yield elastic_search.search(index='the-best-test',
                                             doc_type='item')
        hits = result.get(HITS_TAG)
        raise gen.Return(hits)


    @gen.coroutine
    def add_item(question, answer): # insert_question(q)
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
    def update_item_answer(item_id, answer): # insert_answer(q, a)
        elastic_search = AsyncElasticsearch(hosts=ELASTIC_SEARCH_ENDPOINT)

        item = yield elastic_search.get(index='the-best-test', doc_type='item', id=item_id)
        item[SOURCE_TAG][ANSWER_TAG] = answer

        elastic_search.index(index='the-best-test', doc_type='item', id=item_id, body=item[SOURCE_TAG])
"""