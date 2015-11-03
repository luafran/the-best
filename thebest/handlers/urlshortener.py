from tornado import gen

from thebest.app import utils
from thebest.common.handlers import base
from thebest.common.handlers import decorators


# pylint: disable=arguments-differ
class UrlShortenerHandlerV1(base.BaseHandler):

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self, id):

        data = self.request.body_arguments
        urlshortener = utils.Utils(self.context)

        long_url = data.get("longUrl")
        response = yield urlshortener.create_urlshortener(long_url)
        self.build_response(response)

    @gen.coroutine
    def get(self, id):

        urlshortener = utils.Utils(self.context)

        long_url = yield urlshortener.get_urlshortener(id)
        self.redirect(long_url)
