#coding:utf8
import sys
from DBUtils import PersistentDB
reload(sys)
import MySQLdb

sys.setdefaultencoding='utf8'

import ConfigParser

cf = ConfigParser.ConfigParser()

cf.read('database.ini')
host = cf.get('database', 'host')
port = cf.get('database', 'port')
user = cf.get('database', 'user')
db = cf.get('database', 'db')
passwd = cf.get('database', 'passwd')

persist = PersistentDB.PersistentDB(MySQLdb, host=host, port=int(port), user=user,\
                                    passwd=passwd, db=db, charset='utf8')


# persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
#                                     passwd='123456', db='fkmodelt', charset='utf8')

# persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
#                                     passwd='8e1c7d52557b', db='fkmodel', charset='utf8')
