#_*_ coding:utf-8 _*_
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import tornado.gen

#from db import orm

from bs4 import BeautifulSoup as bs 
from tornado.options import define,options

#sub_orm = orm.SubManagerORM()

define("port",default=8000,help="run on the given port",type=int)

class GetHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        url = 'http://acm.hdu.edu.cn/status.php'
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(client.fetch,url)
        text = response.body 
        text = bs(text,'lxml')
        sou = text.find_all('div')
        sou = str(sou)
        sou = bs(sou,'lxml')
        art = []
        for i in sou.find_all('td'):
           art.append(i.text)
        d1,d2 = [],{}
        a,b = 0,0
        for i in range(9,len(art)):
            num=8
            if art[i]=='14-软2-郭慧峰':
                while num>=0:
                    d2[art[i%9]]=art[i]
                    i=i-1
                    num=num-1
                d1.append(d2)
                break
        print(d1)
        #sub_orm.CreateNewSub(d1)

        d_json = json.dumps(d1)
        #self.redirect('/vjudge/status')
        self.write(d_json)
        self.finish()

if __name__ == '__main__':
    app = tornado.web.Application(
            handlers=[(r'/',GetHandler)]
            )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
