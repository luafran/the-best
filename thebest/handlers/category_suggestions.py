from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class CategorySuggestionsHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        prefix = self.get_query_arguments('prefix')[0]

        suggestions = []
        items = yield items_repository.get_category_suggestions(prefix)

        for item in items:
            suggestion = {
                'name': item,
                '_id': item
            }

            suggestions.append(suggestion)

        response = {
            "suggestions": suggestions
        }

        self.build_response(response)
