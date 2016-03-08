#coding:utf8
import time
import sys
import email
import os
import time
import pdb
import eventlet
eventlet.monkey_patch()
from parse1 import parse_eml
from email import Parser
from scipy.stats.mstats_basic import tmax
reload(sys)
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

def handle_time(timestr):
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

def generate_name(mailtm, folder_path):
    path = [folder_path]
    timestr = handle_time(mailtm)
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
    messageid = msg.get('Message-Id')
    subject = msg.get('Subject')
    # if not check_email(messageid_dct, messageid):
    #     return [decode_header(subject)[0][0].replace(' ', '')]

    mailtm = msg.get('date')
    name = generate_name(mailtm, folder_path)
    print decode_header(subject)[0][0].replace(' ', '')
    write_mail(name, msg_content)
    return name

def parse_eml(msg_content):
    msg = email.message_from_string(msg_content)
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        print '*****************************'
        print header,':',value
        if header == 'Subject':
            print decode_header(value)[0][0]

    emailaddress = msg.get('from')[msg.get('from').find('<')+1:msg.get('from').find('>')]
    print '======================================================='
    print 'email:',emailaddress
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
            data = bar.get_payload(decode=True)
            if bar.get_content_charset() == 'gb2312':
                print data.decode('gbk').encode('utf-8')
                content = data.decode('gbk').encode('utf-8')
            else:
                print data.decode(bar.get_content_charset()).encode('utf-8')
                content = data.decode(bar.get_content_charset()).encode('utf-8')
            # try:
            #     print data.decode('gb2312').encode('utf-8')
            #     content = data.decode('gb2312').encode('utf-8')
            # except UnicodeDecodeError:
            #     print data
            #     content = data
#             print bar.get_content_maintype()
#             print bar.get_content_type()
            break

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
        if isinstance(result, list):
            subject_lst.append(result[0])
        else:
            eml_name_lst.append(result)
    except:
        print traceback.print_exc()
        bug_index.append(index)
        bug_eml_lst.append(result)

if __name__ == '__main__':
    user = 'bugemail@nrnr.me'
    password = 'Naren2016'
    pop3_server = 'pop.exmail.qq.com'
    server = poplib.POP3(pop3_server)
    folder_path = validate_mail_path(user)
    pool = eventlet.GreenPool()

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

    # index = len(mails)
    index = [306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333]
    pdb.set_trace()
    paramlst = []
    # for v in range(index):
    for v in index:
        recive_eml([v, messageid_dct, subject_lst, eml_name_lst], bug_index)
    # pool.imap(recive_eml, paramlst)
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