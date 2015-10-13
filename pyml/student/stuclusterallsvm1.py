import os

import MySQLdb
try:
    scorearff = open('d:/student/svm/stuclusterall1.arff', 'w+')
    scorearff.write("@relation student\n")
    scorearff.write('@attribute xuehao numeric\n')
    scorearff.write('@attribute paiming numeric\n')
    scorearff.write('@attribute librarykey numeric\n')

    bookindsql = 'select distinct(kinds) from bookkind'
    consumeddsql = 'select distinct(didian) from consume_test'

    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='student')
    cur = conn.cursor()
    cur.execute(bookindsql)
    bookindlsr = cur.fetchall()
    bookindlst = []
    bookindw = []
    for bookind in bookindlsr:
        bookindw.append('@attribute %s numeric\n' % bookind[0])
        bookindlst.append(bookind[0])
    consumeddlst = []
    consumekindct = {}
    cur.execute(consumeddsql)
    consumeddlsr = cur.fetchall()
    consumecnt = 0
    for consumedd in consumeddlsr:
        consumekindct[consumedd[0]] = consumecnt
        consumecnt += 1
        consumeddlst.append('@attribute %s numeric \n' % consumedd[0])
    bookindct = {}
    i = 0
    for bkd in bookindlst:
        bookindct[bkd] = i
        i += 1

    consumeddlst.append('@data\n')
    scorearff.writelines(bookindw)
    scorearff.writelines(consumeddlst)
    librarykeysql = "select a.xuehao ,count(b.riqi), a.paiming from score_test as a left join createlibrarykey_test \
                                   as b on a.xuehao = b.xuehao and a.xueqi = b.xueqi where a.xueqi = 1 group by a.xuehao"
    cur.execute(librarykeysql)
    librarylsr = cur.fetchall()
    stulbrylst = []
    xuehaolst = []
    stulbrydct = {}
    scorelsr = []
    consumestudct = {}
    for lbr in librarylsr:
        stulbrylst.append(lbr[1])
        xuehaolst.append(lbr[0])
        scorelsr.append(lbr[2])
        #if lbr[2] < 46:
        #    scorelsr.append(1)
        ##else:
        #    scorelsr.append(0)
        stulbrydct[lbr[0]] = [0 for i in xrange(len(bookindlsr))]
        consumestudct[lbr[0]] = [0 for i in xrange(len(consumeddlsr))]

    stulbrybksql = 'select t.xuehao, t.shuhao, k.kinds from tushuguan_test as t left join bookkind as k on \
                       t.shuhao = k.shuhao where t.xueqi = 1'
    cur.execute(stulbrybksql)
    stulbrylsr = cur.fetchall()
    import pdb
    for stulb in stulbrylsr:
        if stulb[2] is None:
            continue
        #if not stulbrydct.has_key(stulb[0]):
        #    stulbrydct[stulb[0]] = [0 for i in xrange(len(bookindlsr))]
        #    stulbrydct[stulb[0]][bookindct[stulb[2]]] += 1
        #else:
        stulbrydct[stulb[0]][bookindct[stulb[2]]] += 1
    consumestusql = 'select a.xuehao, a.paiming, c.didian, c.shijian from score_test as a left \
                    join consume_test as c on a.xuehao = c.xuehao and c.xueqi = c.xueqi where \
                    a.xueqi = 1'
    cur.execute(consumestusql)
    consumestulsr = cur.fetchall()
    pdb.set_trace()
    for consumestu in consumestulsr:
        print consumestu
        if consumestu[2] is None:
            continue
        consumestudct[consumestu[0]][consumekindct[consumestu[2]]] += 1
    for xuehao in xuehaolst:
        print xuehao
        stulslst = []
        stulslst.append(scorelsr[xuehao-1])
        stulslst.append(stulbrylst[xuehao-1])

        #pdb.set_trace()
        print stulbrydct[xuehao]
        stulslst = stulslst + stulbrydct[xuehao]
        stulslst = stulslst + consumestudct[xuehao]
        stulslnes = map(lambda x : str(x) + ',', stulslst)
        stulslnes[-1] = stulslnes[-1][:-1]
        stulslnes.append('\n')
        scorearff.writelines(stulslnes)

    scorearff.close()
    conn.close()

except Exception as e:

    scorearff.close()
    conn.close()
    print e






















































