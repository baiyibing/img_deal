#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: model.py
@time: 2018/7/18 10:31
@desc:
'''
from sqlalchemy import *
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://lhuser:123456@120.79.37.165:5432/lhdw',echo=True)
DBsession = sessionmaker(bind=engine)
DBsession = DBsession()

engine2 = create_engine('oracle://baidu_map:yess5678@120.78.213.209:1521/xe',echo=True)
DBsession2 = sessionmaker(bind=engine2)
DBsession2 = DBsession2()

# 创建对象的基类:
Base = declarative_base()

class AreaImg(Base):
    __tablename__ = 'area_img'
    id = Column(Integer, primary_key=True)
    img = Column(BLOB)

class Test1(Base):
    __tablename__ = 'TEST1'
    id = Column(Integer, primary_key=True)
    img = Column(BLOB)
    name = Column(String)





