#coding:utf8
import sys
import time
import utils
reload(sys)
import pdb
from collections import Counter
import os
import jieba
import re
import traceback
import numpy as np
import json

sys.setdefaultencoding('utf8')

start = time.time()

salaryp = re.compile('\d+')

jieba.load_userdict('../textfile/dict.txt')

keyword_dct = {}
num = 0


with open('../textfile/dict.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if not keyword_dct.has_key(line.strip().lower().decode('utf8')):
            keyword_dct[line.strip().lower().decode('utf8')] = num
            num += 1


def get_keywords(content):
    # pdb.set_trace()
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


def get_description_feature(com_description, pro_hisprojects, pro_descriptions, pro_otherinfo):

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
        description_feature.append(len(com_count))
        inter_con = set(com_count.keys()).intersection(set(pro_count.keys()))
        description_feature.append(len(inter_con))
        description_feature.append(len(comlst))
        # pdb.set_trace()
        description_feature.append(reduce(lambda x, y:x+y, [com_count[key] for key in inter_con] + [0]))
        description_feature.append(reduce(lambda x, y:x+y, [pro_count[key] for key in inter_con] + [0]))

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

    except:
        pdb.set_trace()
        traceback.print_exc()

    return description_feature


def get_feature(cur, feature_lines, flag):
    sql = 'select position_name, description, position_id, low_income, low_workage from mail_company'

    cur.execute(sql)
    company_rst = cur.fetchall()

    for compy in company_rst:
        com_low_income = 0
        pro_low_income = 0
        com_position = ''
        pro_position = ''
        com_description = ''
        pro_decription = ''
        pro_hisprojects = ''
        pro_otherinfo = ''
        position_id = compy[2]

        com_lst = []
        low_income = int(compy[3])
        if low_income < 500 and low_income > 0:
            low_income = (low_income * 8000) / 12
        com_low_income = low_income / 5000
        low_workage = int(compy[4])
        com_position = compy[0]
        if not low_workage:
            low_workage = 0
        com_lst.append(low_workage)

        keywords = get_keywords(compy[1])
        com_description = compy[1]

        sqlp = 'select dessalary, latesttitle , resume_id, selfappraise from mail_profile where \
                 position_id = %d' % (position_id)

        cur.execute(sqlp)
        profile = cur.fetchall()

        for pro in profile:
            incomes = salaryp.search(pro[0])
            pro_position = pro[1]
            pro_selfapp = pro[3]
            if incomes:
                low_income = incomes.group(0)
            else:
                low_income = 0
            pro_low_income = int(low_income) / 5000
            resume_id = pro[2]
            sql_work = 'select description from mail_work where position_id = %d and resume_id = %d' % (position_id, resume_id)
            cur.execute(sql_work)

            pro_decription = cur.fetchall()

            position_feature = get_position_feature(com_position, pro_position)
            com_feature = []
            descrip_feature = get_description_feature(com_description, pro_selfapp, pro_decription, pro_otherinfo)
            com_feature.append(com_low_income)
            com_feature.append(pro_low_income)
            com_feature.append(round(position_feature, 3))
            com_feature += descrip_feature
            com_feature.append(flag)
            # com_feature.append(position_id)
            # com_feature.append(resume_id)
            feature_lines.append(','.join(map(lambda x: str(x), com_feature)))

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

    get_feature(cur, feature_lines, 1)
    with open('d:/naren/recommend/test_model_mail', 'wb') as file:
        file.writelines('\n'.join(feature_lines))
    conn.close()

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start
