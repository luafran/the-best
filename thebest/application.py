"""
Application definitions and URL mappings
"""
import os
from tornado import web

from thebest.common import settings
from thebest.common.handlers import health
from thebest.handlers import user_question
from thebest.handlers import system_question
from thebest.handlers import user_answer
from thebest.handlers import category_suggestions

base_dir = os.path.dirname(__file__)

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
        (r'.*/category/suggestions', category_suggestions.CategorySuggestionsHandler,
         {'application_settings': settings, 'handler': 'CategorySuggestions'}, 'category_suggestions'),
        (r'/static/(.*)', web.StaticFileHandler,
         {'path': os.path.join(base_dir, "web", "static")}),
    ],
    service_name='the-best',
    template_path=os.path.join(base_dir, "web", "templates"),
    autoreload=settings.AUTO_RELOAD)
