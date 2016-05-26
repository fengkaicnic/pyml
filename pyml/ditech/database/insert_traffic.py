import utils
import traceback
import os
import time
import pdb

start = time.time()
try:
    path = 'D:/ditech/citydata/season_1/test_set_1/traffic_data'
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
                    for tline in lst[1:-1]:
                        sql = 'insert into traffic_test(district_hash, tj_level, tj_time) \
                                values("%s", "%s", "%s")' % (lst[0], tline, lst[-1])
                    
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
