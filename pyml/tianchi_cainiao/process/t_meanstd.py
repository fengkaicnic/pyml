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
        nm = 0
        for rs in rst:
            item_id = rs[0]
            store_code = rs[1]
            if item_id == 75871 and store_code == "2":
                pdb.set_trace()
            if store_code == 'all':
                p_sql = 'select qty_alipay_njhs, date from item_feature where item_id = %d and date \
                        > "%s" and date <= "%s" ' % (item_id, start_date, end_date)
            else:
                p_sql = 'select qty_alipay_njhs, date from item_store_feature where item_id = %d and \
                         date > "%s" and date <= "%s" and store_code = "%s"' % (item_id, start_date, end_date, store_code)

            cur.execute(p_sql)

            result = cur.fetchall()
            testarry = [x[0] for x in result]
            
            testary = np.array(testarry)
            testaryn = (testary - testary.mean())/(testary.std() + 0.001)
            if len(testaryn) > 0:
                stastic, p_value = stats.kstest(testaryn, 'norm')
            else:
                p_value = 2.0
            # print normal.cdf(test_dt[0])
            # print p_value, item_id, store_code
            
            mssql = 'update config set tmean = %f , tstd = %f, normal = %f where item_id = %d and store_code = "%s"' % (testary.mean(),\
                                                                                             testary.std(), p_value, item_id, store_code)
            try:
                cur.execute(mssql)
            except:
                traceback.print_exc()
            nm += 1
            print nm
            
        conn.commit()
        conn.close()
    except:
        traceback.print_exc()
        pdb.set_trace()
        conn.close()


if __name__ == '__main__':
    start_date = '20151212'
    end_date = '20151227'

    update_config(start_date, end_date, 'doublet', '20151212', 'doublet_mv')

end = time.time()
print end - start
