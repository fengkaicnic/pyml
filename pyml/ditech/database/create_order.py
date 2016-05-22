import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table order_data_test(id int primary key not null auto_increment, order_id varchar(64), driver_id varchar(64), passenger_id varchar(64), start_district_hash varchar(64),\
                    dest_district_hash varchar(64), price decimal(10, 5), time varchar(36), date varchar(25), splice int)'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
