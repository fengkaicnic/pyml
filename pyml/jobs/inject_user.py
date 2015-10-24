#test git
import os
import json
import re
import MySQLdb
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='gbk')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    mode = re.compile(r'\d+')
    with open('d:/jobs/practice.json') as file:
        while True:
            line = file.readline()
            if line:
                sc = json.loads(line)
                age = mode.findall(sc['age'])
                if len(age) ==0:
                    age = [100]
                usersql = 'insert into jobs_uinfo (userid, age, gender, major) values ("%s", %d, "%s", "%s")' % (sc['id'], int(age[0]), sc['gender'], sc['major'])
                print usersql
                cur.execute(usersql)
            else:
                break
    conn.commit()
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e