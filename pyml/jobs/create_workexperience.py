import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs')
    cur = conn.cursor()
    sql1 = 'drop '
    scoresql = 'create table workexperience(id int primary key not null auto_increment, userid varchar(64), \
    department varchar(64), end_date varchar(12), industry varchar(64), position_name varchar(64),\
    salary int, size int, start_date varchar(12), type varchar(12))'
    scoretol = cur.execute(scoresql)
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e
    