from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class UserQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        items = yield items_repository.get_items()
        self.render('user_question.tpl', items=items)
