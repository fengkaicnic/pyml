import utils
import traceback
import pdb

date = '2016-01-15'
try:
    weatct = {}
    conn = utils.persist.connection()
    cur = conn.cursor()
    spsql = 'select * from weather where weather is not null'
    cur.execute(spsql)
    sprst = cur.fetchall()
    for sp in sprst:
        weatct[int(sp[-2])] = [int(sp[1]), float(sp[2]), float(sp[3])]

    sql = 'select distinct(splice) from weather where date = "%s" order by splice' % date
    cur.execute(sql)
    rst = cur.fetchall()
    gaped_splice = []
    splice = 1
    pdb.set_trace()
    for rs in rst:
        if splice == rs[0]:
            splice += 1
            continue
        total = rs[0] - splice
        tsplice = splice
        # pdb.set_trace()
        num = total
        while num > 0:
            if total/num > 2 and tsplice - 1 > 0 :
                weather = weatct[tsplice - 1][0]
                temperature = weatct[tsplice - 1][1]
                pm25 = weatct[tsplice - 1][2]
            else:
                weather = weatct[rs[0]][0]
                temperature = weatct[rs[0]][1]
                pm25 = weatct[rs[0]][2]
            sql = 'insert into weather(date, splice, weather, temperature, pm25) values ("%s", %d, %f, %f, %f)' % (date, int(splice), weather, temperature, pm25)
            cur.execute(sql)
            num -= 1
            splice += 1
        splice += 1

    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    conn.close()
