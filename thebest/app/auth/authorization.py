import json
import uuid

import redis
from tornado import gen

from thebest.common import exceptions
from thebest.common import settings
from thebest.common.tokens import jwt_token

VALID_GRANT_TYPES = (
    AUTHORIZATION_CODE, REFRESH_TOKEN) = (
    'authorization_code', 'refresh_token')


class Authorization(object):
    def __init__(self, context):
        self.context = context

    @gen.coroutine
    def get_session(self, session_id):
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

        try:
            response = json.loads(r.get(session_id))
        except redis.ConnectionError:
            raise exceptions.DatabaseOperationError('Cannot get session')

        return response

    @gen.coroutine
    def create_session(self, session_data):

        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

        session_id = str(uuid.uuid4())
        session_ttl = settings.SESSION_TTL_SECONDS
        try:
            r.set(session_id, json.dumps(session_data), ex=session_ttl)
        except redis.ConnectionError:
            raise exceptions.DatabaseOperationError('Cannot store session')

        response = {
            'sessionId': session_id,
            'expires_in': session_ttl
        }

        return response

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
