import utils
import traceback
import pdb
import time

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code from config limit 1'
    cur.execute(sql)

    rst = cur.fetchall()
    num = 0

    results = []
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        if store_code == 'all':
            sql_ce = 'select max(dateid) from item_feature where item_id = %d' % item_id
        else:
            sql_ce = 'select max(dateid) from item_store_feature where item_id = %d and\
                              store_code = %s' % (item_id, store_code)
        cur.execute(sql_ce)
        dates = cur.fetchall()
        the_end = dates[0]
        end_date1 = 1
        end11 = end_date1 + 14
        for i in range(50):
            end1 = end11 + i
            end_date =end_date1 + i
            if end1 + 14 > the_end:
                break
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
            # pdb.set_trace()
            if not feature[0][1] :
                pdb.set_trace()
            result = [ x for x in feature[0]]

            cur.execute(sql_label)
            label = cur.fetchall()
            result.append(label[0][0]>feature[0][0] and '1' or '0')
            results.append(','.join(map(lambda x:str(x), result)))

        print item_id
        print store_code
    for rs in results:
        print rs

except:
    traceback.print_exc()

end = time.time()

print end - start
