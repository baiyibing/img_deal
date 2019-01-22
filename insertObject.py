#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: insertMonth.py
@time: 2018/7/11 14:30
@desc:
'''
from util import CONN,DBSession,getFirstChars
session = DBSession

def createArea():
    session.execute('SELECT DISTINCT area_name from temp1 WHERE area_id IS NULL')
    for row in session.fetchall():
        session.execute("INSERT INTO dw_area(area_name) VALUES('"+row[0]+"') ON conflict(area_name) DO nothing")
    CONN.commit()
    print 'createArea', 'complete!'

def createExcel():
    createArea()
    session.execute('SELECT DISTINCT excel_name, area_id from temp1 WHERE excel_id2 IS NULL')
    for row in session.fetchall():
        session.execute("INSERT INTO dw_zhs_d_excel(excel_name, excel_code, area_id) VALUES('"+row[0]+"','"+getFirstChars(row[0])+"',"+str(row[1])+") ON conflict(excel_name, area_id) DO nothing")
    CONN.commit()
    print 'createExcel', 'complete!'

def createSheet():
    createExcel()
    session.execute('SELECT DISTINCT sheet_name, excel_id2 from temp1 WHERE sheet_id IS NULL')
    for row in session.fetchall():
        session.execute("INSERT into dw_zhs_d_sheet(sheet_name,excel_id,sheet_code) VALUES('"+row[0]+"','"+str(row[1])+"','"+getFirstChars(row[0])+"') ON conflict(sheet_name,excel_id) DO nothing")
    CONN.commit()
    print 'createSheet', 'complete!'

def createTable():
    createSheet()
    session.execute('SELECT DISTINCT table_name, sheet_id from temp1 WHERE table_id IS NULL')
    for row in session.fetchall():
        session.execute("INSERT into dw_zhs_d_table(table_name,sheet_id,table_code) VALUES('"+row[0]+"','"+str(row[1])+"','"+getFirstChars(row[0])+"') ON conflict(table_name,sheet_id) DO nothing")
    CONN.commit()
    print 'createTable', 'complete!'

def createObject():
    createTable()
    session.execute('SELECT DISTINCT object_name from temp1 WHERE object_id IS NULL')
    for row in session.fetchall():
        session.execute("INSERT into dw_zhs_d_object(object_name) VALUES('"+row[0]+"') ON conflict(object_name) DO nothing")
        session.execute("UPDATE dw_zhs_d_object set object_id=object_id1, object_code=object_id1,object_order=object_id1 where object_name='"+row[0]+"' and object_code is NULL")
    CONN.commit()
    print 'createObject', 'complete!'

def createZbzm():
    createObject()
    session.execute('SELECT DISTINCT zbzm_name,table_id from temp1 WHERE zbzm_id IS NULL')
    for row in session.fetchall():
        session.execute("INSERT into dw_zhs_d_zbzm(zbzm_name,table_id,zbzm_code) VALUES('" + row[0] + "','" + str(row[1]) + "','" + getFirstChars(row[0]) + "') ON conflict(zbzm_name,table_id) DO nothing")
    CONN.commit()
    print 'createZbzm', 'complete!'

def createZbfm():
    createZbzm()
    session.execute('SELECT DISTINCT zbfm_name from temp1 where zbfm_id is null')
    for row in session.fetchall():
        session.execute("INSERT into dw_zhs_d_zbfm(zbfm_name) VALUES('"+row[0]+"') ON conflict(zbfm_name) DO nothing")
    CONN.commit()
    print 'createZbfm', 'complete!'



if __name__=='__main__':
    createZbfm()