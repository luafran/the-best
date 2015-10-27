from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class BestAnswerHandlerV1(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):

        limit = int(self.get_query_argument(api.LIMIT_TAG, '1'))

        question = self.get_query_argument(api.QUESTION_TAG, None)
        if not question:
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.QUESTION_TAG))
        else:
            app = api.Application(self.context, self.application_settings.items_repository)
            items = yield app.get_best_answers(question, limit)
            response = items[0] if items else None

        self.build_response(response)


class BestAnswerHandlerV2(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):

        limit = int(self.get_query_argument(api.LIMIT_TAG, '1'))

        question = self.get_query_argument(api.QUESTION_TAG, None)
        if not question:
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.QUESTION_TAG))
        else:
            app = api.Application(self.context, self.application_settings.items_repository)
            items = yield app.get_best_answers(question, limit)
            response = {'answers': items[0:limit] if items else []}

        self.build_response(response)
