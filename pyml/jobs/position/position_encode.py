#encoding:utf8

import os
import json
import sys
import re
import MySQLdb
import time
import pdb
import codecs
from jobs import utils
from jobs.majorposition import get_position
from jobs.utils import get_industry_position

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
    
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            lintlst = uline.split(',')
            position_dct[lintlst[0]] = lintlst[1]
    
    file = open('d:/jobs/xgboost/data.csv', 'w+')
    pdb.set_trace()
    keyshare = utils.read_rst('keyshare')
    sql = 'select position_name, industry from work_size'
    cur.execute(sql)
    datalst = []
    positionlst = cur.fetchall()
    i = 0
    for j in xrange(70000):
        worklst = positionlst[i:i+3]
       
        i += 1
        if not position_dct.has_key(worklst[1][0]):
            continue
        else:
            rst = []
            if keyshare.has_key(worklst[0][0]):
                rst.append(keyshare[worklst[0][0]])
            else:
                rst.append(keyshare[worklst[0][1]])
            if keyshare.has_key(worklst[2][0]):
                rst.append(keyshare[worklst[2][0]])
            else:
                rst.append(keyshare[worklst[2][1]])
            if worklst[0][1] != worklst[2][1]:
                rst.append(0)
            else:
                rst.append(1)
            rst.append(str(keyshare[worklst[1][0]]) + '\n')
            datalst.append(rst)
    pdb.set_trace()
    for data in datalst:
        file.write(','.join(map(str, data)))
        
    end = time.clock()
    file.close()
#     print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    