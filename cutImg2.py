#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: cutImg.py
@time: 2018/7/17 14:50
@desc:图片裁剪测试,相关链接：https://blog.csdn.net/wuguangbin1230/article/details/71119955
'''

import os
from PIL import Image
import re
ori_dir = 'img'
target_w = 1000
target_h = 600
target_dir = 'img_deal'
for path in os.listdir(ori_dir):
    img = Image.open(ori_dir+'/'+path)
    w, h = img.size
    if w*100/h > target_w*100/target_h:
        cut_w = h*target_w*100/target_h/100
        cut_h = h
    else:
        cut_w = w
        cut_h = w*target_h*100/target_w/100

    box = ((w-cut_w)/2,(h-cut_h)/2,(w+cut_w)/2,(h+cut_h)/2)
    img = img.crop(box)
    img = img.resize((target_w, target_h))
    img.show()
    img.save(target_dir+'/'+path)

