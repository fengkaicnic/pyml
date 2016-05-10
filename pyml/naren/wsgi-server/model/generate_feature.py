#coding:utf8
import sys
import time
import utils
reload(sys)
import pdb
import os
import jieba
import re
import traceback
import numpy as np
from collections import Counter
import json

sys.setdefaultencoding('utf8')

start = time.time()

salaryp = re.compile('\d+')

jieba.load_userdict('dict.txt')

education_dct = {'初中及以下':0, '初中':0, '高中':1, '大专':2, '本科':3, '硕士':4, '博士':5, '博士后':6}

keyword_dct = {}
num = 0
with open('dict.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if not keyword_dct.has_key(line.strip().lower().decode('utf8')):
            keyword_dct[line.strip().lower().decode('utf8')] = num
            num += 1

def get_keywords(content):
    keywords = [0 for i in range(len(keyword_dct))]
    seglst = jieba.cut(content, cut_all=False)
    for seg in seglst:
        if keyword_dct.has_key(seg.lower()):
            keywords[keyword_dct[seg.lower()]] += 1

    return keywords

def get_position_feature(com_position, pro_position):
    comseg = jieba.cut(com_position, cut_all=False)
    proseg = jieba.cut(pro_position, cut_all=False)
    com_pos_lst = [seg for seg in comseg]
    total = len(com_pos_lst)
    for seg in proseg:
        if seg in com_pos_lst:
            com_pos_lst.pop(com_pos_lst.index(seg))

    return 1 - len(com_pos_lst) / float(total)

def get_description_feature(com_description, pro_hisprojects, pro_descriptions, pro_otherinfo, skills):

    description_feature = []

    try:
        com_seg = jieba.cut(com_description, cut_all=False)
        comlst = [seg.lower() for seg in com_seg if keyword_dct.has_key(seg.lower())]
        his_seg = jieba.cut(pro_hisprojects, cut_all=False)
        hislst = [seg.lower() for seg in his_seg if keyword_dct.has_key(seg.lower())]
        deslst = []
        for description in pro_descriptions:
            des_seg = jieba.cut(description[0], cut_all=False)
            deslst += [seg.lower() for seg in des_seg if keyword_dct.has_key(seg.lower())]
        oth_seg = jieba.cut(pro_otherinfo, cut_all=False)
        othlst = [seg.lower() for seg in oth_seg if keyword_dct.has_key(seg.lower())]
        feature_lst = []
        pro_dec_lst = hislst + deslst + othlst
        com_count = Counter(comlst)
        pro_count = Counter(pro_dec_lst)
        description_feature.append(len(comlst))
        description_feature.append(len(com_count))
        inter_con = set(com_count.keys()).intersection(set(pro_count.keys()))
        # description_feature.append(len(inter_con))
        description_feature.append(len(inter_con)/float(len(com_count) + 0.001))
        com_inter_num = reduce(lambda x, y:x+y, [com_count[key] for key in inter_con] + [0])
        pro_inter_num = reduce(lambda x, y:x+y, [pro_count[key] for key in inter_con] + [0])
        description_feature.append(float(com_inter_num)/(len(comlst) + 0.001))
        description_feature.append(float(pro_inter_num)/(len(pro_dec_lst)+0.001))

    except:
        pdb.set_trace()
        traceback.print_exc()

    return description_feature


def get_description_feature_old(com_description, pro_hisprojects, pro_descriptions, pro_otherinfo):
    try:
        com_seg = jieba.cut(com_description, cut_all=False)
        comlst = [seg.lower() for seg in com_seg if keyword_dct.has_key(seg.lower())]
        description_feature = [0 for i in range(len(keyword_dct))]
        his_seg = jieba.cut(pro_hisprojects, cut_all=False)
        hislst = [seg.lower() for seg in his_seg if keyword_dct.has_key(seg.lower())]
        deslst = []
        for description in pro_descriptions:
            des_seg = jieba.cut(description[0], cut_all=False)
            deslst += [seg.lower() for seg in des_seg if keyword_dct.has_key(seg.lower())]
        oth_seg = jieba.cut(pro_otherinfo, cut_all=False)
        othlst = [seg.lower() for seg in oth_seg if keyword_dct.has_key(seg.lower())]
        feature_lst = []
        pro_dec_lst = hislst + deslst + othlst
        com_count = Counter(comlst)
        pro_count = Counter(pro_dec_lst)
        for key in com_count.keys():
            description_feature[keyword_dct[key]] = np.exp(pro_count.get(key, 0.0) / float(com_count[key]))

        # for seg in hislst:
        #     if seg in comlst:
        #         description_feature[keyword_dct[seg]] += 1
        # for seg in deslst:
        #     if seg in comlst:
        #         description_feature[keyword_dct[seg]] += 1
        # for seg in othlst:
        #     if seg in comlst:
        #         description_feature[keyword_dct[seg]] += 1
    except:
        pdb.set_trace()
        traceback.print_exc()


    return description_feature


def set_train_flg(cur, pos_id, resume_id):
    setsq = 'update pos_resume set train_flag = 1 where pos_id = %d and resume_id =\
             "%s"' % (pos_id, resume_id)

    cur.execute(setsq)


def get_feature(cur, feature_lines, flag):
    sql = 'select position_id, low_income, description, low_workage, position_name,\
            workage, degree from company'

    cur.execute(sql)
    rst = cur.fetchall()
    nummn = 0
    for term in rst:
        com_low_income = term[1]
        pro_low_income = 0
        com_position = term[4].replace('u', '\u').decode('unicode-escape')
        pro_position = ''
        com_description = term[2].replace('u', '\u').decode('unicode-escape')
        pro_decription = ''
        pro_hisprojects = ''
        pro_otherinfo = ''

        com_lst = []
        if com_low_income < 500 and com_low_income > 0:
            com_low_income = (com_low_income * 8000) / 12
        com_low_income = com_low_income / 5000
        low_workage = term[5]
        if not low_workage:
            low_workage = 0
        com_lst.append(low_workage)
        com_workage = term[5]
        com_degree = term[6]

        keywords = get_keywords(term[2].replace('u', '\u').decode('unicode-escape'))
        com_description = term[2].replace('u', '\u').decode('unicode-escape')

        try:
            sqlp = 'select dessalary, skills, latesttitle, hisprojects, otherinfo, pf.resume_id, workyear, latestdegree, \
                    pr.pos_id, pr.resume_id from pos_resume as pr left join profile as pf on pr.resume_id = pf.resume_id \
                    where pr.train_flag = 0 and pr.pos_id = %d and pr.hr_confirm = %d limit 5' % (term[0], flag)

            cur.execute(sqlp)
            profile = cur.fetchall()
        except:
            pdb.set_trace()
        for pro in profile:
            nummn += 1
            print nummn
            if not pro[0]:
                incomes = salaryp.search('0')
            else:
                incomes = salaryp.search(pro[0])
            try:
                resume_id = pro[5]
                if not resume_id:
                    continue
                pos_sql = 'select position_name from work where resume_id = %d order by end_time desc' % resume_id
                cur.execute(pos_sql)
                pos_rst = cur.fetchall()
                pro_position = pos_rst[0][0].replace('u', '\u').decode('unicode-escape')
            except:
                pro_position = pro[2].replace('u', '\u').decode('unicode-escape')
            if incomes:
                low_income = incomes.group(0)
            else:
                low_income = 0
            pro_low_income = int(low_income) / 5000
            pro_hisprojects = pro[3].replace('u', '\u').decode('unicode-escape')
            pro_otherinfo = pro[4].replace('u', '\u').decode('unicode-escape')
            pro_skills = pro[1].replace('u', '\u').decode('unicode-escape')
            try:
                sql_work = 'select description from work where resume_id = "%s"' % resume_id
            except:
                traceback.print_exc()
                pdb.set_trace()

            cur.execute(sql_work)

            pro_decription = cur.fetchall()

            position_feature = get_position_feature(com_position, pro_position)
            com_feature = []
            descrip_feature = get_description_feature(com_description, pro_hisprojects, \
                                                      pro_decription, pro_otherinfo, pro_skills)
            com_feature.append(com_low_income)
            com_feature.append(pro_low_income)
            pro_workage = pro[6]
            workage = salaryp.search(pro_workage)
            if workage:
                pro_workage = int(workage.group(0))
            else:
                pro_workage = 0
            pro_degree = pro[7].replace('u', '\u').decode('unicode-escape')
            if '科' in pro_degree or '学' in pro_degree:
                pro_degree = 1
            elif '硕' in pro_degree or '士' in pro_degree:
                pro_degree = 2
            else:
                pro_degree = 0
            com_feature.append(com_workage)
            com_feature.append(pro_workage - com_workage)
            com_feature.append(com_degree)
            com_feature.append(pro_degree - com_degree)
            com_feature.append(round(position_feature, 3))
            com_feature += descrip_feature
            com_feature.append(flag)
            feature_lines.append(','.join(map(lambda x: str(x), com_feature)))
            set_train_flg(cur, term[0], resume_id)


def generate_test_feature(cur, pos_id, resume_id):
    sql = 'select position_id, low_income, description, low_workage, position_name,\
            workage, degree from companytest where position_id = %d' % pos_id

    cur.execute(sql)
    rst = cur.fetchall()

    for term in rst:
        com_low_income = term[1]
        pro_low_income = 0
        com_position = term[4].replace('u', '\u').decode('unicode-escape')
        com_workage = term[5]
        com_degree = term[6]
        pro_position = ''
        com_description = term[2].replace('u', '\u').decode('unicode-escape')
        pro_decription = ''
        pro_hisprojects = ''
        pro_otherinfo = ''

        com_lst = []
        if com_low_income < 500 and com_low_income > 0:
            com_low_income = (com_low_income * 8000) / 12
        com_low_income = com_low_income / 5000
        low_workage = term[5]
        if not low_workage:
            low_workage = 0
        com_lst.append(low_workage)
        com_workage = term[5]
        com_degree = term[6]

        keywords = get_keywords(term[2].replace('u', '\u').decode('unicode-escape'))
        com_description = term[2].replace('u', '\u').decode('unicode-escape')

        try:
            sqlp = 'select dessalary, skills, destitle, hisprojects, otherinfo, resume_id, workyear, latestdegree \
                    from profiletest where resume_id = "%s" limit 5' % (resume_id)

            cur.execute(sqlp)
            profile = cur.fetchall()
        except:
            pdb.set_trace()
        for pro in profile:
            if not pro[0]:
                incomes = salaryp.search('0')
            else:
                incomes = salaryp.search(pro[0])
            try:
                if not resume_id:
                    continue
                pos_sql = 'select position_name from worktest where resume_id = "%s" order by end_time desc' % resume_id
                cur.execute(pos_sql)
                pos_rst = cur.fetchall()
                pro_position = pos_rst[0][0]
            except:
                pro_position = pro[2]
            if incomes:
                low_income = incomes.group(0)
            else:
                low_income = 0
            pro_low_income = int(low_income) / 5000
            pro_hisprojects = pro[3].replace('u', '\u').decode('unicode-escape')
            pro_otherinfo = pro[4].replace('u', '\u').decode('unicode-escape')
            pro_skills = pro[1].replace('u', '\u').decode('unicode-escape')
            try:
                sql_work = 'select description from worktest where resume_id = "%s"' % resume_id
            except:
                traceback.print_exc()
                pdb.set_trace()

            cur.execute(sql_work)

            pro_decription = cur.fetchall()

            position_feature = get_position_feature(com_position, pro_position)
            com_feature = []
            descrip_feature = get_description_feature(com_description, pro_hisprojects, \
                                                      pro_decription, pro_otherinfo, pro_skills)
            com_feature.append(com_low_income)
            com_feature.append(pro_low_income)
            pro_workage = pro[6]
            workage = salaryp.search(pro_workage)
            if workage:
                pro_workage = int(workage.group(0))
            else:
                pro_workage = 0
            pro_degree = pro[7]
            if '科' in pro_degree or '学' in pro_degree:
                pro_degree = 1
            elif '硕' in pro_degree or '士' in pro_degree:
                pro_degree = 2
            else:
                pro_degree = 0
            com_feature.append(com_workage)
            com_feature.append(pro_workage - com_workage)
            com_feature.append(com_degree)
            com_feature.append(pro_degree - com_degree)
            com_feature.append(round(position_feature, 3))
            com_feature += descrip_feature

            return com_feature


def generate_test(pos_id, resume_id):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        cur.execute('set character_set_client=utf8')
        cur.execute('set character_set_connection=utf8')
        cur.execute('set character_set_database=utf8')
        cur.execute('set character_set_results=utf8')
        cur.execute('set character_set_server=utf8')
        conn.commit()

        feature_lines = generate_test_feature(cur, pos_id, resume_id)

        conn.close()
        return feature_lines

    except:
        traceback.print_exc()
        conn.close()


def generate_train(data_path='data'):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        cur.execute('set character_set_client=utf8')
        cur.execute('set character_set_connection=utf8')
        cur.execute('set character_set_database=utf8')
        cur.execute('set character_set_results=utf8')
        cur.execute('set character_set_server=utf8')
        conn.commit()
        feature_lines = []
        # pdb.set_trace()
        get_feature(cur, feature_lines, 1)
        conn.commit()
        get_feature(cur, feature_lines, 0)
        conn.commit()
        if len(feature_lines) > 0:
            with open(data_path.replace("'", '') + '/traindata', 'a') as file:
                file.writelines('\n'.join(feature_lines))
                file.write('\n')
        conn.close()

    except:
        traceback.print_exc()
        conn.close()


if __name__ == '__main__':
    pos_id = 1012931
    resume_id = 21991437

    generate_train()
    # generate_test(pos_id, resume_id)

end = time.time()

print end - start
