from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class UserQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        items = yield api.get_question_for_user()

        response = {
            "items": items
        }

        self.build_response(response)
