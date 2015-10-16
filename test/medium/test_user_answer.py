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


class TestUserAnswerHandler(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestUserAnswerHandler, self).setUp()

        self._headers = {
            'Content-Type': 'application/json'
        }

    def get_app(self):
        return app

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    def test_when_no_item_in_body_then_returns_400(self):
        request = HTTPRequest(
            self.get_url('/api/user_answer'),
            method='POST',
            headers=self._headers,
            body=json.dumps({})
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)
        self.assertIn('Missing item in body', response_body.get('context'))

    def test_when_item_in_body_without_q_and_a_then_returns_400(self):

        item = {
            api.ITEM_TAG: {
            }
        }

        request = HTTPRequest(
            self.get_url('/api/user_answer'),
            method='POST',
            headers=self._headers,
            body=json.dumps(item)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)

        self.assertIn('Missing item in body', response_body.get('context'))

    def test_when_item_in_body_without_q_then_returns_400(self):

        item = {
            api.ITEM_TAG: {
                api.ANSWER_TAG: 'imperial'
            }
        }

        request = HTTPRequest(
            self.get_url('/api/user_answer'),
            method='POST',
            headers=self._headers,
            body=json.dumps(item)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)

        self.assertIn('Missing "{0}" or "{1}" field in body'.format(api.QUESTION_TAG, api.ANSWER_TAG),
                      response_body.get('context'))

    def test_when_item_in_body_without_a_then_returns_400(self):

        item = {
            api.ITEM_TAG: {
                api.QUESTION_TAG: 'beer'
            }
        }

        request = HTTPRequest(
            self.get_url('/api/user_answer'),
            method='POST',
            headers=self._headers,
            body=json.dumps(item)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 400)
        response_body = json.loads(response.body)

        self.assertIn('Missing "{0}" or "{1}" field in body'.format(api.QUESTION_TAG, api.ANSWER_TAG),
                      response_body.get('context'))

    @mock.patch('thebest.repos.items_repository.add_item')
    @mock.patch('thebest.repos.items_repository.get_items_with_q_and_a')
    def test_when_item_with_this_answer_already_exists_then_votes_are_increased(self, mock_repo1, mock_repo2):

        item_from_repo = {
            items_repository.QUESTION_TAG: 'hotel',
            items_repository.ANSWER_TAG: 'Holiday inn express'
        }

        hits = {
            items_repository.TOTAL_TAG: 1,
            'hits': [
                {
                    items_repository.ID_TAG: 'some_id_that_should_not_be_in_response',
                    items_repository.SOURCE_TAG: item_from_repo
                }
            ]
        }

        future1 = Future()
        future1.set_result(hits)

        mock_repo1.return_value = future1

        question = 'hotel'
        answer = 'holiday inn express'
        request_body = {
            api.ITEM_TAG: {
                api.QUESTION_TAG: question,
                api.ANSWER_TAG: answer
            }
        }

        request = HTTPRequest(
            self.get_url('/api/user_answer'),
            method='POST',
            headers=self._headers,
            body=json.dumps(request_body)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 201)
        response_body = json.loads(response.body)
        self.assertEqual(None, response_body)

        mock_repo1.assert_called_with(question, answer)
        self.assertFalse(mock_repo2.called)

    @mock.patch('thebest.repos.items_repository.add_item')
    @mock.patch('thebest.repos.items_repository.get_items_with_q_and_a')
    def test_when_item_with_this_answer_does_not_exists_then_new_item_is_inserted(self, mock_repo1, mock_repo2):

        hits = {
            items_repository.TOTAL_TAG: 0,
            'hits': []
        }

        future1 = Future()
        future1.set_result(hits)
        mock_repo1.return_value = future1

        item = {
            items_repository.CREATED_TAG: True,
            items_repository.ID_TAG: '123'
        }

        future2 = Future()
        future2.set_result(item)
        mock_repo2.return_value = future2

        question = 'hotel'
        answer = 'Holiday inn express'
        request_body = {
            api.ITEM_TAG: {
                api.QUESTION_TAG: question,
                api.ANSWER_TAG: answer
            }
        }

        request = HTTPRequest(
            self.get_url('/api/user_answer'),
            method='POST',
            headers=self._headers,
            body=json.dumps(request_body)
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 201)
        response_body = json.loads(response.body)

        expected_body = {
            api.ITEM_TAG: {
                api.ID_TAG: item[items_repository.ID_TAG],
                api.QUESTION_TAG: question,
                api.ANSWER_TAG: answer
            }
        }
        self.assertEqual(expected_body, response_body)

        mock_repo2.assert_called_with(question, answer)
