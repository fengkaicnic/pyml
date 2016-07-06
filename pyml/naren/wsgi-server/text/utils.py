#coding:utf8
import sys
from DBUtils import PersistentDB
import traceback

import pdb
reload(sys)
import MySQLdb

sys.setdefaultencoding='utf8'


# persist = PersistentDB.PersistentDB(MySQLdb, host='127.0.0.1', port=3306, user='root',\
#                                     passwd='123456', db='fkmodel', charset='utf8')

persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
                                    passwd='8e1c7d52557b', db='fkmodel', charset='utf8')


digitlst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


def discrement_unicode(stw):
    try:
        stw = stw.replace(u'\u201c', "'")
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

def convert_code(com_lines):
    com_lines = com_lines.replace('": "', "''':'''")
    com_lines = com_lines.replace("': '", "''':'''")
    com_lines = com_lines.replace('"], "', "'''],'''")
    com_lines = com_lines.replace("'], '", "'''],'''")
    com_lines = com_lines.replace('", "', "''','''")
    com_lines = com_lines.replace("', '", "''','''")
    com_lines = com_lines.replace(', "', ",'''")
    com_lines = com_lines.replace(", '", ",'''")
    com_lines = com_lines.replace('": {"', "''':{'''")
    com_lines = com_lines.replace("': {'", "''':{'''")
    com_lines = com_lines.replace('": [{"', "''':[{'''")
    com_lines = com_lines.replace("': [{'", "''':[{'''")
    com_lines = com_lines.replace('"}], "', "'''}],'''")
    com_lines = com_lines.replace("'}], '", "'''}],'''")
    com_lines = com_lines.replace('": ["', "''':['''")
    com_lines = com_lines.replace("': ['", "''':['''")
    com_lines = com_lines.replace('"}', "'''}")
    com_lines = com_lines.replace("'}", "'''}")
    com_lines = com_lines.replace('":', "''':")
    com_lines = com_lines.replace("':", "''':")
    com_lines = com_lines.replace('{"', "{'''")
    com_lines = com_lines.replace("{'", "{'''")
    com_lines = com_lines.replace("'''''", "'''''''")
    com_lines = com_lines.replace("'''''''", "'''")
    com_lines = com_lines.replace("''''''''", "''''''")
    com_lines = com_lines.replace(u"”,'''", u"”，“")

    com_lines = com_lines.replace('"', u'“')
    com_lines = com_lines.replace('\\', '/')

    return com_lines
