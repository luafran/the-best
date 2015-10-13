from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base


class UserQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        question = yield api.get_question_for_user()

        response = {
            "items": question
        }

        self.build_response(response)
