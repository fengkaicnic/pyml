#coding:gb2312
import os
import json
import sys
import re
import pdb
import MySQLdb
import types
import time
reload(sys)

start = time.clock()
def long2str(nm):
    if type(nm) is types.LongType:
        return str(nm)
    else:
        return nm

try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select userid,age,gender,major,start_age,start_salary,bstart_year,degree from jobs_uinfo limit 1100;'
    cur.execute(sql)
    file = open('d:/jobs/bm1100.csv', 'w+')
    useridlst = cur.fetchall()
    file.write('userid,age,gender,major,start_age,start_salary,bstart_year,degree\n')
    for userid in useridlst:
        print userid
        userid = map(long2str, userid)
        strs = ','.join(userid)
        strs += '\n'
        file.write(strs.encode('utf-8'))
        
    conn.commit()
    conn.close()
    file.close()
    end = time.clock()
    print (end - start)
except Exception as e:
    file.close()
    conn.close()
    print e
    

    