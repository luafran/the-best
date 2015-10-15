from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class BestAnswerHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):
        question = self.get_query_argument(api.QUESTION_TAG, None)
        if not question:
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.QUESTION_TAG))
        else:
            items = yield api.get_best_answer(question)

            response = {
                "items": items
            }

        self.build_response(response)
