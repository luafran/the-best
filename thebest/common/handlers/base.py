"""
BaseHandler
"""
import collections
import dateutil.parser
import json
import os
import sys
import uuid
from datetime import datetime

import geoip2.database
from logging import config
from logging import getLogger
import strict_rfc3339
from tornado import httpclient
from tornado import web
from tornado import locale

from thebest.common import constants
from thebest.common import exceptions
from thebest.common import settings
from thebest.common import translations
from thebest.common.utils.support import Support


METHODS = (OPTIONS, GET, POST, PUT, DELETE, HEAD, PATCH) = (
    'OPTIONS', 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH'
)

translations.load_json_translations(settings.RESOURCES_PATH)
locale.set_default_locale(constants.DEFAULT_LANGUAGE)


class BaseStaticFileHandler(web.StaticFileHandler):
    def set_default_headers(self):
        self.set_header("Server", "Miramar Web Server")
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Max-Age', '1728000')

    def data_received(self, chunk):
        pass


class BaseHandler(web.RequestHandler):  # pylint: disable=too-many-instance-attributes
    """
    BaseHandler
    """
    def __init__(self, application, request, **kwargs):
        """
        Constructor
        """
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.context = None
        self.created_time = datetime.now()

    def data_received(self, chunk):
        pass

    def _get_language(self):
        return self.get_browser_locale(constants.DEFAULT_LANGUAGE).code

    def initialize(self, application_settings, handler=None):  # pylint: disable=arguments-differ
        self.application_settings = application_settings
        self.handler = handler
        self.request_id = self.request.headers.get(constants.REQUEST_ID_HTTP_HEADER,
                                                   'be-'+str(uuid.uuid4()))
        self.request_timestamp = self.request.headers.get(constants.LOCALTIME_HTTP_HEADER)
        self.request.language = self._get_language()

        config.dictConfig(settings.LOGGING)
        logger = getLogger(settings.LOGGER_NAME)

        mfs_environment_name = 'TB_ENV'

        mfs_environment = os.environ.get(mfs_environment_name)
        if not mfs_environment:
            raise exceptions.GeneralInfoException(
                '{0} environment variable not found'.format(mfs_environment_name))
        self.mfs_environment = mfs_environment

        session_info = {
            'mfs_environment': mfs_environment,
            'service': self.settings.get('service_name'),
            'handler': handler,
            'requestId': self.request_id
        }
        self.support = Support(logger, session_info)

        self.resource_name = "{0}_{1}".format(session_info['service'],
                                              handler if handler else '')

    def prepare(self):
        """
        Called at the beginning of a request before get/post/etc.
        Override this method to perform common initialization regardless of the
        request method
        """

        try:
            self.process_query()
            self.process_headers()
            self.process_body()

            request = self.request

            self.support.notify_debug(
                "[BaseHandler] request: %s %s" % (str(request.method), str(request.uri)))
            self.support.notify_debug(
                "[BaseHandler] request query: %s" % str(request.query))
            self.support.notify_debug(
                "[BaseHandler] request headers: %s" % str(['{0}: {1}'.format(k,v)
                                                           for k, v in request.headers.get_all()]))
            self.support.notify_debug(
                "[BaseHandler] request body: %s" % str(request.body))

            body_size = sys.getsizeof(request.body)
            self.support.stat_increment('net.requests.total_count')
            self.support.stat_increment('net.requests.total_bytes', body_size)
            self.support.stat_increment('net.requests.' + str(request.method) + '_count')
            self.support.stat_increment('net.requests.' + str(request.method) + '_bytes', body_size)

        except exceptions.InfoException as ex:
            self.support.notify_error(ex)
            self.build_response(ex)
        except Exception as ex:  # pylint: disable=W0703
            self.support.notify_error(ex)
            self.build_response(ex)

    def set_default_headers(self):
        self.set_header("Server", "Miramar Web Server")
        self.set_header('Access-Control-Allow-Headers', 'Authorization, ' + 'Content-Type, ' +
                        constants.REQUEST_ID_HTTP_HEADER +
                        ', ' + constants.SESSION_ID_HTTP_HEADER)
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Max-Age', '1728000')

    def process_headers(self, required_headers=None):
        """
        Process the request headers to validate if the headers in required_headers
        come in the request.
        Overwrite this method to extend this behavior or to change it at all.
        """

        if required_headers is None:
            required_headers = []
        else:
            pass

        if (self.request.method == 'POST') or (self.request.method == 'PUT'):
            required_headers.append('Content-Type')
        else:
            pass

        missing_headers = []
        for header in required_headers:
            if self.request.headers.get(header) is None:
                missing_headers.append(header)
            else:
                pass

        if len(missing_headers):
            raise exceptions.MissingArgumentValue('these headers are required: %s' %
                                                  missing_headers)
        else:
            pass

    def process_query(self, supported_query_attributes=None):
        """
        Process the request query.
        Overwrite this method to extend this behavior or to change it at all.
        """
        if supported_query_attributes:
            processed_query = self.request.arguments
            unsupported_attributes = list(
                set(processed_query.keys()) - set(supported_query_attributes))
            if unsupported_attributes:
                raise exceptions.InvalidArgument(
                    'The following query parameters are not supported: %s' %
                    unsupported_attributes)

    def process_body(self):
        """
        Process the request body to validate if it is valid based on the
        Content-Type header.
        Overwrite this method to extend this behavior or to change it at all.
        """

        body = self.request.body
        method = self.request.method

        if method == 'POST' or method == 'PUT':
            content_type = self.request.headers.get('Content-Type')

            if content_type.startswith('application/json'):
                try:
                    processed_body = json.loads(
                        body, object_pairs_hook=collections.OrderedDict)
                except (TypeError, ValueError) as ex:
                    raise exceptions.InvalidArgument('invalid body: %s' % ex)
            else:
                processed_body = self.request.arguments
        else:
            processed_body = None

        self.request.body_arguments = processed_body

    def build_response(self, result, status_code=None):
        """
        Build the response data with the required format according to result
        """
        self._build_response_internal(True, result, status_code)

    def build_response_without_format(self, result, status_code=None):
        """
        Build the response data with the required format according to result
        """
        self._build_response_internal(False, result, status_code)

    def _build_response_internal(self, apply_format, result, status_code=None):
        """
        Build the response data with the required format according to result
        """

        if apply_format:
            self.set_header("Content-Type", "application/json")

        if isinstance(result, Exception):
            body = self._build_response_from_exception(result)
            self.write(body)
        else:
            if apply_format:
                body = json.dumps(result)
            else:
                body = result

            if self.request.method == 'GET':
                self.set_status(status_code if status_code is not None else 200)
                self.write(body)
            elif self.request.method == 'POST':
                self.set_status(status_code if status_code is not None else 201)
                self.write(body)
            elif self.request.method == 'PUT':
                self.set_status(status_code if status_code is not None else 204)
            elif self.request.method == 'DELETE':
                self.set_status(status_code if status_code is not None else 200)
            else:
                pass

        if self.request_id:
            self.set_header(constants.REQUEST_ID_HTTP_HEADER, self.request_id)

        self.support.stat_increment('net.responses.total_count')
        self.support.stat_increment('net.responses.total_bytes', sys.getsizeof(body))
        self.support.stat_increment('net.responses.' + str(self.get_status()))

        total_time = datetime.now() - self.created_time
        timing = int(total_time.total_seconds() * 1000)
        self.support.notify_debug("[BaseHandler] Processing Time: %i ms" % timing)
        self.support.stat_timing('net.responses.time', timing)

        self.support.notify_debug(
            "[BaseHandler] response code: %s" % str(self.get_status()))
        self.support.notify_debug(
            "[BaseHandler] response body: %s" % str(body))

        self.finish()

    def _build_response_from_exception(self, ex):
        """
        Build HTTP response from an exception
        """
        if isinstance(ex, exceptions.BadRequestBase):
            self.set_status(400)
        elif isinstance(ex, exceptions.UnauthorizedBase):
            self.set_status(401)
        elif isinstance(ex, exceptions.ForbiddenBase):
            self.set_status(403)
        elif isinstance(ex, exceptions.NotFoundBase):
            self.set_status(404)
        elif isinstance(ex, exceptions.Conflict):
            self.set_status(409)
        elif isinstance(ex, exceptions.PermanentServiceError):
            self.set_status(500)
        elif isinstance(ex, exceptions.TemporaryServiceError):
            self.set_status(503)
        elif isinstance(ex, web.HTTPError):
            self.set_status(ex.status_code)
            ex = exceptions.GeneralInfoException('Web HTTPError')
        elif isinstance(ex, httpclient.HTTPError):
            self.set_status(ex.code)
            ex = exceptions.GeneralInfoException('Client HTTPError')
        else:
            self.set_status(500)
            import traceback
            formatted_lines = traceback.format_exc().splitlines()
            ex = exceptions.GeneralInfoException(formatted_lines[-1])

        ex.info[exceptions.REQUEST_ID_KEY] = self.request_id
        response_body = str(ex)
        return response_body

    def options(self, *args, **kwargs):
        options_list = [OPTIONS]

        if self.__class__.get != BaseHandler.get:
            options_list.append(GET)

        if self.__class__.post != BaseHandler.post:
            options_list.append(POST)

        if self.__class__.put != BaseHandler.put:
            options_list.append(PUT)

        if self.__class__.delete != BaseHandler.delete:
            options_list.append(DELETE)

        if self.__class__.head != BaseHandler.head:
            options_list.append(HEAD)

        if self.__class__.patch != BaseHandler.patch:
            options_list.append(PATCH)

        self.set_header('Access-Control-Allow-Methods',
                        ', '.join(options_list))


class Context(object):  # pylint: disable=too-many-instance-attributes
    """
    Context
    """

    def __init__(self, request=None, support=None):
        """
        Constructor
        """
        self.support = support
        self.session_data = None
        self.account_id = None
        self.client_id = None
        self.device_id = None
        self.member_id = None
        self.role = None
        self.products = None
        self.token = None
        self.request_id = None
        self.request_timestamp = None
        self.request_timezone = None
        self.timestamp_header_value = None
        self.language = None
        self.remote_ip = None
        self.request_country_code = None

        if request:
            self.request_id = request.headers.get(
                constants.REQUEST_ID_HTTP_HEADER)
            self.timestamp_header_value = request.headers.get(
                constants.LOCALTIME_HTTP_HEADER, "")
            if strict_rfc3339.validate_rfc3339(self.timestamp_header_value):
                self.request_timestamp = self.timestamp_header_value
                self.request_timezone = dateutil.parser.parse(
                    self.request_timestamp).strftime('%z')
                self.request_timezone = ':'.join([
                    self.request_timezone[:-2], self.request_timezone[-2:]])
            self.language = getattr(request, 'language', constants.DEFAULT_LANGUAGE)

            self.remote_ip = request.headers.get('X-Forwarded-For',
                                                 request.headers.get('X-Real-Ip',
                                                                     request.remote_ip))
            self.support.notify_debug("[BaseHandler] Remote IP: {0}".format(self.remote_ip))
            try:
                reader = geoip2.database.Reader(settings.GEOIP_DATABASE_FILE)
                response = reader.city(self.remote_ip)
                self.request_country_code = response.country.iso_code
                reader.close()
            except geoip2.errors.AddressNotFoundError:
                pass
            except IOError:
                self.support.notify_warning(
                    "[BaseHandler] geoip database: {0} not found".format(settings.GEOIP_DATABASE_FILE))

            self.support.notify_debug("[BaseHandler] Request Country: {0}".format(self.request_country_code))

        token = getattr(request, 'token', None)
        self.update_from_token(token)

    def update_from_token(self, token):
        if token:
            self.account_id = token.payload.get(constants.ACCOUNT_ID)
            self.client_id = token.payload.get(constants.CLIENT_ID)
            self.device_id = token.payload.get(constants.DEVICE_ID)
            self.member_id = token.payload.get(constants.MEMBER_ID)
            self.role = token.payload.get(constants.ROLE)
            self.products = token.payload.get(constants.PRODUCTS)
            self.products = self.products.split(',') if self.products else []
            self.token = token.token if token.token else None

    def update_from_session_data(self, session_data):
        if session_data:
            self.session_data = session_data
            self.device_id = session_data.get(constants.DEVICE_ID)

    def get_owner(self):
        return {
            'owner': {
                'applicationId': self.client_id,
                'userId': self.account_id,
                'memberId': self.member_id,
                'deviceId': self.device_id
            }
        }

    def __bool__(self):
        return True if self.account_id and self.client_id else False

    __nonzero__ = __bool__
