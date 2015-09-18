from tornado import gen

from thebest.common.handlers import base
from thebest.repos import items_repository


class MainHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        self.render('main.tpl')
