import utils
import traceback
import os
import time
import pdb

start = time.time()
try:
    path = 'D:/ditech/citydata/season_1/test_set_1/poi_data/poi_data'
    conn = utils.persist.connection()
    cur = conn.cursor()

    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            lst = line.split('\t')
            lst = map(lambda x:x.strip(), lst)
            for tline in lst[1:]:
                sql = 'insert into poi_test values("%s", "%s")' % (lst[0], tline)
            
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
