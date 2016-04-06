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

        resume = com_pro_inf['resume']
        position = com_pro_inf['position']
        workexperience = resume['work_experience']
        for experience in workexperience:
            try:
                sql = '''insert into mail_work(wage, unit_name, scale, description, start_time, \
                    trade, position_name, unittype, end_time, department, resume_id, pos_id) values("%s","%s",\
                    "%s", "%s", "%s", "%s","%s","%s","%s","%s", %d, %d)''' % (experience['wage'], \
                    experience['unit_name'], experience['scale'], experience['description'], experience['start_time'], \
                    experience['trade'], experience['position_name'], experience['unittype'], experience['end_time'], \
                    experience['department'], int(resume['resume_id']), int(position['position_distinct_id']))


                cur.execute(sql)
            except:
                pdb.set_trace()
                traceback.print_exc()
    conn.commit()
    conn.close()

except Exception as e:
    traceback.print_exc()
    conn.close()
    print e