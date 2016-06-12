import utils

import traceback
import pdb
import time

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    table = 'weather_test2'
    sql = 'select id, time from %s' % table
    
    cur.execute(sql)
    
    rst = cur.fetchall()
    for rs in rst:
        id = rs[0]
        times = rs[1]
        tsr = times.split(' ')
        datestr = tsr[0]
        tm = tsr[1].split(':')
        num = int(tm[0]) * 60 + int(tm[1])
        splice = num/10 + 1
        
        dssql = 'update %s set date = "%s" , splice = %d where id = %d' % (table, datestr, splice, id)
        
        cur.execute(dssql)

    conn.commit()    
    conn.close()
except:
    traceback.print_exc()
    print dssql
    conn.close()
    
end = time.time()
print end - start
