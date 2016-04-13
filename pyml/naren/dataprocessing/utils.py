#coding:utf8
import sys
from DBUtils import PersistentDB
reload(sys)
import MySQLdb

sys.setdefaultencoding='utf8'


persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
                                    passwd='123456', db='naren', charset='utf8')


