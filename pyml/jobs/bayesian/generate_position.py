#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
reload(sys)
from jobs import utils
import codecs
sys.setdefaultencoding('utf8')
import pdb
start = time.clock()

def get_position_meta():
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            position_dct[uline] = '1'
    return position_dct

try:    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    position_dct = get_position_meta()
    sql = 'select industry, position_name from work_sizetest'
    cur.execute(sql)
    workprobdct = utils.read_rst('workprobdct')
    worklst = cur.fetchall()
    i = 0
    for j in xrange(20000):
        tworks = worklst[i:i+2]
        
        
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)