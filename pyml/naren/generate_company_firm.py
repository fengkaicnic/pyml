#coding:utf8
import sys
import time
import utils
reload(sys)
import pdb
import os
import traceback

sys.setdefaultencoding('utf8')

start = time.time()

CONFIRM = 0

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
    sql = 'select pos_id, resume_id from profile where recommend = 1 and confirm = %d limit 5' % CONFIRM
    cur.execute(sql)
    rst = cur.fetchall()

    num = 0
    for item in rst:
        sql2 = 'select description, position_name from company where position_id = %d' % item[0]
        cur.execute(sql2)
        pos_desc = cur.fetchall()
        sql3 = 'select hisprojects, skills from profile where resume_id = %d' % item[1]
        cur.execute(sql3)
        profiles = cur.fetchall()
        sql5 = 'select description, start_time, end_time from work where resume_id = %d' % item[1]
        cur.execute(sql5)
        works = cur.fetchall()
        if CONFIRM:
            path = 'd:/naren/recommend/test/' + '-'.join([str(item[0]), str(item[1])])
        else:
            path = 'd:/naren/recommend/test/' + '-'.join([str(item[0]), str(item[1]), 'un'])
        with open(path, 'wb') as file:
            file.writelines('*' * 20 + 'position description' + '*' * 20 + '\n')
            file.writelines('position_name:' + pos_desc[0][1].decode('utf8').encode('gbk') + '\n')
            file.writelines(pos_desc[0][0].decode('utf8').encode('gbk') + '\n')
            file.writelines('*' * 20 + 'hisprojects description' + '*' * 20 + '\n')
            # pdb.set_trace()
            if item[1] == 4753813:
                pdb.set_trace()
            for profile in profiles:
                file.writelines(profile[1].decode('utf8').encode('gbk') + '\n')
                pro = profile[0].replace('“: “', "''':'''")
                pro = pro.replace('{“', "{'''")
                pro = pro.replace('“, “', "''','''")
                pro = pro.replace('“}', "'''}")
                pro = pro.replace('“: [“', "''':['''")
                pro = pro.replace('“: ]“', "''':]'''")
                pro = pro.replace('“]}', "''']}")
                pro = pro.replace('“], “', "'''],'''")

                try:
                    profilelst = eval(pro)
                    if profilelst:

                        for profile in profilelst:
                            for key in profile.keys():
                                file.writelines(key.decode('utf8').encode('gbk') + ':' + profile[key].decode('utf8').encode('gbk') + '\n')
                except:
                    num += 1
                    continue
            for work in works:
                file.writelines('*' * 20 + 'work description' + '*' * 20 + '\n')
                file.writelines('start_time:' + work[1].decode('utf8').encode('gbk') + '\n')
                file.writelines('start_time:' + work[2].decode('utf8').encode('gbk') + '\n')
                file.writelines(work[0].decode('utf8').encode('gbk') + '\n')

except Exception as e:
    pdb.set_trace()
    traceback.print_exc()
    conn.close()
    print e

end = time.time()

print num

print (end - start)
