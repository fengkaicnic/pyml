#coding:gb2312
import os
import json
import sys

import re
import MySQLdb
import time
reload(sys)
start = time.clock()
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    #sql = 'select userid from jobs_uinfotest'
    sql = 'select userid, salary from workexperience where num = 1'
    sqlt = 'select userid, salary from workexperiencetest where num = 1'
    cur.execute(sql)
    salarylst = cur.fetchall()
    cur.execute(sqlt)
    salarytlst = cur.fetchall()
    for sal in salarylst:
        userid = sal[0]
        salary = sal[1]
        sqlsalary = 'update jobs_uinfo set start_salary = %d where userid = "%s"' % (salary, userid)
        cur.execute(sqlsalary)
    for sal in salarytlst:
        userid = sal[0]
        salary = sal[1]
        sqlsalary = 'update jobs_uinfotest set start_salary = %d where userid = "%s"' % (salary, userid)
        cur.execute(sqlsalary)
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    