from tornado import gen

from thebest.repos import items_repository


@gen.coroutine
def get_question_suggestions(text):

    items = yield items_repository.get_question_suggestions(text)

    suggestions = []
    for item in items:
        suggestion = {
            'text': item,
            'itemId': item
        }

        suggestions.append(suggestion)

    raise gen.Return(suggestions)
