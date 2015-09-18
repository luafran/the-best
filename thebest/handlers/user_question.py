from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class UserQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        user_question = self.get_query_arguments('user_question')[0]
        system_answer = yield items_repository.get_answer(user_question)
        if system_answer:
            system_question = yield items_repository.get_question_for_user()
            self.render('system_question.tpl', user_question=user_question, system_question=system_question)
        else:
            self.render('first_time_question.tpl', user_question=user_question)
