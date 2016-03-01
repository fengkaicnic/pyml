#coding=UTF-8
import logging
import getpass, poplib
import imaplib
import email
import os
import sys
import re
from email import utils
from email import Header
import time
import datetime
import hashlib
import itertools

from emlparse import new_mail_handler

import shutil
import random
import string

import base64
import json

import nanautil.dbhelper as dbhelper
import nanautil.util as nautil
reload(sys)
sys.setdefaultencoding('utf-8')


argv_dict={}

logger = logging.getLogger()
def initlog(logfile):
    logdir = time.strftime("logs/%Y%m%d",time.localtime())
    if not os.access(logdir, os.F_OK):
        os.makedirs(logdir)

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=logdir+logfile,
                    filemode='a+')

class CMailMsg(object):
    def __init__(self, strMsg):
        self.msg=email.message_from_string(strMsg)
        self.From = self.msg.get("from","nofrom <nofrom>")
        self.Date = self.msg.get("Date","Sat, 1 Jan 2000 00:00:00 +0800")
        self.Subject = self.msg.get('subject',"no-subject")
        self.id = self.msg.get('Message-Id',"no-msgid")
        self.to = self.msg.get('To')

    @staticmethod
    def __decode_item(item):
        if isinstance(item, str) and item.startswith('=?') :
            _item = "?=\r\n=?".join(item.split("?==?"))
            decodefrag = Header.decode_header(_item)
            subj_fragments = []
            for s, enc in decodefrag:
                if enc is None:
                    subj_fragments.append(s)
                    continue
                if enc.lower() in ('gb2312', 'gbk', 'gb_1988-80'):
                    enc = 'gb18030'
                s = unicode(s, enc).encode('utf8', 'replace')
                subj_fragments.append(s)
            return ''.join(subj_fragments)
        return item

    def get_to(self, decode=True):
        if not decode:
            return self.to
        _to = self.to
        if _to is None:
            _to = 'no_to'
        return ','.join([utils.parseaddr(i)[1].strip() for i in _to.split(',')])

    def get_from(self, decode=True):
        if not decode:
            return self.From
        return self.__decode_item(utils.parseaddr(self.From)[1])

    def get_date(self, decode=True):
        if not decode:
            return self.Date
        if self.Date is None:
            return 946656000 #2000-01-01
        return utils.mktime_tz(utils.parsedate_tz(self.Date))

    def get_subject(self, decode=True):
        if not decode:
            return self.Subject
        return self.__decode_item(self.Subject)

    def get_eml_name(self):
        dtime = time.localtime(self.get_date())
        m = hashlib.md5()
        m.update(self.id)
        m.update(self.get_from(False))
        m.update(self.get_subject(False))
        sYearMonth = time.strftime("%Y%m",dtime)
        fname = time.strftime("%d-%H%M%S-",dtime) + m.hexdigest()+"-"+self.get_from()+".eml"
        return (sYearMonth,fname)

class smtp_setting(object):
    def __init__(self, setting_str):
        (self.host, self.port,self.user,self._pass,self._from)=setting_str.split('`')
        self.port = int(self.port)

class CEmailReceiver(object):
    def __init__(self,smtp_str,host,user,passwd, **kargs):
        #use_ssl=True, autoDele=False, port=None
        self.host = host
        self.user = user
        self.passwd = passwd
        self.use_ssl= kargs.get('use_ssl',True)
        self.port = kargs.get('port',0)
        self.autoDele=kargs.get('autoDele',False)
        self.smtp = smtp_setting(smtp_str)
        self.cur_dir=os.path.dirname(os.path.realpath(__file__))+"/"
        self.data_root = self.cur_dir+"data/"

        #self.emailroot = "data/"+argv_dict['unit_folder']
        if not os.access(self.cur_dir+"/err_email/all", os.F_OK):
            os.makedirs(self.cur_dir+"/err_email/all")
        if not os.access(self.cur_dir+"/err_email/bydate", os.F_OK):
            os.makedirs(self.cur_dir+"/err_email/bydate")

        self.exceptions = 0
        self.already_exists=0
        self.deleted = 0
        self.ok_email=0
        self.err_records={}
        self.p3=None

    @property
    def email_root(self):
        return "data/" + self.unit_folder

    def calc_unit_parameters(self, mm):
        _to = mm.get_to()
        mm = re.findall(r'([^,]*@smtp.xnaren.cn)', _to, re.I)
        if not mm or argv_dict.get('unit') != 'naren_email_dispatch':
            self.unit_folder = argv_dict['unit_folder']
            self.unit_name = argv_dict.get('unit')
            self.unit_id = str(argv_dict['unit_id'])
            return

        real_emails = ','.join(map(nautil.quote_string, mm))
        # get unit info from resume email
        pldb = dbhelper.CPDB(True)
        sql = "select un.unit_id, un.unit_name from unit_resume_mailbox urm join unit un on un.unit_id=urm.unit_id " \
              "where urm.resume_email in (%s) or urm.alter_naren_email in (%s)" % (real_emails, real_emails)
        unit_info = dbhelper.select_one(pldb.cur, sql).merge()

        self.unit_name = unit_info.unit_name
        self.unit_folder = '%s.%s' % (unit_info.unit_id,unit_info.unit_name.decode('utf8'))
        self.unit_id = unit_info.unit_id

    def calEmlName(self, strMsg):
        mm=CMailMsg(strMsg)
        self.calc_unit_parameters(mm)
        folder, fname = mm.get_eml_name()
        cur_dir = self.email_root+"/"+folder
        cur_dir = nautil.to_utf8(cur_dir)
        if not os.access(cur_dir, os.F_OK):
            os.makedirs(cur_dir);
        #if not os.access(self.emailroot+"/err_emails", os.F_OK):
        #    os.makedirs(self.emailroot+"/err_emails")
        return (cur_dir+"/"+fname,mm)

    def on_new_email(self, emlfile, inbox_time):
        _argv_dict = argv_dict.copy()
        _argv_dict['unit'] = self.unit_name
        _argv_dict['unit_folder'] = self.unit_folder
        _argv_dict['unit_id'] = self.unit_id
        return new_mail_handler(self.cur_dir+emlfile, **_argv_dict)

    def log_statistics(self):
        logger.info("email stat: (OK, duplicated, ERR, exceptions) ( %d,%d,%d,%d )" %
                    (self.ok_email, self.already_exists, len(self.err_records), self.exceptions) )
        if self.deleted:
            _email = self.user
            if _email.find('@') < 0:
                _email += '@' + self.host
            logger.warning("%s emails deleted from %s" % (self.deleted, _email))




class CPop3Client(CEmailReceiver):
    def __init__(self,smtp_str,host,user,passwd, **kargs):
        CEmailReceiver.__init__(self,smtp_str, host,user,passwd, **kargs)

    def relogin(self):
        if self.p3:
            self.p3.quit()
            self.p3=None
        try:
            if self.use_ssl:
                self.p3 = poplib.POP3_SSL(self.host, self.port and self.port or poplib.POP3_SSL_PORT)
            else:
                self.p3 = poplib.POP3(self.host, self.port and self.port or poplib.POP3_PORT)
            #self.p3._debugging =1
            self.p3.user(self.user)
            self.p3.pass_(self.passwd)
        except:
            self.p3 = None
            pass
        return self.p3 is not None


    def fetch_one(self,which):
        try:
            top_retry = 0
            msg = None
            while top_retry < 3:
                try:
                    msg = self.p3.top(which, 1)
                    break
                except:
                    time.sleep(3)
                    top_retry += 1
            if top_retry > 0:
                if msg is None:
                    nautil.dlog.warning("emailclient-pop3(%s:%s): top failed after %s retries" % (argv_dict.get('unit_folder', ''), which, top_retry))
                    return None, 'exception', None
                else:
                    nautil.dlog.warning("emailclient-pop3(%s:%s): top succeeded after %s retries" % (argv_dict.get('unit_folder', ''), which, top_retry))
            strMsg = "\n".join(msg[1])
            del msg
            sFileName, mm=self.calEmlName(strMsg)
            if mm.get_to() == "no_to":
                open(sFileName,"wb").write("no_to")
                nautil.dlog.warning("emailclient-pop3(%s:%s): ignore one email %s" % (argv_dict.get('unit_folder', ''), which, sFileName))
                logger.warning("emailclient-pop3(%s:%s): ignore one email %s" % (argv_dict.get('unit_folder', ''), which, sFileName))
                return None, 'ignore', None

            subject = mm.get_subject(True)
            # print subject.decode('utf8')

            inbox_time = mm.get_date()
            timestamp  = time.time()
            disposes = []
            if os.access(sFileName,os.F_OK):
                disposes.append('handled')
                self.already_exists += 1

            if timestamp-inbox_time > 86400*10:
                disposes.append('pre-dele')

            if timestamp-inbox_time > 86400*60:
                disposes.append('old')

            if 'old' in disposes or 'handled' in disposes:  #old or handled
                return sFileName, disposes, mm.get_date()

            logger.info("retring(%s) %s" % (which, subject))
            msg= self.p3.retr(which)
            if self.autoDele and (timestamp-inbox_time > 86400*15): #15 days
                self.p3.dele(which)
                self.deleted += 1
                disposes.append('deleted')

            open(sFileName,"wb").write("\n".join(msg[1]))
            try:
                handler_ok = self.on_new_email(sFileName, inbox_time)
            except:
                return None, 'handler_exception', None

            if handler_ok:
                self.ok_email += 1
            else:
                logger.error("on_new_email failed for %s" % sFileName)
                retries = self.err_records.get(sFileName,0)
                self.err_records[sFileName] = retries+1
                sFileNameLow = sFileName.lower()
                if sFileNameLow.find('zhaopin')>0 or sFileNameLow.find('51job')>0:
                    try:
                        shutil.move(sFileName, self.data_root+'error_emails')
                    except Exception, e:
                        logger.error("move failed %s: %s" % (sFileName, str(e)))
                        os.unlink(sFileName)
                    sFileName=None
            return sFileName, ['new'], None
        except Exception,e:
            logger.exception("fetch_one(%s) %d" % (argv_dict.get('unit_folder', ''), which))
            nautil.dlog.exception("fetch_one(%s) %d" % (argv_dict.get('unit_folder', ''), which))
        return None, 'exception', None

    def fetch_all_impl(self):
        numMessages,total_size = self.p3.stat()
        _reverse = 'Unknown'
        if numMessages >= 2:
            msg_end = CMailMsg("\n".join(self.p3.top(numMessages,1)[1]))
            msg_one = CMailMsg("\n".join(self.p3.top(1,1)[1]))
            if msg_end.get_date() > msg_one.get_date():
                _reverse = False

        logger.info("retr reverse order %s" % _reverse)
        msgs = xrange(numMessages) if _reverse else xrange(numMessages-1,-1,-1)
        old_emails = 0
        successive_exceptions = 0
        dispos = []
        ignore_every = 1

        max_errors = 10
        ignored = set([])
        if argv_dict.get('unit', '') == 'naren_email_dispatch':
            max_errors = 300

        for i in itertools.chain(msgs, ignored):
            if "handled" in dispos:
                if 'old' in dispos:
                    continue
                ignore_every = 3
                if argv_dict.get('unit', '') == 'naren_email_dispatch':
                    ignore_every = 13
                if i % ignore_every != 0:
                    ignored.add(i)
                    if len(ignored) > 5*ignore_every:
                        ignored.pop()
                    continue
            else:
                ignore_every = 1
            #if i % ignore_every != 0:
            #    continue
                
            eml_fname,dispos,rztime = self.fetch_one(i+1)
            if 'old' in dispos:
                old_emails += 1
                if old_emails >= max_errors: #连续 5 封老邮件
                    emsg = "(%s) %s个连续老邮件, 退出" % (argv_dict.get('unit_folder', ''), max_errors)
                    logger.info(emsg)
                    nautil.dlog.info("emailclient-pop3: %s " % emsg)
                    break
            else:
                old_emails = 0

            if 'exception' in dispos:
                self.exceptions += 1
                successive_exceptions += 1
                if successive_exceptions > max_errors:
                    emsg = "(%s) %s次连续异常, 退出" % (argv_dict.get('unit_folder', ''), max_errors)
                    logger.error(emsg)
                    nautil.dlog.error("emailclient-pop3: %s " % emsg)
                    break
            else:
                successive_exceptions = 0

    def fetch_all(self):
        try:
            self.fetch_all_impl()
            self.p3.quit()
        except Exception,e:
            logger.exception("fetch_all")

class CImapClient(CEmailReceiver):
    def __init__(self, smtp_str, host, user, passwd, **kargs):
        CEmailReceiver.__init__(self,smtp_str, host,user,passwd,**kargs)

    def relogin(self):
        if self.p3:
            self.p3.logout()
            self.p3.close()
            self.p3=None
        try:
            if self.use_ssl:
                self.p3 = imaplib.IMAP4_SSL(self.host, self.port and self.port or imaplib.IMAP4_SSL_PORT)
            else:
                self.p3 = imaplib.IMAP4(self.host, self.port and self.port or imaplib.IMAP4_PORT)
            #self.p3._debugging =1
            self.p3.login(self.user,self.passwd)
        except Exception,e:
            self.p3 = None
            logger.exception("login failed")
        return self.p3 is not None

    def fetch_one(self,which):
        try:
            status, msg= self.p3.fetch(which, '(BODY.PEEK[HEADER])')
            (sFileName,mm)=self.calEmlName(msg[0][1])
            inbox_time = mm.get_date()
            if os.access(sFileName,os.F_OK):
                self.already_exists +=1
                return (sFileName, 'handled', mm.get_date())

            if time.time()-inbox_time > 86400*15:
                return (sFileName,'old',mm.get_date())

            status, msg= self.p3.fetch(which, '(RFC822)')
            open(sFileName,"wb").write(msg[0][1])
            inbox_time = mm.get_date()
            if self.on_new_email(sFileName, inbox_time):
                self.ok_email+=1
            else:
                logger.error("on_new_email failed for %s" % sFileName)
                retries = self.err_records.get(sFileName,0)
                self.err_records[sFileName] = retries+1
                os.unlink(sFileName)
                sFileName=None
            return (sFileName,'new',None)
        except Exception,e:
            logger.exception("fetch_one")
        self.exceptions += 1
        return None, 'exception', None

    def fetch_all_impl(self):
        try:
            result, message = self.p3.select()
            try:
                typ, data = self.p3.search(None,  '(SINCE "%s")' % (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%d-%b-%Y"))
            except Exception,e:
                typ, data = self.p3.search(None,  'ALL')
            msgs = string.split(data[0])
            msgs.reverse()
            for which in msgs:
                handle_ok = False
                try:
                    #logger.info("handling email %s" % str(which))
                    eml_fname,dispos,rztime = self.fetch_one(which)
                except Exception,e:
                    logger.exception('handling email')
                    #self.p3.copy(which,"RESUME_EXCEPT")
                else:
                    pass
                    #if not self.autoDele:
                    #    self.p3.copy(which,handle_ok and "RESUME_OK" or "RESUME_ERR")
                #self.p3.store(which, '+FLAGS', '\\Deleted')
        except Exception,e:
            logger.exception('got msg error')

    def fetch_all(self):
        try:
            self.fetch_all_impl()
            if self.autoDele:
                typ, data = self.p3.search(None,  '(BEFORE "%s")' % (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%d-%b-%Y"))
                msgs = string.split(data[0])
                for which in msgs:
                    self.p3.store(which, '+FLAGS', '\\Deleted')
                self.deleted = len(msgs)
                self.p3.expunge()
        except Exception,e:
            logger.exception("fetch_all")

def serv(protocol, smtpstr, host, port,user, passwd, use_ssl):
    try:
        initlog("/"+argv_dict['unit_folder']+".log")
        #time.sleep(random.random()*60)
        #return 0
        smtpstr = base64.decodestring(smtpstr)
        if protocol=='IMAP':
            p3c = CImapClient(smtpstr,host, user, passwd, **{'use_ssl':use_ssl,'port':port, 'autoDele':argv_dict.get('auto_del',0) } )
        elif protocol=='POP3':
            p3c = CPop3Client(smtpstr,host, user, passwd, **{'use_ssl':use_ssl,'port':port, 'autoDele':argv_dict.get('auto_del',0) } )
        if not p3c.relogin():
            logger.error("######## login failed, please check parameters")
            return 2

        argv_dict['smtp']=p3c.smtp
        p3c.fetch_all()
        p3c.log_statistics()

        #shutil.rmtree(p3c.working_folder)
        return 0
    except Exception,e:
        logger.exception("serv failed")
    return 1


def usage(appname):
    print "Usage: %s pop3|imap email_server port username passwd ssl|nossl smtpstr unitname" % appname

def main(argv):
    if len(argv) != 9:
        usage(argv[0])
        return 101

    global argv_dict
    argv_dict = nautil.json_loads_utf8(argv[8].replace("'", '"'))
    return serv(argv[1],argv[7], argv[2], int(argv[3]), argv[4],argv[5], argv[6]=='ssl')

def main_test(argv):
    time.sleep(random.randint(15,40))
    return 0


def rundispatcher():
    dbhelper.CPDB.init_db_pool('online')
    pldb = dbhelper.CPDB(True)
    u = dbhelper.select_xxx(pldb.cur, "select * from unit_resume_mailbox where unit_id=2")[0]
    argv_dict['unit_folder'] = '2.naren_email_dispatch'
    argv_dict['unit'] = 'naren_email_dispatch'
    argv_dict['unit_id'] = 2
    serv(u.incoming_prot,base64.encodestring(('0`'*5)[:-1]),u.incoming_server, u['incoming_port'],u.incoming_account, u.incoming_pass,u['incoming_ssl'])
    sys.exit(0)

#emailclient.py pop3 owa.hold.founder.com 0 hrit Founder@2011! nossl b3dhLmhvbGQuZm91bmRlci5jb21gMGBocml0YEZvdW5kZXJAMjAxMSFg5LiW57qq5Lq65omN5LmQ5ZutIDxocml0QGZvdW5kZXIuY29tPg==  "{'unit': '北京方正世纪信息系统有限公司', 'auto_del': 0}"
if __name__ == "__main__":
    nautil.dlog.init("emailclient", server='42.120.18.245')
    if 'rundispatcher' in sys.argv:
        rundispatcher()
        sys.exit(0)

    dbhelper.CPDB.init_db_pool('online')
    nautil.dlog.init('emailclient', server='10.241.42.149')
    sys.exit(main(sys.argv))

