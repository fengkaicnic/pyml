#coding:utf8
import utils
import traceback

try:
    conn = utils.persist.connection()
    cur = conn.cursor()

    resume_id = '10898194-2'

    sql = 'select resumekeywords, dessalary, latestmajor, latestcollege,\
            latestdegree, workyear, latestcompany, latesttitle from profile where \
             resume_id = "%s"' % resume_id

    cur.execute(sql)
    rst = cur.fetchall()

    for rs in rst:
        for tem in rs:
            print utils.discrement_unicode(tem)

    sql = 'select start_time, end_time, position_name, description from work where\
                                      resume_id = "%s"' % resume_id

    cur.execute(sql)
    rst = cur.fetchall()
    for rs in rst:
        for tem in rs:
            print utils.discrement_unicode(tem)

    conn.close()
except:
    traceback.print_exc()
    conn.close()
