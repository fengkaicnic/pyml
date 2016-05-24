import utils
import traceback
import copy
import time
import pdb

start = time.time()

path = 'D:/ditech/citydata/read_me_1.txt'

try:
    splice_lst = []
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            lst = line.split('-')
            splice_lst.append(int(lst[-1]))
    splice_lst = list(set(splice_lst))
    results = []
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql_hash = 'select * from cluster_map'
    cur.execute(sql_hash)
    rst = cur.fetchall()
    hash_dct = {}
    for rs in rst:
        hash_dct[rs[0]] = [rs[0], rs[1]]
    num = 0
    for key in hash_dct.keys():
        num += 1; print num
        for splice in splice_lst:
            rsult = copy.deepcopy(hash_dct[key])
            # sqltf = 'select count(*) from order_data where start_district_hash = "%s" and\
            #       splice = %d' % (key, splice)
            sqlntf = 'select date, count(*) from order_data where start_district_hash = "%s" and\
                  splice = %d and driver_id = "NULL" group by date order by date' % (key, splice)

            # cur.execute(sqltf)
            # rst1 = cur.fetchall()
            rsult.append(splice)
            cur.execute(sqlntf)
            rst2 = cur.fetchall()
            tnum = 1
            for rs in rst2:
                if int(rs[0].split('-')[-1]) == tnum:
                    rsult.append(rs[1])
                    tnum += 1
                else:
                    # pdb.set_trace()
                    rnum = int(rs[0].split('-')[-1]) - tnum
                    for i in range(rnum):
                        rsult.append(0)
                        tnum += 1
                    rsult.append(rs[1])
                    tnum += 1
            results.append(','.join(map(lambda x:str(x), rsult)))

    with open('d:/ditech/splice_series.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    conn.close()
except:

    traceback.print_exc()
    conn.close()

end = time.time()
print end - start
