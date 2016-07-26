#coding:utf8
import sys
from DBUtils import PersistentDB
reload(sys)
import MySQLdb
import ConfigParser

import pdb

sys.setdefaultencoding='utf8'

cf = ConfigParser.ConfigParser()

cf.read('database.ini')
host = cf.get('database', 'host')
port = cf.get('database', 'port')
user = cf.get('database', 'user')
db = cf.get('database', 'db')
passwd = cf.get('database', 'passwd')

persist = PersistentDB.PersistentDB(MySQLdb, host=host, port=int(port), user=user,\
                                    passwd=passwd, db=db, charset='utf8')

# persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
#                                     passwd='8e1c7d52557b', db='fkmodel', charset='utf8')

digitlst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
def discrement_unicode(stw):
    try:
        strs = stw.replace('u', '\u')
    except:
        return stw
    sls = strs.split('\\')
    change = 0
    for index, sl in enumerate(sls):
        flag = True
        if len(sl) < 5:
            flag = False
        # pdb.set_trace()
        for s in sl[1:5]:
            if not s in digitlst:
                flag = False

        if flag:
            sls[index] = '\\' + sls[index]
            change = 1

    if change:
        # sls = filter(lambda x:len(x) < 7, sls)
        return ''.join(sls).decode('unicode-escape')


    return stw


if __name__ == '__main__':
    conn = persist.connection()
    cur = conn.cursor()
    sql = 'select * from pos_resume where pos_id = 1122334 and resume_id = 3322115'
    cur.execute(sql)
    rst = cur.fetchall()
    print not rst
    print rst
