import mock
import unittest
from tornado import testing

from thebest.common import exceptions
from test.utils.dummy_application import APPLICATION

app = APPLICATION


class TestHealthCheck(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestHealthCheck, self).setUp()

    def tearDown(self):
        pass

    def get_app(self):
        return app

    def test_healthcheck_simple_get(self):
        self.http_client.fetch(self.get_url('/health'), self.stop, method='GET')
        response = self.wait()
        self.assertEqual(200, response.code, "Response should be 200, getting %s instead" % response.code)

    def test_healthcheck_with_query(self):
        self.http_client.fetch(self.get_url('/health?include_details=true'), self.stop, method='GET')
        response = self.wait()
        self.assertEqual(200, response.code, "Response should be 200, getting %s instead" % response.code)


class TestHealthCheckFailure(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestHealthCheckFailure, self).setUp()

    def tearDown(self):
        pass

    def get_app(self):
        return app

    def test_healthcheck_with_invalid_query(self):
        self.http_client.fetch(self.get_url('/health?include_invalid=true'), self.stop, method='GET')
        response = self.wait()
        self.assertEqual(400, response.code, "Response should be 400, getting %s instead" % response.code)

    def test_healthcheck_with_invalid_query_value(self):
        self.http_client.fetch(self.get_url('/health?include_details=invalid'), self.stop, method='GET')
        response = self.wait()
        self.assertEqual(400, response.code, "Response should be 400, getting %s instead" % response.code)

    def test_healthcheck_servicemonitor_raises_info_exception(self):
        with mock.patch('thebest.common.health.health_monitor.HealthMonitor.get_status') as get_status:
            get_status.side_effect = exceptions.InfoException({exceptions.CONTEXT_KEY: ''})

            self.http_client.fetch(self.get_url('/health'), self.stop, method='GET')
            response = self.wait()
            self.assertEqual(500, response.code, "Response should be 500, getting %s instead" % response.code)

    def test_healthcheck_servicemonitor_raises_exception(self):
        with mock.patch('thebest.common.health.health_monitor.HealthMonitor.get_status') as get_status:
            get_status.side_effect = Exception()

            self.http_client.fetch(self.get_url('/health'), self.stop, method='GET')
            response = self.wait()
            self.assertEqual(500, response.code, "Response should be 500, getting %s instead" % response.code)
