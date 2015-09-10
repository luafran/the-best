import mock

from tornado import httpclient
from tornado import testing

from thebest.common import constants
from thebest.common.handlers import base
from thebest.common.utils import dictionaries
from thebest.common.utils.rest_adapter import RestAdapter


class TestRestAdapter(testing.AsyncTestCase):

    def _create_context(self):
        payload = {'account_id': '123',
                   'client_id': '123',
                   'member_id': '123',
                   'device_id': '123'}
        token = dictionaries.DictAsObject({'payload': payload, 'token': 'xxx'})
        context = base.Context(dictionaries.DictAsObject({
            "token": token, "headers": {constants.REQUEST_ID_HTTP_HEADER: "823123"}}))
        return context

    @mock.patch.object(RestAdapter, "_create_request")
    def test_request_sends_request_id(self, create_request):
        create_request.return_value = httpclient.HTTPRequest("/tmp")
        rest_adapter = RestAdapter("endpoint", self._create_context(), None)
        rest_adapter.get('/a_get')

        request_headers = create_request.call_args_list[0][1]['headers']
        self.assertEquals(request_headers[constants.REQUEST_ID_HTTP_HEADER], "823123")
