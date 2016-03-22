#coding:utf8
import time
import sys
import email
import os
import time
import argparse
import pdb
import logging
import eventlet
from email import utils
import re
eventlet.monkey_patch()
from parse1 import parse_eml
from email import Parser
from scipy.stats.mstats_basic import tmax
reload(sys)
import json
import hashlib
import traceback
import uuid
import parseutils
import codecs
from email.header import decode_header
import poplib
import pickle
sys.setdefaultencoding('utf-8')
start = time.time()

messageid_dct = {}
pth = 'd:/pop3/'
mona = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# filter_words = ['智联招聘', '在线考评', '51job', '已经有', '不合适', '最新职位', '推荐', '简历排名',  '猎头', '网易考拉', '互联网淘金', '已投']
filter_words = ['智联', '汇总', '奖品', '确认', '提醒', '在线考评', '薪水', '电影',\
                '会员', '注册', '51job', '已经有', '不合适', '最新职位', '手机',\
                '简历', '跳槽',  '猎头', '网易考拉', '互联网淘金', '已投', '安全问题', '机会',\
                '靠谱', '推荐']
mailst = ['service@steelport.zhaopin.com', 'service@51job.com']
subject_key = ['failure', 'Addressverification', u'错误', u'失败']
mailtype={1:'bugmail', 2:'spam'}
emailp = re.compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')

logger = parseutils.set_logger('extract_mail.log')
# log_filename = 'extract_mail.log'
# log_format = '%(filename)s [%(asctime)s] [%(levelname)s] %(message)s'
# logging.basicConfig(format=log_format, dataformat='%Y-%m-%d %H:%M:%S', filename=log_filename, filemode='w', level=logging.INFO)


def handle_time(timestr):
    if timestr is None:
        return 946656000 #2000-01-01
    return utils.mktime_tz(utils.parsedate_tz(timestr))

def handle_time_old(timestr):
    timelst = timestr.split(' ')
    mon = ''
    year = ''
    day = ''
    hds = ''
    for tm in timelst:
        if tm.find(':') != -1 and tm.find('+') == -1:
            hds = tm
            continue
        if tm in mona:
            mon = tm
            continue
        if tm.isdigit():
            if int(tm) < 32:
                day = tm
            else:
                year = tm
    return ' '.join([year, mon, day, hds])

def validate_mail_path(user):
    path = pth + user
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isfile(path + '/messageid'):
        pkl_fle = open(path + '/messageid', 'wb')
        pickle.dump({}, pkl_fle)
        pkl_fle.close()
    
    return path

def decode_subject(subject):
    subject = decode_header(subject)[0][0].replace(' ', '')
    try:
        subject = subject.decode('utf8').encode('utf8')
    except:
        try:
            subject = subject.decode('gbk').encode('utf8')
        except:
            try:
                subject = subject.decode('gb18030').encode('utf8')
            except:
                pdb.set_trace()
    return subject

#检查邮件是否是垃圾邮件
#param: [from_mail, subject]
#from_mail: 发件人邮箱
#subject: 邮件的主题
#返回码： （0 代表正常邮件）（1 代表发送出错的油价）（2 代表垃圾邮件）
def check_from_subject(from_mail, subject):
    flag = 0
    from_mail = from_mail or 'none'
    subject = decode_subject(subject)
    if 'postmaster' in from_mail.lower():
        return 1 #failure send
    for key in subject_key:
        if key in subject:
            return 1    #/failure send
    # for word in filter_words:
    #     if word in subject:
    #         return 2 #spam
    if not parseutils.predict_mail(subject):
        return 2
    print subject

    return 0

#此函数的功能是产生路径和文件名称，以便于存储邮件
#在此过程中会检查一下邮件是否垃圾邮件或者错误邮件
#检查调用check_from_subject来检查，根据发件邮箱和邮件主题检查
#返回两个参数，一个是flag，另一个是路径
#这个flag如果0代表正常邮件，1代表垃圾邮件
def generate_name(msg, folder_path):
    mailtm = msg.get('Date')
    messageid = msg.get('Message-Id')
    subject = msg.get('Subject')
    from_email = msg.get('From')
    path = [folder_path]
    flag = 0
    flag = check_from_subject(from_email, subject)  #检查邮件的类型
    if flag: #根据邮件的类型，来分开存放
        path.append(mailtype[flag])
    mailtime = time.localtime(handle_time(mailtm))
    m = hashlib.md5()
    m.update(msg.get('message-id', 'none'))
    m.update(msg.get('From', 'none'))
    m.update(msg.get('Subject', 'None'))
    inbox_time = time.strftime('%Y-%m-%d %H:%M:%S', mailtime)
    if '@' in utils.parseaddr(msg.get('From'))[1]:
        fle_name = time.strftime("%d-%H%M%S-",mailtime) + m.hexdigest()+"-"+ utils.parseaddr(msg.get('From'))[1]+".eml"
    else:
        fle_name = time.strftime("%d-%H%M%S-",mailtime) + m.hexdigest()+".eml"
    folder = time.strftime('%Y%m', mailtime)
    path.append(folder)
    if not os.path.exists('/'.join(path)):
        os.makedirs('/'.join(path))
    path.append(fle_name)
    return (flag, inbox_time, '/'.join(path), m.hexdigest())

def generate_name_old(mailtm, folder_path):
    path = [folder_path]
    timestr = handle_time_old(mailtm)
    print mailtm
    # print timestr
    mailtime = time.strptime(timestr, '%Y %b %d %H:%M:%S')
#     if mailtm.find('+') != -1:
#         mailtm = mailtm[:mailtm.find('+')-1]
#     else:
#         mailtm = mailtm[:mailtm.find('-')-1]
#     print mailtm
#     try:
#         mailtime = time.strptime(mailtm, '%a, %d %b %Y %H:%M:%S')
#     except:
#         mailtime = time.strptime(mailtm, '%d %b %Y %H:%M:%S')
    folder = time.strftime('%Y%m', mailtime)
    path.append(folder)
    if not os.path.exists('/'.join(path)):
        os.makedirs('/'.join(path))
    fle_name = time.strftime('%d%H%M%S', mailtime)
    path.append(fle_name+uuid.uuid1().hex+'.eml')
    return '/'.join(path)

def get_message_dct(user):
    pkl_fle = open(pth + user + '/messageid', 'rb')
    messageid_dct = pickle.load(pkl_fle)
    pkl_fle.close()
    return messageid_dct
    
def check_email(messageid_dct, messageid):
    if not messageid:
        return False
    if messageid_dct.has_key(messageid):
        return False
    else:
        messageid_dct[messageid] = 1
    return True

def write_mail(path, content):
    with open(path, 'wb') as file:
        file.write(content)

def get_eml_name(name, user):
    eml_name_path = pth + user + '/emlname'
    if not os.path.isfile(eml_name_path):
        pkl_fle = open(eml_name_path, 'wb')
        pkl_fle.close()
        return {}
    else:
        pkl_fle = open(eml_name_path, 'rb')
        eml_name_dct = pickle.loads(pkl_fle)
        pkl_fle.close()
        return eml_name_dct

def write_eml_name():
    pass

#此函数是获取和检查之后的处理邮件函数
#param:
#msg_content: 这个参数是邮件内容
#folder_path：此参数是邮件的存储位置
#user：邮箱名
#此函数先根据邮件内容和folder_path两个参数来确定存储的位置和邮件生成的名称
#调用generate_name来生成邮件存储路径和判断邮件类型
#如果是正常邮件，则检查邮件是否已经存储，已存则直接返回1，未存的话就解析再存储
#如果是垃圾邮件，那就存储，然后解析出from_email就可以
def handle_eml(msg_content, folder_path, user):
    # fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_string(msg_content)
    subject = msg.get('Subject')
    subject = decode_subject(subject)
    fmail = msg.get('From')
    from_mail = utils.parseaddr(msg.get('From'))[1]
    content = parseutils.get_mail_content(msg)
    if 'gb2312' in from_mail:
        emailq = emailp.search(content)
        if emailq:
            from_mail = emailq.group(0)
        else:
            from_mail = ''
    # nick = utils.parseaddr(msg.get('From'))[0]
    nick = fmail.split(' ')[0]
    mailtm = msg.get('date')
    flag, inbox_time, name, uuid = generate_name(msg, folder_path)
    if flag == 0:         #如果是正常邮件的话则走这个过程
        if os.path.isfile(name):
            return 1
        else:
            rst = parseutils.generate_table_data(subject, nick)
            lines = []
            lines.append(subject.strip())
            lines.append(rst[1].replace('"', ''))
            lines.append(rst[0])
            result = parse_eml(msg, content)
            lines.append(result.get(u'联系人', '').strip())
            lines.append(result.get(u'手机', '').strip())
            lines.append(result.get(u'座机', '').strip())
            lines.append(result.get(u'地址', '').strip())
            lines.append(from_mail.strip().replace('"', ''))
            lines.append(user.strip())
            lines.append(content)
            lines.append(int(time.time()))
            lines.append(uuid)
            lines.append(name)
            lines.append(inbox_time)
            # parseutils.write_table([','.join(lines)])
            parseutils.write_table([lines], logger)
            write_mail(name, msg_content)
            return result
    else:   #如果是垃圾邮件或者错误邮件的话，就走这个流程
        result = 'spam'
        if os.path.isfile(name):
            return name
        if flag == 1:
            result = parse_eml(msg, True)
        print decode_header(subject)[0][0].replace(' ', '')
        write_mail(name, msg_content)
        return result

#这里是处理邮件的函数，首先从服务器提取出邮件，然后生成邮件内容
#生成邮件内容后，调用handle_eml来处理邮件，返回结果
#处理的时候还要看结果的返回码，返回码有这几种
#[0,1,2]0代表邮件存储和处理都正常
#1代表此邮件已经存储和处理过
#2代表处理过程中出现异常
def recive_eml(lst, bug_index):
    result = 'error'
    index = lst[0]
    subject_lst = lst[1]
    eml_name_lst = lst[2]
    try:
        resp, lines, octets = server.retr(index+1)
        msg_content = '\r\n'.join(lines)
#         print msg_content
        result = handle_eml(msg_content, folder_path, user)
        if isinstance(result, int):
            return [1]
        else:
            eml_name_lst.append(result)
            return [0, result]
    except:
        logger.exception("Exception Logged")
        print traceback.print_exc()
        bug_index.append(index)
        bug_eml_lst.append(result)
        return [2]

if __name__ == '__main__':
    # user = 'bugemail@nrnr.me'
    # password = 'Naren2016'
    # pop3_server = 'pop.exmail.qq.com'
    # user = 'nrall001@163.com'
    # password = 'nr1531032'
    # pop3_server = 'pop.163.com'

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='d:/pop3', help='the path to store result')
    parser.add_argument('--num', type=int, default=5, help='the repeat num to terminate the program')
    parser.add_argument('--user', default='nrall001@163.com', help='the user of the email')
    parser.add_argument('--password', default='nr1531032', help='the password of the email')
    parser.add_argument('--pop3server', default='pop.163.com', help='the pop3 server of email')
    args = parser.parse_args()
    pth = args.path
    if pth[-1] != '/':
        pth = pth + '/'
    repeatnum = args.num

    # messageid_dct = get_message_dct(user)
    eml_name_lst = []
    bug_eml_lst = []
    subject_lst = []
    bug_index = []
    pop3_server = args.pop3server
    user = args.user
    password = args.password
    server = poplib.POP3(pop3_server)
    folder_path = validate_mail_path(user)
    print server.getwelcome()
    server.user(user)
    server.pass_(password)

    print 'Message: %s. Size: %s' % server.stat()

    resp, mails, octets = server.list()
    print mails
    flag = 0
    index = len(mails)
    # pdb.set_trace()
    paramlst = []
    resultlst = []
    # for v in range(index):
    for v in range(index):
        rst = recive_eml([index-v, subject_lst, eml_name_lst], bug_index)
        if rst[0] == 0:
            if flag != 0:
                flag = 0
            resultlst.append(rst[1])
        elif rst[0] == 1:
            flag += 1
            if flag > repeatnum:
                break
    pdb.set_trace()
    for result in resultlst:
        print json.dumps(result, encoding='utf8', ensure_ascii=False)
    print bug_index
    server.quit()
    print '=================================='
    for subject in subject_lst:
        print subject
end = time.time()
print (end - start)