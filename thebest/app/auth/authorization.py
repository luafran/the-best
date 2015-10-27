from tornado import gen

from thebest.common import settings
from thebest.common.tokens import jwt_token

VALID_GRANT_TYPES = (
    AUTHORIZATION_CODE, REFRESH_TOKEN) = (
    'authorization_code', 'refresh_token')


class Authorization(object):
    def __init__(self, context):
        self.context = context

    @gen.coroutine
    def generate_tokens(self):

        payload = {}
        access_token = jwt_token.JWTToken(
            payload=payload,
            certificate=settings.PRIVATE_CERTIFICATE,
            expiration_timedelta=None)

        refresh_token = jwt_token.JWTToken(
            payload=payload,
            certificate=settings.PRIVATE_CERTIFICATE,
            expiration_timedelta=None)

        response = {
            'access_token': str(access_token),
            'token_type': 'Bearer',
            'expires_in': (access_token.expiration_timedelta.total_seconds()
                           if access_token.expiration_timedelta else None),
            'refresh_token': str(refresh_token)}

        return response
