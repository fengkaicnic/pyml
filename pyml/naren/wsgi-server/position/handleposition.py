#coding:utf8

import os
import json
import re
import utils
import json
import traceback
from nanabase import baseutil as nautil
import pdb


def get_resume(cur, fname):
    resume_id = fname.split('-')[1].split('.')[0]
    sql = 'select id from profile where resume_id = %d' % int(resume_id)
    cur.execute(sql)
    rst = cur.fetchall()
    if len(rst) == 0:
        return True
    else:
        return False

def insert_company(fobj, database, type=None, tablename='company'):
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

        check_p = 'select id from %s where position_id = %d' % (tablename, int(fobj['position_id']))
        cur.execute(check_p)
        rst = cur.fetchall()

        if not rst:
            table_sql = 'select column_name, data_type from information_schema.columns where table_schema="%s" and table_name="%s"' % (database, tablename)
            cur.execute(table_sql)
            rst = cur.fetchall()

            fobj['type'] = type
            fobj['degree'] = 0
            fobj['workage'] = 0

            insertsql = ['insert into %s(' % tablename]
            valuesql = [' values(']
            valuelst = []

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
                    # pdb.set_trace()
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
            except Exception as e:
                traceback.print_exc()
                nautil.dlog.exception('ModelTrainHandler')
                num += 1
                raise e
            conn.commit()
            conn.close()
            print num
    except Exception as e:
        # pdb.set_trace()
        traceback.print_exc()
        conn.close()
        nautil.dlog.exception('ModelTrainHandler')
        raise e
