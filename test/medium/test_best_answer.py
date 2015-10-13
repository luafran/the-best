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


class TestBestAnswerHandler(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestBestAnswerHandler, self).setUp()

    def get_app(self):
        return app

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def test_when_no_q_in_query_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/best_answer'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('Missing argument q', response_body.get('context'))

    @mock.patch('thebest.repos.items_repository.get_best_answer')
    def test_when_no_hits_then_returns_empty_list(self, mock_repo):

        future = Future()
        future.set_result({'hits': []})
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/best_answer?q=beer'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'items': []
        }
        self.assertEqual(expected_body, json.loads(response.body))

    @mock.patch('thebest.repos.items_repository.get_best_answer')
    def test_when_hit_then_returns_list(self, mock_repo):

        future = Future()

        item = {
            items_repository.QUESTION_TAG: 'beer',
            items_repository.ANSWER_TAG: 'imperial'
        }

        hits = {
            'hits': [
                {
                    items_repository.SOURCE_TAG: item
                }
            ]
        }

        future.set_result(hits)
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/best_answer?q=beer'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'items': [
                {
                    api.QUESTION_TAG: item[items_repository.QUESTION_TAG],
                    api.ANSWER_TAG: item[items_repository.ANSWER_TAG],
                }
            ]
        }
        self.assertEqual(expected_body, json.loads(response.body))
