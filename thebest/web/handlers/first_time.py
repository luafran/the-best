from tornado import gen

from thebest.common.handlers import base


class FirstTimeHandler(base.BaseHandler):

    @gen.coroutine
    def get(self):
        self.render('bye.tpl')
