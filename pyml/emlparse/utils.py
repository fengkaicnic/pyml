#coding:utf8
import time
import sys
import email
import os
import traceback
import time
import argparse
import pdb
import eventlet
from email import utils
import MySQLdb

def get_mail_name(msg):
    pass

def read_from_csv(path):
    pass

def write_table(datas):
    conn = MySQLdb.connect(host='121.40.183.7', user='fengkai', passwd='8e1c7d52557b', db='reply_analyze', use_unicode=True, charset='utf8')
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    try:
        for data in datas:
            datalst = data.split(',')
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