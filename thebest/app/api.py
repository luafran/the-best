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


@gen.coroutine
def get_question_suggestions(text):

    # TODO: Return from repository dict with text key

    items = yield items_repository.get_question_suggestions(text)

    suggestions = []
    for item in items:
        suggestion = {
            TEXT_TAG: item
        }

        suggestions.append(suggestion)

    raise gen.Return(suggestions)


@gen.coroutine
def get_answer_suggestions(question, text):

    # TODO: return answers only for this question
    # TODO: Return from repository dict with text key

    items = yield items_repository.get_answer_suggestions(question, text)

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
    items = []
    include_id = True
    hits = yield items_repository.get_items_without_answer()
    total = hits.get(items_repository.TOTAL_TAG)
    if total == 0:
        print "No item without answer"
        # TODO: This is returning just one page, we have to change that so we get the total and choose a random item
        # TODO: from the database directly, not from the hits array returned in this query
        hits = yield items_repository.get_items()
        include_id = False
    total = hits.get(items_repository.TOTAL_TAG)
    hits = hits.get(items_repository.HITS_TAG)
    print 'total:', total
    print 'hits:', hits

    if total > 0:
        rand_index = randrange(len(hits))
        print 'rand_index:', rand_index
        item_for_user = hits[rand_index]
        item = {
            QUESTION_TAG: item_for_user.get(items_repository.SOURCE_TAG).get(items_repository.QUESTION_TAG)
        }

        if include_id and item_for_user.get(items_repository.ID_TAG):
            item[ID_TAG] = item_for_user.get(items_repository.ID_TAG)

        items.append(item)
    else:
        items = []

    raise gen.Return(items)


@gen.coroutine
def get_items_q_a(question, answer):
    hits = yield items_repository.get_items_q_a(question.lower(), answer.lower())
    hits = hits.get(items_repository.HITS_TAG)
    result = [hit.get(items_repository.SOURCE_TAG) for hit in hits]

    raise gen.Return(result)


@gen.coroutine
def get_items_q(question):
    result_list = []
    hits = yield items_repository.get_items_q(question.lower())
    hits = hits.get(items_repository.HITS_TAG)

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

    if result.get(items_repository.CREATED_TAG):
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
