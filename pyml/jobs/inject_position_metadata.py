#what's the fuck
#coding:gb2312
import os
import json
import sys

import re
import MySQLdb
import time
import codecs
reload(sys)
start = time.clock()
sys.setdefaultencoding('utf8')
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    #sql = 'select userid from jobs_uinfotest'
    import pdb
    pdb.set_trace()
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            sql = 'insert into metadata(name, type) values ("%s", "%s")' % (uline, 'potision_meta')
            cur.execute(sql)
    
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    