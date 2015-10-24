import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', charset='utf8')
    cur = conn.cursor()
    sql1 = 'drop '
    scoresql = 'create table jobs_uinfo(id int primary key not null auto_increment, userid varchar(64), age int, degree int, gender varchar(12), major varchar(128)\
    , start_age int, bstart_year int, agenormal float(5, 3), startyearnormal float(5, 3), start_salary int)'
    scoretol = cur.execute(scoresql)
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e
    