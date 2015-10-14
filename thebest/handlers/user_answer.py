from tornado import gen

from thebest.app import api
from thebest.common import exceptions
from thebest.common.handlers import base


class UserAnswerHandler(base.BaseHandler):

    @gen.coroutine
    def post(self):
        item = self.request.body_arguments.get(api.ITEM_TAG)
        if not item:
            response = exceptions.MissingArgumentValue('Missing {0} in body'.format(api.ITEM_TAG))
        elif not (item.get(api.QUESTION_TAG) and item.get(api.ANSWER_TAG)):
            response = exceptions.MissingArgumentValue(
                'Missing "{0}" or "{1}" field in body'.format(api.QUESTION_TAG, api.ANSWER_TAG))
        else:
            response = yield api.process_user_answer(item.get(api.QUESTION_TAG), item.get(api.ANSWER_TAG))

        self.build_response(response)
