#encdoing:utf-8

import weibosp
import urllib
import urllib2
import sys
import getWeiBoPage
sys.setdefaultencoding('utf-8')
import pdb
pdb.set_trace()

username = 'fengkaibnu@sina.cn'
pwd = 'woxihuanni'

# WBLogin = weibosp.weiboLogin()
# WBLogin.login(username, pwd)

WBmsg = getWeiBoPage.getWeiboPage()
# url = 'http://weibo.com/chenshake'
url = 'http://weibo.com/?topnav=1&wvr=6&mod=logo'

WBmsg.get_firstpage(url)
WBmsg.get_secondpage(url)
WBmsg.get_thirdpage(url)