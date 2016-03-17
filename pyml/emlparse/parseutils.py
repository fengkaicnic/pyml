#coding:utf8
import time
import sys
from DBUtils import PersistentDB
import email
from naren_solr import sales_solr
import pdb
import jieba
from email import utils
import traceback
import base64
from email.header import decode_header
import MySQLdb

stop_words = ['面试', '邀请', '介绍', '加入', '公司', '有限', '机会', '职位', '推荐', '简介', '月薪', '工作',\
              '服务', '开发', '北京', '高级', '回复', '邀请函', '并', '查收', '工程师', '】', '来信', '您',\
              '请', '收到', '谢谢', '通知', '网络', '沟通', '邮件', '诚邀', '来自', '北京', '-', '技术',\
              '核心', '关于', '的', '—', '候选人', '有限公司', '软件', '（', '上海', '【', '资深', 'PHP',\
              '来自', '：', '招聘', '上市', '互联网', '金融']

persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
                                    passwd='8e1c7d52557b', db='reply_analyze', charset='utf8')

def decode_nck(nick):
    nklst = nick.split('?')
    return base64.decodestring(nklst[3]).decode(nklst[1])

def generate_table_data(subject, nick):
    subject = decode_header(subject)[0][0].replace(' ', '')
    try:
        subject = subject.decode('utf8').encode('utf8')
    except:
        try:
            subject = subject.decode('gbk').encode('utf8')
        except:
            subject = subject.decode('gb18030').encode('utf8')
    subject = subject.replace(',', '|')
    page_index = 0
    countofpage = 1
    solr_ip_port = '121.41.27.143:11082'

    com_lst = []
    if not nick:
        nick = ''
    else:
        if '=' in nick:
            nick = decode_nck(nick)
    seg_lst = jieba.cut(subject, cut_all=False)
    com_flag = 0
    for seg in seg_lst:
        if seg not in stop_words:
            com_flag = 1
            com_lst.append(seg)
        elif com_lst:
            break
    print ''.join(com_lst)
    if com_lst:
        arg_map = {'name':''.join(com_lst)}
    else:
        arg_map = {'name': nick}
    rst = sales_solr.sales_search(arg_map, page_index, countofpage, solr_ip_port)
    return (rst[0], arg_map['name'])

def get_mail_name(msg):
    pass

def read_from_csv(path):
    pass

#做测试用，传入的参数是[[], []]形式，以后要修改
def write_table(datas):
    conn = persist.connection()
    cur = conn.cursor()
    try:
        for data in datas:
            datalst = data.split(',')
            print datalst
            datasql = 'insert into result(subject, company_name, matches, contact_name, mobile,\
                        phone, address, email_address) values ("%s", "%s", %d, "%s", "%s", "%s", "%s", "%s")' % \
                        (datalst[0], datalst[1], int(datalst[2]), datalst[3], datalst[4], datalst[5], datalst[6], datalst[7])
            print datasql
            cur.execute(datasql)
        conn.commit()
        cur.close()
        conn.close()
    except:
        traceback.print_exc()
        conn.close()