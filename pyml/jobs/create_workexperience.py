import os

import MySQLdb
try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='jobs', charset='utf8')
    cur = conn.cursor()
    scoresql = 'create table workexperience(id int primary key not null auto_increment, userid varchar(64), \
    department varchar(255), end_date varchar(12), industry varchar(255), position_name varchar(255),\
    salary int, size int, start_date varchar(12), type varchar(12)), num int, position_alias varchar(96)'
    scoretol = cur.execute(scoresql)
    conn.close()
    
except Exception as e:
 
    conn.close()
    print e