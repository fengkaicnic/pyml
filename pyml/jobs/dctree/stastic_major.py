#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import pdb
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
    sql = 'select major, degree, start_salary from jobs_uinfo'
    pdb.set_trace()
    cur.execute(sql)
    useridlst = cur.fetchall()
    major_dct = {}
    for userid in useridlst:
        if major_dct.has_key(userid[0]):
            major_dct[userid[0]][userid[1]] += 1
        else:
            major_dct[userid[0]] = [0, 0, 0]
            major_dct[userid[0]][userid[1]] += 1
    
    for key in major_dct.iterkeys():
        sq = 'update major set degree0=%d, degree1=%d, degree2=%d where name = "%s"' % (major_dct[key][0], major_dct[key][1], major_dct[key][2], key)
        cur.execute(sq)
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)