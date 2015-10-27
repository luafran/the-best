from tornado import gen

from thebest.app.auth import authorization
from thebest.common.handlers import base
from thebest.common.handlers import decorators


# pylint: disable=arguments-differ
class SessionHandlerV1(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self):

        session_data = self.request.body_arguments

        auth = authorization.Authorization(self.context)
        response = yield auth.create_session(session_data)
        self.build_response(response)
