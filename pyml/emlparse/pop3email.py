#coding:utf8
import sys
import email
import os
import time
import pdb
from email import Parser
reload(sys)
import uuid
import codecs
from email.header import decode_header
import poplib
import pickle
sys.setdefaultencoding('utf-8')

messageid_dct = {}
pth = 'd:/pop3/'

def validate_mail_path(user):
    path = pth + user
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isfile(path + '/messageid'):
        pkl_fle = open(path + '/messageid', 'wb')
        pickle.dump({}, pkl_fle)
        pkl_fle.close()
    
    return path

def generate_name(subject, mailtm, folder_path):
    path = [folder_path]
    mailtm = mailtm[:mailtm.find('+')-1]
    mailtime = time.strptime(mailtm, '%a,%d %b %Y %H:%M:%S')
    folder = time.strftime('%Y%m', mailtime)
    path.append(folder)
    if not os.path.exists('/'.join(path)):
        os.makedirs('/'.join(path))
    fle_name = time.strftime('%d%H%M%S', mailtime)
    subject_name = decode_header(subject)[0][0].replace(' ', '')
    path.append(fle_name+uuid.uuid1().hex+'.eml')
    return '/'.join(path)

def get_message_dct(user):
    pkl_fle = open(pth + user + '/messageid', 'rb')
    messageid_dct = pickle.load(pkl_fle)
    pkl_fle.close()
    return messageid_dct
    
def check_email(messageid_dct, messageid):
    if messageid_dct.has_key(messageid):
        return False
    else:
        messageid_dct[messageid] = 1
    return True

def write_mail(path, content):
    with open(path, 'wb') as file:
        file.write(content)

def handle_eml(messageid_dct, msg_content, folder_path, user):
    # fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_string(msg_content)
    messageid = msg.get('Message-Id')
    if not check_email(messageid_dct, messageid):
        return
    subject = msg.get('Subject')
    mailtm = msg.get('date')
    name = generate_name(subject, mailtm, folder_path)
    write_mail(name, msg_content)

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

if __name__ == '__main__':
    user = 'bugemail@nrnr.me'
    password = 'Naren2016'
    pop3_server = 'pop.exmail.qq.com'
    server = poplib.POP3(pop3_server)
    pdb.set_trace()
    folder_path = validate_mail_path(user)
    
    messageid_dct = get_message_dct(user)
    print server.getwelcome()
    server.user(user)
    server.pass_(password)

    print 'Message: %s. Size: %s' % server.stat()

    resp, mails, octets = server.list()
    print mails

    index = len(mails)
    resp, lines, octets = server.retr(index-1)
    msg_content = '\r\n'.join(lines)
    print msg_content
    handle_eml(messageid_dct, msg_content, folder_path, user)
    pkl_fle = open(pth + user + '/messageid', 'wb')
    pickle.dump(messageid_dct, pkl_fle)
    pkl_fle.close()
    server.quit()