#coding:utf8
import utils
import traceback
import jieba

try:
    sql = 'select description, low_workage, id, high_workage from company where low_workage = 0'
    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    count = 0
    for rs in rst:
        desc = rs[0]
        seglst = desc.split('\n')
        # seglst = jieba.cut(desc, cut_all=False)
        for seg in seglst:
            if u'年以上' in seg:
                index = seg.index(u'年以上')
                count += 1
                print seg[index-1:index+3]
        print rs[1], rs[2], rs[3], '========'

    print len(rst)
    print count

except:
    traceback.print_exc()
