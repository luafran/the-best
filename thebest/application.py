"""
Application definitions and URL mappings
"""
from tornado import web

from thebest.common import settings
from thebest.common.handlers import health
from thebest.handlers import user_question
from thebest.handlers import system_question
from thebest.handlers import user_answer


APPLICATION = web.Application(
    [
        (r'.*/health/?$', health.HealthHandler,
         {'application_settings': settings, 'handler': 'Health'}),
        (r'.*/', user_question.UserQuestionHandler,
         {'application_settings': settings, 'handler': 'UserQuestion'}, 'user_question'),
        (r'.*/system_question', system_question.SystemQuestionHandler,
         {'application_settings': settings, 'handler': 'SystemQuestion'}, 'system_question'),
        (r'.*/user_answer', user_answer.UserAnswerHandler,
         {'application_settings': settings, 'handler': 'UserAnswer'}, 'user_answer'),
    ],
    service_name='the-best',
    autoreload=settings.AUTO_RELOAD)
