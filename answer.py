# -*- coding: utf-8 -*-

import jsexe as js
import time
from common import wpq_adb, wpq_pic, wpq_json, wpq_baiduai, wpq_crawler, wpq_mongo
import numpy as np
import re

#选择
def ans_touch(choice, point):
    return wpq_adb.click(360,point[3]-(4-choice)*100)

#搜索答案
def ans_get_answer(words):
    num = len(words)
    question = ['', '', '', '']
    for i in range(num - 1, -1, -1):
        if i > 1:
            question[i - 1] = words[i]['words'][2:]
        else:
            question[0] = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。?？、~@#￥%……&*（）]+","",words[i]['words']) + question[0]
    mongo = wpq_mongo.mongodb('answer','youku')
    que = {"question":question[0]}
    ans = mongo.select(que,True)
    print(ans)
    if ans == None:
        html = wpq_crawler.baidu_search(question[0]).text
        ans_list = []
        if html.count(question[1]) > html.count(question[2]):
            if html.count(question[1]) > html.count(question[3]):
                return 1
            else:
                return 3
        else:
            if html.count(question[2]) > html.count(question[3]):
                return 2
            else:
                return 3
    else:
        ans = ans['answer']
        if question[3] == ans:
            return 3
        elif question[2] == ans:
            return 2
        else:
            return 1

#错题处理
def ans_error():
    print(3)

#开始答题
def ans_begin():
    id = wpq_adb.get_screenshot_id()
    flag = True
    point = []
    while True:
        wpq_adb.get_screen_shot(id)
        if flag:
            pos = wpq_pic.get_img_pos(r'screenshot\2.jpg', r'config\img\zzpp.jpg')
            if pos != (360.5, 538.0):
                img, point = deal_pic()
                ans_value = ans_get_answer(wpq_baiduai.get_chinese(img.getvalue())['words_result'])
                if ans_touch(ans_value, point) == 1:
                    print('选择成功')
                    flag = False
                else:
                    print('操作失败')
                    return 0
            else:
                print('继续检测题目')
        else:
            print('7')
        time.sleep(1)

#打开app
def ans_open_app():
    c = js.Excute('youku.json', 'youku.json')
    c.run()
    return c.get_result()

#初始函数
def answer():
    if ans_open_app()==1:
        ans_begin()
    else:
        print('程序开启失败')

#图片处理
def deal_pic():
    # pic_path = r'screenshot\autoshot_.jpg'
    pic_path = r'screenshot\3.png'
    img = wpq_pic.get_img(pic_path,'cv2')
    contours = wpq_pic.get_contours(img, 254)
    point = []
    long = 0
    for contour in contours:
        if len(contour) > 100 :
            temp_max = contour.max(axis=0)[0]
            temp_min = contour.min(axis=0)[0]
            temp_long = np.hypot(temp_max[0]-temp_min[0], temp_max[1]-temp_min[1])
            if temp_long > long:
                long = temp_long
                point = [temp_min[0], temp_min[1], temp_max[0], temp_max[1]]
    img = img[point[1]+140:point[3], point[0]:point[2]]
    return img, point



def answer2():
    text='新浪财经讯洪涛股份4月的最后一个交易日披露年报，2017年实现营业收入33.31亿元，同比增长15.77%，归母净利润1.37亿元，同比增长4.88%。　　洪涛股份以装修装饰业务起家，2015年开始跨界涉足教育产业，按年报中的说法，公司目前是“以建筑装饰为主业，以职业教育为第二主业”。　　或许正是因为没有把教育当作“第一主业”，相比同样转型职业教育的文化长城和开元股份等上市公司，洪涛股份的业绩实在有些拿不出手。3%的净利率和ROE显示业务基本没有盈利能力，而66%的负债率和负的经营现金流也表明公司日常经营面临一定压力。　　将两项主业拆分开来看，相比一直平稳的原装修业务，布局已三年之久的职业教育产业似乎更有“看点”。新浪财经结合年报，带大家着重了解一下洪涛股份转型的成绩单。'
    wpq_baiduai.get_morphology(text)