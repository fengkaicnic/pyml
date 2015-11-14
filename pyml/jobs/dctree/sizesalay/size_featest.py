#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
reload(sys)
sys.setdefaultencoding('utf8')
import pdb
start = time.clock()
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select jb.age,jb.gender,jb.major \
                                        from jobs_uinfotest as jb left join workexperiencetest as wk on \
                                        jb.userid = wk.userid and wk.num = 1'
    cur.execute(sql)
    file = open('d:/jobs/dctree/size/ss-test.csv', 'w+')
    useridlst = cur.fetchall()
    sqlze = 'select userid, size, salary from work_sizetest'
    cur.execute(sqlze)
    sizelst = cur.fetchall()
    sq = 'select name from major where degreer0 >=0.6'
#     pdb.set_trace()
    cur.execute(sq)
    degreer0lst = cur.fetchall()
    degreer0dct = {}
    for degree in degreer0lst:
        degreer0dct[degree[0]] = 1
    sq1 = 'select name from major where degreer1 >=0.6'
    cur.execute(sq1)
    degreer1lst = cur.fetchall()
    degreer1dct = {}
    for degree in degreer1lst:
        degreer1dct[degree[0]] = 1
    sq2 = 'select name from major where degreer2 >=0.6'
    cur.execute(sq2)
    degreer2lst = cur.fetchall()
    degreer2dct = {}
    for degree in degreer2lst:
        degreer2dct[degree[0]] = 1
    #file.write('age,bstart_year,gender,major,size1,size2,size\n')
#     pdb.set_trace()
    i = 0
    for userid in useridlst:
        sizes = sizelst[i:i+2]
        i += 2
        print userid
        userid = list(userid)
        if int(userid[0]) <= 20:
            userid[0] = '20'
        elif int(userid[0]) >= 60:
            userid[0] = '60'
        if degreer0dct.has_key(userid[2]):
            userid.pop(-1)
            userid.append(0)
        elif degreer1dct.has_key(userid[2]):
            userid.pop(-1)
            userid.append(1)
        elif degreer2dct.has_key(userid[2]):
            userid.pop(-1)
            userid.append(2)
        else:
            userid.pop(-1)
            userid.append(3)
        userid.append(sizes[0][1])
        userid.append(sizes[1][1])
        #userid.append(sizes[0][2])
        #userid.append(sizes[1][2])
        #userid.append(sizes[1][2])
        userid.append(0)
        userlst = map(str, userid)
        strs = ','.join(userlst) + '\n'
        file.write(strs)
        
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print (end - start)