from tornado import gen

from thebest.app import suggestions
from thebest.common.handlers import base


class QuestionSuggestionsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):

        text = self.get_query_arguments('text')[0]

        items = yield suggestions.get_question_suggestions(text)

        response = {
            "suggestions": items
        }

        self.build_response(response)
