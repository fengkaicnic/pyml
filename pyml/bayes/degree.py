#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
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
    sql = 'select major, count(major) from jobs_uinfo where degree = 0 group by major'
    cur.execute(sql)
    file = open('d:/jobs/dctree/dct-test.csv', 'w+')
    useridlst = cur.fetchall()
    file.write('degree,age,start_age,bstart_year,gender,start_salary,start_size\n')
    for userid in useridlst:
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