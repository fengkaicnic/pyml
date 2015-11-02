#coding:gb2312
import os
import json
import sys
import re
import MySQLdb
import time
import pdb
reload(sys)
sys.setdefaultencoding('utf8')
start = time.clock()

def read_tree(filename):
    '''
    从文件中读取决策树，返回决策树
    '''
    import pickle
    reader = open(filename,'rU')
    return pickle.load(reader)

try:
    result = read_tree('result.txt')
    result = map(str, result)
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
    file.write('id,degree,size,salary,position_name\n')
    i = 0
    pdb.set_trace()
    for userid in useridlst:
        userlst = [userid[0]]
        userlst.append(result[i])
        if result[i] == '0':
            userlst.append(u'4,1,销售经理')
        if result[i] == '1':
            userlst.append(u'4,1,销售经理')
        if result[i] == '2':
            userlst.append(u'5,6,项目经理')
        print userlst
        print i
        strs = ','.join(userlst) + '\n'
        file.write(strs)
        i +=1
        
    conn.commit()
    conn.close()
    file.close()
except Exception as e:
    file.close()
    conn.close()
    print e
end = time.clock()
print (end - start)