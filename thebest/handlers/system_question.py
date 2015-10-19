from tornado import gen

from thebest.app import api
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class SystemQuestionHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):
        app = api.Application(self.application_settings.items_repository)
        response = yield app.get_system_question()

        self.build_response(response)
