from tornado import gen

from thebest.app import api
from thebest.common.handlers import base


class SystemQuestionHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):

        # Add or update this Q&A item
        system_question = self.get_query_argument('system_question').lower()
        user_answer = self.get_query_argument('user_answer').lower()
        yield api.process_user_answer(system_question, user_answer)

        # Find and show answer for user question
        user_question = self.get_query_argument('user_question')
        item = yield api.get_best_answer(user_question)
        self.render('user_answer.tpl',
                    user_question=user_question,
                    system_answer=item.get(api.ANSWER_TAG))
