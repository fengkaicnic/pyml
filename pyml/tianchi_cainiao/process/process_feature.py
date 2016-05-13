import utils
import traceback
import pdb

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select ss_pv_uv from item_feature where item_id = 9597 order by date'

    cur.execute(sql)
    # pdb.set_trace()
    rst = cur.fetchall()

    sequc = [x[0] for x in rst]

    print sequc

except:
    traceback.print_exc()
