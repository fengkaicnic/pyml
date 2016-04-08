#coding:utf8

import os
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import utils
import traceback
import pdb
import time

start = time.time()


try:

    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    mode = re.compile(r'\d+')
    with open('d:/tianchi/cainiao/item_store_feature1.csv') as file:
        lines = file.readlines()

    table_sql = 'select column_name, data_type from information_schema.columns where \
                  table_schema="test" and table_name="item_store_feature" and column_name != "id"'
    cur.execute(table_sql)
    rst = cur.fetchall()


    for line in lines:
        insertsql = ['insert into item_store_feature(']
        valuesql = [' values(']
        valuelst = line.split(',')
        valuelst = map(lambda x: x.strip(), valuelst)
        for index, term in enumerate(rst):
            insertsql.append(term[0])
            insertsql.append(',')
            if term[1] == 'int':
                valuesql.append('%d')
                valuelst[index] = int(valuelst[index])
            elif term[1] == 'float':
                valuesql.append('%f')
                valuelst[index] = float(valuelst[index])
            else:
                valuesql.append('"%s"')
            valuesql.append(',')

        insertsql.pop()
        insertsql.append(')')
        valuesql.pop()
        valuesql.append(')')

        allsql = insertsql + valuesql
        # pdb.set_trace()
        sql = ''.join(allsql) % tuple(valuelst)

        cur.execute(sql)

    conn.commit()
    conn.close()


except Exception as e:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
    print e

end = time.time()
print (end - start)