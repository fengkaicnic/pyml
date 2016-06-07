#coding:utf8
import utils
import traceback
import jieba

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select latesttitle from profile'
    cur.execute(sql)
    rst = cur.fetchall()
    worddct= {}
    for rs in rst:
        seglst = jieba.cut(rs[0].lower(), cut_all=False)
        for seg in seglst:
            if not worddct.has_key(seg):
                worddct[seg] = 1
            else:
                worddct[seg] += 1

    print len(worddct)

    # for key in worddct.keys():
    #     print key, worddct[key]

    wordlst = sorted(worddct.items(), key=lambda x:x[1])

    for word in wordlst:
        print word[0], word[1]

    conn.close()
except:
    traceback.print_exc()
    conn.close()
