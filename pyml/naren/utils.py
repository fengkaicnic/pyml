#coding:utf8
import sys
from DBUtils import PersistentDB

reload(sys)
import MySQLdb
import datetime
import traceback
import pdb

sys.setdefaultencoding='utf8'


# persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
#                                     passwd='123456', db='naren', charset='utf8')


persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
                                    passwd='8e1c7d52557b', db='fkmodel', charset='utf8')

company_lst = []

def get_company(cur):
    sqlcom = 'select name from company_name'
    cur.execute(sqlcom)
    comrt = cur.fetchall()
    for rs in comrt:
        company_lst.append(rs[0])

def get_work_feature(cur, resume_id):

    if not company_lst:
        get_company(cur)

    sqlw = 'select unit_name, start_time, end_time from work where resume_id = "%s"' % resume_id
    features = [0 for i in range(16)]
    cur.execute(sqlw)
    rst = cur.fetchall()

    stfp1 = '%Y-%m-%d'
    stfp2 = '%Y/%m'

    for index, rs in enumerate(rst):
        # pdb.set_trace()
        for name in company_lst:
            if name in rs[0].replace(u'北京', ''):
                features[index*2] = 1
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
            features[index*2+1] = days/30 + 1
        except:
            traceback.print_exc()

    return features

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
