#coding:utf8
import sys
from DBUtils import PersistentDB
reload(sys)
import MySQLdb
import pdb

sys.setdefaultencoding='utf8'


persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
                                    passwd='123456', db='test', charset='utf8')


# 
# with open('d:/tianchi/last_two_week_adjust_four.csv', 'r') as file:
#     lines = file.readlines()
# 
# resultlst = []
# pdb.set_trace()
# for line in lines:
#     print line.replace('\x00', '')
#     line = line.strip()
#     resultlst.append(line.replace('\x00', ''))
#     
# with open('d:/tianchi/last_two_week_adjust_four.csv', 'wb') as file:
#     file.writelines('\n'.join(resultlst))
