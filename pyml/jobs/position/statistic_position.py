#encoding:utf8

import os
import json
import sys
import re
import MySQLdb
import time
import copy
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
    keynm = 130
    position_dct = {}
    pdb.set_trace()
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            lintlst = uline.split(',')
            position_dct[lintlst[0]] = lintlst[1]
    sql = 'select position_name, industry from work_size'
    cur.execute(sql)
    positionlst = cur.fetchall()
    positions = []
    positiondct = {}
    industrydct = {}
    industrys = []
    result = []
#     pdb.set_trace()
    flag = False
    i = 0
    
    for j in xrange(70000):
        worklst = positionlst[i:i+3]
        i += 3
        if not position_dct.has_key(worklst[1][0]):
            continue

        else:
            if positiondct.has_key(worklst[0][0]):
                positiondct[worklst[0][0]] += 1
            else:
                positiondct[worklst[0][0]] = 1
            if positiondct.has_key(worklst[2][0]):
                positiondct[worklst[2][0]] += 1
            else:
                positiondct[worklst[2][0]] = 1
            if not industrydct.has_key(worklst[0][1]):
                industrydct[worklst[0][1]] = 1
            if not industrydct.has_key(worklst[2][1]):
                industrydct[worklst[2][1]] = 1
    
    sq = 'select position_name from work_sizetest'
    cur.execute(sq)
    positiontst = cur.fetchall()
    share = 0
    nos = 0
    i = 0
    tst_dict = {}
    for j in xrange(20000):
        worklst = positiontst[i:i+2]
        i += 2
        if positiondct.has_key(worklst[0][0]):
            share += 1
        else:
            nos += 1
        if positiondct.has_key(worklst[1][0]):
            share += 1
        else:
            nos += 1
        if tst_dict.has_key(worklst[0][0]):
            tst_dict[worklst[0][0]] += 1
        else:
            tst_dict[worklst[0][0]] = 1
        if tst_dict.has_key(worklst[1][0]):
            tst_dict[worklst[1][0]] += 1
        else:
            tst_dict[worklst[1][0]] = 1
            
    keyshare = 0
    keynos = 0
    keysharedct = copy.deepcopy(position_dct)
    for key in tst_dict.keys():
        if positiondct.has_key(key):
            keyshare += 1
            if not position_dct.has_key(key):
                keysharedct[key] = keynm
                keynm += 1
        else:
            keynos += 1
            print key
    for industry in industrydct.keys():
        keysharedct[industry] = keynm
        keynm += 1
    utils.store_rst(keysharedct, 'keyshare')
    
    print 'poslenght : %d' % len(positiondct)
    print 'tstlenght : %d' % len(tst_dict)
    print 'share : %d' % share
    print 'nos : %d' % nos
    print 'keyshare : %d' % keyshare
    print 'keynos : %d' % keynos
    conn.commit()
    conn.close()
    end = time.clock()
#     print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    