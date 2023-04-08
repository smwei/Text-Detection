# OBB xml(rolabelImg)->txt(yolo)
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import math
from os import getcwd
from cmath import pi
import os
import xml.etree.ElementTree as ET
import pickle
import math

classes1_5 = ['text']  # 改成自己的类别

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] * dw
    y = box[1] * dh
    w = box[2] * dw
    h = box[3] * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open('.//VOC2007//Annotations//%s.xml' % (image_id), encoding='UTF-8')    # 存放xml标签的文件夹
    out_file = open('.//VOC2007//YOLOLabels//%s.txt' % (image_id), 'w')    # 转换出的txt标签存放文件夹
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes1_5 or int(difficult) == 1:
            continue
        cls_id = classes1_5.index(cls)
        xmlbox = obj.find('robndbox')
        b = [float(xmlbox.find('cx').text), float(xmlbox.find('cy').text), float(xmlbox.find('w').text),
             float(xmlbox.find('h').text)]
        theta = float(xmlbox.find('angle').text)
        b1, b2, b3, b4 = b
        theta *= (180 / pi)
        if b3 < b4:
            b = (b1, b2, b4, b3)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + " " + str(theta) + '\n')


if not os.path.exists('labels/'):
    os.makedirs('labels/')    # yolo格式的标签存放地址
fileDir = ".//VOC2007//Annotations"
image_name = os.listdir(fileDir)    # 获取指定文件夹下所有文件名，含后缀
image_ids = [x.split('.')[0] for x in image_name]    # 去除文件名列表的后缀
print(image_ids)
for image_id in image_ids:
    convert_annotation(image_id)
print("转换完成")