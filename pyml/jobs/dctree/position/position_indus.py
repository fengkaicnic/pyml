#encoding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
import codecs
from jobs import utils
from jobs.majorposition import get_position
reload(sys)
start = time.clock()
sys.setdefaultencoding('utf8')
postdct = get_position.get_pos()
        
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
    
    sql = 'select count(industry), industry from work_size group by industry'
    cur.execute(sql)
    positionlst = cur.fetchall()
    for industry in positionlst: 
        position_dct[industry[1]] = []
        sq = 'select count(position_name) as nu, position_name from work_size where industry = "%s" group by position_name order by nu desc limit 1' % industry[1]
        cur.execute(sq)
        indusp = cur.fetchall()
        position_dct[industry[1]].append(indusp[0][1])
        position_dct[industry[1]].append(float(indusp[0][0])/industry[0])
    utils.store_rst(position_dct, 'industryr.txt')
    print position_dct
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    