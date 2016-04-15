#coding:utf8

import os
import json
import re
import utils
import json
import traceback
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

def insert_position_resume(cur, pos_id, resume_id):
    try:
        prsql = 'insert into pos_resume(pos_id, resume_id) values(%d, %d)' % (int(pos_id), int(resume_id))
        cur.execute(prsql)

    except Exception as e:
        # pdb.set_trace()
        traceback.print_exc()
        print e

def update_position_resume(cur, body):
    try:
        pos_id = body['pos_id']
        resume_id = body['resume_id']
        confirm = body['confirm']
        up_sql = 'update pos_resume set %s = 1 where pos_id = %d \
                  and resume_id = %d' % (confirm, pos_id, resume_id)
        cur.execute(up_sql)
    except:
        traceback.print_exc()

def insert_education(cur, content):
    table_sql = 'select column_name, data_type from information_schema.columns where table_schema="wsgiserver" and table_name="education"'
    cur.execute(table_sql)
    rst = cur.fetchall()

    fobjlst = eval(content['education_history'])

    for fobj in fobjlst:
        insertsql = ['insert into education(']
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
            # pdb.set_trace()
            traceback.print_exc()

def insert_work(cur, content):
    table_sql = 'select column_name, data_type from information_schema.columns where table_schema="wsgiserver" and table_name="work"'
    cur.execute(table_sql)
    rst = cur.fetchall()

    fobjlst = eval(content['work_history'])

    for fobj in fobjlst:
        insertsql = ['insert into work(']
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
                valuesql.append('"%s"')
                valuelst.append(str(fobj[item[0]]).replace('"', '“').replace('\'', '‘'))
            valuesql.append(',')
        insertsql.pop()
        insertsql.append(')')
        valuesql.pop()
        valuesql.append(')')
        allsql = insertsql + valuesql
        sql = ''.join(allsql) % tuple(valuelst)
        try:
            cur.execute(sql)
        except:
            traceback.print_exc()

def insert_profile(fobj, pos_id=None):
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

        resume_id = fobj['resume_id']

        check_r = 'select id from profile where resume_id = %d' % int(resume_id)

        cur.execute(check_r)
        rst = cur.fetchall()
        if len(rst) == 0:
            table_sql = 'select column_name, data_type from information_schema.columns where table_schema="wsgiserver" and table_name="profile"'
            cur.execute(table_sql)
            rst = cur.fetchall()

            insertsql = ['insert into profile(']
            valuesql = [' values(']
            valuelst = []

            fobj['readflag'] = 1
            fobj['confirm'] = 0
            fobj['pos_id'] = 0
            fobj['recommend'] = 0

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
                # pdb.set_trace()
                traceback.print_exc()
            # pdb.set_trace()
            insert_education(cur, fobj)
            insert_work(cur, fobj)
        if pos_id:
            insert_position_resume(cur, pos_id, resume_id)
        conn.commit()
        conn.close()
    except Exception as e:
        # pdb.set_trace()
        traceback.print_exc()
        conn.close()
        print e

def update_profile(body):
    conn = utils.persist.connection()
    cur = conn.cursor()

    pos_id = body['pos_id']
    resume_id = body['resume_id']
    flag = body['confirm']

    update_sql = 'update pos_resume set %s = 1 where pos_id = %d and resume_id = %d'\
                 % (flag, int(pos_id), int(resume_id))

    cur.execute(update_sql)
    conn.commit()
    conn.close()
