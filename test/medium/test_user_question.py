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


class TestUserQuestionHandler(testing.AsyncHTTPTestCase):

    def setUp(self):
        super(TestUserQuestionHandler, self).setUp()

    def get_app(self):
        return app

    def get_new_ioloop(self):
        return ioloop.IOLoop.instance()

    @mock.patch('thebest.repos.items_repository.get_items_without_answer')
    def test_when_there_are_items_without_answer_then_one_is_returned(self, mock_repo):

        future = Future()

        item_id = 'id_that_should_be_in_response'
        item = {
            items_repository.QUESTION_TAG: 'beer',
            items_repository.ANSWER_TAG: None
        }

        hits = {
            items_repository.TOTAL_TAG: 1,
            items_repository.HITS_TAG: [
                {
                    items_repository.ID_TAG: item_id,
                    items_repository.SOURCE_TAG: item
                }
            ]
        }

        future.set_result(hits)
        mock_repo.return_value = future

        request = HTTPRequest(
            self.get_url('/api/user_question'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'items': [
                {
                    api.ID_TAG: item_id,
                    api.QUESTION_TAG: item[items_repository.QUESTION_TAG]
                }
            ]
        }

        self.assertEqual(expected_body, json.loads(response.body))

    @mock.patch('thebest.repos.items_repository.get_items')
    @mock.patch('thebest.repos.items_repository.get_items_without_answer')
    def test_when_there_are_not_items_without_answer_then_another_is_returned(self, mock_repo1, mock_repo2):

        future1 = Future()
        hits = {
            items_repository.TOTAL_TAG: 0,
            'hits': []
        }
        future1.set_result(hits)
        mock_repo1.return_value = future1

        item = {
            items_repository.QUESTION_TAG: 'beer',
            items_repository.ANSWER_TAG: 'imperial'
        }

        hits = {
            items_repository.TOTAL_TAG: 1,
            'hits': [
                {
                    items_repository.ID_TAG: 'some_id_that_should_not_be_in_response',
                    items_repository.SOURCE_TAG: item
                }
            ]
        }

        future2 = Future()
        future2.set_result(hits)
        mock_repo2.return_value = future2

        request = HTTPRequest(
            self.get_url('/api/user_question'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'items': [
                {
                    api.QUESTION_TAG: item[items_repository.QUESTION_TAG]
                }
            ]
        }
        self.assertEqual(expected_body, json.loads(response.body))

    @mock.patch('thebest.repos.items_repository.get_items')
    @mock.patch('thebest.repos.items_repository.get_items_without_answer')
    def test_when_there_are_no_item_in_database_then_nothing_is_returned(self, mock_repo1, mock_repo2):

        future1 = Future()
        hits = {
            items_repository.TOTAL_TAG: 0,
            'hits': []
        }
        future1.set_result(hits)
        mock_repo1.return_value = future1

        hits = {
            items_repository.TOTAL_TAG: 0,
            'hits': []
        }

        future2 = Future()
        future2.set_result(hits)
        mock_repo2.return_value = future2

        request = HTTPRequest(
            self.get_url('/api/user_question'),
            method='GET'
        )
        self.http_client.fetch(request, self.stop)
        response = self.wait()

        self.assertEqual(response.code, 200)
        expected_body = {
            'items': []
        }
        self.assertEqual(expected_body, json.loads(response.body))
