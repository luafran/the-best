from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class UserAnswerHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        user_category = self.get_query_arguments('user_category')[0]
        system_answer = yield items_repository.get_category_answer(user_category)
        self.render('user_answer.tpl', user_category=user_category, system_answer=system_answer)
