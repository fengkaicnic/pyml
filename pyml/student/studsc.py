import os
import MySQLdb

try:
    sccmarff = open('d:/student/studtucom.arff', 'w+')
    sccmarff.write("@relation student\n")
    sccmarff.write('@attribute shubenshu numeric\n')
    sccmarff.write('@attribute xiaofei numeric\n')
    sccmarff.write('@attribute paiming numeric\n')
    sccmarff.write('@data\n')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='student')
    cur = conn.cursor()
    scoresql = 'select xuehao, group_concat(paiming order by xueqi) from score group by xuehao'
    tushusql = "select a.xuehao, a.paiming, count(b.shuhao) from score as a left \
    join tushuguan as b on a.xuehao = b.xuehao and a.xueqi = b.xueqi\
     where a.xueqi = 1 group by a.xuehao"
    consumsql = "select a.xuehao, sum(c.jineff) from score as a left join consume as c \
    on a.xuehao = c.xuehao and a.xueqi = c.xueqi where a.xueqi = 1 group by a.xuehao"
    studtol = cur.execute(tushusql)
    tushulsr = cur.fetchall()
    tushudct = {}
    cur.execute(consumsql)
    consumelsr = cur.fetchall()
    consumedct = {}
    paimingdct = {}
    i = 1
    while i < studtol + 1:
        tushudct[i] = tushulsr[i-1][2]
        if not consumelsr[i-1][1]:
            consumedct[i] = 0
        else:
            consumedct[i] = consumelsr[i-1][1]
        paimingdct[i] = tushulsr[i-1][1]
        i += 1
    scmarfflst = []
    for i in xrange(studtol):
        scmarfflst.append(str(tushudct[i+1])+','+str(consumedct[i+1])+','+str(paimingdct[i+1])+'\n')
    
    sccmarff.writelines(scmarfflst)

    sccmarff.close()
    conn.close()
    
except Exception as e:
    
    sccmarff.close()
    conn.close()
    print e
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    