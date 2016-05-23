import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table weather(time varchar(64), weather int, temperature decimal(5, 2), pm25 decimal(5, 2))'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
