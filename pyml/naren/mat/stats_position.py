import utils
import traceback
import pdb

try:
    conn = utils.persist.connection()
    cur = conn.cursor()

    sql = 'select pos_id, sum(hunter_read) as nm, sum(hunter_confirm), sum(hr_confirm) from pos_resume group by pos_id having nm > 0 order by nm'
    cur.execute(sql)
    rst = cur.fetchall()

    for rs in rst:
        try:
            sql2 = 'select position_name from company where position_id = %d' % rs[0]
            cur.execute(sql2)
            rsst = cur.fetchall()
            print rsst[0][0], rs[0], rs[1], rs[2], rs[3]
        except:
            print sql2

except:
    pdb.set_trace()
    traceback.print_exc()
