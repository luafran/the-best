from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class UserQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        user_question = self.get_query_argument('user_question').lower()

        system_answer = yield api.get_best_answer(user_question)
        self.support.notify_debug('system_answer: {0}'.format(system_answer))
        if system_answer:
            item = yield api.get_question_for_user()
            self.render('system_question.tpl',
                        user_question=user_question,
                        system_question=item.get(api.QUESTION_TAG))
        else:
            self.support.notify_debug('First time for question: {0}'.format(user_question))
            existing_item = yield api.get_items_q(user_question)
            print "###### existing_item:", existing_item
            if not existing_item:
                api.add_item(user_question, None)
            self.render('first_time_question.tpl', user_question=user_question)
