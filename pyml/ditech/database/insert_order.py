import utils
import traceback
import os
import time
import pdb

start = time.time()
try:
    path = 'D:/ditech/citydata/season_1/training_data/order_data'
    conn = utils.persist.connection()
    cur = conn.cursor()
    num = 0
    for pl in os.listdir(path):
        if not '.' in pl:
            with open(path + '/' + pl) as file:
                lines = file.readlines()
                for line in lines:
                    lst = line.split('\t')
                    lst = map(lambda x:x.strip(), lst)
                    sql = 'insert into order_data(order_id, driver_id, passenger_id, start_district_hash, dest_district_hash, price, time) \
                             values("%s", "%s", "%s", "%s", "%s", %f, "%s")' % (lst[0], lst[1], lst[2], lst[3], lst[4], float(lst[5]), lst[6])
                    
                    cur.execute(sql)
                    
    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    print sql
    conn.commit()
    conn.close()
end = time.time()
print end - start
