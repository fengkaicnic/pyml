import utils
import traceback
import time

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'insert into tmp_table values(%d)'

    for i in range(8, 872):
        cur.execute(sql % i)
        print i

    conn.commit()

except:
    traceback.print_exc()

end = time.time()

print end - start
