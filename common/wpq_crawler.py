# -*- coding: utf-8 -*-

import requests

def baidu_search(text):
    bd_url = 'https://www.baidu.com/s'
    headers = {
       'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    data = {
       'wd' : text
    }
    res  = requests.get(bd_url,params=data,headers=headers)
    res.encoding = 'utf-8'
    return res

