from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


# pylint: disable=arguments-differ
class QuestionHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self):
        item = self.request.body_arguments
        if not item.get(api.QUESTION_TAG):
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.QUESTION_TAG))
        else:
            app = api.Application(self.context, self.application_settings.items_repository)
            response = yield app.add_question(item.get(api.QUESTION_TAG))

        self.build_response(response)
