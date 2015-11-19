#coding:utf8
import os
import json
import sys
import re
import MySQLdb
import time
from jobs import utils
reload(sys)
import pdb
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
    sql = 'select jb.userid,jb.degree,jb.age,jb.start_age,jb.bstart_year,jb.gender,jb.start_salary,wk.size \
                                        from jobs_uinfotest as jb left join workexperiencetest as wk on \
                                        jb.userid = wk.userid and wk.num = 1'
    cur.execute(sql)
    file = open('d:/jobs/dctree/bresult.csv', 'w+')
    useridlst = cur.fetchall()
    rsultlabel = utils.read_rst('result.txt')
    pdb.set_trace()
    #wsresult = utils.read_rst('wsresult.txt')
    sizeresult = utils.read_rst('sizeresult.txt')
    salaryresult = utils.read_rst('salaryresult.txt')
    posresult = utils.read_rst('position.txt')
    #degreelst = utils.read_rst('degree.txt')
    degreelst = utils.read_rst('result.txt')
    rsultlabel = map(str, rsultlabel)
    file.write('id,degree,size,salary,position_name\n')
    i = 0
    print rsultlabel
    pdb.set_trace()
    j = 0
    for userid in useridlst:
        result = []
        result.append(userid[0])
        print i
        result.append(degreelst[i])
        result.append(sizeresult[i])
        result.append(salaryresult[i])
        if posresult[i] == 'test':
            result.append(u'销售经理\n')
            j += 1
        else:
            print posresult[i]
            result.append(str(posresult[i])+'\n')
        #if rsultlabel[i] == '0':
        #    result.append('0')
        #    result.append(wsresult[i][0])
        #    result.append(wsresult[i][1])
        #    result.append(u'���۾���\n')
        #if rsultlabel[i] == '1':
        #    result.append('1')
        #    result.append(wsresult[i][0])
        #    result.append(wsresult[i][1])
        #    result.append(u'���۾���\n')
        #if rsultlabel[i] == '2':
        #    result.append('2')
        #    result.append(wsresult[i][0])
        #    result.append(wsresult[i][1])
        #    result.append(u'��Ŀ����\n')
  #      print userid[0] 
        result = map(str, result)
        strs = ','.join(result)
        file.write(strs.encode('utf-8'))
        i += 1                
    conn.commit()
    print j
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print(end - start)