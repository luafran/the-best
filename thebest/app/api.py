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

        # TODO: Return from repository dict with text key

        items = yield self.items_repository.get_question_suggestions(text)

        suggestions = []
        for item in items:
            suggestion = {

                TEXT_TAG: item
            }

            suggestions.append(suggestion)

        raise gen.Return(suggestions)


    @gen.coroutine
    def get_answer_suggestions(self, question, text):

        # TODO: return answers only for this question
        # TODO: Return from repository dict with text key

        items = yield self.items_repository.get_answer_suggestions(question, text)

        suggestions = []
        for item in items:
            suggestion = {
                TEXT_TAG: item
            }

            suggestions.append(suggestion)

        raise gen.Return(suggestions)

@gen.coroutine
def get_best_answer(question):
    hits = yield items_repository.get_best_answer(question)
    hits = hits.get(items_repository.HITS_TAG)

    items = []
    for hit in hits:
        source = hit.get(items_repository.SOURCE_TAG)
        item = {
            QUESTION_TAG: source.get(QUESTION_TAG),
            ANSWER_TAG: source.get(ANSWER_TAG)
        }
        items.append(item)

    raise gen.Return(items)


@gen.coroutine
def get_question_for_user():
    hits = yield items_repository.get_items_without_answer()
    total = hits.get('total')
    if total == 0:
        print "No item without answer"
        hits = yield items_repository.get_items()
    total = hits.get('total')
    result = [item.get('_source') for item in hits.get('hits')]
    rand_index = randrange(total-1)
    item = {
        QUESTION_TAG: result[rand_index].get(QUESTION_TAG)
    } if result else None

    raise gen.Return(item)


@gen.coroutine
def get_items_q_a(question, answer):
    hits = yield items_repository.get_items_q_a(question.lower(), answer.lower())
    hits = hits.get(items_repository.HITS_TAG)
    result = [hit.get('_source') for hit in hits]

    raise gen.Return(result)


@gen.coroutine
def get_items_q(question):
    result_list = []
    hits = yield items_repository.get_items_q(question.lower())
    hits = hits.get('hits')

    for hit in hits:
        source = hit.get(items_repository.SOURCE_TAG)
        result_item = {
            ID_TAG: hit.get(items_repository.ID_TAG),
            QUESTION_TAG: source.get(items_repository.QUESTION_TAG),
            ANSWER_TAG: source.get(items_repository.ANSWER_TAG)
        }

        result_list.append(result_item)

    raise gen.Return(result_list)


@gen.coroutine
def add_item(question, answer):
    result = yield items_repository.add_item(question, answer)

    if result.get('created'):
        item = {
            ITEM_TAG: {
                ID_TAG: result.get(items_repository.ID_TAG),
                QUESTION_TAG: question,
                ANSWER_TAG: answer
            }
        }

        result = item
    else:
        result = None

    raise gen.Return(result)


@gen.coroutine
def update_item_answer(item_id, answer):
    # TODO: convert external item to internal item
    result = yield items_repository.update_item_answer(item_id, answer)
    raise gen.Return(result)