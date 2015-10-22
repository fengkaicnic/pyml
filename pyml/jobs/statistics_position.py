#test git
import os
import json
import re
import MySQLdb
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
            linedct[line] = 0
            print line
    sql = 'select position_name, userid from workexperience limit 200'
    import pdb
    pdb.set_trace()
    cur.execute(sql)
    results = cur.fetchall()
    for result in results:
        if linedct.has_key(result[0]):
            linedct[result[0]] += 1
    pdb.set_trace()
    for key in linedct.iterkeys():
        print key + ':' + str(linedct[key])
    conn.commit()
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e