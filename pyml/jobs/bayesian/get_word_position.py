#coding:utf8
import sys
import MySQLdb
import time
reload(sys)
from jobs import utils
from jobs.majorposition import get_position
import codecs
import jieba
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

def get_letter_position(key, pos, letter, wordprobdct):
    prob = 1.0
    for let in letter:
        prob *= float(wordprobdct[key][pos].get(let, 1))/wordprobdct[key][pos]['total']
    return prob
    
    
def get_position_prob(key, wordprobdct, works):
    seg_lst = jieba.cut(works[0][0])
    pos1prob = get_letter_position(key, 'pos1', seg_lst, wordprobdct)
    seglst = jieba.cut(works[1][0])
    pos2prob = get_letter_position(key, 'pos2', seglst, wordprobdct)
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
    
    total = float(wordprobdct[key]['total'])/wordprobdct['total']
    total = total*(pos1prob + pos2prob)
    
    return total

try:    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    
    sql = 'select position_name from work_sizetest'
    cur.execute(sql)
    wordprobdct = utils.read_rst('position_word')
    wordlst = cur.fetchall()
    i = 0
    result = []
#     pdb.set_trace()
    for j in xrange(20000):
        tworks = wordlst[i:i+2]
        i += 2
        position_prob = {}
        for key in position_dct.keys():
            position_prob[key] = get_position_prob(key, wordprobdct, tworks)
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