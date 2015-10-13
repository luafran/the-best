from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base


class ItemsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        question = self.get_query_argument(api.QUESTION_TAG)
        answer = self.get_query_argument(api.ANSWER_TAG, None)
        if answer:
            items = yield api.get_items_q_a(question, answer)
        else:
            items = yield api.get_items_q(question)

        response = {
            "items": items
        }

        self.build_response(response)

    @gen.coroutine
    def post(self):
        item = self.request.body_arguments.get(api.ITEM_TAG)
        if not item:
            self.build_response(exceptions.MissingArgumentValue(
                'Missing argument {0}'.format(api.ITEM_TAG)))
            return
        response = yield api.add_item(item.get(api.QUESTION_TAG),
                                      item.get(api.ANSWER_TAG))

        if not response:
            response = exceptions.DatabaseOperationError("Item not inserted")
        self.build_response(response)
