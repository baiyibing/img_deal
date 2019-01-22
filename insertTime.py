#!/usr/bin/env python
# encoding: utf-8
'''
@author: lurenjia
@contact: 1499418300@qq.com
@file: insertTime.py
@time: 2018/7/12 15:05
@desc:
'''
import calendar
import datetime
from time import time,localtime,asctime,strftime
from util import CONN,DBSession,getFirstChars
session = DBSession
type_y = '39'
type_hy = '40'
type_q = '41'
type_m = '42'
formatStr = '%Y-%m-%d %H:%M:%S'

def yearDays(year):
    year = int(year)
    return (datetime.datetime(year+1,1,1) - datetime.datetime(year,1,1)).days

def halfYearDays(year, part):
    year = int(year)
    if part==1:
        return (datetime.datetime(year,6*part+1,1) - datetime.datetime(year,6*part-5,1)).days
    else:
        return (datetime.datetime(year+1,1,1) - datetime.datetime(year,6*part-5,1)).days

def quarterDays(year, part):
    year = int(year)
    if part==4:
        return (datetime.datetime(year+1,1,1) - datetime.datetime(year,3*part-2,1)).days
    else:
        return (datetime.datetime(year,3*part+1,1) - datetime.datetime(year,3*part-2,1)).days

def monthDays(year, part):
    year = int(year)
    if part==12:
        return (datetime.datetime(year+1,1,1) - datetime.datetime(year,part,1)).days
    else:
        return (datetime.datetime(year,part+1,1) - datetime.datetime(year,part,1)).days

def getToTime(timeStr):
    return "to_timestamp('"+timeStr+"', 'YYYY-MM-DD HH24:MI:SS')"

def createYear(year):
    begin = datetime.datetime.strptime(year+'-01-01 00:00:00',formatStr)
    end = begin+datetime.timedelta(days=yearDays(year))
    end -= datetime.timedelta(seconds=1)

    session.execute("select time_id from dw_time where time_code='"+str(int(year)-1)+"'")
    pre_id = session.fetchone()[0]

    time_code = year
    time_name = '%s年' %year
    time_type_id = type_y
    time_timetype = getToTime(begin.strftime(formatStr))
    begin_time = time_timetype
    end_time = getToTime(end.strftime(formatStr))
    duration = yearDays(year)
    order_in_year = '1'
    parent_term_id = '0'
    previous_term_id = pre_id
    lastyear_term_id = pre_id
    sql = '''insert into dw_time(time_code,time_name,time_type_id,time_timetype,begin_time,end_time,duration,order_in_year,parent_term_id,previous_term_id,lastyear_term_id) 
    values('%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s') ON conflict(time_name) DO nothing''' %(time_code,time_name,time_type_id,time_timetype,begin_time,end_time,duration,order_in_year,parent_term_id,previous_term_id,lastyear_term_id)
    session.execute(sql)
    CONN.commit()

def createHalfYear(year):
    createYear(year)
    for i in range(1,3):
        begin = datetime.datetime.strptime(year+'-'+str(6*i-5)+'-01 00:00:00',formatStr)
        end = begin+datetime.timedelta(days=halfYearDays(year,i))
        end -= datetime.timedelta(seconds=1)

        session.execute("select time_id from dw_time where time_code='"+year+"'")
        parent = session.fetchone()[0]
        session.execute("select time_id from dw_time where time_code='"+str(int(year)-1)+str(i)+"' and time_type_id='"+type_hy+"'")
        lastYear = session.fetchone()[0]
        pre_id = '-1'
        if i>1:
            session.execute("select time_id from dw_time where time_code='"+year+str(i-1)+"' and time_type_id='"+type_hy+"'")
            pre_id = session.fetchone()[0]

        time_code = year+str(i)
        time_name = '%s年上半年' %year if i==1 else '%s年下半年' %year
        time_type_id = type_hy
        time_timetype = getToTime(begin.strftime(formatStr))
        begin_time = time_timetype
        end_time = getToTime(end.strftime(formatStr))
        duration = halfYearDays(year,i)
        order_in_year = str(i)
        parent_term_id = parent
        previous_term_id = '0' if i==1 else pre_id
        lastyear_term_id = lastYear
        sql = '''insert into dw_time(time_code,time_name,time_type_id,time_timetype,begin_time,end_time,duration,order_in_year,parent_term_id,previous_term_id,lastyear_term_id) 
        values('%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s') ON conflict(time_name) DO nothing''' %(time_code,time_name,time_type_id,time_timetype,begin_time,end_time,duration,order_in_year,parent_term_id,previous_term_id,lastyear_term_id)
        session.execute(sql)
    CONN.commit()


def createQuarter(year):
    createHalfYear(year)
    for i in range(1,5):
        begin = datetime.datetime.strptime(year+'-'+str(3*i-2)+'-01 00:00:00',formatStr)
        end = begin+datetime.timedelta(days=quarterDays(year,i))
        end -= datetime.timedelta(seconds=1)

        session.execute("select time_id from dw_time where begin_time<="+getToTime(begin.strftime(formatStr))+" and end_time>="+getToTime(begin.strftime(formatStr))+" and time_type_id='"+type_hy+"'")
        parent = session.fetchone()[0]
        session.execute("select time_id from dw_time where time_code='"+str(int(year)-1)+str(i)+"' and time_type_id='"+type_q+"'")
        lastYear = session.fetchone()[0]
        pre_id = '-1'
        if i>1:
            session.execute("select time_id from dw_time where time_code='"+year+str(i-1)+"' and time_type_id='"+type_q+"'")
            pre_id = session.fetchone()[0]

        time_code = year+str(i)
        time_name = '%s年%s季度' %(year,str(i))
        time_type_id = type_q
        time_timetype = getToTime(begin.strftime(formatStr))
        begin_time = time_timetype
        end_time = getToTime(end.strftime(formatStr))
        duration = quarterDays(year,i)
        order_in_year = str(i)
        parent_term_id = parent
        previous_term_id = '0' if i==1 else pre_id
        lastyear_term_id = lastYear
        sql = '''insert into dw_time(time_code,time_name,time_type_id,time_timetype,begin_time,end_time,duration,order_in_year,parent_term_id,previous_term_id,lastyear_term_id) 
        values('%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s') ON conflict(time_name) DO nothing''' % (time_code, time_name, time_type_id, time_timetype, begin_time, end_time, duration, order_in_year,parent_term_id, previous_term_id, lastyear_term_id)
        session.execute(sql)
    CONN.commit()


def createMonth(year):
    createQuarter(year)
    for i in range(1,13):
        begin = datetime.datetime.strptime(year+'-%02d' %i+'-01 00:00:00',formatStr)
        end = begin+datetime.timedelta(days=monthDays(year,i))
        end -= datetime.timedelta(seconds=1)

        session.execute("select time_id from dw_time where begin_time<="+getToTime(begin.strftime(formatStr))+" and end_time>="+getToTime(begin.strftime(formatStr))+" and time_type_id='"+type_q+"'")
        parent = session.fetchone()[0]
        session.execute("select time_id from dw_time where time_code='"+str(int(year)-1)+'%02d'%i+"' and time_type_id='"+type_m+"'")
        lastYear = session.fetchone()[0]
        pre_id = '-1'
        if i>1:
            session.execute("select time_id from dw_time where time_code='"+year+'%02d'%(i-1)+"' and time_type_id='"+type_m+"'")
            pre_id = session.fetchone()[0]

        time_code = year+'%02d'%i
        time_name = '%s年%02d月' %(year,i)
        time_type_id = type_m
        time_timetype = getToTime(begin.strftime(formatStr))
        begin_time = time_timetype
        end_time = getToTime(end.strftime(formatStr))
        duration = monthDays(year,i)
        order_in_year = str(i)
        parent_term_id = parent
        previous_term_id = '0' if i==1 else pre_id
        lastyear_term_id = lastYear
        sql = '''insert into dw_time(time_code,time_name,time_type_id,time_timetype,begin_time,end_time,duration,order_in_year,parent_term_id,previous_term_id,lastyear_term_id) 
        values('%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s') ON conflict(time_name) DO nothing''' % (time_code, time_name, time_type_id, time_timetype, begin_time, end_time, duration, order_in_year,parent_term_id, previous_term_id, lastyear_term_id)
        session.execute(sql)
    CONN.commit()


if __name__ == '__main__':
    for i in range(2018, 2038):
        print i
        createMonth(str(i))
