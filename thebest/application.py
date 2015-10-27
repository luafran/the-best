"""
Application definitions and URL mappings
"""
import os
from tornado import web

from thebest.common import settings
from thebest.common.handlers import health
from thebest.handlers import action
from thebest.handlers import best_answer
from thebest.handlers import question
from thebest.handlers import session
from thebest.handlers import suggestions
from thebest.handlers import token
from thebest.handlers import user_answer
from thebest.handlers import system_question as api_system_question
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
        (r'.*/api/session', session.SessionHandlerV1,
         {'application_settings': settings, 'handler': 'SessionV1'}, 'api_session'),
        (r'.*/api/token', token.TokenHandlerV1,
         {'application_settings': settings, 'handler': 'TokenV1'}, 'api_token'),
        (r'.*/api/suggestions', suggestions.SuggestionsHandlerV1,
         {'application_settings': settings, 'handler': 'QuestionSuggestionsV1'}, 'api_suggestions'),
        (r'.*/api/best_answer', best_answer.BestAnswerHandlerV1,
         {'application_settings': settings, 'handler': 'APIBestAnswerV1'}, 'api_best_answer'),
        (r'.*/api/v2/best_answer', best_answer.BestAnswerHandlerV2,
         {'application_settings': settings, 'handler': 'APIBestAnswerV2'}, 'api_best_answer'),
        (r'.*/api/question/?$', question.QuestionHandlerV1,
         {'application_settings': settings, 'handler': 'APIQuestionV1'}, 'api_question'),
        (r'.*/api/system_question', api_system_question.SystemQuestionHandlerV1,
         {'application_settings': settings, 'handler': 'APISystemQuestionV1'}, 'api_system_question'),
        (r'.*/api/user_answer', user_answer.UserAnswerHandlerV1,
         {'application_settings': settings, 'handler': 'APIUserAnswerV1'}, 'api_user_answer'),
        (r'.*/api/action', action.ActionHandlerV1,
         {'application_settings': settings, 'handler': 'ActionV1'}, 'action'),
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
