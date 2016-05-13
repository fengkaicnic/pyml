import utils
import traceback
import pdb
import time
import gbdt_model

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code from config limit 3, 1'
    cur.execute(sql)

    rst = cur.fetchall()
    num = 0
    period = 7
    period_l = 14
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
            if end1 + period > the_end:
                break
            # pdb.set_trace()
            if store_code == 'all':
                sql_feature = 'select sum(qty_alipay_njhs), sum(pv_ipv), sum(pv_uv), sum(ss_pv_ipv), \
                            sum(ss_pv_uv), sum(collect_uv), sum(qty_alipay - qty_alipay_njhs), sum(ztc_pv_uv),\
                             sum(tbk_pv_uv) from item_feature where item_id = %d \
                          and dateid < %d and dateid >= %d' % (item_id, end1 + period, end1)
                sql_label = 'select (select sum(qty_alipay_njhs) from item_feature where item_id = %d and dateid <%d and\
                            dateid >= %d) as nexts, (select sum(qty_alipay_njhs) from item_feature where item_id = %d and \
                            dateid <%d and dateid >=%d) as passs' % (item_id, end_date + 14, end_date, item_id, end_date+14*2, end_date+14)
            else:
                sql_feature = 'select sum(qty_alipay_njhs), sum(pv_ipv), sum(pv_uv), sum(ss_pv_ipv), \
                            sum(ss_pv_uv), sum(collect_uv),  sum(qty_alipay - qty_alipay_njhs), sum(ztc_pv_uv), \
                            sum(tbk_pv_uv) from item_store_feature where item_id = %d \
                          and store_code = %s and dateid < %d and dateid >= %d' % (item_id, store_code, end1 + period, end1)
                sql_label = 'select (select sum(qty_alipay_njhs) from item_store_feature where item_id = %d and\
                              store_code = %s and dateid <%d and dateid >= %d) as nexts, (select sum(qty_alipay_njhs) \
                              from item_store_feature where item_id = %d and store_code = %s and dateid <%d and dateid >=%d)\
                               as passs' % (item_id, store_code, end_date + 14, end_date, item_id,\
                                            store_code, end_date+14*2, end_date+14)
            cur.execute(sql_feature)
            feature = cur.fetchall()
            # pdb.set_trace()
            # if not feature[0][1] :
            #     pdb.set_trace()
            result = []
            for x in feature[0]:
                if not x :
                    result.append(0)
                else:
                    result.append(x)

            cur.execute(sql_label)
            label = cur.fetchall()
            result.append(label[0][0]>label[0][1] and 1 or 0)
            results.append(result)

        print item_id
        print store_code
    for rs in results:
        print rs

except:
    traceback.print_exc()

# gbdt_model.gbdt_model(results)
gbdt_model.svm_model(results, 10)

end = time.time()

print end - start
