import json
import Crypto.PublicKey.RSA as RSA
from six.moves import urllib_parse
from tornado import gen
from tornado import httpclient
from tornado import testing
from tornado import web
from tornado.httpclient import HTTPRequest

from thebest.common import exceptions
from thebest.common import settings
from test.utils.dummy_application import APPLICATION
from thebest.common.tokens.jwt_token import JWTToken
from thebest.common.handlers import base
from thebest.common.handlers import decorators


class OAuth2AuthorizationHandler(base.BaseHandler):
    LOG_TAG = '[Dummy Handler] %s'

    @decorators.oauth2_authorization
    @gen.coroutine
    def get(self):
        self.set_status(200)

        # Little hack to test context
        response = {
            'context': {
                'client_id': self.context.client_id,
                'products': self.context.products
            }
        }
        self.write(json.dumps(response))


class ApiKeyAuthorizationHandler(base.BaseHandler):
    LOG_TAG = '[Dummy Handler] %s'

    def __init__(self, application, request, **kwargs):
        super(ApiKeyAuthorizationHandler, self).__init__(application, request, **kwargs)

    @decorators.api_key_authorization
    @gen.coroutine
    def get(self):
        self.set_status(200)
        self.write('OK')

    @decorators.api_key_authorization
    @gen.coroutine
    def post(self):
        self.set_status(200)
        self.write('OK')


class ExceptionAuthorizationHandler(base.BaseHandler):
    LOG_TAG = '[Dummy Handler] %s'

    @decorators.oauth2_authorization
    @gen.coroutine
    def get(self, exception_type):
        exception_type_to_exception = {
            'BadRequest': exceptions.BadRequest('Invalid Request'),
            'Unauthorized': exceptions.Unauthorized('Unauthorized'),
            'Forbidden': exceptions.Forbidden('Forbidden'),
            'NotFound': exceptions.NotFound('Not Found'),
            'Conflict': exceptions.Conflict('Conflict'),
            'ExternalProviderUnavailableTemporarily':
            exceptions.ExternalProviderUnavailableTemporarily('Permanent Service Error'),
            'ExternalProviderUnavailablePermanently':
            exceptions.ExternalProviderUnavailablePermanently('Temporary Service Error'),
            'web.HTTPError': web.HTTPError(500),
            'httpclient.HTTPError': httpclient.HTTPError(500),
            'default': Exception("Exception")
        }

        exception = exception_type_to_exception.get(exception_type, 'default')
        raise exception


app = APPLICATION
app.add_handlers(r'.*$', [(r'/oauth2', OAuth2AuthorizationHandler,
                           {'application_settings': settings}),
                          (r'/api_key', ApiKeyAuthorizationHandler,
                           {'application_settings': settings}),
                          (r'/exception/?([^/]*)$', ExceptionAuthorizationHandler,
                           {'application_settings': settings})])


class TestOAuth2Authorization(testing.AsyncHTTPTestCase):
    def setUp(self):
        super(TestOAuth2Authorization, self).setUp()

    def tearDown(self):
        pass

    def get_app(self):
        return app

    def test_valid_token_no_products(self):
        test_client_id = '123'
        token = JWTToken(payload={"client_id": test_client_id},
                         certificate=settings.PRIVATE_CERTIFICATE)
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)

    def test_valid_token_three_products(self):
        test_client_id = '123'
        test_products = 'test:prod1,test:prod2,test:prod3'
        payload = {
            "client_id": test_client_id,
            "products": test_products
        }
        token = JWTToken(payload=payload,
                         certificate=settings.PRIVATE_CERTIFICATE)
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)

        expected_response = {
            'context': {
                'client_id': test_client_id,
                'products': test_products.split(',')
            }
        }
        self.assertEqual(expected_response, json.loads(response.body))

    def test_invalid_token_with_missing_client_id(self):
        token = JWTToken(payload={}, certificate=settings.PRIVATE_CERTIFICATE)
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(401, response.code)

    def test_invalid_token(self):
        token = '123456789'
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(401, response.code)

    def test_empty_token(self):
        token = ''
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(token)})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(401, response.code)

    def test_not_supported_token_type(self):
        token = JWTToken(payload={"client_id": "123"},
                         certificate=settings.PRIVATE_CERTIFICATE)
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Basic {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(401, response.code)

    def test_authorization_header_missing(self):
        request = HTTPRequest(self.get_url('/oauth2'), method='GET')
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(401, response.code)

    def test_valid_token_invalid_certificate(self):
        certificate = RSA.generate(2048)
        token = JWTToken(payload={"client_id": "123"}, certificate=certificate)
        request = HTTPRequest(
            self.get_url('/oauth2'), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(401, response.code)


class TestApiKeyAuthorization(testing.AsyncHTTPTestCase):
    def setUp(self):
        super(TestApiKeyAuthorization, self).setUp()

    def tearDown(self):
        pass

    def get_app(self):
        return app

    def test_missing_api_key(self):
        request = HTTPRequest(self.get_url('/api_key'), method='GET')
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        # We are using this decorator just to catch exceptions right now
        self.assertEqual(200, response.code)

    def test_valid_api_key_query_param(self):
        api_key = '101'
        request = HTTPRequest(
            self.get_url('/api_key?client_id={0}'.format(api_key)),
            method='GET')
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)

    def test_valid_api_key_in_body(self):
        api_key = '101'
        post_data = {'client_id': api_key}
        body = urllib_parse.urlencode(post_data)

        request = HTTPRequest(
            self.get_url('/api_key'),
            method='POST', body=body)
        self.http_client.fetch(request, self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)


class TestExceptionAuthorization(testing.AsyncHTTPTestCase):
    def setUp(self):
        super(TestExceptionAuthorization, self).setUp()

    def tearDown(self):
        pass

    def get_app(self):
        return app

    def do_request_and_get_response(self, exception_type):
        token = JWTToken(payload={"client_id": "1234",
                                  "products": "Trial"},
                         certificate=settings.PRIVATE_CERTIFICATE)
        request = HTTPRequest(
            self.get_url('/exception/' + exception_type), method='GET',
            headers={'Authorization': 'Bearer {0}'.format(str(token))})
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        return response

    def assert_response(self, response, expected_code):
        self.assertEqual(expected_code, response.code)
        self.assertTrue(exceptions.DEVELOPER_MESSAGE_KEY in response.body)
        self.assertTrue(exceptions.USER_MESSAGE_KEY in response.body)
        self.assertTrue(exceptions.CONTEXT_KEY in response.body)
        self.assertTrue(exceptions.REQUEST_ID_KEY in response.body)

    def test_bad_request_is_translated_to_400(self):
        response = self.do_request_and_get_response('BadRequest')
        self.assert_response(response, 400)

    def test_unauthorized_is_translated_to_401(self):
        response = self.do_request_and_get_response('Unauthorized')
        self.assert_response(response, 401)

    def test_forbidden_is_translated_to_403(self):
        response = self.do_request_and_get_response('Forbidden')
        self.assert_response(response, 403)

    def test_not_found_is_translated_to_404(self):
        response = self.do_request_and_get_response('NotFound')
        self.assert_response(response, 404)

    def test_conflict_is_translated_to_409(self):
        response = self.do_request_and_get_response('Conflict')
        self.assert_response(response, 409)

    def test_permanent_service_is_translated_to_500(self):
        response = self.do_request_and_get_response('ExternalProviderUnavailablePermanently')
        self.assert_response(response, 500)

    def test_temporary_service_is_translated_to_503(self):
        response = self.do_request_and_get_response('ExternalProviderUnavailableTemporarily')
        self.assert_response(response, 503)

    def test_web_http_error_exception_is_translated_to_500(self):
        response = self.do_request_and_get_response('web.HTTPError')
        self.assert_response(response, 500)

    def test_client_http_error_exception_is_translated_to_500(self):
        response = self.do_request_and_get_response('httpclient.HTTPError')
        self.assert_response(response, 500)

    def test_exception_is_translated_to_500(self):
        response = self.do_request_and_get_response('')
        self.assert_response(response, 500)
