import utils
import traceback
import os
import time
import pdb

start = time.time()
try:
    path = 'D:/ditech/citydata/season_1/training_data/weather_data'
    conn = utils.persist.connection()
    cur = conn.cursor()
    num = 0
    for pl in os.listdir(path):
        if not '.' in pl:
            with open(path + '/' + pl) as file:
                lines = file.readlines()
                for line in lines:
                    lst = line.split('\t')
                    lst = map(lambda x:x.strip(), lst)
                    sql = 'insert into weather(time, weather, temperature, pm25) values("%s", %d, %f, %f)' % (lst[0], int(lst[1]), float(lst[2]), float(lst[3]))
                    
                    cur.execute(sql)
                    
    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    print sql
    conn.commit()
    conn.close()
end = time.time()
print end - start
