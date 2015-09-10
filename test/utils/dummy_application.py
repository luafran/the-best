"""
Dummy Application definitions and URL mappings
"""
from tornado import web
from thebest.common.handlers.health import HealthHandler
from thebest.common import settings


APPLICATION = web.Application(
    [
        (r'.*/health/?$', HealthHandler, {
            'application_settings': settings})
    ])
