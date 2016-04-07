import os
import pdb
import utils

import MySQLdb
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    companysql = 'create table item_store_feature(id int primary key not null auto_increment, date varchar(12), \
                   item_id int, store_code int, cate_id int, cate_level_id int, brand_id int, supplier_id int, \
                   pv_ipv float(10, 2), pv_uv float(10, 2), cart_ipv float(10, 2), cart_uv float(10, 2), \
                   collect_uv float(10, 2), num_gmv float(10, 2), amt_gmv float(10, 2), qty_gmv float(10, 2),\
                  unum_gmv float(10, 2), amt_alipay float(10, 2), num_alipay float(10, 2), qty_alipay float(10, 2), \
                  unum_alipay float(10, 2), ztc_pv_ipv float(10, 2), tbk_pv_ipv float(10, 2), ss_pv_ipv float(10, 2),\
                   jhs_pv_ipv float(10, 2), ztc_pv_uv float(10, 2), tbk_pv_uv float(10, 2), ss_pv_uv float(10, 2), \
                   jhs_pv_uv float(10, 2), num_alipay_njhs float(10, 2), amt_alipay_njhs float(10, 2), \
                   qty_alipay_njhs float(10, 2), unum_alipay_njhs float(10, 2))'

    scoretol = cur.execute(companysql)
    conn.commit()
    conn.close()

except Exception as e:

    conn.close()
    print e
