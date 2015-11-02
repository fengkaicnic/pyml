#what's the fuck
#are you fucking
#encoding:utf-8
import os
import json
import sys

import re
import MySQLdb
import time
import codecs
from jobs import utils
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
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            position_dct[uline] = '1'
    sql = 'select position_name from work_sizetest'
    cur.execute(sql)
    positionlst = cur.fetchall()
    positions = []
    result = []
    for position in positionlst:
        if len(positions) < 2:
            positions.append(position[0])
        else:
            if position_dct.has_key(positions[0]):
                result.append(positions[0])
            elif position_dct.has_key(positions[1]):
                result.append(positions[1])
            else:
                result.append('test')
            positions = [position[0]]
    
    utils.store_rst(result, 'position.txt')
    
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    