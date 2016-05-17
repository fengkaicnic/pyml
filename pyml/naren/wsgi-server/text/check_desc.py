import utils
import traceback

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description, position_name from company where id = %d' % 40

    cur.execute(sql)

    rst = cur.fetchall()

    for rs in rst:
        print utils.discrement_unicode(rs[0])
        print utils.discrement_unicode(rs[1])
except:
    traceback.print_exc()
    conn.close()
