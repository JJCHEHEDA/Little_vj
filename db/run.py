#-*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

from bs4 import BeautifulSoup as bs

from other import get_limit

import orm
pro_orm = orm.ProManagerORM()

pi = {'Problem Description':'description',
        'Input':'input',
        'Output':'output',
        'Sample Input':'sample_input',
        'Sample Output':'sample_output',
        'Source':'source'
        }

num=1000
real_info=[]
er='System Message'

for i in range(num,num+201): 
    url='http://acm.hdu.edu.cn/showproblem.php?pid='+str(i) 
    client=tornado.httpclient.HTTPClient()
    response=client.fetch(url)
    text=response.body

    text=bs(text,'html5lib')
    sou=text.find_all('td',attrs={'align':'center'})

    sou=list(sou)
    art=str(sou[2])
    info={'pro_id':i,
          'pro_title':er,
          'time_limit':0,
          'memory_limit':0,
          'input':'',
          'output':'',
          'sample_input':'',
          'sample_output':'',
          'source':'',
          'description':''
          }

    art=bs(art,'html5lib')
    info['pro_title']=art.find('h1').text

    if info['pro_title']!=er:
        info['pro_id']=i
        if i%10==0 :
            print(i)
        the_limit=str(art.find('span').text)
        the_limit=get_limit(the_limit) 
        info['time_limit']=int(the_limit[0])
        info['memory_limit']=int(the_limit[1])

        the_art=art.find_all('div', attrs={'class':'panel_content'})
        the_text,the_title=[],[] 
        for j in the_art:
            the_text.append(j.text)
        the_art=art.find_all('div', attrs={'class':'panel_title','align':'left'})
        for j in the_art:
            the_title.append(j.text)
        for j in range(len(the_title)):
            q=the_title[j]
            if q!='Recommend' and q!='Author':
                info[pi[q]]=the_text[j]

    real_info.append(info)

print(real_info[0]['pro_title'])
pro_orm.CreateNewPro(real_info)


