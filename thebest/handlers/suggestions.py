from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base


class SuggestionsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):

        suggestion_type = self.get_query_argument(api.TYPE_TAG, None)
        if not suggestion_type:
            self.build_response(exceptions.MissingArgumentValue(
                'Missing argument {0}'.format(api.TYPE_TAG)))
            return

        text = self.get_query_argument(api.TEXT_TAG, None)
        if not text:
            self.build_response(exceptions.MissingArgumentValue(
                'Missing argument {0}'.format(api.TEXT_TAG)))

        if suggestion_type == api.QUESTION_TAG:
            items = yield api.get_question_suggestions(text)
        elif suggestion_type == api.ANSWER_TAG:
            question = self.get_query_argument(api.QUESTION_TAG, None)
            if not question:
                self.build_response(exceptions.MissingArgumentValue(
                    'Missing argument {0}'.format(api.QUESTION_TAG)))
                return
            items = yield api.get_answer_suggestions(question, text)
        else:
            self.build_response(exceptions.InvalidArgumentValue(
                'Invalid value {0} for argument {1}'.format(suggestion_type, api.TYPE_TAG)))
            return

        response = {
            "suggestions": items
        }

        self.build_response(response)
