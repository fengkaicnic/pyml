import utils
import traceback
import datetime
import time
import pdb
import copy

start = time.time()

try:
    table = 'order_data_test'
    conn = utils.persist.connection()
    path = 'D:/ditech/citydata/read_me_1.txt'
    cur = conn.cursor()
    with open(path, 'r') as file:
        lines = file.readlines()
        
    sql = 'select * from cluster_map_test'
    resultdct = {}
    cur.execute(sql)
    
    rst = cur.fetchall()
    for rs in rst:
        district_hash = rs[0]
        district_id = rs[1]
        resultdct[district_hash] = []
        resultdct[district_hash].append(district_hash)
        resultdct[district_hash].append(district_id.strip())
    results = []
    
    num = 0
    for line in lines:
        num += 1
        print num
        line = line.strip()
        lst = line.split('-')
        splice1 = int(lst[-1])
        datestr = '-'.join(lst[:-1])
        nm = 0
        
        for key in resultdct.keys():
            nm += 1
            print nm
            rstlst = copy.deepcopy(resultdct[key])
            rstlst.append(line)
#             pdb.set_trace()
            splice = splice1
            for i in range(1, 4):
                splice = splice - 1
                sql1 = 'select count(*) from %s where date = "%s" and splice = %d\
                         and start_district_hash = "%s"' % (table, datestr, splice, key)
                cur.execute(sql1)
                rst1 = cur.fetchall()
                sql2 = 'select count(*) from %s where date = "%s" and splice = %d and driver_id = "Null" \
                         and start_district_hash = "%s"' % (table, datestr, splice, key)
                cur.execute(sql2)
                rst2 = cur.fetchall()
                cunt1 = rst1[0][0]
                cunt2 = rst2[0][0]
                rstlst.append(cunt1)
                rstlst.append(cunt2)
#             pdb.set_trace()
            results.append(','.join(map(lambda x:str(x), rstlst)))
    
    with open('d:/ditech/result_3_inter', 'wb') as file:
        file.writelines('\n'.join(results))
    
    conn.close()
except:
    traceback.print_exc()
    conn.close()

end = time.time()
print end - start
