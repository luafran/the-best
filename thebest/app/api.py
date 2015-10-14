from random import randrange
from tornado import gen
from thebest.common import exceptions
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

    # ToDo: Return from repository dict with text key

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

    # ToDo: return answers only for this question
    # ToDo: Return from repository dict with text key

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
    hits = yield items_repository.get_items_with_answer_to_q(question)
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
        # ToDo: This is returning just one page, we have to change that so we get the total and choose
        # ToDo: a random item from the database directly, not from the hits array returned in this query
        hits = yield items_repository.get_all_items()
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
def process_user_answer(question, answer):
    items_with_same_answer = yield get_items_q_a(question, answer)
    print "items_with_same_answer: {0}".format(items_with_same_answer)
    if items_with_same_answer:
        print "Item already exists for question: {0} and answer: {1}".format(question, answer)
        # ToDo: Check that we have only one item with same answer. What to do in case we have more?
        # ToDo: Add a vote to this item
        response = None
    else:
        # It should not happen that we have an item with this question and no answer since
        # in that case clients should update the answer using PUT to /items/:id
        print "Adding new item for question: {0} and answer: {1}".format(question, answer)
        response = yield add_item(question, answer)

    # ToDo: Check what should we return here
    raise gen.Return(response)


@gen.coroutine
def get_items_q_a(question, answer):
    hits = yield items_repository.get_items_with_q_and_a(question.lower(), answer.lower())
    hits = hits.get(items_repository.HITS_TAG)
    result = [hit.get(items_repository.SOURCE_TAG) for hit in hits]

    raise gen.Return(result)


@gen.coroutine
def get_items_q(question):
    result_list = []
    hits = yield items_repository.get_items_with_question(question.lower())
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
    try:
        hit = yield items_repository.get_item(item_id)
        item = hit.get(items_repository.SOURCE_TAG)
        item[items_repository.ANSWER_TAG] = answer
        result = yield items_repository.update_item(item_id, item)
        result = None
    except exceptions.NotFound as ex:
        result = ex
    except exceptions.DatabaseOperationError as ex:
        result = ex

    raise gen.Return(result)
