#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
reload(sys)
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select userid from jobs_uinfotest'
    cur.execute(sql)
    file = open('d:/jobs/result.csv', 'w+')
    useridlst = cur.fetchall()
    file.write('id,degree,size,salary,position_name\n')
    for userid in useridlst:
        print userid[0] 
        strs = userid[0] + u',1,3,2,销售专员\n'
        file.write(strs.encode('utf-8'))
        
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
    