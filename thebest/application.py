"""
Application definitions and URL mappings
"""
import os
from tornado import web

from thebest.common import settings
from thebest.common.handlers import health
from thebest.handlers import items
from thebest.handlers import main
from thebest.handlers import user_question
from thebest.handlers import system_question
from thebest.handlers import first_time
from thebest.handlers import suggestions

base_dir = os.path.dirname(__file__)

APPLICATION = web.Application(
    [
        # /api urls should go first
        (r'.*/health/?$', health.HealthHandler,
         {'application_settings': settings, 'handler': 'Health'}),
        (r'.*/api/suggestions/question', suggestions.QuestionSuggestionsHandler,
         {'application_settings': settings, 'handler': 'QuestionSuggestions'}, 'api_question_suggestions'),
        (r'.*/api/suggestions/answer', suggestions.AnswerSuggestionsHandler,
         {'application_settings': settings, 'handler': 'AnswerSuggestions'}, 'api_answer_suggestions'),
        (r'.*/api/user_question', items.UserQuestionHandler,
         {'application_settings': settings, 'handler': 'APIUserQuestion'}, 'api_user_question'),
        (r'.*/api/user_answer', items.UserAnswerHandler,
         {'application_settings': settings, 'handler': 'APIUserAnswer'}, 'api_user_answer'),
        (r'.*/api/best_answer', items.BestAnswerHandler,
         {'application_settings': settings, 'handler': 'APIBestAnswer'}, 'api_best_answer'),
        (r'.*/api/items', items.ItemsHandler,
         {'application_settings': settings, 'handler': 'Items'}, 'items'),
        (r'.*/', main.MainHandler,
         {'application_settings': settings, 'handler': 'Main'}, 'main'),
        (r'.*/user_question', user_question.UserQuestionHandler,
         {'application_settings': settings, 'handler': 'UserQuestion'}, 'user_question'),
        (r'.*/system_question', system_question.SystemQuestionHandler,
         {'application_settings': settings, 'handler': 'SystemQuestion'}, 'system_question'),
        (r'.*/first_time', first_time.FirstTimeHandler,
         {'application_settings': settings, 'handler': 'FirstTime'}, 'first_time'),
        (r'/static/(.*)', web.StaticFileHandler,
         {'path': os.path.join(base_dir, "web", "static")}),
    ],
    service_name='the-best',
    template_path=os.path.join(base_dir, "web", "templates"),
    autoreload=settings.AUTO_RELOAD)
