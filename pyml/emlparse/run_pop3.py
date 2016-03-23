import os
import ConfigParser
import multiprocessing
import subprocess

def run_pop_mail(path, num, user, password, pop3server):
    cmd = 'python pop3email.py --path %s --num %s --user %s --password %s --pop3server %s' \
           % (path, num, user, password, pop3server)
    # cmd = 'python testsub.py'
    print cmd
    s = subprocess.Popen(cmd)
    print s.communicate()

cf = ConfigParser.ConfigParser()

cf.read('pop.ini')

secs = cf.sections()
print 'setction:', secs
for sec in secs:
    path = cf.get(sec, 'path')
    num = cf.get(sec, 'num')
    user = cf.get(sec, 'user')
    password = cf.get(sec, 'password')
    pop3server = cf.get(sec, 'pop3server')
    run_pop_mail(path, num, user, password, pop3server)