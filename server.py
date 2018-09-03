# -*- coding:utf-8 -*-

import os.path
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options

import my_uimodules

from view import view
from oj import get_status

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r'/', view.MainHandler),
                (r'/vjudge/problem', view.ProListHandler),
                (r'/vjudge/problem/(\w+)/', view.ProInfoHandler),
                (r'/vjudge/submit', view.ProSubmitHandler),
                (r'/vjudge/status', view.StatusHandler),
                (r'/vjudge/(login|register)', view.AuthHandler),
                (r'/getstatus', get_status.GetHandler),
        ]
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                ui_modules=my_uimodules,
                cookie_secret='11',
                debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(8000)
    print("Your application is running here: http://localhost:8000")
    tornado.ioloop.IOLoop.current().start()
