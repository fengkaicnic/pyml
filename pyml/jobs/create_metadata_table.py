import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', charset='utf8')
    cur = conn.cursor()
    sql1 = 'drop '
    metasql = 'create table metadata(id int primary key not null auto_increment, name varchar(128), letter varchar(255), type varchar(20))'
    scoretol = cur.execute(metasql)
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e
    