#coding:utf8
import os

import json
import sys

import re
import MySQLdb
import time
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
    majorsql = 'select distinct(major) from jobs_uinfotest '
    cur.execute(majorsql)
    majorlst = cur.fetchall()
    majordct = {}
    for major in majorlst:
        name = major[0]
        name = name.strip()
        sq = 'update jobs_uinfotest set shortmar = "%s" where major = "%s"' % (name[:4], major[0])
        cur.execute(sq)
        if not majordct.has_key(name[:4]):
            majordct[name[:4]] = 1
        else:
            majordct[name[:4]] += 1
   
        
    print len(majordct)
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    