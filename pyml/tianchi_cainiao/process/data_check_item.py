import utils
import os
import time
import traceback
import datetime


start = time.time()

def check_store_data():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select id, date from item_store_feature'
        cur.execute(sql)
        end_date = datetime.datetime(2015, 12, 28)
        rst = cur.fetchall()
        for rs in rst:
            item_id = rs[0]
            id = rs[0]
            date = rs[1]
            date = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:]))
            day = (end_date - date).days
            d_sql = 'update item_store_feature set dateid = %d where id = %d' % \
                      (day, id)

            cur.execute(d_sql)

        conn.commit()
        conn.close()

    except:
        traceback.print_exc()
        conn.close()


def check_data():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select id, date from item_feature'
        cur.execute(sql)
        end_date = datetime.datetime(2015, 12, 28)
        rst = cur.fetchall()
        for rs in rst:
            id = rs[0]

            date = rs[1]
            date = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:]))
            day = (end_date - date).days
            d_sql = 'update item_feature set dateid = %d where id = %d' % \
                      (day, id)

            cur.execute(d_sql)

        conn.commit()
        conn.close()

    except:
        traceback.print_exc()
        conn.close()


if __name__ == '__main__':
    check_store_data()

end = time.time()

print end - start
