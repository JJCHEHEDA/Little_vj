#-*- coding:utf-8 -*-

import urllib.parse 
import urllib.request
import http.cookiejar
from tornado.httpclient import HTTPClient
from tornado.ioloop import PeriodicCallback

class Base(object):
    SUBMIT_LANGUAGE = {
            'G++': 0,
            'GCC': 1,
            'G++': 2,
            'C': 3,
            'Pascal': 4,
            'Java': 5,
            'C#': 6
    }

    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    HDU_SUBMIT_URL = 'http://acm.hdu.edu.cn/submit.php?action=submit' 

    HDU_LOGIN_URL = 'http://acm.hdu.edu.cn/userloginex.php?action=login'

    ACDREAM_HOST_URL = 'http://acm.hdu.edu.cn'

    ACCOUNT = 'YJaiLSY'
    PASSWORD = '865975626'

    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            }


class SubmitHandler(Base):

    def user_login(self, account=Base.ACCOUNT, password=Base.PASSWORD):
        print('Logining....')
        form_data={
                'username': account,
                'userpass': password,
                'login': 'Sign In',
                }
        '''
        response=HTTPClient().fetch(
                self.HDU_LOGIN_URL, method='POST', headers=self.headers, body=urlencode(form_data)
        )'''

        data = urllib.parse.urlencode(form_data).encode(encoding='utf-8')
        resquest = urllib.request.Request(self.HDU_LOGIN_URL, data, self.headers)
        response = self.opener.open(resquest)

        #resquest = HTTPClient().fetch(self.ACDREAM_HOST_URL)
        request = urllib.request.Request(self.ACDREAM_HOST_URL)
        response = self.opener.open(request)
        htmltext = str(response.read())
        if htmltext.find('YJaiLSY') > -1:
            print('Login success')
            return True
        else:
            print('Unlogin')
            return False

    def get_submit_data(self, the_id, language, code):
        postdata=dict(
                check=0,
                problemid=the_id,
                language=self.SUBMIT_LANGUAGE[language],
                usercode=code
               ) 
        print(postdata)
        print(type(postdata))
        return postdata

    def submiting(self, submit_data):
        '''
        response = HTTPClient().fetch(
                self.HDU_SUBMIT_URL, method='POST', body=urllib.parse.urlencode(submit_data)
                )
        '''
        print(submit_data)
        data = urllib.parse.urlencode(submit_data).encode(encoding='utf-8')
        request = urllib.request.Request(self.HDU_SUBMIT_URL, data, self.headers)
        response = self.opener.open(request)




PeriodicCallback(SubmitHandler().user_login, 800000).start()
