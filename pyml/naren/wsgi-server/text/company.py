#coding:utf8
import utils
import sys
import traceback
reload(sys)
import pdb
sys.setdefaultencoding('utf8')

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    with open('d:/naren/company/company.txt', 'r') as file:
        lines = file.readlines()

    pdb.set_trace()
    for line in lines:
        sql = 'insert into company_name(name) values("%s")' % line.strip().decode('gbk')
        cur.execute(sql)

    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    conn.commit()
    conn.close()
