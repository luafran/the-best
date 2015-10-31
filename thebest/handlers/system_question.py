from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class SystemQuestionHandlerV1(base.BaseHandler):

    @decorators.session_authorization
    @gen.coroutine
    def get(self):

        limit = int(self.get_query_argument(api.LIMIT_TAG, '1'))

        question = self.get_query_argument(api.QUESTION_TAG, None)
        if not question:
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.QUESTION_TAG))
        else:
            app = api.Application(self.context, self.application_settings.items_repository)
            items = yield app.get_system_questions(question, limit)
            response = {'questions': items[0:limit] if items else []}

        self.build_response(response)
