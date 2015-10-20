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
    sql = 'select start_age, bstart_year from jobs_uinfo;'
    sqlt = 'select userid, start_age, bstart_year from jobs_uinfotest'
    cur.execute(sql)

    import pdb
    pdb.set_trace()
    ageyearlst = cur.fetchall()
    cur.execute(sqlt)
    ageyeartestlst = cur.fetchall()
    agelst = []
    agetlst = []
    yearlst = []
    yeartlst = []
    useridlst = []
    for term in ageyearlst:
        agelst.append(term[0])
        yearlst.append(term[1])
    for term in ageyeartestlst:
        useridlst.append(term[0])
        agetlst.append(term[1])
        yeartlst.append(term[2])
    pdb.set_trace()
    agearray = np.array(agelst)
    agetarray = np.array(agetlst)
    yeararray = np.array(yearlst)
    yeartarray = np.array(yeartlst)
    agemean = np.array([np.mean(agearray)]*len(agetlst))
    yearmean = np.array([np.mean(yeararray)]*len(yeartlst))
    agestand = np.array([np.sqrt(np.var(agearray))]*len(agetlst))
    yearstand = np.array([np.sqrt(np.var(yeararray))]*len(yeartlst))
    ageresult = (agetarray-agemean)/agestand
    yearresult = (yeartarray-yearmean)/yearstand
    for i in xrange(len(useridlst)):
        sqls = 'update jobs_uinfotest set agenormal = %f, startyearnormal = %f where userid = "%s"' % (ageresult[i], yearresult[i], useridlst[i])
        cur.execute(sqls)
    
    conn.commit()
    conn.close()
    end = time.clock()
    print (end-start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
    