#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
from logging import getLevelName
reload(sys)
from jobs import utils
from jobs.majorposition import get_position
import codecs
sys.setdefaultencoding('utf8')
import pdb
start = time.clock()

postdct = get_position.get_pos()

def get_position_meta():
    position_dct = {}
    with codecs.open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-2]
            uline = unicode(line)
            position_dct[uline] = '1'
    return position_dct

position_dct = get_position_meta()

def get_letter_position(key, letter, workletterprobdct):
    prob = 0.0
    for let in letter:
        prob += workletterprobdct[key]['pos1'][let]/workprobdct[key]['pos1']['total']
    if prob == 0.0:
        prob = 0.0001
    return prob/len(letter)
    
    
def get_position_prob(key, workprobdct, works):
    pos1prob = get_letter_position(key, works[0][1], workprobdct)
    pos2prob = get_letter_position(key, works[1][1], workprobdct)
    industry1prob = get_letter_position(key, works[0][0], workprobdct)
    industry2prob = get_letter_position(key, works[1][0], workprobdct)
#     if workprobdct[key]['pos1'].has_key(works[0][1]):
#         pos1prob = 1000*float(workprobdct[key]['pos1'][works[0][1]])/workprobdct[key]['pos1']['total']
#     else:
#         pos1prob = 0.0001/workprobdct[key]['pos1']['total']
#     if workprobdct[key]['pos2'].has_key(works[1][1]):
#         pos2prob = 500*float(workprobdct[key]['pos2'][works[1][1]])/workprobdct[key]['pos2']['total']
#     else:
#         pos2prob = 0.0001/workprobdct[key]['pos2']['total']
#     if workprobdct[key]['industry1'].has_key(works[0][0]):
#         industry1prob = float(workprobdct[key]['industry1'][works[0][0]])/workprobdct[key]['industry1']['total']
#     else:
#         industry1prob = 0.0001/workprobdct[key]['industry1']['total']
#     if workprobdct[key]['industry2'].has_key(works[1][0]):
#         industry2prob = float(workprobdct[key]['industry2'][works[1][0]])/workprobdct[key]['industry2']['total']
#     else:
#         industry2prob = 0.0001/workprobdct[key]['industry2']['total']
    
    total = float(workprobdct[key]['total'])/workprobdct['total']
    total = total*(pos1prob + pos2prob + industry1prob + industry2prob)
    
    return total

try:    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    
    sql = 'select industry, position_name from work_sizetest'
    cur.execute(sql)
    workprobdct = utils.read_rst('workletterprobdct')
    worklst = cur.fetchall()
    i = 0
    result = []
    
    for j in xrange(20000):
        tworks = worklst[i:i+2]
        i += 2
        position_prob = {}
        pdb.set_trace()
        for key in position_dct.keys():
#             pdb.set_trace()
            position_prob[key] = get_position_prob(key, workprobdct, tworks)
#         pdb.set_trace()
        sortedprob = sorted(position_prob.iteritems(), key=lambda jj:jj[1], reverse=True)
#         for prob in sortedprob:
#             print prob[0] + str(prob[1])
        result.append(sortedprob[0][0])
        
    utils.store_rst(result, 'positionlet')
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)