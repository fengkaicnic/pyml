import utils
import traceback

try:
    path = 'D:/ditech/citydata/season_1/test_set_1/cluster_map/cluster_map'
    conn = utils.persist.connection()
    cur = conn.cursor()
    with open(path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        lst = line.split('\t')
        sql = 'insert into cluster_map_test(district_hash, district_id) values("%s", "%s")' % (lst[0], lst[1])
        cur.execute(sql)
    
    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    