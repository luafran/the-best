"""
Base settings used in all environments
"""
import datetime
import os

import Crypto.PublicKey.RSA as RSA

from thebest.common import settings

APPLICATION_ID = '1'

AUTO_RELOAD = True
ENFORCE_POLICIES = True
STATS_ENABLED = False

SESSION_TTL_SECONDS = 86400

JWT_TOKEN_NOT_BEFORE_TIMEDELTA = datetime.timedelta(minutes=1)

RESOURCES_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'web', 'static', 'resources')

JSON_SCHEMA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                'json_schema', 'schemas')
JSON_SCHEMA_BASE_URL = "http://thebest/jsonschema/"

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

MYSQL_MAX_CONNECTIONS = 20
MYSQL_IDLE_SECONDS = 7200
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWD = "password"
MYSQL_DB = "thebest"
MYSQL_CHARSET = "utf8"

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

GEOIP_DATABASE_FILE = os.path.join(os.path.expanduser("~"), 'GeoLite2-City.mmdb')

LOG_DIR = os.path.expanduser("~")
LOG_LEVEL = 'DEBUG'
LOGGER_NAME = 'service'
ANALYTICS_LOGGER_NAME = 'analytics'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(env)s %(service)s %(handler)s %(requestId)s '
                      '%(message)s'
        },
        'analytics': {
            'format': '%(asctime)s %(env)s %(service)s %(handler)s %(app)s %(account)s %(user)s %(device)s'
        }
    },
    'handlers': {
        'local_internal': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'local_analytics': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'thebest_analytics.log'),
            'formatter': 'analytics'
        },
    },
    'loggers': {
        LOGGER_NAME: {
            'handlers': ['local_internal'],
            'level': settings.LOG_LEVEL,
            'propagate': True,
        },
        ANALYTICS_LOGGER_NAME: {
            'handlers': ['local_analytics'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

PRIVATE_CERTIFICATE_FILE = os.path.join(
    os.path.dirname(__file__), 'certs', 'the-best')
if os.path.exists(PRIVATE_CERTIFICATE_FILE):
    with open(PRIVATE_CERTIFICATE_FILE, 'r') as fd:
        PRIVATE_CERTIFICATE = RSA.importKey(fd.read())
else:
    PRIVATE_CERTIFICATE = None

AES_SECRET = ("\\\xb3f\xd6\xf2\xc4H\x18\x11\x87\r`\x14\x97ez\xed\xd8\xfd"
              "\x03pF\xa1\xc1\x94\xee\xe3\x1b\xa9p\x81.")
