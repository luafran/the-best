from tornado import gen

from thebest.app.auth import authorization
from thebest.common import exceptions
from thebest.common.handlers import base
from thebest.common.handlers import decorators


# pylint: disable=arguments-differ
class TokenHandler(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self):
        # grant_type = self.get_argument('grant_type')
        # if grant_type not in authorization.VALID_GRANT_TYPES:
        #     raise exceptions.InvalidArgumentValue(
        #         'grant_type must be one of these {0}'.format(
        #             authorization.VALID_GRANT_TYPES))

        auth = authorization.Authorization(self.context)
        response = yield auth.generate_tokens()
        self.build_response(response)
