from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


# pylint: disable=arguments-differ
class ItemsHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self, item_id):  # pylint: disable=unused-argument
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

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self, item_id):  # pylint: disable=unused-argument
        item = self.request.body_arguments.get(api.ITEM_TAG)
        if not item:
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.ITEM_TAG))
        elif item.get(api.ANSWER_TAG):
            response = exceptions.InvalidArgument('Item "{0}" field should be null'.format(api.ANSWER_TAG))
        else:
            response = yield api.add_item(item.get(api.QUESTION_TAG), None)

        if not response:
            response = exceptions.DatabaseOperationError("Item not inserted")

        self.build_response(response)

    @decorators.api_key_authorization
    @gen.coroutine
    def put(self, item_id):
        item = self.request.body_arguments.get(api.ITEM_TAG)
        if not item:
            response = exceptions.MissingArgumentValue('Missing argument {0}'.format(api.ITEM_TAG))
        else:
            response = yield api.update_item_answer(item_id, item.get(api.ANSWER_TAG))

        self.build_response(response)
