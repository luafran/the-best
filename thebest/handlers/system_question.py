from thebest.common.handlers import base
from thebest.repos import items_repository


class SystemQuestionHandler(base.BaseHandler):
    def get(self):
        user_item = self.get_query_arguments('item')[0]
        system_item = items_repository.get_items()[0]
        self.render('system_question.tpl', user_item=user_item, system_item=system_item)
