import os
import MySQLdb

try:
    stockarff = open('d:/stock/stocknew.arff', 'w+')
    stockarff.write("@relation stock\n")
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='stock')
    cur = conn.cursor()
    stknmsql = 'select distinct(stocknm) from stockta'
    stkdate = 'select distinct(stockdate) from stockta where stockdate > "2015-06-01"'
    stknmtol = cur.execute(stknmsql)
    stknmlsr = cur.fetchall()
    stknmdatetol = cur.execute(stkdate)
    stknmdatelsr = cur.fetchall()
    stknmlst = []
    stknmdct = {}
    i = 0
    for stknm in stknmlsr:
        print stknm
        stknmdct[stknm[0]] = i
        i += 1
        stknmlst.append("@attribute %s {-1, 1}\n" % stknm[0])
    stknmlst.append("@data\n")
    stockarff.writelines(stknmlst)
    for stknmdate in stknmdatelsr:
        sql = 'select stockper, stocknm from stockta where stockdate = "%s"' % stknmdate[0]
        recordtol = cur.execute(sql)
        if recordtol == 0:
            continue
        stknmdaterecord = cur.fetchall()
        stknmdatelst1 = ['{']; stknmdatelst0=['{']
        for record in stknmdaterecord:
            if record[0] < 0:
                stknmdatelst0.append(str(stknmdct[record[1]])+' -1,')
            else: 
                stknmdatelst1.append(str(stknmdct[record[1]])+' 1,')
        stknmdatelst0[-1] = stknmdatelst0[-1].replace(',', '}\n')
        stknmdatelst1[-1] = stknmdatelst1[-1].replace(',', '}\n')
        stockarff.writelines(stknmdatelst0)
        stockarff.writelines(stknmdatelst1)
    stockarff.close()
    conn.close()
except Exception as e:
    stockarff.close()
    conn.close()
    print e
    