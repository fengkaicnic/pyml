#coding:utf8
import sys
from DBUtils import PersistentDB
reload(sys)
import MySQLdb

sys.setdefaultencoding='utf8'


persist = PersistentDB.PersistentDB(MySQLdb, host='localhost', port=3306, user='root',\
                                    passwd='mysql', db='test', charset='utf8')

