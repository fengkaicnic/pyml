#coding:utf8
import sys
from DBUtils import PersistentDB
reload(sys)
import MySQLdb

import pdb

sys.setdefaultencoding='utf8'


# persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
#                                     passwd='123456', db='fkmodel', charset='utf8')

persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
                                    passwd='8e1c7d52557b', db='fkmodel', charset='utf8')



if __name__ == '__main__':
    conn = persist.connection()
    cur = conn.cursor()
    sql = 'select * from pos_resume where pos_id = 1122334 and resume_id = 3322115'
    cur.execute(sql)
    rst = cur.fetchall()
    print not rst
    print rst
