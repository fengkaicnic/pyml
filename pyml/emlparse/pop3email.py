#coding:utf8
import time
import sys
import email
import os
import time
import argparse
import pdb
import eventlet
from email import utils
eventlet.monkey_patch()
from parse1 import parse_eml
from email import Parser
from scipy.stats.mstats_basic import tmax
reload(sys)
import json
import hashlib
import traceback
import uuid
import codecs
from email.header import decode_header
import poplib
import pickle
sys.setdefaultencoding('utf-8')
start = time.time()

messageid_dct = {}
pth = 'd:/pop3/'
mona = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
subject_key = ['failure', 'Addressverification', u'错误', u'失败']

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

def check_from_subject(from_mail, subject):
    flag = 0
    from_mail = from_mail or 'none'
    subject = decode_header(subject)[0][0].replace(' ', '')
    if 'postmaster' in from_mail.lower():
        return 1
    for key in subject_key:
        if key in subject:
            return 1

def generate_name(msg, folder_path):
    mailtm = msg.get('Date')
    messageid = msg.get('Message-Id')
    subject = msg.get('Subject')
    from_email = msg.get('From')
    path = [folder_path]
    flag = 0
    if check_from_subject(from_email, subject):
        flag = 1
        path.append('bugemail')
    mailtime = time.localtime(handle_time(mailtm))
    m = hashlib.md5()
    m.update(msg.get('message-id', 'none'))
    m.update(msg.get('From', 'none'))
    m.update(msg.get('Subject', 'None'))
    fle_name = time.strftime("%d-%H%M%S-",mailtime) + m.hexdigest()+"-"+ utils.parseaddr(msg.get('From'))[1]+".eml"

    folder = time.strftime('%Y%m', mailtime)
    path.append(folder)
    if not os.path.exists('/'.join(path)):
        os.makedirs('/'.join(path))
    path.append(fle_name)
    return (flag, '/'.join(path))

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

def handle_eml(messageid_dct, msg_content, folder_path, user):
    # fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_string(msg_content)
    subject = msg.get('Subject')
    # if not check_email(messageid_dct, messageid):
    #     return [decode_header(subject)[0][0].replace(' ', '')]

    mailtm = msg.get('date')
    flag, name = generate_name(msg, folder_path)
    if flag == 0:
        if os.path.isfile(name):
            return 1
        else:
            result = parse_eml(msg)
            print decode_header(subject)[0][0].replace(' ', '')
            write_mail(name, msg_content)
            return result
    elif flag == 1:
        if os.path.isfile(name):
            return name
        else:
            result = parse_eml(msg, True)
            print decode_header(subject)[0][0].replace(' ', '')
            write_mail(name, msg_content)
            return result

def recive_eml(lst, bug_index):
    result = 'error'
    index = lst[0]
    messageid_dct = lst[1]
    subject_lst = lst[2]
    eml_name_lst = lst[3]
    try:
        resp, lines, octets = server.retr(index+1)
        msg_content = '\r\n'.join(lines)
#         print msg_content
        result = handle_eml(messageid_dct, msg_content, folder_path, user)
        if isinstance(result, int):
            return [1]
        else:
            eml_name_lst.append(result)
            return [0, result]
    except:
        print traceback.print_exc()
        bug_index.append(index)
        bug_eml_lst.append(result)
        return [2]

if __name__ == '__main__':
    user = 'bugemail@nrnr.me'
    password = 'Naren2016'
    pop3_server = 'pop.exmail.qq.com'
    # user = 'nrall001@163.com'
    # password = 'nr1111'
    # pop3_server = 'pop.163.com'
    server = poplib.POP3(pop3_server)
    folder_path = validate_mail_path(user)

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='d:/pop3', help='the path to store result')
    parser.add_argument('--num', type=int, default=5, help='the repeat num to terminate the program')
    args = parser.parse_args()
    pth = args.path
    if pth[-1] != '/':
        pth = pth + '/'
    repeatnum = args.num

    messageid_dct = get_message_dct(user)
    eml_name_lst = []
    bug_eml_lst = []
    subject_lst = []
    bug_index = []
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
        rst = recive_eml([index-v, messageid_dct, subject_lst, eml_name_lst], bug_index)
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
    pkl_fle = open(pth + user + '/messageid', 'wb')
    pickle.dump(messageid_dct, pkl_fle)
    pkl_fle.close()
    print bug_index
    # for path in eml_name_lst:
    #     try:
    #         parse_eml(path)
    #     except Exception, e:
    #         print e
    #         print traceback.print_exc()
    server.quit()
    print '=================================='
    for subject in subject_lst:
        print subject
end = time.time()
print (end - start)