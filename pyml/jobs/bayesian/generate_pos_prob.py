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
import copy
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
    sqlze = 'select  industry, position_name from work_size'
    cur.execute(sqlze)
    worklst = cur.fetchall()
    i = 0
    workprobdct = {}
    pos1key = {}
    pos2key = {}
    industry1key = {}
    industry2key = {}
    
    for j in xrange(70000):
        works = worklst[i:i+3]
        i += 3
        if not position_dct.has_key(works[1][1]):
            continue
        if not industry1key.has_key(works[0][0]):
            industry1key[works[0][0]] = 1
        if not industry2key.has_key(works[2][0]):
            industry2key[works[2][0]] = 1
        if not pos1key.has_key(works[0][1]):
            pos1key[works[0][1]] = 1
        if not pos2key.has_key(works[2][1]):
            pos2key[works[2][1]] = 1
#     pdb.set_trace()
    for key in position_dct.keys():
#         workprobdct[key] = {'total':0, 'pos1':copy.deepcopy(pos1key), 'pos2':copy.deepcopy(pos2key), 'industry1':copy.deepcopy(industry1key), 'industry2':copy.deepcopy(industry2key)}
        workprobdct[key] = {'total':0, 'pos1':{}, 'pos2':{}, 'industry1':{}, 'industry2':{}}
    i = 0
    t = 0
#     pdb.set_trace()
    for j in xrange(70000):
#         print j
        works = worklst[i:i+3]
        if not position_dct.has_key(works[1][1]):
            i += 3
            continue
        i += 3
        t += 1
        print t
        if workprobdct[works[1][1]]['pos1'].has_key(works[0][1]):
            workprobdct[works[1][1]]['pos1'][works[0][1]] += 1
        else:
            workprobdct[works[1][1]]['pos1'][works[0][1]] = 1
        if workprobdct[works[1][1]]['pos2'].has_key(works[2][1]): 
            workprobdct[works[1][1]]['pos2'][works[2][1]] += 1
        else:
            workprobdct[works[1][1]]['pos2'][works[2][1]] = 1
        if workprobdct[works[1][1]]['industry1'].has_key(works[0][0]):
            workprobdct[works[1][1]]['industry1'][works[0][0]] += 1
        else:
            workprobdct[works[1][1]]['industry1'][works[0][0]] = 1
        if workprobdct[works[1][1]]['industry2'].has_key(works[2][0]):
            workprobdct[works[1][1]]['industry2'][works[2][0]] += 1
        else:
            workprobdct[works[1][1]]['industry2'][works[2][0]] = 1
        workprobdct[works[1][1]]['total'] += 1
    workprobdct['total'] = t
    for key in position_dct.keys():
        workprobdct[key]['pos1']['total'] = reduce(lambda x,y:x+y, workprobdct[key]['pos1'].itervalues())
        workprobdct[key]['pos2']['total'] = reduce(lambda x,y:x+y, workprobdct[key]['pos2'].itervalues())
        workprobdct[key]['industry1']['total'] = reduce(lambda x,y:x+y, workprobdct[key]['industry1'].itervalues())
        workprobdct[key]['industry2']['total'] = reduce(lambda x,y:x+y, workprobdct[key]['industry2'].itervalues())
#     pdb.set_trace()
    for key in workprobdct.keys():
        if key == 'total':
            continue
        print key +str(workprobdct[key]['pos1']['total'])
    
    utils.store_rst(workprobdct, 'workprobdct')
        
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)