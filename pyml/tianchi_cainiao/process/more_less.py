import os
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import utils
import traceback
import pdb


try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()

    sql = 'select id, a_b from config'
    cur.execute(sql)
    rst = cur.fetchall()
    pdb.set_trace()
    for term in rst:
        id = term[0]
        term = term[1]
        more_les = term.split('_')
        more = float(more_les[1])
        less = float(more_les[0])
        sqlr = 'update config set more=%f , less=%f where id = %d' % (more, less, id)
        cur.execute(sqlr)

    conn.commit()
    conn.close()

except Exception as e:
    traceback.print_exc()
    conn.close()
    print e