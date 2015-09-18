from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class SystemQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        user_question = self.get_query_arguments('user_question')[0]
        system_answer = yield items_repository.get_answer(user_question)
        self.render('user_answer.tpl', user_question=user_question, system_answer=system_answer)
