#coding:utf8
import time
import sys
from DBUtils import PersistentDB
import email
from naren_solr import sales_solr
import pdb
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import os
reload(sys)
import jieba
from sklearn.feature_extraction.text import HashingVectorizer
import logging
from email import utils
import traceback
from sklearn.externals import joblib
import base64
from email.header import decode_header
import MySQLdb
sys.setdefaultencoding('utf8')

stop_words = ['面试', '邀请', '介绍', '加入', '公司', '有限', '机会', '职位', '推荐', '简介', '月薪', '工作',\
              '服务', '开发', '北京', '高级', '回复', '邀请函', '并', '查收', '工程师', '】', '来信', '您',\
              '请', '收到', '谢谢', '通知', '网络', '沟通', '邮件', '诚邀', '来自', '北京', '-', '技术',\
              '核心', '关于', '的', '—', '候选人', '有限公司', '软件', '（', '上海', '【', '资深', 'PHP',\
              '来自', '：', '招聘', '上市', '互联网', '金融']

persist = PersistentDB.PersistentDB(MySQLdb, host='121.40.183.7', port=3306, user='fengkai',\
                                    passwd='8e1c7d52557b', db='reply_analyze', charset='utf8')

comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)
clf = joblib.load('mailclassify/clf.model')

def vectorize(test_words):
    v = HashingVectorizer(tokenizer=comma_tokenizer, n_features=30000, non_negative=True)
    test_data = v.fit_transform(test_words)
    return test_data

def predict_mail(subject):
    # pdb.set_trace()
    data = vectorize([subject])
    code = clf.predict(data)
    return int(code[0].strip())

def decode_nck(nick):
    nklst = nick.split('?')
    return base64.decodestring(nklst[3]).decode(nklst[1])


def html_parser(content):
    content = content.strip()
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(content)
    parser.close()
    return ''.join(result)


def get_mail_content(msg):
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
            # if bar.get_content_type() == 'text/plain':
            #     data = bar.get_payload(decode=True)
            # else:
            #     data = html_parser(bar.get_payload(decode=True))
            data = bar.get_payload(decode=True)
            try:
                if bar.get_content_charset() == 'gb2312':
                    # print data.decode('gbk').encode('utf-8')
                    content = data.decode('gbk').encode('utf-8')
                else:
                    # print data.decode(bar.get_content_charset()).encode('utf-8')
                    content = data.decode(bar.get_content_charset() and \
                                          bar.get_content_charset() or 'utf8').encode('utf-8')
                    # return content
            except UnicodeDecodeError:
                # print data
                content = data
                # return content
            if bar.get_content_type() == 'text/html':
                content = html_parser(content)
            return content


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
    try:
        rst = sales_solr.sales_search(arg_map, page_index, countofpage, solr_ip_port)
    except:
        return (0, arg_map['name'])
    return (rst[0], arg_map['name'])

def get_mail_name(msg):
    pass


def read_from_csv(path):
    pass

def write_error_mail(datas, logger):
    conn = persist.connection()
    cur = conn.cursor()
    try:
        for data in datas:
            try:
                datasql = '''insert into error_mail(subject, email_address, recive_mail, time_stamp, \
                              uuid, store_path, inbox_time) values ("%s", "%s", "%s", %d, "%s", "%s", "%s")\
                              ''' % (data[0], data[1], data[2], data[3], data[4], data[5], data[6])
            except:
                traceback.print_exc()

            cur.execute(datasql)
        conn.commit()
        cur.close()
        conn.close()
    except:
        logger.exception("Exception Logged")
        traceback.print_exc()
        conn.close()

#做测试用，传入的参数是[[], []]形式，以后要修改
def write_table(datas, logger):
    conn = persist.connection()
    cur = conn.cursor()
    try:
        for data in datas:
            datalst = data
            # print datalst
            try:
                datasql = '''insert into result(subject, company_name, matches, contact_name, mobile,\
                        phone, address, email_address, recive_email, content, time_stamp, uuid, store_path, inbox_time) values\
                         ("%s", "%s", %d, "%s", "%s", "%s", "%s", "%s", "%s", "%s", %d, "%s", "%s", "%s")''' % (datalst[0], datalst[1], \
                         datalst[2], datalst[3], datalst[4], datalst[5], datalst[6], datalst[7], datalst[8],\
                            datalst[9].replace('"', r'\"'), datalst[10], datalst[11], datalst[12], datalst[13])
            except:
                traceback.print_exc()
            # print datasql
            cur.execute(datasql)
        conn.commit()
        cur.close()
        conn.close()
    except:
        logger.exception("Exception Logged")
        traceback.print_exc()
        conn.close()


def set_logger(filename):
    # 创建一个logger,可以考虑如何将它封装
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(os.path.join(os.getcwd(), filename))
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger