#coding:utf8
import sys
import os
import utils
reload(sys)
import json
import time
import pdb
sys.setdefaultencoding('utf8')
import traceback

start = time.time()

path_confirm = 'd:/naren/data/confirm/'
path_read = 'd:/naren/data/read/'
path_recommend = 'd:/naren/data/recommend/'

base_path = path_read

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

    table_sql = 'select column_name, data_type from information_schema.columns where table_schema="naren" and table_name="education"'
    cur.execute(table_sql)
    rst = cur.fetchall()

    for fname in os.listdir(base_path):
        with open(base_path + fname, 'r') as file:
            content = json.load(file)
            fobjlst = eval(content['education_history'])

        for fobj in fobjlst:
            insertsql = ['insert into education(']
            valuesql = [' values(']
            valuelst = []
            fobj['readflag'] = 0
            fobj['confirm'] = 1
            fobj['recommend'] = 0
            fobj['pos_id'] = int(fname.split('-')[0])

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
                pdb.set_trace()
                num += 1
    conn.commit()
    conn.close()
    print num
except Exception as e:
    pdb.set_trace()
    traceback.print_exc()
    conn.close()
    print e

end = time.time()

print (end - start)