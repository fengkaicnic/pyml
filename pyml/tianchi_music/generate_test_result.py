#test git
import os
import json
import re
import time
import utils
import datetime
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

    sql = 'select artist_id, song_id from songs'
    cur.execute(sql)
    rst = cur.fetchall()
    results = {}
    pdb.set_trace()
    for item in rst:
        if not results.has_key(item[0]):
            results[item[0]] = 0
        sql1 = 'select count(song_id) from useraction where song_id = "%s"' % item[1]
        cur.execute(sql1)
        num = cur.fetchall()
        results[item[0]] += num[0][0]
    dltim = datetime.datetime(2015, 9, 1)
    rsttt = []
    for key in results.iterkeys():
        for i in range(60):
            dm = dltim + datetime.timedelta(days=i)
            rsttt.append(key + ',' + str(results[key]/180) + ',' + dm.strftime('%Y%m%d'))

    with open('d:/tianchi/music/mars_tianchi_artist_plays_predict.csv', 'wb') as file:
        file.writelines('\n'.join(rsttt))
    pdb.set_trace()
    conn.commit()
    conn.close()

except Exception as e:
    pdb.set_trace()
    conn.commit()
    conn.close()
    print e

end = time.time()

print (end - start)