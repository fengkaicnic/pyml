import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table education(id int primary key not null auto_increment, major varchar(128), schoolid int, \
                  description text, degree varchar(128), schoolname varchar(128), start_time varchar(20), end_time varchar(20), \
                  resume_id int, education_id int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
