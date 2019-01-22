#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: config.py
@time: 2018/7/6 17:10
@desc:
'''
# from sqlalchemy import *
# from sqlalchemy.orm import sessionmaker
# engine = create_engine('oracle://baidu_map:yess5678@120.78.213.209:1521/xe', pool_size=100, encoding='utf8')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
import psycopg2
import sys
reload(sys)
sys.setdefaultencoding('utf8')

CONN = psycopg2.connect(database="lhdw", user="lhuser", password="123456", host="120.79.37.165", port="5432")
DBSession = CONN.cursor()

time_code = '2018年05月'
object_name = '龙华'

# 用于选出对象名称一列，优先级最大的认为为对象名
objectmc = [{
    'text': '项目名称',
    'priority': 10
},{
    'text': '单位名称',
    'priority': 1
},{
    'text': '企业名称',
    'priority': 2
},{
    'text': '行业名称',
    'priority': 1
},{
    'text': '区域',
    'priority': 1
},{
    'text': '国别地区',
    'priority': 1
},{
    'text': '项目',
    'priority': 1
},{
    'text': '对象名称',
    'priority': 1
}]

# 用于查找指标对比名称，zbPercent设置匹配度，100完全匹配，具体见util的isZbzm方法
zmPercent = 80
zbdbs = ['工业产值', '税收收入', '规模以上工业增加值', '常住人口', '用电量', '固定资产投资完成额', '出口总额', '出口交货值', '进出口总额', '规模以上工业总产值', '规模以上服务业', '辖区面积', '社会消费品零售总额', '一般公共预算收入', '利润总额', '地区生产总值']

# 用于定位指标副名
zbfms = ['累计同比', '上年同期累计', '上期数', '计量单位', '占比', '环比', '排名', '累计数', '计算单位', '本期数']
fmDealer = {
    '占比': ['累计比重', '占进口比重', '比重', '占出口比重'],
    '累计同比': ['累计同比', '比去年同期', '比上年同期', '增长', '同比'],
    '累计数': ['本年累计', '总量', '本年累计金额', '自本年初累计', '累计值', '累计'],
    '上期数': ['上月数'],
    '本期数': ['本月', '本月数'],
    '计算单位': ['单位', '计量单位']
}

# 用于查找指标名称一列
zbmcs = ['指标名称']

# 将表中工业产值、营业额等识别成指标主名，并将该列认作累计数
zmDealer = {
    '累计数': ['工业产值', '营业额', '零售额', '零售额', '零售额', '零售额', '营业收入', '销售额'],
    '已完成': ['投资额']
}

# 特殊处理，将数组中的字符替换成前面的
replaceKeys = {
    '龙华': ['龙华区'],
    '深圳': ['全市']
}

# 判断为表格最后一列
endKeys = ['注：', '-\d+-']
# 有以下字符该行忽略
ignoreRows = ['-\d+-', '。']
# 以下副指标忽略
ignoreZbfms = ['备注', '计算单位']


