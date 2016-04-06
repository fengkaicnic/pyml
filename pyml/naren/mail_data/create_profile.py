import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table mail_profile(id int primary key not null auto_increment, \
                  gender varchar(5), latesttitle varchar(128), latestcollege varchar(255), \
                  selfappraise varchar(255), latestcompany varchar(255), latestdegree varchar(19), \
                  curemploystatus varchar(255), dessalary varchar(96), age int, desworkproperty varchar(128), \
                  destitle varchar(128), desindustry varchar(128), certificates varchar(64), \
                  desworklocation varchar(128), position_id int, resume_id int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e