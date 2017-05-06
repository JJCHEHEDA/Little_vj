#-*- coding:utf-8 -*-

import tornado.web

class AuthUI(tornado.web.UIModule):
    def render(self):
        return self.render_string("auth.html")

