#coding:utf8
#generate test set by all

import utils
import traceback
import datetime
import pdb
import time

start = time.time()

period = 14

try:

    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select distinct(item_id) from config'
    cur.execute(sql)
    rst = cur.fetchall()
    start_date = datetime.datetime(2014, 10, 1)
    item_date = datetime.datetime(2015, 12, 27)
    tem_dct = {}
    result_lst = []
    for term_id in rst:
        term_id = term_id[0]
        for num in range(1):
            rst_ls = []
            if item_date - datetime.timedelta(num * period) < start_date:
                break
            en_date = (item_date - datetime.timedelta(num * period)).strftime('%Y%m%d')
            st_date = (item_date - datetime.timedelta((num + 1) * period)).strftime('%Y%m%d')

            sql = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(collect_uv), sum(ss_pv_ipv), sum(ss_pv_uv), sum(qty_alipay_njhs),\
             sum(jhs_pv_ipv), sum(jhs_pv_uv), sum(qty_alipay) - sum(qty_alipay_njhs), sum(qty_alipay_njhs)/sum(cart_ipv), \
             sum(qty_alipay_njhs)/sum(pv_uv) from item_feature where date > "%s" and date <= "%s" and item_id = %d' % (st_date, en_date, term_id)
            cur.execute(sql)
            f_rst = cur.fetchall()
#             pdb.set_trace()
            rst_ls.append(f_rst[0][0])
            rst_ls.append(f_rst[0][1])
            rst_ls.append(f_rst[0][2])
            rst_ls.append(f_rst[0][3])
            rst_ls.append(f_rst[0][4])
            rst_ls.append(f_rst[0][5])
            rst_ls.append(f_rst[0][6])
            rst_ls.append(f_rst[0][7])
            rst_ls.append(f_rst[0][8])
            rst_ls.append(f_rst[0][9])
            rst_ls.append(f_rst[0][10])
            rst_ls.append(term_id)
            rst_ls = [x or 0 for x in rst_ls]
            result_lst.append(','.join(map(lambda x:str(x), rst_ls)))
            
    conn.commit()
    conn.close()
    
    with open('d:/tianchi/model/test_store_jhs_per_all_%d.csv' % period, 'wb') as file:
        file.writelines('\n'.join(result_lst))

except Exception as e:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
    print e

end = time.time()

print (end - start)
