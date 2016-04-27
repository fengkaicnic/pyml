import time
import utils
import pdb
import traceback


start = time.time()
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code from config'

    cur.execute(sql)
    rst = cur.fetchall()

    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        sql_tw = 'insert into config_two(item_id, store_code, twnum0, twnumd0, twnum1, twnumd1,\
                  twnum2, twnumd2, twnum3, twnumd3, twnum4, twnumd4, twnum5, twnumd5, twnum6, twnumd6) values \
                  (%d, "%s", %f, %d, %f, %d, %f, %d, %f, %d, %f, %d, %f, %d, %f, %d)'
        result_lst = []
        result_lst.append(item_id)
        result_lst.append(store_code)
        for i in range(7):
            start_d = i * 14 + 1
            end_d = i * 14 + 15
            if store_code == 'all':
                sqlt = 'select sum(qty_alipay_njhs), count(*) from item_feature where dateid >= %d and \
                    dateid < %d and item_id = %d' % (start_d, end_d, item_id)
            else:
                sqlt = 'select sum(qty_alipay_njhs), count(*) from item_store_feature where dateid >= %d and \
                    dateid < %d and item_id = %d and store_code = %s' % (start_d, end_d, item_id, store_code)
            cur.execute(sqlt)

            rsl = cur.fetchall()
            result_lst.append(rsl[0][0])
            result_lst.append(rsl[0][1])
        try:
            for index, rs in enumerate(result_lst):
                if rs == None:
                    result_lst[index] = -1
            sql_tw = sql_tw % tuple(result_lst)
        except:
            pdb.set_trace()
            traceback.print_exc()
        # pdb.set_trace()
        cur.execute(sql_tw)

    conn.commit()
    conn.close()

except:
    conn.close()
    traceback.print_exc()

end = time.time()

print end - start
