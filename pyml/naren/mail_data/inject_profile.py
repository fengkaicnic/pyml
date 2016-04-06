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
    path = 'd:/naren/recommend/email_log/'
    for fle in os.listdir(path):
        with open(path + fle, 'r') as file:
            lines = file.readline()
        com_pro_inf = eval(''.join(lines).replace('null', "''"))
        resume = com_pro_inf['resume']
        position = com_pro_inf['position']

        sql = '''insert into mail_profile(gender, latesttitle, latestcollege, selfappraise, latestcompany,\
                latestdegree, curemploystatus, dessalary, age, desworkproperty, destitle, \
                desindustry, desworklocation, position_id) values("%s", "%s", "%s", "%s", "%s", "%s", "%s",\
                "%s", %d, "%s", "%s", "%s", "%s", "%s")''' % (resume['sex'], resume['latesttitle'], \
                resume['latestcollege'], resume['selfappraise'], resume['latestcompany'], resume['latestdegree'],\
                resume['curemploystatus'], resume['dessalary'], resume['age'], resume['desworkproperty'], \
                resume['destitle'], resume['desindustry'], resume['desworklocation'], position['position_j51_id'])
        try:
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