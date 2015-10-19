from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class UserAnswerHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self):
        item = self.request.body_arguments
        if not (item.get(api.QUESTION_TAG) and item.get(api.ANSWER_TAG)):
            response = exceptions.MissingArgumentValue(
                'Missing "{0}" or "{1}" field in body'.format(api.QUESTION_TAG, api.ANSWER_TAG))
        else:
            app = api.Application(self.application_settings.items_repository)
            response = yield app.process_user_answer(item.get(api.QUESTION_TAG), item.get(api.ANSWER_TAG))

        self.build_response(response)
