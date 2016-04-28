import utils
import traceback
import datetime
import pdb

try:
    conn = utils.persist.connection()
    cur = conn.cursor()

    sql = 'select item_id, store_code from config'
    cur.execute(sql)

    rst = cur.fetchall()
    end_date = datetime.datetime(2015, 12, 28)
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        if store_code == 'all':
            p_sql = 'select min(date) from item_feature where item_id = %d' % item_id
        else:
            p_sql = 'select min(date) from item_store_feature where item_id = %d and store_code = "%s"' % (item_id, store_code)

        cur.execute(p_sql)
        rsw = cur.fetchall()

        if not rsw[0][0]:
            num = -1
        else:
            # pdb.set_trace()
            m_date = rsw[0][0]
            try:
                num = (end_date - datetime.datetime(int(m_date[:4]), int(m_date[4:6]), int(m_date[6:]))).days
            except:
                pdb.set_trace()

        u_sql = 'update config set sday = %d where item_id = %d and store_code = "%s" ' % (num, item_id, store_code)

        cur.execute(u_sql)

    conn.commit()
    conn.close()

except:
    traceback.print_exc()
    conn.close()
