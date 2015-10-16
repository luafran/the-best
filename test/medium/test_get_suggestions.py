import json
import mock
from tornado import ioloop
from tornado import testing
from tornado.concurrent import Future
from tornado.httpclient import HTTPRequest

from thebest import application


app = application.APPLICATION


class TestSuggestionsHandler(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestSuggestionsHandler, self).setUp()

    def get_app(self):
        return app

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def test_when_no_type_in_query_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/suggestions?text=something'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('type', response_body.get('context'))

    def test_when_no_text_in_query_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/suggestions?type=q'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('text', response_body.get('context'))

    def test_when_invalid_type_in_query_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/suggestions?type=unknown_type&text=something'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('unknown_type', response_body.get('context'))
        self.assertIn('type', response_body.get('context'))

    def test_when_answer_type_and_no_question_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/suggestions?type=a&text=something'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('Missing argument q', response_body.get('context'))

    @mock.patch('thebest.repos.items_repository.get_question_suggestions')
    def test_when_question_suggestion_and_no_items_return_empty_list(self, mock_repo):

        future = Future()
        future.set_result([])
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/suggestions?type=q&text=be'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'suggestions': []
        }
        self.assertEqual(expected_body, json.loads(response.body))

    @mock.patch('thebest.repos.items_repository.get_question_suggestions')
    def test_when_question_suggestion_and_3_items_return_list(self, mock_repo):

        future = Future()
        future.set_result(['beer', 'beach', 'beacon', 'corte de asado'])
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/suggestions?type=q&text=be'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'suggestions': [
                {'text': 'beer'},
                {'text': 'beach'},
                {'text': 'beacon'},
                {'text': 'corte de asado'}
            ]
        }
        self.assertEqual(expected_body, json.loads(response.body))

    @mock.patch('thebest.repos.items_repository.get_answer_suggestions')
    def test_when_answer_suggestion_and_no_items_return_empty_list(self, mock_repo):

        future = Future()
        future.set_result([])
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/suggestions?type=a&q=beer&text=imp'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'suggestions': []
        }
        self.assertEqual(expected_body, json.loads(response.body))

    @mock.patch('thebest.repos.items_repository.get_answer_suggestions')
    def test_when_answer_suggestion_and_3_items_return_list(self, mock_repo):

        future = Future()
        future.set_result(['imperial', 'important', 'impetu'])
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/suggestions?type=a&q=beer&text=imp'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'suggestions': [
                {'text': 'imperial'},
                {'text': 'important'},
                {'text': 'impetu'}
            ]
        }
        self.assertEqual(expected_body, json.loads(response.body))
