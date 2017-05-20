#-*- coding:utf-8 -*-

def get_limit(the_str):
    l = len(the_str)
    re = []
    for i in range(l):
        if the_str[i]=='/':
            i=i+1
            st=''
            while the_str[i]<='9' and the_str[i]>='0' and i<l:
                st+=the_str[i]
                i=i+1
            if st:
                re.append(st)
            if len(re)==2:
                return re  

def get_num(the_str):
    l=len(the_str)
    i,re=0,''
    while i<l:
        j=the_str[i]
        while j<='9' and j>='0' and i<l:
            re=re+j
            i=i+1
            j=the_str[i]
        i=i+1
    return int(re)
