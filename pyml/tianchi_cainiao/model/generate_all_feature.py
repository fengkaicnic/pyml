#coding:utf8

import utils
import traceback
import datetime
import pdb
import time

start = time.time()

store_code = 5

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
            if item_date - datetime.timedelta(num * 14) < start_date:
                break
            e_date = (item_date - datetime.timedelta(num * 14)).strftime('%Y%m%d')
            s_date = (item_date - datetime.timedelta((num + 1) * 14)).strftime('%Y%m%d')
            sql_num = 'select sum(qty_alipay_njhs) from item_feature where \
                         date <= "%s" and date > "%s" and item_id = %d' % (e_date, s_date, term_id)
            cur.execute(sql_num)
            r_num = cur.fetchall()
            
            en_date = s_date
            st_date = (item_date - datetime.timedelta((num + 2) * 14)).strftime('%Y%m%d')
            sql = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(cart_uv), sum(collect_uv) from item_feature where \
                     date > "%s" and date <= "%s" and item_id = %d' % (st_date, en_date, term_id)
            cur.execute(sql)
            f_rst = cur.fetchall()
#             pdb.set_trace()
            rst_ls.append(f_rst[0][0])
            rst_ls.append(f_rst[0][1])
            rst_ls.append(f_rst[0][2])
            rst_ls.append(f_rst[0][3])
            rst_ls.append(f_rst[0][4])
            rst_ls.append(r_num[0][0])
            rst_ls.append(term_id)
            result_lst.append(','.join(map(lambda x:str(x), rst_ls)))
            
    conn.commit()
    conn.close()
    
    with open('d:/tianchi/model/train_store_all.csv', 'wb') as file:
        file.writelines('\n'.join(result_lst))

except Exception as e:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
    print e

end = time.time()

print (end - start)