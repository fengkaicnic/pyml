#coding:utf8

import os
import pdb
import time
import sys
import traceback
import utils
reload(sys)
sys.setdefaultencoding('utf8')

start = time.time()

try:
    num = 0
    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    sql = 'select description from company where recommend = 1 and confirm = 1'
    cur.execute(sql)
    rst = cur.fetchall()

except:
    pdb.set_trace()
    traceback.print_exc()
    conn.close()

end = time.time()

print (end - start)
