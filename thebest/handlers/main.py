from tornado import gen

from thebest.common.handlers import base


class MainHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        self.render('main.tpl')
