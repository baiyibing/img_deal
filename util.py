#!/usr/bin/env python
#encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: keywords.py
@time: 2018/6/7 15:54
@desc: 辅助挑选出标题等关键信息
'''
import re
import jieba
from config import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def isZbmc(zbmcStr):
    zbmcStr = str(zbmcStr)
    zbmcStr = re.sub(u'[\s止]', '', zbmcStr.decode('utf8'))
    zbmcStr = re.sub(u'　', '', zbmcStr)
    zbmcStr = re.sub(u'[\(\（].+[\）\)]', '', zbmcStr)
    return zbmcStr in zbmcs

def isZbzm(zbzmStr, percent=zmPercent, getStr=False):
    if not zbzmStr:
        return False
    zbzmStr = str(zbzmStr)
    zbzmStr = re.sub(u'[\s止]', '', zbzmStr.decode('utf8'))
    zbzmStr = re.sub(u'　', '', zbzmStr)
    zbzmStr = re.sub(u'[\(\（].+[\）\)]', '', zbzmStr)
    if zbzmStr=='':
        return False
    zbzmIn = list(jieba.cut(zbzmStr))
    for zbzm in zbdbs:
        count = 0
        temp = list(jieba.cut(zbzm.decode('utf8')))
        for i in zbzmIn:
            if i in temp:
                count+=1
        if count*100/len(zbzmIn)>percent and count*100/len(temp)>percent:
            if getStr:
                return zbzm
            return True
    if getStr:
        return zbzmStr
    return False

def isZbfm(zbfmStr, getStr=False):
    zbfmStr = str(zbfmStr)
    zbfm = re.sub(u'[\s止]', '', zbfmStr.decode('utf8'))
    zbfm = re.sub(u'　', '', zbfm)
    zbfm = re.sub(u'[\(\（].+[\）\)]', '', zbfm)
    zbfm = re.sub(u'[±%]+', '', zbfm)
    zbfm = re.sub(u'\d.+月', '', zbfm)
    for i in fmDealer:
        if zbfm in fmDealer[i]:
            if getStr:
                return str(i)
            return str(i) in zbfms
    if getStr:
        return str(zbfm)
    return str(zbfm) in zbfms

def zbfmDelSpace(zbfmStr):
    if not zbfmStr:
        return zbfmStr
    zbfmStr = str(zbfmStr)
    zbfm = re.sub(u'[\s止]', '', zbfmStr.decode('utf8'))
    zbfm = re.sub(u'　', '', zbfm)
    zbfm = re.sub(u'[±%]+', '', zbfm)
    zbfm = re.sub(u'\d.+月', '', zbfm)
    zbfm = re.sub(u'[\(\（][\）\)]', '', zbfm)
    return str(zbfm)


def isObject(objectStr):
    objectStr = str(objectStr)
    objectStr = re.sub(u'\s', '', objectStr.decode('utf8'))
    objectStr = re.sub(u'　', '', objectStr)
    for object in objectmc:
        if objectStr == object['text']:
            return object
    return None

def parseZbzm(inStr):
    inStr = str(inStr)
    inStr = re.sub(u'\s', '', inStr.decode('utf8'))
    inStr = re.sub(u'　', '', inStr)
    inStr = re.sub(u'[\(\（].+[\）\)]', '', inStr)
    for i in zmDealer:
        if str(inStr) in zmDealer[i]:
            return str(i)
    return str(inStr)

def keyReplace(inStr):
    keys = {
        '龙华': ['龙华区'],
        '深圳': ['全市']
    }
    for i in keys:
        for j in keys[i]:
            inStr = re.sub(j.decode('utf8'), i, inStr)
    return str(inStr)

def delPreStr(inStr):
    inStr = re.sub(u'\s', '', inStr)
    inStr = re.sub(u'　', '', inStr)
    inStr = re.sub(u'其中[:：]', '#', inStr)
    # inStr = re.sub(u'\d+[\、\.]', '', inStr)
    # inStr = re.sub(u'[\(\（].+?[\）\)]', '', inStr)
    # inStr = re.sub(u'^[一二三四五六七八九十]?\、', '', inStr)
    inStr = re.sub(u'^[\、\.]', '', inStr)
    if '合计' in inStr:
        inStr = '合计'
    return keyReplace(inStr)

def delTime(inStr):
    return re.sub(u'\d+年[\d-]+月|\d+年|[\d\-]月', '', inStr.decode('utf8'))

def getFirstChar(str, codec='utf8'):
    str = str.decode(codec).encode("GBK")

    if str < "\xb0\xa1" or str > "\xd7\xf9":
        return '0'
    if str < "\xb0\xc4":
        return "a"
    if str < "\xb2\xc0":
        return "b"
    if str < "\xb4\xed":
        return "c"
    if str < "\xb6\xe9":
        return "d"
    if str < "\xb7\xa1":
        return "e"
    if str < "\xb8\xc0":
        return "f"
    if str < "\xb9\xfd":
        return "g"
    if str < "\xbb\xf6":
        return "h"
    if str < "\xbf\xa5":
        return "j"
    if str < "\xc0\xab":
        return "k"
    if str < "\xc2\xe7":
        return "l"
    if str < "\xc4\xc2":
        return "m"
    if str < "\xc5\xb5":
        return "n"
    if str < "\xc5\xbd":
        return "o"
    if str < "\xc6\xd9":
        return "p"
    if str < "\xc8\xba":
        return "q"
    if str < "\xc8\xf5":
        return "r"
    if str < "\xcb\xf9":
        return "s"
    if str < "\xcd\xd9":
        return "t"
    if str < "\xce\xf3":
        return "w"
    if str < "\xd1\x88":
        return "x"
    if str < "\xd4\xd0":
        return "y"
    if str < "\xd7\xf9":
        return "z"

def getFirstChars(inStr):
    result = ''
    inStr = inStr.decode('utf8')
    for i in inStr:
        result += getFirstChar(i)
    return result

if __name__ == '__main__':
    print delPreStr(u'7、一、国、地税收入')



