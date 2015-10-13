import os

import MySQLdb
try:
    scorearff = open('d:/student/studentall.arff', 'w+')
    scorearff.write("@relation student\n")
    scorearff.write('@attribute xuehao numeric\n')
    scorearff.write('@attribute paimingone numeric\n')
    scorearff.write('@attribute paimingtwo numeric\n')
    scorearff.write('@attribute paimingthe numeric\n')
    scorearff.write('@data\n')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='student')
    cur = conn.cursor()
    scoresql = 'select xuehao, group_concat(paiming order by xueqi) from score group by xuehao'
    scoretol = cur.execute(scoresql)
    scorelsr = cur.fetchall()
    scoredct = {}
    scoretoarf = []
    for score in scorelsr:
        scoretoarf.append(str(score[0]) + ',' + score[1] + '\n')
    scorearff.writelines(scoretoarf)

    scorearff.close()
    conn.close()
    
except Exception as e:
    
    scorearff.close()
    conn.close()
    print e
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    