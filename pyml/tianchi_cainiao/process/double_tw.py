import utils

import os
import pdb
from scipy import stats
import traceback
import numpy as np
import time

start = time.time()

def update_config(start_date, end_date, doubles, date_tar, double_mv):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select item_id, store_code from config'
        cur.execute(sql)
        rst = cur.fetchall()
        for rs in rst:
            item_id = rs[0]
            store_code = rs[1]
            if store_code == 'all':
                p_sql = 'select qty_alipay_njhs, date from item_feature where item_id = %d and date \
                        > "%s" and date <= "%s" ' % (item_id, start_date, end_date)
            else:
                p_sql = 'select qty_alipay_njhs, date from item_store_feature where item_id = %d and \
                         date > "%s" and date <= "%s" and store_code = "%s"' % (item_id, start_date, end_date, store_code)

            cur.execute(p_sql)

            result = cur.fetchall()
            if item_id == 36844 and store_code == '4':
                pdb.set_trace()
            testarry = [x[0] for x in result]
            test_dt = [r[0] for r in result if r[1] == date_tar]
            if not test_dt:
                continue
            testary = np.array(testarry)
            total = testary.sum() - test_dt[0]
            double_mpv = total / (len(testary) - 1)
            normal = stats.norm(testary.mean(), testary.std())
            testary = (testary - testary.mean())/testary.std()
            stastic, p_value = stats.kstest(testary, 'norm')
            # print normal.cdf(test_dt[0])
            # print p_value, item_id, store_code
            if normal.cdf(test_dt[0]) > 0.9:
                try:
                    up_sql = 'update config set %s = 1, %s = %f where item_id = %d and\
                              store_code = "%s"' % (doubles, double_mv, double_mpv, item_id, store_code)
                    cur.execute(up_sql)
                except:
                    pdb.set_trace()
                    traceback.print_exc()

        conn.commit()
        conn.close()
    except:
        traceback.print_exc()
        conn.close()


if __name__ == '__main__':
    t_start_date = '20151205'
    t_end_date = '20151219'

    e_start_date = '20151104'
    e_end_date = '20151118'

    update_config(t_start_date, t_end_date, 'doublet', '20151212', 'doublet_mv')
    update_config(e_start_date, e_end_date, 'doublee', '20151111', 'doublee_mv')

end = time.time()
print end - start
