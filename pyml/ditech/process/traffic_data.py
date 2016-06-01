import utils
import traceback
import pdb
import datetime

# date = '2016-01-20'

def suppliment_traffic(hash_id, date):
    try:
        tratct = {}
        conn = utils.persist.connection()
        cur = conn.cursor()
        spsql = 'select * from traffic where date = "%s" and district_hash = "%s" ' % (date, hash_id)
        cur.execute(spsql)
        sprst = cur.fetchall()
        for sp in sprst:
            # pdb.set_trace()
            if tratct.has_key(sp[-2]):
                tratct[sp[-2]].append(sp[2])
            else:
                tratct[sp[-2]] = [sp[2]]
    
        sql = 'select distinct(splice) from traffic where date = "%s" and district_hash = "%s" order by splice' % (date, hash_id)
        cur.execute(sql)
        rst = cur.fetchall()
        gaped_splice = []
        tnum = 0
        splice = 1
        # pdb.set_trace()
        for rs in rst:
            if splice >= rs[0]:
                splice += 1
                continue
            total = rs[0] - splice
            tsplice = splice
            # pdb.set_trace()
            num = total
            while num > 0:
                if total/num < 2 and tsplice - 1 > 0 :
                    trafficlst = tratct[tsplice - 1]
                    # pdb.set_trace()
                    for tra in trafficlst:
                        sql = 'insert into traffic(district_hash, tj_level, date, splice) values ("%s", "%s", "%s", %d)' % (hash_id, tra, date, splice)
                        cur.execute(sql)
                        print sql
                else:
                    # pdb.set_trace()
                    trafficlst = tratct[rs[0]]
                    for tra in trafficlst:
                        sql = 'insert into traffic(district_hash, tj_level, date, splice) values ("%s", "%s", "%s", %d)' % (hash_id, tra, date, splice)
                        cur.execute(sql)
                        print sql
                tnum += 1
                # cur.execute(sql)
                num -= 1
                splice += 1
            splice += 1

        # pdb.set_trace()
        while splice < 145:
            # pdb.set_trace()
            total = 145 - splice
            tsplice = splice
            # pdb.set_trace()
            num = total
            while num > 0:
                trafficlst = tratct[tsplice - 1]
                for tra in trafficlst:
                    sql = 'insert into traffic(district_hash, tj_level, date, splice) values ("%s", "%s", "%s", %d)' % (hash_id, tra, date, splice)
                    cur.execute(sql)
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


def all_suppliment(date):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select * from cluster_map'
        cur.execute(sql)
        rst = cur.fetchall()
        for rs in rst:
            suppliment_traffic(rs[0], date)
        
        conn.close()
    except:
        traceback.print_exc()
        conn.close()
        
if __name__ == '__main__':
    dateste = '2016-01-01'
    for i in range(21):
        # pdb.set_trace()
        datestr = datetime.datetime.strptime(dateste, '%Y-%m-%d') + datetime.timedelta(i)
        all_suppliment(datestr.strftime('%Y-%m-%d'))
