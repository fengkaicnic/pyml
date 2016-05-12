import utils
import traceback
import pdb
import time

start = time.time()

end_date = 1

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    end1 = end_date + 14
    start1 = end_date + 14 * 2
    sql = 'select item_id, store_code from config limit 1'
    cur.execute(sql)

    rst = cur.fetchall()
    num = 0
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        if store_code == 'all':
            sql_feature = 'select sum(qty_alipay_njhs), sum(pv_ipv), sum(pv_uv), sum(ss_pv_ipv), \
                        sum(ss_pv_uv), sum(collect_uv) from item_feature where item_id = %d \
                      and dateid < %d and dateid >= %d' % (item_id, end1 + 14, end1)
            sql_label = 'select sum(qty_alipay_njhs) from item_feature where item_id = %d \
                      and dateid < %d and dateid >= %d' % (item_id, end_date + 14, end_date)
        else:
            sql_feature = 'select sum(qty_alipay_njhs), sum(pv_ipv), sum(pv_uv), sum(ss_pv_ipv), \
                        sum(ss_pv_uv), sum(collect_uv) from item_store_feature where item_id = %d \
                      and store_code = %s and dateid < %d and dateid >= %d' % (item_id, store_code, end1 + 14, end1)
            sql_label = 'select sum(qty_alipay_njhs) from item_store_feature where item_id = %d \
                      and store_code = %s and dateid < %d and dateid >= %d' % (item_id, store_code,\
                                                                    end_date + 14, end_date)
        cur.execute(sql_feature)
        feature = cur.fetchall()

        cur.execute(sql_label)
        label = cur.fetchall()


    print num

except:
    traceback.print_exc()

end = time.time()

print end - start
