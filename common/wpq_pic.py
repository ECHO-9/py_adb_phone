# -*- coding: utf-8 -*-

import aircv
import cv2
from PIL import Image
import numpy
from io import BytesIO

def get_byte(img):
    temp_io = BytesIO()
    img.save(temp_io, 'png')
    return temp_io

def cv2_to_image(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def image_to_cv2(img):
    return cv2.cvtColor(numpy.asarray(img),cv2.COLOR_RGB2BGR)

def get_img(filename, type='cv2'):
    if type == 'cv2':
        return cv2.imread(filename)
    else:
        return Image.open(filename)

#获取图片位置
def get_img_pos(bg, flag):
    try:
        imgbg = aircv.imread(bg)
        imgflag = aircv.imread(flag)
        pos = aircv.find(imgbg,imgflag)
        if pos == None:
            pos = (0, 0)
        return pos
    except Exception:
        return (0, 0)

#二值化获取边框
def get_contours(img,value):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, value, 255, cv2.THRESH_BINARY)
    im, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
