"""
Application definitions and URL mappings
"""
from tornado import web

from thebest.common import settings
from thebest.common.handlers import health
from thebest.service1.handlers import user_question
from thebest.service1.handlers import system_question
from thebest.service1.handlers import user_answer


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
        #(r'/(.*)', statics.StaticHandler, {'path': msf_site_settings['template_path'],
        #                                   "default_filename": "index.html"})
    ],
    service_name='service1',
    autoreload=settings.AUTO_RELOAD)
