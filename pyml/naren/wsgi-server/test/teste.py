
import utils
import sys
import traceback
reload(sys)
import time
import pdb

start = time.time()

digitlst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

def discrement_unicode(stw):
    strs = stw.replace('u', '\u')
    sls = strs.split('\\')
    change = 0
    for index, sl in enumerate(sls):
        flag = True
        if len(sl) < 5:
            flag = False
        # pdb.set_trace()
        for s in sl[1:5]:
            if not s in digitlst:
                flag = False
        if flag:
            sls[index] = '\\' + sls[index]
            change = 1

    if change:
        return ''.join(sls).decode('unicode-escape')

    return stw


def position_unicode_handle(wordct):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select id, position_name from company'
        cur.execute(sql)
        rst = cur.fetchall()
        # pdb.set_trace()
        for rs in rst:
            # pdb.set_trace()
            rsl = discrement_unicode(rs[1])
            # up_sql = 'update company set position_name = "%s" where id = %d' % (rsl, rs[0])
            # cur.execute(up_sql)
            # print rsl
            for word in wordct:
                try:
                    if word.decode('utf8').lower() in rsl.lower():
                        up_sql = 'update company set type = "%s" where id = %d' % (word, rs[0])
                        cur.execute(up_sql)
                        break
                except:
                    pdb.set_trace()
                    traceback.print_exc()
        conn.commit()
    except:
        traceback.print_exc()


def profile_title():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select latesttitle from profile order by id desc limit 256'
        cur.execute(sql)
        rst = cur.fetchall()

        for rs in rst:
            print discrement_unicode(rs[0])
            # print rs[0]
    except:
        traceback.print_exc()


if __name__ == '__main__':
    stw = 'u9ad8u7ea7u5ba2u6237u4e3bu4efbSeniorAccountExecutive(u5317u4eac)'

    wordct = []

    with open('../dict1.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            # pdb.set_trace()
            wordct.append(line.strip())

    position_unicode_handle(wordct)
    #profile_title()

end = time.time()

print end - start
