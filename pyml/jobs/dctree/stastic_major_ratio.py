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
    sql = 'select name, degree0, degree1, degree2 from major'
    pdb.set_trace()
    cur.execute(sql)
    useridlst = cur.fetchall()
    ratio_dct = {}
    for userid in useridlst:
        total = userid[1] + userid[2] + userid[3]
        total = float(total)
        ratio_dct[userid[0]] = [userid[1]/total, userid[2]/total, userid[3]/total]
    
    for key in ratio_dct.iterkeys():
        sq = 'update major set degreer0=%f, degreer1=%f, degreer2=%f where name = "%s"' % (ratio_dct[key][0], ratio_dct[key][1], ratio_dct[key][2], key)
        cur.execute(sq)
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)