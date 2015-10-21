from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class SuggestionsHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):

        suggestion_type = self.get_query_argument(api.TYPE_TAG, None)
        if not suggestion_type:
            raise exceptions.MissingArgumentValue(
                'Missing argument {0}'.format(api.TYPE_TAG))

        if suggestion_type == api.QUESTION_TAG or suggestion_type == api.ANSWER_TAG:
            text = self.get_query_argument(api.TEXT_TAG, None)
            if not text:
                raise exceptions.MissingArgumentValue(
                    'Missing argument {0}'.format(api.TEXT_TAG))

        if suggestion_type == api.ANSWER_TAG:
            question = self.get_query_argument(api.QUESTION_TAG, None)
            if not question:
                raise exceptions.MissingArgumentValue(
                    'Missing argument {0}'.format(api.QUESTION_TAG))

        app = api.Application(self.context, self.application_settings.items_repository)
        if suggestion_type == api.QUESTION_TAG:
            items = yield app.get_question_suggestions(text)
        elif suggestion_type == api.ANSWER_TAG:
            items = yield app.get_answer_suggestions(question, text)
        elif suggestion_type == api.SYSTEM_Q_TAG:
            items = yield app.get_system_suggestions()
        else:
            raise exceptions.InvalidArgumentValue(
                'Invalid value {0} for argument {1}'.format(suggestion_type, api.TYPE_TAG))

        response = {
            "suggestions": items
        }

        self.build_response(response)
