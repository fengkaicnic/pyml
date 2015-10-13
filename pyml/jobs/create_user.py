import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs')
    cur = conn.cursor()
    sql1 = 'drop '
    scoresql = 'create table jobs_uinfo(id int primary key not null auto_increment, userid varchar(64), age int, degree int, gender varchar(12), major varchar(64))'
    scoretol = cur.execute(scoresql)
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e
    