#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import codecs
import time
from jobs.utils import read_rst
from jobs.utils import get_key_positionsingle
reload(sys)
from jobs.majorposition import get_position
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

def get_share_mar():
    major_dct = {}
    with codecs.open('sharemajor') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            major_dct[uline] = '1'
    return major_dct

postpropertydct = get_position.get_pos()

try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    file = open('d:/jobs/dctree/position/train.csv', 'w+')
    sql = 'select userid, age, bstart_year, gender, shortmar from jobs_uinfo'
    cur.execute(sql)
    userdlst = cur.fetchall()
    sqlze = 'select wk.salary, wk.industry, wk.position_name from work_size as wk'
    position_dct = get_position_meta()
    major_dct = read_rst('sharemajor')
    cur.execute(sqlze)
    sizelst = cur.fetchall()
    i = 0
    for userd in userdlst:
        sizes = sizelst[i:i+3]
        i += 3
        if not position_dct.has_key(sizes[1][2]):
            continue
#         print userd
        userid = []
        userd = list(userd)
        if int(userd[1]) <= 20:
            userd[1] = '18'
        elif int(userd[1]) >= 60:
            userd[1] = '60'
        userid.append(userd[1])
        userid.append(userd[2])
        userid.append(userd[3])
#         if major_dct.has_key(userd[1]):
#             userid.append(userd[1])
#         else:
#             userid.append('None')
        
        #userid.append(sizes[0][1])
        #userid.append(sizes[2][1])
        #userid.append(sizes[0][0])
        #userid.append(sizes[2][0])
        userid.append(sizes[0][1])
        userid.append(sizes[2][1])
        userid.append(get_key_positionsingle(postpropertydct, position_dct, sizes[0][2]))
        userid.append(get_key_positionsingle(postpropertydct, position_dct, sizes[2][2]))
        userid.append(sizes[1][2])
        userlst = map(str, userid)
        strs = ','.join(userlst) + '\n'
        file.write(strs)
        
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print (end - start)