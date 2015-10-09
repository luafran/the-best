from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class ItemsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        question = self.get_query_argument(api.QUESTION_TAG)
        answer = self.get_query_argument(api.ANSWER_TAG)
        items = yield api.get_items_q_a(question, answer)

        response = {
            "items": items
        }

        self.build_response(response)


class UserQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        question = yield api.get_question_for_user()

        response = {
            "item": question
        }

        self.build_response(response)


class UserAnswerHandler(base.BaseHandler):

    @gen.coroutine
    def post(self):
        item = self.request.body_arguments.get('item')
        response = yield api.add_item(item.get(api.QUESTION_TAG),
                                      item.get(api.ANSWER_TAG))

        self.build_response(response)


class BestAnswerHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        question = self.get_query_argument(api.QUESTION_TAG)
        answer = yield api.get_best_answer(question)

        response = {
            "item": answer
        }

        self.build_response(response)
