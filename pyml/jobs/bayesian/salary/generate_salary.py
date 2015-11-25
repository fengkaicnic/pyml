#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
reload(sys)
from jobs import utils
from jobs.majorposition import get_position
import codecs
sys.setdefaultencoding('utf8')
import pdb
start = time.clock()

# postdct = get_position.get_pos()

def get_position_meta():
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            position_dct[uline] = '1'
    return position_dct

# position_dct = get_position_meta()

def get_salary_prob(key, salaryprobdct, salarys):
#     salarys = convert_pos(position_dct, salarys)
    if salaryprobdct[key]['salary1'].has_key(salarys[0][1]):
        salary1prob = 1*float(salaryprobdct[key]['salary1'][salarys[0][1]])/salaryprobdct[key]['salary1']['total']
    else:
        salary1prob = 0.0001/salaryprobdct[key]['salary1']['total']
    if salaryprobdct[key]['salary2'].has_key(salarys[1][1]):
        salary2prob = 1*float(salaryprobdct[key]['salary2'][salarys[1][1]])/salaryprobdct[key]['salary2']['total']
    else:
        salary2prob = 0.0001/salaryprobdct[key]['salary2']['total']
    if salaryprobdct[key]['industry1'].has_key(salarys[0][0]):
        industry1prob = float(salaryprobdct[key]['industry1'][salarys[0][0]])/salaryprobdct[key]['industry1']['total']
    else:
        industry1prob = 0.0001/salaryprobdct[key]['industry1']['total']
    if salaryprobdct[key]['industry2'].has_key(salarys[1][0]):
        industry2prob = float(salaryprobdct[key]['industry2'][salarys[1][0]])/salaryprobdct[key]['industry2']['total']
    else:
        industry2prob = 0.0001/salaryprobdct[key]['industry2']['total']
    
    total = float(salaryprobdct[key]['total'])/salaryprobdct['total']
#     total = total*(salary1prob + salary2prob + industry1prob + industry2prob)
    total = total*salary1prob*salary2prob
#     pdb.set_trace()
    return total

try:    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    
    sql = 'select industry, salary from work_sizetest'
    cur.execute(sql)
    salaryprobdct = utils.read_rst('salaryprobdct')
    worklst = cur.fetchall()
    i = 0
    result = []
    
    for j in xrange(20000):
        salarys = worklst[i:i+2]
        i += 2
        salary_prob = {}
        for key in range(7):
#             pdb.set_trace()
            salary_prob[key] = get_salary_prob(key, salaryprobdct, salarys)
#         pdb.set_trace()
        sortedprob = sorted(salary_prob.iteritems(), key=lambda jj:jj[1], reverse=True)
#         for prob in sortedprob:
#             print prob[0] + str(prob[1])
        result.append(sortedprob[0][0])
        
    utils.store_rst(result, 'salary')
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)