"""
Application definitions and URL mappings
"""
import os
from tornado import web

from thebest.common import settings
from thebest.common.handlers import health
from thebest.handlers import best_answer
from thebest.handlers import question
from thebest.handlers import suggestions
from thebest.handlers import user_answer
from thebest.handlers import user_question as api_user_question
from thebest.web.handlers import main
from thebest.web.handlers import user_question
from thebest.web.handlers import system_question
from thebest.web.handlers import first_time
from thebest.repos.mysql import items_repository

BASE_DIR = os.path.dirname(__file__)

items_repository = items_repository.TheBestRepository()
settings.items_repository = items_repository

APPLICATION = web.Application(
    [
        # /api urls should go first
        (r'.*/health/?$', health.HealthHandler,
         {'application_settings': settings, 'handler': 'Health'}),
        (r'.*/api/suggestions', suggestions.SuggestionsHandler,
         {'application_settings': settings, 'handler': 'QuestionSuggestions'}, 'api_suggestions'),
        (r'.*/api/best_answer', best_answer.BestAnswerHandler,
         {'application_settings': settings, 'handler': 'APIBestAnswer'}, 'api_best_answer'),
        (r'.*/api/question/?$', question.QuestionHandler,
         {'application_settings': settings, 'handler': 'APIQuestion'}, 'api_question'),

        (r'.*/api/user_question', api_user_question.UserQuestionHandler,
         {'application_settings': settings, 'handler': 'APIUserQuestion'}, 'api_user_question'),
        (r'.*/api/user_answer', user_answer.UserAnswerHandler,
         {'application_settings': settings, 'handler': 'APIUserAnswer'}, 'api_user_answer'),
        (r'.*/', main.MainHandler,
         {'application_settings': settings, 'handler': 'Main'}, 'main'),
        (r'.*/user_question', user_question.UserQuestionHandler,
         {'application_settings': settings, 'handler': 'UserQuestion'}, 'user_question'),
        (r'.*/system_question', system_question.SystemQuestionHandler,
         {'application_settings': settings, 'handler': 'SystemQuestion'}, 'system_question'),
        (r'.*/first_time', first_time.FirstTimeHandler,
         {'application_settings': settings, 'handler': 'FirstTime'}, 'first_time'),
        (r'/static/(.*)', web.StaticFileHandler,
         {'path': os.path.join(BASE_DIR, "web", "static")}),
    ],
    service_name='the-best',
    template_path=os.path.join(BASE_DIR, "web", "templates"),
    autoreload=settings.AUTO_RELOAD)
