from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class SystemQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        # Add or update this Q&A item
        system_question = self.get_query_argument('system_question').lower()
        user_answer = self.get_query_argument('user_answer').lower()
        existing_items = yield api.get_items(system_question, user_answer)
        self.support.notify_debug("existing_items: {0}".format(existing_items))
        if existing_items:
            self.support.notify_debug(
                "Item already exists for question: {0} and answer: {1}".format(system_question,
                                                                               user_answer))
            # TODO: Add a vote to this item
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
