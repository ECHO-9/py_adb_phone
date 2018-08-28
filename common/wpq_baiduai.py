# -*- coding: utf-8 -*-

from aip import AipOcr, AipNlp
from PIL import Image

#百度账号ID,配置信息
BAIDU_KEY = {
    'PIC' :{
        'APP_ID': '10838860',
        'API_KEY' : 'fOWYnTqqlj8O2FsvsbH7cyXN',
        'SECRET_KEY' : '2vCqq81Eyhgk42GzWGBDOysIlaqw5pMq'
    },
    'WORD':{
        'APP_ID': '11176031',
        'API_KEY': 'ZTlXK8xAHiTvfkEW0yxW0mrU',
        'SECRET_KEY': 'tG6arXgb7ytrRCFCORq7lPc1Bqge3BpY'
    }
}

options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

#获取中文
def get_chinese(img):
    aipOcr = AipOcr(BAIDU_KEY['PIC']['APP_ID'], BAIDU_KEY['PIC']['API_KEY'], BAIDU_KEY['PIC']['SECRET_KEY'])
    result = aipOcr.basicGeneral(img,options)
    return  result

def get_morphology(text):
    client = AipNlp(BAIDU_KEY['WORD']['APP_ID'], BAIDU_KEY['WORD']['API_KEY'], BAIDU_KEY['WORD']['SECRET_KEY'])
    results = client.lexer(text)['items']
    word_list = {}
    for result in results:
        if result['ne'] != '':
            if result['item'] in word_list.keys():
                word_list[result['item']] += 1
            else:
                word_list[result['item']] = 1
        elif result['pos'] != 'w' and result['pos'] != 'u' and result['pos'] != 'm':
            if result['item'] in word_list.keys():
                word_list[result['item']] += 1
            else:
                word_list[result['item']] = 1
    word = []
    for i in word_list:
        j = word_list[i]
        if j>3:
            word.append(i)
    print(word)


    print(word_list)