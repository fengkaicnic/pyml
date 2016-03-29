import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table work(id int primary key not null auto_increment, wage varchar(128), unit_name varchar(255), \
                  scale int, description text, position_num int, start_time varchar(20), end_time varchar(20), \
                  trade_num varchar(12), trade varchar(128), position_name varchar(128), unittype int, department varchar(128),\
                  otherfield varchar(255), experience_id int, resume_id int, last_time varchar(37))'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
