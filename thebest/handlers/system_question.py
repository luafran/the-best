from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class SystemQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        user_category = self.get_query_arguments('category')[0]
        system_category = yield items_repository.get_category_for_user_question()
        self.render('system_question.tpl', user_category=user_category, system_category=system_category)
