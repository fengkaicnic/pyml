#coding:utf8

import os
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import utils
import json
import traceback
import pdb

path_confirm = 'd:/naren/data/confirm/'
path_read = 'd:/naren/data/read/'
path_recommend = 'd:/naren/data/recommend/'

base_path = path_recommend

def get_resume(cur, fname):
    resume_id = fname.split('-')[1].split('.')[0]
    sql = 'select id from profile where resume_id = %d' % int(resume_id)
    cur.execute(sql)
    rst = cur.fetchall()
    if len(rst) == 0:
        return True
    else:
        return False


try:
    num = 0
    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    mode = re.compile(r'\d+')
    with open('d:/naren/data/search.json') as file:
        lines = file.readlines()
        company_lst = eval(''.join(lines))

    table_sql = 'select column_name, data_type from information_schema.columns where table_schema="naren" and table_name="profile"'
    cur.execute(table_sql)
    rst = cur.fetchall()

    for fname in os.listdir(base_path):
        insertsql = ['insert into profile(']
        valuesql = [' values(']
        valuelst = []
        with open(base_path + fname, 'r') as file:
            fobj = json.load(file)
            fobj['readflag'] = 1
            fobj['confirm'] = 0
            fobj['recommend'] = 0
            fobj['pos_id'] = int(fname.split('-')[0])
            fobj['flag'] = 'old'

        for item in rst[1:]:
            insertsql.append(item[0])
            insertsql.append(',')
            if item[1] == 'int':
                valuesql.append('%d')
                if fobj[item[0]] == '':
                    valuelst.append(0)
                else:
                    valuelst.append(int(fobj[item[0]]))
            else:
                valuesql.append('"%s"')
                valuelst.append(str(fobj[item[0]]).replace('"', '“').replace('\'', '‘'))
            valuesql.append(',')
        insertsql.pop()
        insertsql.append(')')
        valuesql.pop()
        valuesql.append(')')
        allsql = insertsql + valuesql
        # pdb.set_trace()
        sql = ''.join(allsql) % tuple(valuelst)
        try:
            cur.execute(sql)
        except:
            num += 1
    conn.commit()
    conn.close()
    print num
except Exception as e:
    pdb.set_trace()
    traceback.print_exc()
    conn.close()
    print e