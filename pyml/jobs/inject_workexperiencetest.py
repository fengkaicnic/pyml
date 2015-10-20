import json
import re
import MySQLdb
import time
start = time.clock()
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    with open('d:/jobs/test.json') as file:
        
        lines = file.readlines()
        linelst = lines[:]
        for line in linelst:
            if line:
                sc = json.loads(line)
                uuid = sc['id']
                workexperiencelst = sc['workExperienceList']
                i = 1
                for workdct in workexperiencelst:
                    if workdct is None:
                        continue
                    print workdct
                    worksql = 'insert into workexperiencetest (userid, department, end_date, industry, position_name, salary, size, start_date, type, num) values \
                    ("%s", "%s", "%s", "%s", "%s", %d, %d, "%s", "%s", %d)' % (uuid, workdct['department'], workdct['end_date'], workdct['industry'], workdct['position_name'], workdct['salary'], workdct['size'], workdct['start_date'], workdct['type'], i)
                    print worksql
                    cur.execute(worksql)
                    i += 1
            else:
                break
    conn.commit()
    conn.close()
    end = time.clock()
    print (end - start)
except Exception as e:
    conn.commit()
    conn.close()
    print e
