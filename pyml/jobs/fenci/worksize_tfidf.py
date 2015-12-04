#coding:utf8
import os
import sys
import re
import MySQLdb
import time
import numpy as np
import jieba
from jobs import utils
import pdb
from logging import getLevelName
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

def get_letter_dct(position_dct):
    letter_dct = {}
    for position in position_dct.keys():
        letter_dct[position] = [[], []]
    
    return letter_dct

def get_doc_prob(letter_dct, letter):
    count = 0
    for let in letter_dct:
        if letter in let:
            count += 1
    if count == 0:
        count = 1
    return 32 / float(count)
        
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

    positionlst = cur.fetchall()
    i = 0
    letterdct = {}
    letter_dct = get_letter_dct(position_dct)
    
    for j in xrange(70000):
        poslst = positionlst[j:j+3]
        if not position_dct.has_key(poslst[1][0]):
            continue
        seg_lst = jieba.cut(poslst[0][0])
        for term in seg_lst:
            if len(term) > 1:
                letter_dct[poslst[1][0]][0].append(term)
        seg_lst = jieba.cut(poslst[2][0])
        for term in seg_lst:
            if len(term) > 1:
                letter_dct[poslst[1][0]][1].append(term)
    
    tfidf_dct = {}
    keylst = [item[0] for item in letter_dct.items()]
    tletterlst = [item[1][0] for item in letter_dct.items()]
    for j, tletter in enumerate(tletterlst):
        sletter = set(tletter)
        tfidf_dct[keylst[j]] = [[], [], []]
        for letter in sletter:
            if tletter.count(letter) <= 1:
                continue
            tfidf_dct[keylst[j]][0].append(letter)
            tfidf_dct[keylst[j]][1].append(float(tletter.count(letter))/len(tletter))
            tfidf_dct[keylst[j]][2].append(get_doc_prob(tletterlst, letter))
#         pdb.set_trace()
        tfidf_dct[keylst[j]][1] = np.array(tfidf_dct[keylst[j]][1])
        tfidf_dct[keylst[j]][2] = np.array(tfidf_dct[keylst[j]][2])
        tfidf_dct[keylst[j]][2] = np.log(tfidf_dct[keylst[j]][2])
        tfidf_dct[keylst[j]][1] = tfidf_dct[keylst[j]][1] * tfidf_dct[keylst[j]][2]
    
    for key in keylst:
        print '===================',key,'==================='
        for i in range(len(tfidf_dct[key][0])):
            print tfidf_dct[key][0][i],':',tfidf_dct[key][1][i]
    
    utils.store_rst(tfidf_dct, 'tfidf_dct')
         
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)