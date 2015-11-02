import uuid
import redis

from tornado import gen

from thebest.common import settings
from thebest.common import exceptions


class Utils(object):

    def __init__(self, context):
        self.context = context

    @gen.coroutine
    def create_urlshortener(self, url):
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

        shortener_id = str(uuid.uuid4())
        shortener_ttl = settings.URLSHORTENER_TTL_SECONDS
        try:
            r.set(shortener_id, url, ex=shortener_ttl)
        except redis.ConnectionError:
            raise exceptions.DatabaseOperationError('Cannot store url shortener')

        response = {
            'id': settings.URLSHORTENER_BASE_URL + "/" + shortener_id,
            'longUrl': url,
            'expires_in': shortener_ttl
        }

        return response

    @gen.coroutine
    def get_urlshortener(self, shortener_id):
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

        try:
            response = r.get(shortener_id)
        except redis.ConnectionError:
            raise exceptions.DatabaseOperationError('Cannot get shortener id')

        return response
