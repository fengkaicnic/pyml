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
    path = 'd:/naren/recommend/email_log1/'
    for fle in os.listdir(path):
        with open(path + fle, 'r') as file:
            lines = file.readline()
        com_lines = ''.join(lines).decode('unicode_escape').replace('null', "''").replace('\n', '')

        com_lines = com_lines.replace('": "', "''':'''")
        com_lines = com_lines.replace('"], "', "'''],'''")
        com_lines = com_lines.replace('", "', "''','''")
        com_lines = com_lines.replace(', "', ",'''")
        com_lines = com_lines.replace('": {"', "''':{'''")
        com_lines = com_lines.replace('": [{"', "''':[{'''")
        com_lines = com_lines.replace('"}], "', "'''}],'''")
        com_lines = com_lines.replace('": ["', "''':['''")
        com_lines = com_lines.replace('"}', "'''}")
        com_lines = com_lines.replace('":', "''':")
        com_lines = com_lines.replace('{"', "{'''")

        com_lines = com_lines.replace('"', '“')

        com_pro_inf = eval(com_lines)
        position = com_pro_inf['position']
        sql = '''insert into mail_company(position_name, low_workage, low_income, high_income, description, position_id)\
              values("%s", "%s", "%s", "%s", "%s", %d)''' % (position['name'].replace('"', '“'), position['low_workage'], \
              position['low_income'], position['high_income'], position['description'].replace('"', '“'), position['position_distinct_id'])
        try:
            cur.execute(sql)
        except:
            pdb.set_trace()
            traceback.print_exc()
    conn.commit()
    conn.close()

except Exception as e:
    pdb.set_trace()
    traceback.print_exc()
    conn.close()
    print e