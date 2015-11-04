import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', charset='utf8')
    cur = conn.cursor()
    sql1 = 'drop '
    metasql = 'create table majorposition(id int primary key not null auto_increment, major varchar(128), position varchar(255), ratio float(5, 3))'
    scoretol = cur.execute(metasql)
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e
    