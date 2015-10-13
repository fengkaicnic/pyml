import random
import os
import MySQLdb
try:
    scorearff = open('d:/student/threestu.txt', 'w+')
    scorearff.write("@relation student\n")
    scorearff.write('@attribute xuehao numeric\n')
    scorearff.write('@attribute paimingone numeric\n')
    scorearff.write('@attribute paimingtwo numeric\n')
    scorearff.write('@attribute paimingthe numeric\n')
    scorearff.write('@data\n')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='student')
    cur = conn.cursor()
    consumethrsql = 'select xuehao ,shijian, jine from consume_test where xueqi = 3'
    consumethrtotal = cur.execute(consumethrsql)
    consumethrlsr = cur.fetchall()
    consumethrdct = {}
    for consume in consumethrlsr:
        if consume[1][:2] in ['06','08', '07', '09']:
            if consumethrdct.has_key(consume[0]):
                consumethrdct[consume[0]].append(consume[1])
            else:
                consumethrdct[consume[0]] = [consume[1]]
        
    print consumethrdct
    consumeavgdct = {}
    for key in consumethrdct.iterkeys():
        length = len(consumethrdct[key])
        tot = 0
        for num in consumethrdct[key]:
            tot += int(num[1:])
        consumeavgdct[key] = float(tot)/length
    print consumeavgdct
    non = []
    for i in xrange(1, 92):
        if not consumethrdct.has_key(i):
            non.append(i)
    consumeravgdc = {}
    consumeavlsr = []
    for key in consumeavgdct.iterkeys():
        consumeravgdc[consumeavgdct[key]] = key
        consumeavlsr.append(consumeavgdct[key])
    print consumeravgdc
    consumeavlsr.sort()
    scorert = []
    for con in consumeavlsr:
        scorert.append(consumeravgdc[con])
    for n in non:
        scorert.insert(random.randint(0, len(scorert)-1), n)
    print scorert
    print len(scorert)
    lstdct = {}
    j = 1
    for scr in scorert:
        lstdct[scr] = j
        j += 1
    scorerts = []
    for i in xrange(1, 92):
        scorerts.append(str(lstdct[i]) + '\n') 
    scorearff.writelines(scorerts)
    scorearff.close()
    conn.close()
    
except Exception as e:
    
    scorearff.close()
    conn.close()
    print e
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    