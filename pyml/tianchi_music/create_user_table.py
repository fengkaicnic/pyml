import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    metasql = 'create table useraction(id int primary key not null auto_increment, user_id varchar(36), song_id varchar(36),\
                gmt_time varchar(12), action_type varchar(2), Ds varchar(8))'
    scoretol = cur.execute(metasql)
    conn.close()

except Exception as e:

    conn.close()
    print e