import json
import mock
import unittest

from thebest.common import exceptions
from thebest.common import settings
from thebest.common.handlers import base
from tornado.httpclient import HTTPRequest


class TestBaseHandlerBuildResponseFromException(unittest.TestCase):
    scenarios = [
        dict(exception=exceptions.BadRequestBase,
             http_status_code=400,
             info={exceptions.CONTEXT_KEY: 'aContext', 'foo': 'bar'}),
        dict(exception=exceptions.UnauthorizedBase,
             http_status_code=401,
             info={exceptions.CONTEXT_KEY: 'aContext', 'foo': 'bar'}),
        dict(exception=exceptions.ForbiddenBase,
             http_status_code=403,
             info={exceptions.CONTEXT_KEY: 'aContext', 'foo': 'bar'}),
        dict(exception=exceptions.NotFoundBase,
             http_status_code=404,
             info={exceptions.CONTEXT_KEY: 'aContext', 'foo': 'bar'}),
        dict(exception=exceptions.PermanentServiceError,
             http_status_code=500,
             info={exceptions.CONTEXT_KEY: 'aContext', 'foo': 'bar'}),
        dict(exception=exceptions.TemporaryServiceError,
             http_status_code=503,
             info={exceptions.CONTEXT_KEY: 'aContext', 'foo': 'bar'}),
        dict(exception=Exception,
             http_status_code=500,
             info={'developer_message': 'Exception occurred',
                   'user_message': 'Service error',
                   'context': 'None',
                   'request_id': ''})
    ]

    def test_build_response_from_exception(self):
        with mock.patch('thebest.common.handlers.'
                        'base.BaseHandler.set_status') as set_status:

            for scenario in self.scenarios:

                base_handler = base.BaseHandler(
                    mock.MagicMock(), mock.MagicMock(),
                    application_settings=settings)
                base_handler.request_id = ''

                expected_body = base_handler._build_response_from_exception(
                    scenario.get('exception')(scenario.get('info')))
                self.assertEqual(expected_body, json.dumps(scenario.get('info')))
                set_status.assert_called_with(scenario.get('http_status_code'))


class TestHeaderBaseHandler(unittest.TestCase):

    def test_get_valid_utc_format_from_header(self):
        valid_timestamp = '2015-10-02T19:20:30.45+01:00'
        header = {'Authorization': 'Bearer lsdfhalkdfhladjfhl',
                  'Content-Type': 'application/json',
                  'X-LocalTime': valid_timestamp}
        request = HTTPRequest('/family/v1/members', headers=header)
        context = base.Context(request)
        self.assertEqual(context.request_timestamp, valid_timestamp)
        self.assertEqual(context.request_timezone, '+01:00')

    def test_get_valid_zulu_time_format_from_header(self):
        valid_timestamp = '2002-10-02T15:00:00Z'
        header = {'Authorization': 'Bearer lsdfhalkdfhladjfhl',
                  'Content-Type': 'application/json',
                  'X-LocalTime': valid_timestamp}
        request = HTTPRequest('/family/v1/members', headers=header)
        context = base.Context(request)
        self.assertEqual(context.request_timestamp, valid_timestamp)
        self.assertEqual(context.request_timezone, '+00:00')

    def test_get_invalid_value_from_header(self):
        invalid_value = '2015-10-02TT25:20:30+05:00'
        header = {'Authorization': 'Bearer lsdfhalkdfhladjfhl',
                  'Content-Type': 'application/json',
                  'X-LocalTime': invalid_value}
        request = HTTPRequest('/family/v1/members', headers=header)
        context = base.Context(request)
        self.assertEqual(context.request_timestamp, None)
        self.assertEqual(context.request_timezone, None)

    def test_get_invalid_format_from_header(self):
            invalid_format = 'Thursday, 28 Jun 2015 14:17:15'
            header = {'Authorization': 'Bearer lsdfhalkdfhladjfhl',
                      'Content-Type': 'application/json',
                      'X-LocalTime': invalid_format}
            request = HTTPRequest('/family/v1/members', headers=header)
            context = base.Context(request)
            self.assertEqual(context.request_timestamp, None)
            self.assertEqual(context.request_timezone, None)

    def test_get_empty_XLocalTime_from_header(self):
        empty_timestamp = ""
        header = {'Authorization': 'Bearer lsdfhalkdfhladjfhl',
                  'Content-Type': 'application/json',
                  'X-LocalTime': empty_timestamp}
        request = HTTPRequest('/family/v1/members', headers=header)
        context = base.Context(request)
        self.assertEqual(context.request_timestamp, None)
        self.assertEqual(context.request_timezone, None)

    def test_get_void_XLocalTime_from_header(self):
        header = {'Authorization': 'Bearer lsdfhalkdfhladjfhl',
                  'Content-Type': 'application/json'}
        request = HTTPRequest('/family/v1/members', headers=header)
        context = base.Context(request)
        self.assertEqual(context.request_timestamp, None)
        self.assertEqual(context.request_timezone, None)
