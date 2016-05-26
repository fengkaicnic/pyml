import utils
import traceback

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select low_income, high_income, low_workage, high_workage, description, \
               position_name, naren_created from company where position_id = %d' % 88028

    cur.execute(sql)

    rst = cur.fetchall()

    for rs in rst:
        for tem in rs:
            print utils.discrement_unicode(tem)

except:
    traceback.print_exc()
    conn.close()
