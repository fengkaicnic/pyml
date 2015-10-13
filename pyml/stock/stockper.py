import os
import MySQLdb

try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='stock')
    cur = conn.cursor()
    stocknumsql = 'select distinct(stocknm) from stockta'
    stocktol = cur.execute(stocknumsql)
    stocknumlst = cur.fetchall()
    print stocktol
    for num in stocknumlst:
        print num[0]
        stocksql = 'select stockdate, close , id from stockta where stocknm = "'+num[0]+'" and stockdate >= "2015-05-31" order by stockdate'
        allre = cur.execute(stocksql)
        stock_for_num = cur.fetchall()
        if allre == 0:
            continue
        i = 0
        for stock in stock_for_num:
            if i < allre-1:
                stocknum_pe = (stock_for_num[i+1][1]-stock_for_num[i][1])*100/stock_for_num[i][1]
                stockpersql = 'update stockta set stockper = %f where id = ' % stocknum_pe + str(stock_for_num[i+1][2])
                #import pdb
                #pdb.set_trace()
                print stockpersql
                cur.execute(stockpersql)
                i += 1

        print stock_for_num[0]
        #break
    
    conn.commit()
    cur.close()
    conn.close()

except Exception as e:
    print e
    cur.close()
    conn.close()