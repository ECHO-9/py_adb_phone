# -*- coding: utf-8 -*-

import json
import os

JSON_PATH='D:/PythonS/Phone/config/'

def loadjson(filename):
    if os.path.isfile(JSON_PATH + filename):
        with open(JSON_PATH + filename) as jsonfile:
            print('读取配置文件'+filename)
            return json.load(jsonfile)
    else:
        print('无配置文件')
        return ''
