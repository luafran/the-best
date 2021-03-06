from tornado import gen

# These are the names used externally against clients
# Do not confuse with names used internally in our repository
LIMIT_TAG = 'limit'
ID_TAG = 'id'
ITEM_TAG = 'item'
ITEMS_TAG = 'items'
QUESTION_TAG = 'q'
ANSWER_TAG = 'a'
TEXT_TAG = 'text'
TYPE_TAG = 'type'
SYSTEM_Q_TAG = 'sysq'


class Application(object):

    def __init__(self, context, repository):
        self.context = context
        self.items_repository = repository

    @gen.coroutine
    def get_question_suggestions(self, text):
        suggestions = yield self.items_repository.get_question_suggestions(text)
        raise gen.Return(suggestions)

    @gen.coroutine
    def get_answer_suggestions(self, question, text):
        suggestions = yield self.items_repository.get_answer_suggestions(question, text)
        raise gen.Return(suggestions)

    @gen.coroutine
    def get_system_suggestions(self):
        suggestions = yield self.items_repository.get_system_suggestions()
        raise gen.Return(suggestions)

    @gen.coroutine
    def get_best_answers(self, question, limit):
        items = yield self.items_repository.get_best_answers(question, limit)
        raise gen.Return(items)

    @gen.coroutine
    def add_question(self, question):
        yield self.items_repository.add_question(question)
        raise gen.Return(None)

    @gen.coroutine
    def get_system_questions(self, question, limit):
        items = yield self.items_repository.get_system_questions(question, limit)
        raise gen.Return(items)

    @gen.coroutine
    def process_user_answer(self, question, answer):
        # ToDo: convert external item to internal item
        result = yield self.items_repository.add_answer(question, answer)
        raise gen.Return(result)

    @gen.coroutine
    def process_action(self, action_type, question, answer):
        result = yield self.items_repository.add_action(action_type, question, answer)
        raise gen.Return(result)
