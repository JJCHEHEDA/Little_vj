#-*- coding:utf-8 -*-

#登录的是hdu，hdu采用了重定向，代码中也对重定向做了处理，返回码会是302，但是依然能够登录

import os,sys
import requests
import requests.utils
import pickle

headers = {
    'Pragma': 'no-cache',
    'Origin': 'http://acm.hdu.edu.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

class Client():
    def __init__(self):
        self._clear()
        self.root_path = os.path.dirname(os.path.realpath(sys.argv[0]))

    def _clear(self):
        self.session = requests.Session()
        self.session.headers = headers

    def post(self, url, data):
        response = self.session.post(url, data = data)
        if response.status_code == 200 or response.status_code == 302:
            self.session.headers['Referer'] = response.url
        return response

    def get(self, url):
        response = self.session.get(url)
        if response.status_code == 200 or response.status_code == 302:
            self.session.headers['Referer'] = response.url
        return response

    def load_cookies(self, path):
        with open(path, 'rb') as f:
            self.session.cookies = requests.utils.cookiejar_from_dict(pickle.load(f))

    def save_cookies(self, path):
        with open(path, 'wb') as f:
            cookies_dic = requests.utils.dict_from_cookiejar(self.session.cookies)
            pickle.dump(cookies_dic, f)

    def submitcode(self, submitform, proId):
        submiturl = ''
        response = self.post(submiturl, data = submitform)
        if response.status_code == 200 or response.status_code == 300:
            return True
        else:
            return False
    
    def login(self, username, password):
        self._clear()
        loginurl = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
        #登录表单
        preload ={
            'username': username,
            'userpass': password,
            'login': 'Sign In',
        }
        response = self.post(loginurl, data = preload)
        if (response.status_code == 200 or response.status_code == 302):# and len(response.history) > 0:
            cookies_file = os.path.join(self.root_path, username + ".cookies")
            self.save_cookies(cookies_file)
            print("login success")
            return True
        else:
            print("login fail")
            return False

    def check_login(self):
        check_url = 'http://acm.hdu.edu.cn/viewcode.php?rid=13608122'
        response = self.get(check_url)
        #with open("test.html","wb") as f:
        #    f.write(bytes(response.text, encoding='utf-8'))
        if response.url == check_url:
            print('已登录')
            return True
        else:
            print('未登录')
            return False
    
    def cookies_login(self, username):
        self._clear()
        cookies_file = os.path.join(self.root_path, username+'.cookies')
        if not os.path.exists(cookies_file):
            print("cookie login fail: " + username + ".cookies not exists")
            return False
        self.load_cookies(cookies_file)
        if not self.check_login():
            print("cookies login fail: " + username + '.cookies expire')
            return False
        print("cookies login success!")
        return True

if __name__ == '__main__':
    client = Client()
    #client.login('YJaiLSY', '865975626')
    #client.cookies_login('YJaiLSY')

