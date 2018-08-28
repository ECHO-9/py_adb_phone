# -*- coding: utf-8 -*-

import os
import subprocess
from PIL import Image
import sys
import re

#获取设备id
def get_devices():
    devices = subprocess.Popen(
        'adb devices'.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).communicate()[0]
    devices = devices.decode('utf-8')
    serial_nos = []
    filters = ['*', 'list', 'of', 'device', 'devices', 'attached', 'daemon', 'not', 'runing.', 'starting', 'it', 'now', 'on', 'port', '5037', 'started', 'successfully']
    for item in devices.split():
        if item.lower() not in filters:
            serial_nos.append(item)
    return serial_nos

#获取截图方式
def get_screenshot_id(id=1,device=''):
    if id > 4:
        print('无法截图')
        sys.exit()
    get_screen_shot(id,device)
    try:
        Image.open('screenshot/autoshot_{}.jpg'.format(device)).load()
        print('采用方式 {} 获取截图'.format(id))
        return id
    except Exception:
        id += 1
        return get_screenshot_id(id,device)

#屏幕截图
def get_screen_shot(id,device=''):
    if os.path.isfile('screenshot/autoshot_{}.jpg'.format(device)):
        os.remove('screenshot/autoshot_{}.jpg'.format(device))
    if 1 <= id <= 3:
        process = subprocess.Popen(
            'adb {} shell screencap -p'.format(device),
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if id == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif id == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        f = open('screenshot/autoshot_{}.jpg'.format(device), 'wb')
        f.write(binary_screenshot)
        f.close()
    elif id == 4:
        os.system('adb shell screencap -p /sdcard/autoshot_{}.jpg'.format(device))
        os.system('adb pull /sdcard/autoshot_{}.jpg ./screenshot'.format(device))

#获取屏幕尺寸
def get_screen_size(device=''):
    size_str = os.popen('adb {} shell wm size'.format(device)).read()
    hw = re.search(r'(\d+)x(\d+)', size_str)
    x = hw.group(1)
    y = hw.group(2)
    return x, y

#物理按键事件
def keyevent(key, device=''):
    cmdtext = 'adb {} shell input keyevent {}'.format(device,key)
    os.system(cmdtext)
    return 1

#点击事件
def click(pos_x, pos_y, device=''):
    cmdtext = 'adb {} shell input tap {} {}'.format(
        device,
        pos_x,
        pos_y
    )
    os.system(cmdtext)
    return 1

#滑动事件
def swipe(pos_x, pos_y, dpos_x, dpos_y, taptime=0, device=''):
    if taptime:
        cmdtext = 'adb {de} shell input touchscreen swipe {x1} {y1} {x2} {y2} {time}'.format(
            de = device,
            x1=pos_x,
            y1=pos_y,
            x2=dpos_x,
            y2=dpos_y,
            time = taptime
        )
    else:
        cmdtext = 'adb {de} shell input swipe {x1} {y1} {x2} {y2}'.format(
            de = device,
            x1=pos_x,
            y1=pos_y,
            x2=dpos_x,
            y2=dpos_y
        )
    os.system(cmdtext)
    return 1

#输入事件
def input(text, device=''):
    cmdtext = 'adb {} shell input text {}'.format(device, text)
    os.system(cmdtext)
    return 1