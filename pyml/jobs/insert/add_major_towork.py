#coding:utf8
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
    majorsql = 'select userid, major from jobs_uinfo '
    cur.execute(majorsql)
    majorlst = cur.fetchall()
    for major in majorlst:
        sql = 'update workexperience set major = "%s" where userid = "%s"' % (major[1], major[0])
        cur.execute(sql)
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    