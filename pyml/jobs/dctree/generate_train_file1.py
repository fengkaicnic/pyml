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
    sql = 'select jb.degree,jb.age,jb.start_age,jb.bstart_year,jb.gender,jb.start_salary,wk.size \
                                        from jobs_uinfo as jb left join workexperience as wk on \
                                        jb.userid = wk.userid and wk.num = 1'
    cur.execute(sql)
    file = open('d:/jobs/dctree/dct-train.csv', 'w+')
    useridlst = cur.fetchall()
    file.write('degree,age,start_age,bstart_year,gender,start_salary,start_size\n')
    pdb.set_trace()
    for userid in useridlst:
        print userid
        userid = list(userid)
        if int(userid[1]) <= 18:
            userid[1] = '18'
        elif int(userid[1]) <= 22:
            userid[1] = '22'
        elif int(userid[1]) <= 28:
            userid[1] = '28'
        elif int(userid[1]) <= 32:
            userid[1] = '32'
        elif int(userid[1]) <= 36:
            userid[1] = '36'
        elif int(userid[1]) <= 40:
            userid[1] = '40'
        elif int(userid[1]) <= 47:
            userid[1] = '47'
        elif int(userid[1]) <= 55:
            userid[1] = '55'
        elif int(userid[1]) <= 60:
            userid[1] = '60'
        else:
            userid[1] = '22'
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