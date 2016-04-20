import numpy as np

import utils
import pdb
import time
import traceback
import datetime

def compute_correlate(data1, data2):
    pearson = 0.0
    spearman = 0.0
    data1 = np.array(data1)
    data2 = np.array(data2)
    mole = np.mean(data1 * data2) - np.mean(data1)*np.mean(data2)
    demon = np.sqrt(np.mean(data1 ** 2) - np.mean(data1)**2) * np.sqrt(np.mean(data2 ** 2) - np.mean(data2)**2)

    pearson = float(mole) / demon

    print pearson


def correlate_feature_next(item_id, period):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        date = datetime.datetime(2015, 12, 27)
        pv_ipv, pv_uv, cart_ipv, cart_uv, collect_uv, ss_pv_ipv, ss_pv_uv, qty = ([] for n in range(8))
        for i in range(int(round(445.0/period))):
            en_date = (date - datetime.timedelta(i * period)).strftime('%Y%m%d')
            st_date = (date - datetime.timedelta((i+1) * period)).strftime('%Y%m%d')
            stp_date = (date - datetime.timedelta((i+2) * period)).strftime('%Y%m%d')
            sqlp = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(cart_uv), sum(collect_uv),\
                    sum(ss_pv_ipv), sum(ss_pv_uv) from item_feature where item_id = %d and date > "%s" \
                    and date <= "%s"' % (item_id, stp_date, st_date)
            cur.execute(sqlp)
            resultp = cur.fetchall()
            sqln = 'select sum(qty_alipay_njhs) from item_feature where item_id = %d and\
                    date > "%s" and date <= "%s"' % (item_id, st_date, en_date)
            cur.execute(sqln)
            resultn = cur.fetchall()
            for rst in resultp:
                pv_ipv.append(rst[0]), pv_uv.append(rst[1]), cart_ipv.append(rst[2])
                cart_uv.append(rst[3]), collect_uv.append(rst[4]), ss_pv_ipv.append(rst[5])
                ss_pv_uv.append(rst[6])

            for rsn in resultn:
                qty.append(rsn[0])

        for dex, qt in enumerate(qty):
            if qt is None:
                qty[dex] = 0

        for lst in [pv_ipv, pv_uv, cart_ipv, cart_uv, collect_uv, ss_pv_ipv, ss_pv_uv]:
            for dex, rt in enumerate(lst):
                if rt == None:
                    lst[dex] = 0
            mnum = len(lst) < len(qty) and len(lst) or len(qty)
            compute_correlate(lst[:mnum], qty[:mnum])
    except:
        traceback.print_exc()


def correlate_feature(item_id):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()

        sql = 'select pv_ipv, pv_uv, cart_ipv, cart_uv, collect_uv, qty_alipay_njhs, ss_pv_ipv, ss_pv_uv from \
                item_feature where item_id = %d order by date' % item_id

        cur.execute(sql)
        rst = cur.fetchall()
        pv_ipv = []
        pv_uv = []
        cart_ipv = []
        cart_uv = []
        collect_uv = []
        ss_pv_ipv = []
        ss_pv_uv = []
        qty = []
        for tm in rst:
            pv_ipv.append(tm[0])
            pv_uv.append(tm[1])
            cart_ipv.append(tm[2])
            cart_uv.append(tm[3])
            collect_uv.append(tm[4])
            qty.append(tm[5])
            ss_pv_ipv.append(tm[6])
            ss_pv_uv.append(tm[7])


        for lst in [pv_ipv, pv_uv, cart_ipv, cart_uv, collect_uv, ss_pv_ipv, ss_pv_uv]:
            compute_correlate(lst, qty)

    except:
        traceback.print_exc()

        conn.close()


if __name__ == '__main__':
    item_id = 24366
    correlate_feature(item_id)
    print '===================='
    correlate_feature_next(item_id, 1)
    # lst = [0, 0, 1, 0, 0, 1, 0]
    # lsw = [0, 0, 0, 0, 1, 1, 0]
    # compute_correlate(lst, lsw)
