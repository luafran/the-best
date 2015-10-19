from random import randrange
from tornado import gen
from thebest.repos import items_repository

# These are the names used externally against clients
# Do not confuse with names used internally in our repository
ID_TAG = 'id'
ITEM_TAG = 'item'
ITEMS_TAG = 'items'
QUESTION_TAG = 'q'
ANSWER_TAG = 'a'
TEXT_TAG = 'text'
TYPE_TAG = 'type'


class Application(object):

    def __init__(self, repository):
        self.items_repository = repository

    @gen.coroutine
    def get_question_suggestions(self, text):

        # ToDo: Return from repository dict with text key

        items = yield self.items_repository.get_question_suggestions(text)

        suggestions = []
        for suggestion in items:
            suggestions.append(suggestion)

        raise gen.Return(suggestions)

    @gen.coroutine
    def get_answer_suggestions(self, question, text):

        # ToDo: return answers only for this question
        # ToDo: Return from repository dict with text key

        items = yield self.items_repository.get_answer_suggestions(question, text)

        suggestions = []
        for suggestion in items:
            suggestions.append(suggestion)

        raise gen.Return(suggestions)

    @gen.coroutine
    def get_best_answer(self, question):
        items = yield self.items_repository.get_best_answers(question)

        raise gen.Return(items[0])

    @gen.coroutine
    def add_question(self, question):
        yield self.items_repository.add_question(question)
        raise gen.Return(None)

    @gen.coroutine
    def get_system_question(self):
        items = yield self.items_repository.get_system_questions()
        total = len(items)
        rand_index = randrange(total-1)
        item = items[rand_index] if items else None

        raise gen.Return(item)

    @gen.coroutine
    def process_user_answer(self, question, answer):
        # ToDo: convert external item to internal item
        result = yield self.items_repository.add_answer(question, answer)
        raise gen.Return(result)
