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

        try:

            sql = '''insert into mail_profile(gender, latesttitle, latestcollege, selfappraise, latestcompany,\
                latestdegree, curemploystatus, dessalary, age, desworkproperty, destitle, \
                desindustry, desworklocation, position_id, resume_id) values("%s", "%s", "%s", "%s", "%s", "%s", "%s",\
                "%s", %d, "%s", "%s", "%s", "%s", %d, %d)''' % (resume['sex'], resume['latesttitle'], \
                resume['latestcollege'], resume['selfappraise'], resume['latestcompany'], resume['latestdegree'],\
                resume['curemploystatus'], resume['dessalary'], resume.get('age', 100), resume['desworkproperty'], \
                resume['destitle'], resume['desindustry'], resume['desworklocation'], \
                int(position['position_distinct_id']), int(resume['resume_id']))

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