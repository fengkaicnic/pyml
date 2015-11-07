#coding:utf8
import os

import json
import sys

import re
import MySQLdb
import time
from jobs.utils import store_rst
reload(sys)
sys.setdefaultencoding('utf8')
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
    majorsql = 'select distinct(shortmar) from jobs_uinfo'
    sqlts = 'select distinct(shortmar) from jobs_uinfotest'
    cur.execute(majorsql)
    majorlst = cur.fetchall()
    cur.execute(sqlts)
    sharedct = {}
    shortmar = cur.fetchall()
    majordct = {}
    for major in majorlst:
        majordct[major[0]] = 1
    for major in shortmar:
        if majordct.has_key(major[0]):
            sharedct[major[0]] = 1
            print major[0]
        
    print len(sharedct)
    store_rst(sharedct, 'sharemajor')
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    