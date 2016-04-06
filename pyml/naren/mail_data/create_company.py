import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table mail_company(id int primary key not null auto_increment, position_name varchar(128), \
                  low_workage varchar(5), low_income varchar(9), high_income varchar(9), description text, position_id int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e