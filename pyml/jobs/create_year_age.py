#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
reload(sys)
start = time.clock()
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    #sql = 'select userid from jobs_uinfotest'
    agesql = 'select jb.userid, jb.age, wk.start_date from jobs_uinfo as jb left join workexperience as wk on jb.userid = wk.userid'
    cur.execute(agesql)
    nowuser = None
    age = 0
    start_date = None
    import pdb
    pdb.set_trace()
    userdlst = cur.fetchall()
    for userd in userdlst:
        if nowuser is None:
            nowuser = userd[0]
            age = userd[1]
            start_date = userd[2]
        if nowuser != userd[0]:
            start_year = start_date.split('-')
            bstart_year = int(start_year[0]) - 1968
            start_age = age + int(start_year[0]) - 2015
            asqll = 'update jobs_uinfo set start_age = %d , bstart_year = %d' % (start_age, bstart_year)
            cur.execute(asqll)
            nowuser = userd[0]
            age = userd[1]
            start_date = userd[2]
        #print userd[0] 
        
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.close()
    print e
    