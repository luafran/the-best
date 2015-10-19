from tornado import gen
import tormysql
from thebest.common import settings
from thebest.common import exceptions

QUESTION_TAG = 'q'
ANSWER_TAG = 'a'
TEXT_TAG = 'text'
ID_TAG = 'id'
VOTES_TAG = 'votes'
LAST_VOTE_TAG = 'last_vote'


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
                        result.append({
                            TEXT_TAG: row[0]
                        })
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
                        result.append({
                            TEXT_TAG: row[0]
                        })
        raise gen.Return(result)

    @gen.coroutine
    def get_system_questions(self):
        result = []
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = "SELECT id, "\
                                "       question, "\
                                "       (SELECT count(*) "\
                                "          FROM actions a "\
                                "         WHERE a.answer_question_id = q.id) as votes, "\
                                "       (SELECT max(ts) "\
                                "          FROM actions a "\
                                "         WHERE a.answer_question_id = q.id) as last_vote "\
                                " FROM questions q "\
                                "ORDER BY votes, last_vote;"
                    yield cursor.execute(statement)
                    for row in cursor:
                        result.append({
                            ID_TAG: row[0],
                            QUESTION_TAG: row[1],
                            VOTES_TAG: row[2],
                            LAST_VOTE_TAG: (row[3].isoformat() if row[3] else None),
                        })
        raise gen.Return(result)

    @gen.coroutine
    def get_best_answers(self, question):
        result = []
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = "SELECT a.id as answer_id, "\
                                "       a.answer, "\
                                "       (SELECT count(*) " \
                                "          FROM actions ac " \
                                "         WHERE ac.answer_question_id = q.id) as votes" \
                                "  FROM questions q " \
                                "       LEFT OUTER JOIN answers a " \
                                "         ON a.question_id = q.id " \
                                " WHERE q.id = sha1('{0}') " \
                                " ORDER BY votes DESC "\
                                .format(question)
                    yield cursor.execute(statement)
                    for row in cursor:
                        result.append({
                            ID_TAG: row[0],
                            ANSWER_TAG: row[1],
                            VOTES_TAG: row[2],
                        })
        raise gen.Return(result)

    @gen.coroutine
    def add_question(self, question):
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = "INSERT INTO questions(id, question) " \
                                " VALUES(sha1('{0}'), '{0}');"\
                        .format(question)
                    yield cursor.execute(statement)

    @gen.coroutine
    def add_answer(self, question, answer):
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = "SELECT count(*) " \
                                "  FROM questions " \
                                " WHERE id = sha1('{0}'); " \
                        .format(question)
                    yield cursor.execute(statement)
                    if cursor.fetchone()[0] == 0:
                        raise exceptions.InvalidArgument('The question: {0} does not exist'.format(question))

                    statement = "INSERT IGNORE INTO answers(question_id, id, answer)" \
                                " VALUES(sha1('{0}'), sha1('{1}'), '{1}');"\
                        .format(question, answer)
                    yield cursor.execute(statement)

                    statement = "INSERT INTO actions(answer_question_id, answer_id, type)" \
                                " VALUES(sha1('{0}'), sha1('{1}'), '{1}');"\
                        .format(question, answer, "VOTE")
                    yield cursor.execute(statement)
