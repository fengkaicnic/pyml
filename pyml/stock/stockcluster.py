import os
import MySQLdb
import copy
try:
    stockarff = open('d:/stock/stockcluster.arff', 'w+')
    stockarff.write("@relation stock\n")
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='stock')
    cur = conn.cursor()
    stknmsql = 'select distinct(stocknm) from stockta'
    stkdate = 'select distinct(stockdate) from stockta where stockdate > "2015-06-01"'
    stknmtol = cur.execute(stknmsql)
    stknmlsr = cur.fetchall()
    stknmdatetol = cur.execute(stkdate)
    stknmdatelsr = cur.fetchall()
    stkdatlst = []
    stkdtdct = {};i = 0
    for stkdat in stknmdatelsr:
        stkdtdct[stkdat[0]] = '0'
        stkdatlst.append("@attribute %s {-1, 0, 1}\n" % stkdat[0])
    stkdatlst.append("@data\n")
    stockarff.writelines(stkdatlst)
    for stknm in stknmlsr:
        sql = 'select stockper, stocknm, stockdate from stockta where stocknm = "%s" and stockdate > "2015-06-01"' % stknm[0]
        stknmt = copy.deepcopy(stkdtdct)
        recordtol = cur.execute(sql)
        if recordtol == 0:
            continue
        stknmperecord = cur.fetchall()
        stknmperlst = []
        for record in stknmperecord:
            if record[0] < 0:
                stknmt[record[2]] = '-1'
            else: 
                stknmt[record[2]] = '1'
        for stkdat in stknmdatelsr:
            stknmperlst.append(stknmt[stkdat[0]] + ',')
        stknmperlst[-1] = stknmperlst[-1].replace(',', '\n')
        stockarff.writelines(stknmperlst)
    stockarff.close()
    conn.close()
except Exception as e:
    stockarff.close()
    conn.close()
    print e