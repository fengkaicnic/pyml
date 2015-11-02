#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
import random
from jobs import utils
import pdb
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
    sql = 'select userid, size, salary from work_sizetest ;'
    cur.execute(sql)
    worksizelst = cur.fetchall()
    userid = ''
    worklst = []
    salarylst = []
    resultst = []
    pdb.set_trace()
    for work_size in worksizelst:
        if len(worklst) < 2:
            worklst.append(work_size[1])
            salarylst.append(work_size[2])
        else:
            worklst = sorted(worklst)
            salarylst = sorted(salarylst)
            resultst.append([random.randint(worklst[0], worklst[1]), random.randint(salarylst[0], salarylst[1])])
            worklst = [work_size[1]]
            salarylst = [work_size[2]]
    worklst = sorted(worklst)
    salarylst = sorted(salarylst)
    resultst.append([random.randint(worklst[0], worklst[1]), random.randint(salarylst[0], salarylst[1])])
    pdb.set_trace()
    utils.store_rst(resultst, 'wsresult.txt')
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)