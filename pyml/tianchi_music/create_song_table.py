import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='mysql', db='test', charset='utf8')
    cur = conn.cursor()
    sql1 = 'drop '
    metasql = 'create table songs(id int primary key not null auto_increment, name varchar(128), majorid int, type varchar(20))'
    scoretol = cur.execute(metasql)
    conn.close()

except Exception as e:

    conn.close()
    print e