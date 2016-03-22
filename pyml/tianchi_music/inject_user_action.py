#test git
import os
import json
import re
import time
import utils
import pdb

start = time.time()
try:

    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    mode = re.compile(r'\d+')
    with open('d:/tianchi/music/mars_tianchi_user_actions.csv') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            items = line.strip().split(',')
            sql = 'insert into useraction(user_id, song_id, gmt_time, action_type, DS) values \
                                        ("%s", "%s", "%s", "%s", "%s")' % tuple(items)
            cur.execute(sql)
            print index
    conn.commit()
    conn.close()

except Exception as e:
    pdb.set_trace()
    conn.commit()
    conn.close()
    print e

end = time.time()

print (end - start)