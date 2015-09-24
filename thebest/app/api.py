from tornado import gen

from thebest.repos import items_repository

QUESTION_TAG = items_repository.QUESTION_TAG
ANSWER_TAG = items_repository.ANSWER_TAG
TEXT_TAG = items_repository.TEXT_TAG


@gen.coroutine
def get_question_suggestions(text):

    # TODO: Return from repository dict with text key

    # items = yield items_repository.get_question_suggestions(text)
    items = yield items_repository.get_question_suggestions2(text)

    suggestions = []
    for item in items:
        suggestion = {
            TEXT_TAG: item
        }

        suggestions.append(suggestion)

    raise gen.Return(suggestions)


@gen.coroutine
def get_answer_suggestions(text):

    # TODO: Return from repository dict with text key

    items = yield items_repository.get_answer_suggestions(text)

    suggestions = []
    for item in items:
        suggestion = {
            TEXT_TAG: item
        }

        suggestions.append(suggestion)

    raise gen.Return(suggestions)


@gen.coroutine
def get_best_answer(question):
    answer = yield items_repository.get_best_answer(question)
    raise gen.Return(answer)


@gen.coroutine
def get_question_for_user():
    item = yield items_repository.get_question_for_user()
    raise gen.Return(item)


@gen.coroutine
def get_items(question, answer):
    result = yield items_repository.get_items_q_a(question.lower(), answer.lower())
    raise gen.Return(result)


@gen.coroutine
def item_exists(question):
    result = yield items_repository.get_items_q(question.lower())
    raise gen.Return(result)


@gen.coroutine
def add_item(question, answer):
    result = yield items_repository.add_item(question, answer)
    raise gen.Return(result)
