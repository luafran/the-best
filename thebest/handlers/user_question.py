from tornado import gen

from thebest.app import api
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class UserQuestionHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):
        items = yield api.get_question_for_user()

        response = {
            "items": items
        }

        self.build_response(response)
