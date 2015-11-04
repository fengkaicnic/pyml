#coding:utf8
import os
import json
import sys

import re
import MySQLdb
import time
reload(sys)
start = time.clock()
sys.setdefaultencoding('utf8')
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    #sql = 'select userid from jobs_uinfotest'
    sql = 'select ju.major, wk.position_name from jobs_uinfo as ju left join workexperience as wk on ju.userid = wk.userid'
    cur.execute(sql)
    majorlst = cur.fetchall()
    majordct = {}
    for mj in majorlst:
        if majordct.has_key(mj[0]):
            if majordct[mj[0]].has_key(mj[1]):
                majordct[mj[0]][mj[1]] += 1
            else:
                majordct[mj[0]][mj[1]] = 1
        else:
            majordct[mj[0]] = {}
            majordct[mj[0]][mj[1]] = 1
    
    for key in majordct.keys():
        mdcts = majordct[key]
        for k1 in mdcts.keys():
            sq = 'insert into majorposition(major, position, nu) values ("%s", "%s", %d)' % (key, k1, mdcts[k1])
            cur.execute(sq)
    
    conn.commit()
    conn.close()
except Exception as e:
    conn.commit()
    conn.close()
    print e
end = time.clock()
print (end-start)