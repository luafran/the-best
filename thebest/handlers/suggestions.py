from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class QuestionSuggestionsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):

        text = self.get_query_argument('text')

        items = yield api.get_question_suggestions(text)

        response = {
            "suggestions": items
        }

        self.build_response(response)


class AnswerSuggestionsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):

        text = self.get_query_argument('text')

        items = yield api.get_answer_suggestions(text)

        response = {
            "suggestions": items
        }

        self.build_response(response)
