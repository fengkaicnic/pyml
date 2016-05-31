# add id for all date
import utils
import traceback

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    lines = file.readlines()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select * from cluster_map'
    cluster_dct = {}
    cur.execute(sql)
    rst = cur.fetchall()
    for rs in rst:
        cluster_dct[rs[0]] = rs[1]

    results = []
    for line in lines:
        lst = line.strip().split(',')
        lst.insert(1, cluster_dct[lst[0]])
        results.append(','.join(map(lambda x:str(x), lst)))

    with open('d:/ditech/all_date_gap_id_splice.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    conn.close()

except:
    traceback.print_exc()
    conn.close()
