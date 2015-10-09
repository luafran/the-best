from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class SystemQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        # Add or update this Q&A item
        system_question = self.get_query_argument('system_question').lower()
        user_answer = self.get_query_argument('user_answer').lower()
        items_with_same_answer = yield api.get_items_q_a(system_question, user_answer)
        self.support.notify_debug("items_with_same_answer: {0}".format(items_with_same_answer))
        if items_with_same_answer:
            self.support.notify_debug(
                "Item already exists for question: {0} and answer: {1}".format(system_question,
                                                                               user_answer))
            # TODO: Add a vote to this item
        else:
            items_with_no_answer = yield api.get_items_q(system_question)
            self.support.notify_debug("items_with_no_answer: {0}".format(items_with_no_answer))
            if items_with_no_answer:
                item_id = items_with_no_answer[0].get(api.ID_TAG)
                self.support.notify_debug(
                    "Updating item: {0} with answer: {1}".format(item_id,
                                                                 user_answer))
                api.update_item_answer(item_id, user_answer)
            else:

                self.support.notify_debug(
                    "Adding new item for question: {0} and answer: {1}".format(system_question,
                                                                               user_answer))
                api.add_item(system_question, user_answer)

        # Find and show answer for user question
        user_question = self.get_query_argument('user_question')
        item = yield api.get_best_answer(user_question)
        self.render('user_answer.tpl',
                    user_question=user_question,
                    system_answer=item.get(api.ANSWER_TAG))
