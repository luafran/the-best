from thebest.common.handlers import base
from thebest.repos import items_repository


class UserQuestionHandler(base.BaseHandler):
    def get(self):
        items = items_repository.get_items()
        self.render('user_question.tpl', items=items)
