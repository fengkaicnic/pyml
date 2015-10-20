#coding:gb2312
import os
import json
import sys
import numpy as np
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
    sql = 'select userid, start_age, bstart_year from jobs_uinfo;'
    cur.execute(sql)

    import pdb
    pdb.set_trace()
    ageyearlst = cur.fetchall()
    agelst = []
    yearlst = []
    useridlst = []
    for term in ageyearlst:
        useridlst.append(term[0])
        agelst.append(term[1])
        yearlst.append(term[2])
    agearray = np.array(agelst)
    yeararray = np.array(yearlst)
    agemean = np.array([np.mean(agearray)]*len(agelst))
    yearmean = np.array([np.mean(yeararray)]*len(yearlst))
    agestand = np.array([np.sqrt(np.var(agearray))]*len(agelst))
    yearstand = np.array([np.sqrt(np.var(yeararray))]*len(yearlst))
    ageresult = (agearray-agemean)/agestand
    yearresult = (yeararray-yearmean)/yearstand
    for i in xrange(len(useridlst)):
        sqls = 'update jobs_uinfo set agenormal = %f, startyearnormal = %f where userid = "%s"' % (ageresult[i], yearresult[i], useridlst[i])
        cur.execute(sqls)
    
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    