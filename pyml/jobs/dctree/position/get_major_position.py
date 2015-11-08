#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import codecs
import time
from jobs.utils import read_rst
reload(sys)
sys.setdefaultencoding('utf8')
import pdb
from jobs.utils import store_rst
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

try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    file = open('d:/jobs/dctree/pos-train.csv', 'w+')
    sql = 'select major, industry from workexperience'
    cur.execute(sql)
    shortmarlst = cur.fetchall()
#     sq = 'select shortmar, industry from workexepriencetest'
#     cur.execute(sq)
#     shortmartestlst = cur.fetchall()
    shortmar_dusdct = {}
    for shortmar in shortmarlst:
        if shortmar_dusdct.has_key(shortmar[0]):
            if not shortmar_dusdct[shortmar[0]].has_key(shortmar[1]):
                shortmar_dusdct[shortmar[0]][shortmar[1]] = []
        else:
            shortmar_dusdct[shortmar[0]] = {}
            shortmar_dusdct[shortmar[0]][shortmar[1]] = []
#     for shortmar in shortmartestlst:
#         if shortmar_dusdct.has_key(shortmar[0]):
#             if not shortmar_dusdct[shortmar[0]][shortmar[1]]:
#                 shortmar_dusdct[shortmar[0]][shortmar[1]] = ''
#         else:
#             shortmar_dusdct[shortmar[0]] = {}
#             shortmar_dusdct[shortmar[0]][shortmar[1]] = ''
    pdb.set_trace()
    for keym in shortmar_dusdct.keys():
        for key in shortmar_dusdct[keym].keys():
            sqlkey = 'select position_name, count(position_name) as nu from workexperience\
                                            where major = "%s" and industry = "%s" order by nu desc limit 5' % (keym, key)
            cur.execute(sqlkey)
            poslst = cur.fetchall()
            for pos in poslst:
                shortmar_dusdct[keym][key].append(pos[0])
    
    store_rst(shortmar_dusdct, 'shortmar_dusdct')
    
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print (end - start)