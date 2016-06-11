import utils
import traceback
import time
import numpy as np

start = time.time()

def get_from_mysql():
    try:
        result_dct = {}
        splice = 70
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select count(*), date from order_data where splice = %d and driver_id = "NULL" group by date order by date' % splice
        cur.execute(sql)
        rst = cur.fetchall()
        
        sql = 'select weather, date from weather where splice = %d group by date order by date' % splice
        cur.execute(sql)
        wrst = cur.fetchall()
        for index, rs in enumerate(rst):
            if not result_dct.has_key(wrst[index][0]):
                result_dct[wrst[index][0]] = [rs[0]]
            else:
                result_dct[wrst[index][0]].append(rs[0])
            print rs[0], wrst[index][0], rs[1]
        
        for key in result_dct.keys():
            print key, np.mean(result_dct[key]), len(result_dct[key])
        
        conn.close()
    except:
        traceback.print_exc()
        conn.close()
        

def generate_date():
    with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
        lines = file.readlines()
        
    result_dct = {}
    for line in lines:
        lst = line.strip().split(',')
        

if __name__ == '__main__':
    get_from_mysql()
    
ed = time.time()

print ed - start
