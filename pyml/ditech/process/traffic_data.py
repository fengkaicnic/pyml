import utils
import traceback
import pdb

date = '2016-01-10'
try:
    tratct = {}
    conn = utils.persist.connection()
    cur = conn.cursor()
    spsql = 'select * from traffic where date = "%s" ' % date
    cur.execute(spsql)
    sprst = cur.fetchall()
    for sp in sprst:
        if tratct.has_key(sp[0]+'-'+str(sp[-2])):
            tratct[sp[0]+'-'+str(sp[-2])].append(sp[1])
        else:
            tratct[sp[0]+'-'+str(sp[-2])] = [sp[1]]

    sql = 'select distinct(splice) from traffic where date = "%s" order by splice' % date
    cur.execute(sql)
    rst = cur.fetchall()
    gaped_splice = []
    tnum = 0
    splice = 1
    # pdb.set_trace()
    for rs in rst:
        if splice == rs[0]:
            splice += 1
            continue
        total = rs[0] - splice
        tsplice = splice
        # pdb.set_trace()
        num = total
        while num > 0:
            if total/num < 2 and tsplice - 1 > 0 :
                weather = tratct[tsplice - 1][0]
                temperature = tratct[tsplice - 1][1]
                pm25 = tratct[tsplice - 1][2]
            else:
                weather = tratct[rs[0]][0]
                temperature = tratct[rs[0]][1]
                pm25 = tratct[rs[0]][2]
            sql = 'insert into weather(date, splice, weather, temperature, pm25) values ("%s", %d, %f, %f, %f)' % (date, int(splice), weather, temperature, pm25)
            tnum += 1
            cur.execute(sql)
            num -= 1
            splice += 1
        splice += 1

    while splice < 145:
        total = 145 - splice
        tsplice = splice
        # pdb.set_trace()
        num = total
        while num > 0:
            weather = weatct[tsplice - 1][0]
            temperature = weatct[tsplice - 1][1]
            pm25 = weatct[tsplice - 1][2]
            sql = 'insert into weather(date, splice, weather, temperature, pm25) values ("%s", %d, %f, %f, %f)' % (date, int(splice), weather, temperature, pm25)
            tnum += 1
            cur.execute(sql)
            num -= 1
            splice += 1
    print tnum
    conn.commit()

    conn.close()
except:
    traceback.print_exc()
    conn.close()
