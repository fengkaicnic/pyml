import utils
import traceback

import pdb
import numpy as np

import time
from scipy import stats

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code, doublet, doublee, doublee_mv, doublet_mv from config'
    cur.execute(sql)
    rst = cur.fetchall()
    tgnum = 0
    tonum = 0
    results = []
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        doublet = rs[2]
        doublee = rs[3]
        doublee_mv = rs[4]
        doublet_mv = rs[5]
        sqlt = 'select twnum0, twnum1, twnum2, twnum3, twnum4, twnum5, twnum6 from config_two \
                 as cgt where cgt.item_id = %d and cgt.store_code = "%s"' % (item_id, store_code)

        cur.execute(sqlt)
        rsw = cur.fetchall()

        term_arry = np.array([rsw[0][0], rsw[0][1], rsw[0][2], rsw[0][3], rsw[0][4], rsw[0][5], rsw[0][6]])
        if doublee:
            sqle = 'select qty_alipay_njhs from item_store_feature where item_id = %d and \
                      store_code = "%s" and date = "20151111"' % (item_id, store_code)
            cur.execute(sqle)
            rse = cur.fetchall()
            if not rse:
                num = 0
            else:
                num = rse[0][0]
            term_arry[3] -= num
            term_arry[3] += doublee_mv

        if doublet:
            sqle = 'select qty_alipay_njhs from item_store_feature where item_id = %d and \
                      store_code = "%s" and date = "20151212"' % (item_id, store_code)
            cur.execute(sqle)
            rse = cur.fetchall()
            if not rse:
                num = 0
            else:
                num = rse[0][0]
            term_arry[1] -= num
            term_arry[1] += doublet_mv
        term_arry = np.array([0 if x == -1 else x for x in term_arry])
        mean = term_arry.mean()

        std = term_arry.std()
        normal = stats.norm(mean, std)
        if normal.cdf(term_arry[0]) > 0.9:
            # print term_arry
            
            results.append(','.join([str(item_id), store_code, str(term_arry[0] - (term_arry[0] - mean)/10 + 1)]))
            print item_id, store_code, term_arry[0] - mean
            tgnum +=1
        elif normal.cdf(term_arry[0]) < 0.1:
            results.append(','.join([str(item_id), store_code, str(term_arry[0] + (term_arry[0] - mean)/10 + 1)]))
            print item_id, store_code, term_arry[0] - mean
            tonum += 1
        else:
            results.append(','.join([str(item_id), store_code, str(term_arry[0])]))

    with open('d:/tianchi/result_last_two_week_sign.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print tgnum
    print tonum

except:
    traceback.print_exc()

end = time.time()

print end - start
