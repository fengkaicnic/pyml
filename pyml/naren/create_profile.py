import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table profile(selfappraise text, resumekeywords varchar(128), tel varchar(19),\
                  name varchar(15), position_id varchar(12), dessalary varchar(20), email varchar(19), \
                  otherinfo varchar(255), descworklocation varchar(36), hisprojects text, skills varchar(128), \
                  destitle varchar(128), desindustry varchar(128), desworkproperty varchar(65), certificates varchar(64), \
                  resume_id int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e