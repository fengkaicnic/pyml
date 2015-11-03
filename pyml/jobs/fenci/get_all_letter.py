#coding:gb2312
import os
import sys
import re
import MySQLdb
import time
import jieba
import pdb
reload(sys)
sys.setdefaultencoding('utf8')
start = time.clock()

def read_tree(filename):
    '''
    从文件中读取决策树，返回决策树
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
    sql = 'select distinct(major) from jobs_uinfotest'
    cur.execute(sql)
    
    file = open('d:/jobs/dctree/majortest.csv', 'w+')
    positionlst = cur.fetchall()
    i = 0
    pdb.set_trace()
    letterdct = {}
    for position in positionlst:
        seg_lst = jieba.cut(position[0])
        for term in seg_lst:
            if not letterdct.has_key(term):
                letterdct[term] = 1
            else:
                letterdct[term] += 1
    positions = letterdct.keys()
    positions_num = []
    for letter in positions:
        positions_num.append(letter + ':' + str(letterdct[letter]))
    strss = '\n'.join(positions_num)
    file.write(strss)
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print (end - start)