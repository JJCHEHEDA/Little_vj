#-*- coding:utf-8 -*-

import tornado.web
from db import orm
from tornado.httpclient import HTTPClient
from oj import hdu
from view import CookieHandler
import tornado.gen
import tornado.ioloop
import tornado.httpserver

from bs4 import BeautifulSoup as bs 

pro_orm = orm.ProManagerORM()
user_orm = orm.UserManagerORM()
sub_orm = orm.SubManagerORM()

global haha 
haha = False

class MainHandler(CookieHandler):
    def get(self):
        #if_cookie = self.current_user
        #print(if_cookie)
        self.render('base.html')

class ProListHandler(CookieHandler):
    def get(self):
        problems = pro_orm.GetProList()
        self.render('./vjudge/pro_list.html', problems=problems) 

class ProInfoHandler(CookieHandler):
    def get(self, num):
        pro_info = pro_orm.GetProById(num)
        self.render('./vjudge/pro_info.html', problem=pro_info)

class ProSubmitHandler(CookieHandler):
    def get(self):
        the_id=self.get_query_argument('id')
        the_id = int(the_id)
        the_title=pro_orm.GetTiById(the_id) 
        data={}
        data['id']=the_id
        data['title']=the_title[0]
        self.render('./vjudge/submit.html', **data, language=hdu.Base().SUBMIT_LANGUAGE)

    def post(self):
        hdu.SubmitHandler().user_login()
        source_code=self.get_argument('source_code')
        language=self.get_argument('code_language')
        the_id=self.get_query_argument('id')

        submit_data=hdu.SubmitHandler().get_submit_data(the_id, language, source_code)
        hdu.SubmitHandler().submiting(submit_data) 
        #self.render('./vjudge/status.html', flag=False, d={}, info=())
        global haha
        haha=True
        self.redirect('/vjudge/status')

class StatusHandler(CookieHandler):
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
        global haha
        for i in range(9,len(art)):
            num=8
            if art[i]=='JJC':
                while num>=0:
                    d2[art[i%9]]=art[i]
                    i=i-1
                    num=num-1
                d1.append(d2)
                break
        flag=False
        if d1:
            q = d1[0]['Judge Status']
            if q != 'Queuing' and q != 'Compiling' and haha == True:
                sub_orm.CreateNewSub(d1)
                haha = False
            if q != 'Queuing' and q != 'Compiling':
                flag=True
        info = sub_orm.InfoAll()
        self.render('./vjudge/status.html', flag=flag, q=d1, info=info)

class AuthHandler(CookieHandler):
    def get(self, auth_type):
        print(self.current_user)
        if self.current_user:
            print('xxx')
            self.redirect("/")
        self.render("auth.html")

    def post(self, auth_type):
        if auth_type == 'login':
            print(self.get_body_argument("user", ""))
            print(self.get_body_argument("password", ""))
            user_info={
                "user": self.get_body_argument("user", ""),
                "password": self.get_body_argument("password", ""),
            }
            self.user_login(user_info)
            new_token = self.new_token()
            print(new_token)
            the_id = user_orm.IdByInfo(user_info) 
            print(type(the_id))
            print(the_id)
            print('aaa')
            for i in the_id:
                id = i
            the_id = int(id)
            print(the_id)
            print(type(the_id))
            self.on_login_success(new_token, the_id)
        else:
            li = []
            li.append({
                "username": self.get_body_argument("username", ""),
                "password": self.get_body_argument("password", ""),
                #"repassword": self.get_body_argument("repassword", ""),
                #"email": self.get_body_argument("email", ""),
            })
            self.user_register(li)
        self.redirect('/')

    def user_login(self, form_data):
        if_pass = user_orm.If_Name(form_data['user'])
        if not if_pass:
            self.write("用户名不存在")
            return 
        if not if_pass:
            self.write("密码不正确")
            return 

    def user_register(self, form_data):
        user_orm.CreateNewUser(form_data)
            

