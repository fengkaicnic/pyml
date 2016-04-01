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
import json

sys.setdefaultencoding('utf8')

start = time.time()

salaryp = re.compile('\d+')

jieba.load_userdict('textfile/dict.txt')

keyword_dct = {}
num = 0
with open('textfile/dict.txt', 'r') as file:
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

    return len(com_pos_lst) / float(total)


def get_description_feature(com_description, pro_hisprojects, pro_descriptions, pro_otherinfo):
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
        for seg in comlst:
            if seg in his_seg:
                description_feature[keyword_dct[seg]] += 1
            if seg in deslst:
                description_feature[keyword_dct[seg]] += 1
            if seg in othlst:
                description_feature[keyword_dct[seg]] += 1
    except:
        pdb.set_trace()
        traceback.print_exc()


    return description_feature

def get_feature(cur, feature_lines, flag):
    sql = 'select pos_id, count(*) as num from profile where recommend = 1 and confirm = 1 group by pos_id'

    cur.execute(sql)

    rst = cur.fetchall()

    for term in rst:
        # print str(term[0]) + ':' + str(term[1])
        sql1 = 'select low_income, description, low_workage, position_name, \
                education from company where position_id = %d' % term[0]

        cur.execute(sql1)
        company_rst = cur.fetchall()
        # pdb.set_trace()
        com_low_income = 0
        pro_low_income = 0
        com_position = ''
        pro_position = ''
        com_description = ''
        pro_decription = ''
        pro_hisprojects = ''
        pro_otherinfo = ''
        for compy in company_rst:
            com_lst = []
            low_income = compy[0]
            if low_income < 500 and low_income > 0:
                low_income = (low_income * 8000) / 12
            com_low_income = low_income / 5000
            low_workage = compy[2]
            com_position = compy[3]
            if not low_workage:
                low_workage = 0
            com_lst.append(low_workage)

            keywords = get_keywords(compy[1])
            com_description = compy[1]
            # print json.dumps(keywords, encoding='utf8', ensure_ascii=False)
            # print compy[2]
            # print json.dumps(get_keywords(compy[3]), encoding='utf8', ensure_ascii=False)
            # print compy[3]
            # print compy[4]

        sqlp = 'select dessalary, skills, destitle, hisprojects, otherinfo, resume_id from profile where \
                 pos_id = %d and recommend = 1 and confirm = %d' % (term[0], flag)

        cur.execute(sqlp)
        profile = cur.fetchall()

        for pro in profile:
            # print pro[0]
            incomes = salaryp.search(pro[0])
            pro_position = pro[2]
            if incomes:
                low_income = incomes.group(0)
            else:
                low_income = 0
            pro_low_income = int(low_income) / 5000
            pro_hisprojects = pro[3]
            pro_otherinfo = pro[4]
            resume_id = pro[5]
            sql_work = 'select description from work where pos_id = %d and resume_id = %d' % (term[0], resume_id)
            cur.execute(sql_work)

            pro_decription = cur.fetchall()

            position_feature = get_position_feature(com_position, pro_position)
            com_feature = []
            descrip_feature = get_description_feature(com_description, pro_hisprojects, pro_decription, pro_otherinfo)
            com_feature.append(com_low_income)
            com_feature.append(pro_low_income)
            com_feature.append(round(position_feature, 3))
            com_feature += descrip_feature
            com_feature.append(flag)
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
    get_feature(cur, feature_lines, 0)
    with open('d:/naren/recommend/train', 'wb') as file:
        file.writelines('\n'.join(feature_lines))
    conn.close()

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start
