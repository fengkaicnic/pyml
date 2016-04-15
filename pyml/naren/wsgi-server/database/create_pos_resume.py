import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table pos_resume(id int primary key not null auto_increment, pos_id int, \
                  resume_id int, hunter_confirm int, hr_confirm int, interview_confirm int, \
                  boss_confirm int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
