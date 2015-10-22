#test git
import os
import json
import MySQLdb
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
try:
    
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    mode = re.compile(r'\d+')
    linedct = {}
    with open('position_meta.txt') as file:
        lines = file.readlines()
        for linet in lines:
            line = linet[:-1]
            linedct[unicode(line)] = 0
            print unicode(line)
    sql = 'select position_name, userid from workexperience'
    
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        if linedct.has_key(result[0]):
            linedct[result[0]] += 1
    sortlines = sorted(linedct.items(), key=lambda jj:jj[1], reverse=True)
    ttn = 0
    for line in sortlines:
        ttn += line[1]
        print line[0] + ':' + str(line[1])
    conn.commit()
    conn.close()
    print "the tol num is " + str(ttn)
    
except Exception as e:
 
    conn.close()
    print e