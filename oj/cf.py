#-*- coding:utf-8 -*-

import urllib.parse 
import urllib.request
import http.cookiejar
from tornado.httpclient import HTTPClient
from tornado.ioloop import PeriodicCallback

from bs4 import BeautifulSoup as bs

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

    HDU_SUBMIT_URL = 'http://codeforces.com/problemset/submit?csrf_token=efa72839550bd7924b2dff5dd26214d8' 

    HDU_LOGIN_URL = 'http://codeforces.com/enter?back=%2Fproblemset%2Fproblem%2F807%2FB'

    ACDREAM_HOST_URL = 'http://codeforces.com/'

    ACCOUNT = 'JJC'
    PASSWORD = '865975626'

    headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Origin':'http://codeforces.com',
            #'Cookie':'_ym_uid=1494382967271587659; JSESSIONID=6A9E21F28D3FF9C130D822328DA3A93C-n1; 39ce7=CFuTaqEW; evercookie_png=af1ax3ajrxaucfnml7; evercookie_etag=af1ax3ajrxaucfnml7; evercookie_cache=af1ax3ajrxaucfnml7; 70a7c28f3de=af1ax3ajrxaucfnml7; _ym_isad=2; lastOnlineTimeUpdaterInvocation=1494850166610; X-User=""; __utmt=1; __utma=71512449.12166834.1494382960.1494849891.1494855449.25; __utmb=71512449.3.10.1494855449; __utmc=71512449; __utmz=71512449.1494470540.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
            'Host':'codeforces.com',
            'Referer':'http://codeforces.com/enter?back=%2F',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            }


class SubmitHandler(Base):

    def get_csrf(self):
        request = urllib.request.Request(self.HDU_LOGIN_URL) 
        response = self.opener.open(request)
        text=response.read()
        text=bs(text, 'html5lib')
        sou=text.find('form',attrs={'method':'post'})
        sou=bytes(str(sou), encoding='utf-8')
        text=bs(sou, 'html5lib')
        soup=text.find('input')['value']
        return str(soup)

    def user_login(self, account=Base.ACCOUNT, password=Base.PASSWORD):
        print('Logining....')
        token=self.get_csrf()
        print(token)
        form_data={
                'csrf_token': token,
                'action':'enter',
                'ftaa':'af1ax3ajrxaucfnml7',
                'bfaa':'e601239f20b71bf69ff20c5607703ce0',
                'handle': account,
                'password': password,
                '_tta':'832',
                }
        '''
        response=HTTPClient().fetch(
                self.HDU_LOGIN_URL, method='POST', headers=self.headers, body=urlencode(form_data)
        )'''
        print(account)
        print(password)
        data = urllib.parse.urlencode(form_data).encode(encoding='utf-8')
        resquest = urllib.request.Request(self.HDU_LOGIN_URL, data, self.headers)
        response = self.opener.open(resquest)

        #resquest = HTTPClient().fetch(self.ACDREAM_HOST_URL)
        request = urllib.request.Request(self.ACDREAM_HOST_URL)
        response = self.opener.open(request)
        htmltext = str(response.read())
        if htmltext.find('JJC') > -1:
            print('Login success')
            return True
        else:
            print('Unlogin')
            return False

    def get_submit_data(self, the_id, language, code):
        postdata=dict(
                csrf_token=efa72839550bd7924b2dff5dd26214d8,
                ftaa=af1ax3ajrxaucfnml7,
                bfaa=e601239f20b71bf69ff20c5607703ce0,
                action=submitSolutionFormSubmitted,
                contestId=807,
                submittedProblemIndex=B,
                programTypeId=1,
                source=code,
                tabSize=4,
                sourceFile='',
                _tta=236,
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

#PeriodicCallback(SubmitHandler().user_login, 800000).start()
if __name__=='__main__':
    SubmitHandler().user_login();

