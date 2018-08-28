# -*- coding: utf-8 -*-

from common import wpq_json, wpq_adb, wpq_pic
import threading
import time
import random

def threadexe(js, rejs):
    devices = wpq_adb.get_devices()
    threadlist = []
    for device in devices:
        c = Excute(js, rejs, device)
        threadlist.append(threading.Thread(target=c.run, name=device))
    for t in threadlist:
        t.start()
    for t in threadlist:
        t.join()

#执行脚本(脚本文件，是否多设备)
def jsexe(filename, refilename='', is_mul=False):
    js = wpq_json.loadjson(filename)
    rejs = wpq_json.loadjson(refilename)
    if js == '':
        return 0
    if is_mul:
        threadexe(js,rejs)
    else:
        c = Excute(js,rejs)
        c.run()

class Excute(threading.Thread):
    # 参数
    S_H = 0
    S_W = 0
    SCREENSHOT_WAY = 0
    DEVICE = ''
    JS = ''
    RS = ''
    IS_RS = 0
    FLAG = 0

    # 初始化函数
    def __init__(self, js, rs, device='', is_rs=False):
        if device != '':
            self.DEVICE = '-s ' + device
        self.JS = js
        self.RS = rs
        self.IS_RS = is_rs
        self.SCREENSHOT_WAY = wpq_adb.get_screenshot_id(device=self.DEVICE)
        self.S_W, self.S_H = wpq_adb.get_screen_size(self.DEVICE)

    # 界面检测
    def __checkbg(self, checkimg):
        flag = 0
        wpq_adb.get_screen_shot(self.SCREENSHOT_WAY, self.DEVICE)
        pos = wpq_pic.get_img_pos('screenshot/autoshot_{}.jpg'.format(self.DEVICE), checkimg)
        if pos != (0, 0):
            flag = 1
        return flag

    # 检测并睡眠
    def __check(self, sleep, ischeck, img):
        s = 0
        if len(sleep) == 1:
            s = sleep[0]
        else:
            s = random.randint(sleep[0], sleep[1])
        time.sleep(s)
        # 没发现出错跳出
        if ischeck == 1 and self.__checkbg(img) == 0:
            return 0
        # 没发现不执行动作
        elif ischeck == 2 and self.__checkbg(img) == 0:
            return 2
        # 发现不执行动作
        elif ischeck == 3 and self.__checkbg(img) == 1:
            return 2
        # 没发现执行动作
        elif ischeck == 4 and self.__checkbg(img) == 0:
            return 1
        else:
            return 1

    # 操作分配
    def distribution(self, cmd):
        flag = self.__check(cmd['sleep'], cmd['ischeck'], cmd['checkimg'])
        if flag == 0:
            return 0
        elif flag == 2:
            return 1
        type = cmd['type']
        if type == 'keyevent':
            return wpq_adb.keyevent(cmd['key'], self.DEVICE)
        elif type == 'click':
            if cmd['clickimg'] == False:
                return wpq_adb.click(float(self.S_W) * float(cmd['pos'][0]), float(self.S_H) * float(cmd['pos'][1]), self.DEVICE)
            else:
                wpq_adb.get_screen_shot(self.SCREENSHOT_WAY, self.DEVICE)
                pos = wpq_pic.get_img_pos('screenshot/autoshot_{}.jpg'.format(self.DEVICE), cmd['clickimg'])
                return wpq_adb.click(pos[0], pos[1], self.DEVICE)
        elif type == 'input':
            return wpq_adb.input(cmd['key'], self.DEVICE)
        elif type == 'swipe':
            return wpq_adb.swipe(
                float(self.S_W)*float(cmd['pos'][0]),
                float(self.S_H)*float(cmd['pos'][1]),
                float(self.S_W)*float(cmd['dpos'][0]),
                float(self.S_H)*float(cmd['dpos'][1]),
                cmd['taptime'],
                self.DEVICE
            )
        else:
            print('未知操作')
            return 0

    # 脚本执行run
    def runjs(self, cmd):
        flag = 0
        for i in range(cmd['loop']):
            for ls in cmd['op']:
                if ls.__contains__('loop'):
                    flag = self.runjs(ls)
                else:
                    flag = self.distribution(ls)
                if flag == 0:
                    if self.IS_RS:
                        self.runjs(self.RS)
                    else:
                        print('第{}步失败，退出'.format(ls['num']))
                        return 0
        self.FLAG = flag
        return flag

    def run(self):
        if self.runjs(self.JS) == 1:
            print('执行成功')
        else:
            print('执行失败')

    def get_result(self):
        return self.FLAG