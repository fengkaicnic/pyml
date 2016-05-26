import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table traffic(id int primary key not null auto_increment, \
                    district_hash varchar(64), tj_level varchar(64), tj_time varchar(64),\
                     date varchar(15), splice int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
