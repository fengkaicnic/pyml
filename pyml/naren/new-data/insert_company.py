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

path = 'd:/naren/new-data/positions/'
company_lst = []

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

    for name in os.listdir(path):
        with open(path + name) as file:
            lines = file.readlines()
            com_dct = eval(''.join(lines))
            com_dct['flag'] = 'new'
            company_lst.append(com_dct)

    table_sql = 'select column_name, data_type from information_schema.columns where table_schema="naren" and table_name="company"'
    cur.execute(table_sql)
    rst = cur.fetchall()

    for company in company_lst:
        insertsql = ['insert into company(']
        valuesql = [' values(']
        valuelst = []
        for item in rst[1:]:
            insertsql.append(item[0])
            insertsql.append(',')
            if item[1] == 'int':
                valuesql.append('%d')
                if company[item[0]] == '':
                    valuelst.append(0)
                else:
                    valuelst.append(int(company[item[0]]))
            else:
                valuesql.append('"%s"')
                valuelst.append(str(company[item[0]]).replace('"', '“'))
            valuesql.append(',')
        insertsql.pop()
        insertsql.append(')')
        valuesql.pop()
        valuesql.append(')')
        allsql = insertsql + valuesql
        # pdb.set_trace()
        sql = ''.join(allsql) % tuple(valuelst)
        # print sql
        # insert_sql = 'insert into company(position_id, unit_id,position_name, new_count, low_income, high_income, \
        #         bonus, pic_id, last_time, trade, level,strength, benefit, expdate, qualification, low_workage,\
        #          high_workage, low_age, high_age, first_language,first_language_level, second_language, second_language_level, sex, \
        #         constellation, latitude, longitude, citynum, worklocation, \
        #         workingtime, publish_time, closing_time, admin_user_id, picname, \
        #         state, autoqa, bole_user_id, position_type, total_match_count, school, education, \
        #         position_score, workproperty, description text, position_type1, position_mode, \
        #         jiazhiguan, zhiyexingge, zhiyexingqu, basic_score, \
        #         forward_emails, applier_trade, create_time, last_access_time, \
        #         to_handle_count, edit_time, naren_created, update_flag, score_setting, \
        #         createtime, position_source, auto_forward_emails, dontsendmail, \
        #         total_resume_count) values()'
        cur.execute(sql)
    conn.commit()
    conn.close()

except Exception as e:
    traceback.print_exc()
    conn.close()
    print e