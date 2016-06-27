#coding:utf8
import sys
from DBUtils import PersistentDB

reload(sys)
import MySQLdb
import datetime
import traceback

sys.setdefaultencoding='utf8'


# persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
#                                     passwd='123456', db='naren', charset='utf8')


persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
                                    passwd='8e1c7d52557b', db='fkmodel', charset='utf8')

company_lst = []

def get_work_feature(cur, resume_id):

    if not company_lst:
        sqlcom = 'select name from company_name'
        cur.execute(sqlcom)
        comrt = cur.fetchall()
        for rs in comrt:
            company_lst.append(rs[0])

    sqlw = 'select unit_name, start_time, end_time from work where resume_id = %d' % resume_id
    features = [0 for i in range(10)]
    cur.execute(sqlw)
    rst = cur.fetchall()

    stfp1 = '%Y-%m-%d'
    stfp2 = '%Y/%m'

    for index, rs in enumerate(rst):
        for name in company_lst:
            if name in rs[0].replace(u'北京', ''):
                features[index] = 1
        now_day = datetime.datetime.now()
        try:
            if '-' in rs[1]:
                st = datetime.datetime.strptime(rs[1], stfp1)
            else:
                st = datetime.datetime.strptime(rs[1], stfp2)
            if '-' in rs[2]:
                ed = datetime.datetime.strptime(rs[2], stfp1)
            else:
                ed = datetime.datetime.strptime(rs[2], stfp2)
            days = (ed - st).days

            if not days:
                days = (now_day - st).days
            features[index*2] = days/30 + 1
        except:
            traceback.print_exc()

    return features
