"""
Application definitions and URL mappings
"""
from tornado import web

from thebest.common import settings
from thebest.common.tornado.handlers import health


APPLICATION = web.Application(
    [
        (r'.*/health/?$', health.HealthHandler,
         {'application_settings': settings, 'handler': 'Health'})
    ],
    service_name='service1',
    autoreload=settings.AUTO_RELOAD)
