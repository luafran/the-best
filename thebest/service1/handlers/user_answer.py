from thebest.common.handlers import base
from thebest.service1.repos import items_repository

class UserAnswerHandler(base.BaseHandler):
    def get(self):
        user_item = self.get_query_arguments('user_item')[0]
        system_answer = items_repository.get_item_answer(user_item)
        self.render('user_answer.tpl', user_item=user_item, system_answer=system_answer)
