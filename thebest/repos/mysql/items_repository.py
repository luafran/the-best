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

ACTION_VOTE = 'VOTE'


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
                    statement = u"SELECT question " \
                                u"  FROM questions " \
                                u" WHERE MATCH(question) AGAINST('+{0}*' IN BOOLEAN MODE) " \
                                u" LIMIT 10;"\
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
                    statement = u"SELECT answer " \
                                u"  FROM answers " \
                                u" WHERE question_id = sha1('{0}') " \
                                u"   AND MATCH(answer) AGAINST('+{1}*' IN BOOLEAN MODE) " \
                                u" LIMIT 10;"\
                        .format(question.lower(), text)
                    yield cursor.execute(statement)
                    for row in cursor:
                        result.append({
                            TEXT_TAG: row[0]
                        })
        raise gen.Return(result)

    @gen.coroutine
    def get_system_suggestions(self):
        result = []

        cursor = [('restaurante',),
                  ('restaurante de Cordoba',),
                  ('restaurante de sushi de Cordoba',),
                  ('restaurante de Cordoba en zona norte',),
                  ('restaurante de Cordoba abierto al mediodia',)]

        for row in cursor:
            result.append({
                TEXT_TAG: row[0]
            })

        raise gen.Return(result)

    @gen.coroutine
    def get_system_questions(self, question):
        result = []
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = u"SELECT id, "\
                                u"       question, "\
                                u"       (SELECT count(*) "\
                                u"          FROM actions a "\
                                u"         WHERE a.answer_question_id = q.id) as votes, "\
                                u"       (SELECT max(ts) "\
                                u"          FROM actions a "\
                                u"         WHERE a.answer_question_id = q.id) as last_vote "\
                                u" FROM questions q " \
                                u"WHERE q.id <> sha1('{0}') "\
                                u"ORDER BY votes, last_vote " \
                                u"LIMIT 10;"\
                                .format(question.lower())
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
                    statement = u"SELECT a.id as answer_id, "\
                                u"       a.answer, "\
                                u"       (SELECT count(*) " \
                                u"          FROM actions ac " \
                                u"         WHERE ac.answer_question_id = q.id and ac.answer_id = a.id) as votes" \
                                u"  FROM questions q " \
                                u"       LEFT OUTER JOIN answers a " \
                                u"         ON a.question_id = q.id " \
                                u" WHERE q.id = sha1('{0}') " \
                                u" ORDER BY votes DESC " \
                                u" LIMIT 5;"\
                                .format(question.lower())
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
                    statement = u"INSERT INTO questions(id, question) " \
                                u" VALUES(sha1('{0}'), '{1}');"\
                        .format(question.lower(), question)
                    yield cursor.execute(statement)

    @gen.coroutine
    def add_answer(self, question, answer):
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:
                    statement = u"SELECT count(*) " \
                                u"  FROM questions " \
                                u" WHERE id = sha1('{0}'); " \
                        .format(question.lower())
                    yield cursor.execute(statement)
                    if cursor.fetchone()[0] == 0:
                        raise exceptions.InvalidArgument(u'The question: {0} does not exist'.format(question))

                    statement = u"INSERT IGNORE INTO answers(question_id, id, answer)" \
                                u" VALUES(sha1('{0}'), sha1('{1}'), '{2}');"\
                        .format(question.lower(), answer.lower(), answer)
                    yield cursor.execute(statement)

                    yield self.add_action(ACTION_VOTE, question, answer)

    @gen.coroutine
    def add_action(self, action_type, question, answer):
        with (yield self.pool.Connection()) as conn:
                with conn.cursor() as cursor:

                    # Only VOTE so far
                    # ToDo: should this check be here?
                    if action_type == ACTION_VOTE:
                        statement = u"SELECT count(*) " \
                                    u"  FROM answers " \
                                    u" WHERE question_id = sha1('{0}') and id = sha1('{1}'); " \
                            .format(question.lower(), answer.lower())
                        yield cursor.execute(statement)
                        if cursor.fetchone()[0] == 0:
                            raise exceptions.InvalidArgument(u'No answer for question: {0}'.format(question))

                        statement = u"INSERT INTO actions(answer_question_id, answer_id, type)" \
                                    u" VALUES(sha1('{0}'), sha1('{1}'), '{2}');"\
                            .format(question.lower(), answer.lower(), action_type)
                        yield cursor.execute(statement)
                    else:
                        raise exceptions.InvalidArgument(u'Unsupported action type: {0}'.format(action_type))
