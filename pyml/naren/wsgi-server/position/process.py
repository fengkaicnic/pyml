#coding:utf8
import datetime
import utils
import sys
import traceback
import re
reload(sys)
import time
import pdb
sys.setdefaultencoding('utf8')

start = time.time()

def generate_work_year(cur):
    sql = 'select distinct(resume_id) from profile'
    cur.execute(sql)
    resume_lst = cur.fetchall()
    for rid in resume_lst:
        sql_r = 'select min(start_time), max(end_time) from work where resume_id = %d' % rid[0]
        cur.execute(sql_r)
        rst = cur.fetchall()
        # pdb.set_trace()
        start_t = rst[0][0]
        if not start_t:
            start_tm = datetime.datetime.now()
        else:
            start_tm = time.strptime(start_t, '%Y-%m-%d')
            start_tm = datetime.datetime(start_tm.tm_year, start_tm.tm_mon, start_tm.tm_mday)
        # end_t = rst[0][1]
        end_tm = datetime.datetime.now()
        # end_tm = time.strptime(end_t, '%Y-%m-%d')
        # end_tm = datetime.datetime(end_tm.tm_year, end_tm.tm_mon, end_tm.tm_mday)
        work_age = round((end_tm - start_tm).days/365.0)
        sql_w = 'update profile set workage = %d where resume_id = %d' % (int(work_age), rid[0])
        cur.execute(sql_w)


def generate_com_degree(cur):
    degreep = re.compile(u'(..)以上学历')
    sql = 'select id, description from company'
    cur.execute(sql)
    rst = cur.fetchall()
    for rs in rst:
        degree = degreep.search(rs[1])
        if degree:
            print degree.group(0)
            if '科' in degree.group(0) or '学' in degree.group(0):
                school_degree = 1
            elif '硕' in degree.group(0) or '士' in degree.group(0):
                school_degree = 2
            else:
                school_degree = 0
        else:
            print '1'
            school_degree = 0

        sql_d = 'update company set degree = %d where id = %d' % (school_degree, rs[0])
        cur.execute(sql_d)


def generate_com_workage(cur):
    workp = re.compile(u'(..)年以上')
    year_dct = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, '一':1, '二':2, '两':2, '三':3,\
                '五':5, '四':4, '六':6, '七':7, '八':8, '九':9}
    workagep = re.compile('\d')
    sql = 'select id, description from company'
    cur.execute(sql)
    rst = cur.fetchall()
    for rs in rst:
        work_year = 0
        workye = workp.search(rs[1])
        if workye:
            for key in year_dct.keys():
                if str(key) in workye.group(0):
                    work_year = year_dct[key]
            if work_year == 0:
                work_year = 1
        else:
            work_year = 0
            print '1'
        if workye:
            print workye.group(0), str(work_year)

        sql_w = 'update company set workage = %d where id = %d' % (work_year, rs[0])
        cur.execute(sql_w)

def generate_degree(cur):
    degree_dct = {'本':1, '硕':2, '博':2}
    sql = 'select distinct(resume_id) from profile'
    cur.execute(sql)
    dg_rst = cur.fetchall()
    for rs in dg_rst:
        degree = 0
        sql_d = 'select distinct(degree) from education where resume_id = %d' % rs[0]
        cur.execute(sql_d)
        degst = cur.fetchall()
        for deg in degst:
            for key in degree_dct.keys():
                if key in deg[0]:
                    if degree_dct[key] > degree:
                        degree = degree_dct[key]
        sql_ud = 'update profile set degree = %d where resume_id = %d' % (degree, rs[0])
        cur.execute(sql_ud)


try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()

    # generate_work_year(cur)
    generate_com_degree(cur)
    generate_com_workage(cur)
    # generate_degree(cur)

    conn.commit()
    conn.close()

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print (end - start)