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
    majorsql = 'select count(*) as cu , major from jobs_uinfo group by major having cu >= 10'
    positionsql = 'select count(*) as cu , position_name from workexperience group by position_name having cu >= 10'
    cur.execute(majorsql)
    majorlst = cur.fetchall()
    cur.execute(positionsql)
    positionlst = cur.fetchall()
    for major in majorlst:
        sql = 'insert into metadata(name, type, num) values("%s", "%s", %d)' % (major[1], 'major', major[0])
        cur.execute(sql)
    for position in positionlst:
        sql = 'insert into metadata(name, type, num) values("%s", "%s", %d)' % (position[1], 'position', position[0])
        cur.execute(sql)
    
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    