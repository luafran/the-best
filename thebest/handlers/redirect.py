from tornado import gen

from thebest.app.auth import authorization
from thebest.common.handlers import base
from thebest.common.handlers import decorators

# pylint: disable=arguments-differ
class RedirectHandlerV1(base.BaseHandler):

    @gen.coroutine
    def get(self):

        new_url = "android-app://com.ionicframework.thebest572511/thebest/app/askForAnswer?user_question=auto"
        self.redirect(new_url)

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self):

        data = self.request.body_arguments

        auth = authorization.Authorization(self.context)
        response = yield auth.create_session(session_data)
        self.build_response(response)
