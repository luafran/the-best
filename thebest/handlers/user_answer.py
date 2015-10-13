from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base


class UserAnswerHandler(base.BaseHandler):

    @gen.coroutine
    def post(self):
        item = self.request.body_arguments.get('item')
        response = yield api.add_item(item.get(api.QUESTION_TAG),
                                      item.get(api.ANSWER_TAG))

        self.build_response(response)
