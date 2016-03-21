import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    metasql = 'create table songs(id int primary key not null auto_increment, song_id varchar(36), artist_id varchar(36),\
                publish_time varchar(8), song_init_plays int, launguage int, gender int)'
    scoretol = cur.execute(metasql)
    conn.close()

except Exception as e:

    conn.close()
    print e