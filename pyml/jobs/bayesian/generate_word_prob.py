#coding:utf8
import os
import sys
import re
import MySQLdb
import time
import jieba
import pdb
from jobs import utils
reload(sys)
import codecs
sys.setdefaultencoding('utf8')
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

def read_tree(filename):
    '''
    '''
    import pickle
    reader = open(filename,'rU')
    return pickle.load(reader)
try:
    pdb.set_trace()
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select position_name from work_size'
    cur.execute(sql)
    position_dct = get_position_meta()
#     file = open('d:/jobs/dctree/majortest.csv', 'w+')
    positionlst = cur.fetchall()
    i = 0

    letterdct = {}
    
    position_word_dct = {'total':0}
    for key in position_dct.keys():
        position_word_dct[key] = {'pos1':{'total':0}, 'pos2':{'total':0}, 'total':0}
    
    pdb.set_trace()
    for j in xrange(70000):
        poslst = positionlst[j:j+3]
        j += 3
        if not position_dct.has_key(poslst[1][0]):
            continue
        seg_lst = jieba.cut(poslst[0][0])
        for term in seg_lst:
            if position_word_dct[poslst[1][0]]['pos1'].has_key(term):
                position_word_dct[poslst[1][0]]['pos1'][term] += 1
            else:
                position_word_dct[poslst[1][0]]['pos1'][term] = 1
            position_word_dct[poslst[1][0]]['pos1']['total'] += 1
        seg_lst = jieba.cut(poslst[2][0])
        for term in seg_lst:
            if position_word_dct[poslst[1][0]]['pos2'].has_key(term):
                position_word_dct[poslst[1][0]]['pos2'][term] += 1
            else:
                position_word_dct[poslst[1][0]]['pos2'][term] = 1
            position_word_dct[poslst[1][0]]['pos2']['total'] += 1
        position_word_dct[poslst[1][0]]['total'] += 1
        position_word_dct['total'] += 1
    
    utils.store_rst(position_word_dct, 'position_word')
                
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)