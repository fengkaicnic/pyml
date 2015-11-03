#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
import random
from jobs import utils
import pdb
pdb.set_trace()
reload(sys)
sys.setdefaultencoding('utf8')
start = time.clock()
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select name, degreer0, degreer1, degreer2 from major ;'
    cur.execute(sql)
    majorlst = cur.fetchall()
    majordct = {}
    pdb.set_trace()
    treelst = utils.read_rst('result.txt')
    resultlst = []
    for major in majorlst:
        majordct[major[0]] = [major[1], major[2], major[3]]
    sq = 'select userid, major from jobs_uinfotest'    
    cur.execute(sq)
    usertst = cur.fetchall()
    i = 0
    for user in usertst:
        if majordct.has_key(user[1]):
            majorat = majordct[user[1]]
            mnu = max(majorat)
            index = majorat.index(mnu)
            resultlst.append(index)
        else:
            resultlst.append(0)
        i = i + 1
#     for user in usertst:
#         if majordct.has_key(user[1]):
#             majorat = majordct[user[1]]
#             mnu = max(majorat)
#             if mnu >= 0.8:
#                 index = majorat.index(mnu)
#                 resultlst.append(index)
#             else:
#                 resultlst.append(treelst[i])
#         else:
#             resultlst.append(treelst[i])
#         i = i + 1
    utils.store_rst(resultlst, 'degree.txt')
    conn.commit()
    conn.close()
except Exception as e:
    conn.close()
    print e
end = time.clock()
print (end - start)