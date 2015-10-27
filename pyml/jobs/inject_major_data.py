#coding:gb2312
import os
import json
import sys
import re
import pdb
import MySQLdb
import types
import time
reload(sys)

start = time.clock()
def long2str(nm):
    if type(nm) is types.LongType:
        return str(nm)
    else:
        return nm

try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select distinct(major) from jobs_uinfo'
    cur.execute(sql)
    majorlst = cur.fetchall()
    i = 0
    pdb.set_trace()
    for major in majorlst:
        i += 1
        masql = 'insert into major(name, majorid, type) values ("%s", %d, "%s")' % (major[0], i, 'train')
        cur.execute(masql)
    conn.commit()
    conn.close()
    end = time.clock()
    print (end - start)
except Exception as e:
    conn.close()
    print e
    

    