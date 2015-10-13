import json
import mock
from tornado import ioloop
from tornado import testing
from tornado.concurrent import Future
from tornado.httpclient import HTTPRequest

from thebest import application
from thebest.app import api
from thebest.repos import items_repository

app = application.APPLICATION


class TestItemsHandler(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestItemsHandler, self).setUp()

        self._headers = {
            'Content-Type': 'application/json'
        }

    def get_app(self):
        return app

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def test_when_no_item_in_body_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/items'),
            method='POST',
            headers=self._headers,
            body=json.dumps({})
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('Missing argument item', response_body.get('context'))

    def test_when_item_in_body_with_a_then_returns_400(self):

        item = {
            api.ITEM_TAG: {
                api.QUESTION_TAG: 'beer',
                api.ANSWER_TAG: 'imperial'
            }
        }

        request = HTTPRequest(
            self.get_url('/api/items'),
            method='POST',
            headers=self._headers,
            body=json.dumps(item)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)

        self.assertIn('Item "{0}" field should be null'.format(api.ANSWER_TAG), response_body.get('context'))

    @mock.patch('thebest.repos.items_repository.add_item')
    def test_when_item_in_body_with_a_null_then_item_is_inserted(self, mock_repo):

        item = {
            api.ITEM_TAG: {
                api.QUESTION_TAG: 'beer',
                api.ANSWER_TAG: None
            }
        }

        response_from_repo = {
            'created': True,
            items_repository.ID_TAG: '123'
        }

        future = Future()
        future.set_result(response_from_repo)
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/items'),
            method='POST',
            headers=self._headers,
            body=json.dumps(item)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 201)
        response_body = json.loads(response.body)

        expected_body = {
            api.ITEM_TAG: {
                api.ID_TAG: response_from_repo[items_repository.ID_TAG],
                api.QUESTION_TAG: 'beer',
                api.ANSWER_TAG: None
            }
        }

        self.assertEqual(expected_body, response_body)

        mock_repo.assert_called_with(item[api.ITEM_TAG][api.QUESTION_TAG],
                                     item[api.ITEM_TAG][api.ANSWER_TAG])

    @mock.patch('thebest.repos.items_repository.add_item')
    def test_when_item_in_body_without_a_then_item_is_inserted(self, mock_repo):

        item = {
            api.ITEM_TAG: {
                api.QUESTION_TAG: 'beer'
            }
        }

        response_from_repo = {
            'created': True,
            items_repository.ID_TAG: '123'
        }

        future = Future()
        future.set_result(response_from_repo)
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/items'),
            method='POST',
            headers=self._headers,
            body=json.dumps(item)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 201)
        response_body = json.loads(response.body)

        expected_body = {
            api.ITEM_TAG: {
                api.ID_TAG: response_from_repo[items_repository.ID_TAG],
                api.QUESTION_TAG: 'beer',
                api.ANSWER_TAG: None
            }
        }

        self.assertEqual(expected_body, response_body)

        mock_repo.assert_called_with(item[api.ITEM_TAG][api.QUESTION_TAG], None)
