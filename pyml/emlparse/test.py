#coding:utf8
import time
import sys
import email
import os
import jieba
import time
from parse1 import parse_eml
import argparse
from naren_solr import sales_solr
import traceback
reload(sys)
import pdb
from email import utils
import base64
import poplib
from email.header import decode_header
sys.setdefaultencoding('utf8')

stop_words = ['面试', '邀请', '介绍', '加入', '公司', '有限', '机会', '职位', '推荐', '简介', '月薪', '工作',\
              '服务', '开发', '北京', '高级', '回复', '邀请函', '并', '查收', '工程师', '】', '来信', '您',\
              '请', '收到', '谢谢', '通知', '网络', '沟通', '邮件', '诚邀', '来自', '北京', '-', '技术',\
              '核心', '关于', '的', '—', '候选人', '有限公司', '软件', '（', '上海', '【', '资深', 'PHP',\
              '来自', '：', '招聘', '上市', '互联网', '金融']

filter_words = ['智联', '汇总', '奖品', '确认', '提醒', '在线考评', '薪水', '电影',\
                '会员', '注册', '51job', '已经有', '不合适', '最新职位', '手机',\
                '简历', '跳槽',  '猎头', '网易考拉', '互联网淘金', '已投', '安全问题', '机会'\
                '靠谱']
mailst = ['service@steelport.zhaopin.com', 'service@51job.com']

def decode_nck(nick):
    nklst = nick.split('?')
    return base64.decodestring(nklst[3]).decode(nklst[1])

start = time.time()
if __name__ == '__main__':
    # user = 'bugemail@nrnr.me'
    # password = 'Naren2016'
    # pop3_server = 'pop.exmail.qq.com'
    user = 'nrall001@163.com'
    password = 'nr1531032'
    pop3_server = 'pop.163.com'

    page_index = 0
    countofpage = 1
    solr_ip_port = '121.41.27.143:11082'

    server = poplib.POP3(pop3_server)
    print server.getwelcome()
    server.user(user)
    server.pass_(password)

    print 'Message: %s. Size: %s' % server.stat()

    resp, mails, octets = server.list()
    # print mails
    index = len(mails)
    linecsv = []
    num = 0
    total = 0
    for v in range(index):
        try:
            flag = 0
            com_flag = 0
            resp, lines, octets = server.retr(v+1)
            # resp, lines, octets = server.top(v+1, 7)
            msg_content = '\r\n'.join(lines)
            msg = email.message_from_string(msg_content)
            # pdb.set_trace()
            fmail = msg.get('From')
            from_mail = utils.parseaddr(msg.get('From'))[1]
            # nick = utils.parseaddr(msg.get('From'))[0]
            nick = fmail.split(' ')[0]
            subject = msg.get('Subject')
            subject = decode_header(subject)[0][0].replace(' ', '')
            try:
                subject = subject.decode('utf8').encode('utf8')
            except:
                try:
                    subject = subject.decode('gbk').encode('utf8')
                except:
                    subject = subject.decode('gb18030').encode('utf8')
            for word in filter_words:
                if word in subject:
                    flag = 1
                    break

            if not flag:
                # print '========================================='
                # print from_mail
                com_lst = []
                if not nick:
                    # pdb.set_trace()
                    nick = ''
                else:
                    if '=' in nick:
                        nick = decode_nck(nick)
                print subject,'||',nick
                seg_lst = jieba.cut(subject, cut_all=False)
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
                print rst
                linecsv.append(subject.strip())
                linecsv.append(',')
                linecsv.append(arg_map['name'].strip())
                linecsv.append(',')
                linecsv.append(str(rst[0]))
                linecsv.append(',')
                if rst[0]:
                    total += 1
                num += 1
                result = parse_eml(msg)
                # pdb.set_trace()
                linecsv.append(result.get(u'联系人', '').strip())
                linecsv.append(',')
                linecsv.append(result.get(u'手机', '').strip())
                linecsv.append(',')
                linecsv.append(result.get(u'座机', '').strip())
                linecsv.append(',')
                linecsv.append(result.get(u'地址', '').strip())
                linecsv.append(result.get('email', '').strip())
                linecsv.append('\n')
                # print '*****************************************'
        except:
            pass
    print total
    print num
    with open('d:/naren/test.csv', 'wb') as file:
        file.writelines(''.join(linecsv).encode('utf8'))
    server.quit()
end = time.time()

print (end - start)
