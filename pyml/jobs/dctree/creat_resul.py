#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
reload(sys)
import pdb
sys.setdefaultencoding('utf8')
start = time.clock()

def read_tree(filename):

    import pickle
    reader = open(filename,'rU')
    return pickle.load(reader)

try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    sql = 'select jb.userid,jb.degree,jb.age,jb.start_age,jb.bstart_year,jb.gender,jb.start_salary,wk.size \
                                        from jobs_uinfotest as jb left join workexperiencetest as wk on \
                                        jb.userid = wk.userid and wk.num = 1'
    cur.execute(sql)
    file = open('d:/jobs/dctree/result.csv', 'w+')
    useridlst = cur.fetchall()
    rsultlabel = read_tree('result.txt')
    rsultlabel = map(str, rsultlabel)
    file.write('id,degree,size,salary,position_name\n')
    i = 0
    print rsultlabel
    pdb.set_trace()
    for userid in useridlst:
        result = []
        result.append(userid[0])
        print i
        if rsultlabel[i] == '0':
            result.append(u'0,4,1,销售经理\n')
        if rsultlabel[i] == '1':
            result.append(u'1,4,1,销售经理\n')
        if rsultlabel[i] == '2':
            result.append(u'2,5,6,项目经理\n')
  #      print userid[0] 
        strs = ','.join(result)
        file.write(strs.encode('utf-8'))
        i += 1                
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print(end - start)