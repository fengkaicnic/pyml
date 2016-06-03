#coding:utf8
import utils
import traceback
import pdb
import time

tm = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select resume_id, hisprojects, id from profile where id > 810312 order by id limit 1000'
    cur.execute(sql)
    rst = cur.fetchall()
    # pdb.set_trace()
    for rs in rst:
        print rs[2]
        if rs[1] == '[]' or not rs[1]:
            continue
        # rsff3 = rs[1].replace(u'\u201c', '"')
        # rsff2 = rsff3.replace('\n', '')
        # rsff3 = utils.discrement_unicode(rs[1])
        # pdb.set_trace()
        rsff3 = rs[1].replace('\n', '')

        rsff3 = rsff3.replace(u'\u201c', '"')
        rsff3 = rsff3.replace(u'\u2018', '')
        rsff3 = utils.discrement_unicode(rsff3)
        rsff2 = utils.convert_code(rsff3)
        rsff = eval(rsff2)
        # pdb.set_trace()
        for rsf in rsff:
            for key in rsf.keys():
                rsf[key.decode('utf8')] = rsf[key].decode('utf8')
                # rsf.pop(key)
        for rsf in rsff:
            sql = 'insert into projects(name, start, end, description, resume_id, software,\
                    hardware, developtool, dudescription) values("%s", "%s", "%s", "%s", "%s", "%s",\
                     "%s", "%s", "%s")' % (rsf.get('name', ''), rsf.get('start_time', ''), rsf.get('end_time', ''),\
                    rsf.get(u'项目描述', ''), rs[0], rsf.get(u'软件环境', ''), rsf.get(u'硬件环境', ''), \
                        rsf.get(u'开发工具', ''), rsf.get(u'责任描述', ''))

            cur.execute(sql)

    conn.commit()

    conn.close()
except:
    pdb.set_trace()
    conn.commit()
    traceback.print_exc()
    conn.close()

em = time.time()

print em - tm
