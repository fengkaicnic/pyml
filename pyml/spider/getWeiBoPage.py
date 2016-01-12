#encoding:utf-8
import urllib
import urllib2
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

class getWeiboPage:
    body = {
        '__rnd':'',
        '_k':'',
        '_t':'0',
        'count':'50',
        'end_id':'',
        'max_id':'',
        'page':1,
        'pagebar':'',
        'pre_page':'0',
        'uid':''
    }
    uid_list = []
    charset = 'utf8'

    def get_msg(self,uid):
        getWeiboPage.body['uid'] = uid
        url = self.get_url(uid)
        self.get_firstpage(url)
        self.get_secondpage(url)
        self.get_thirdpage(url)
    def get_firstpage(self,url):
        import pdb
        pdb.set_trace()
        getWeiboPage.body['pre_page'] = getWeiboPage.body['page']-1
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
                   'cookie':'SINAGLOBAL=7988859217148.274.1431684154096; TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013; TC-V5-G0=2030a6a079209a7c31934a48cfe2f5f6; _s_tentry=login.sina.com.cn; Apache=4701654438395.053.1452481470182; ULV=1452481470233:158:3:1:4701654438395.053.1452481470182:1452132590680; TC-Page-G0=9183dd4bc08eff0c7e422b0d2f4eeaec; YF-V5-G0=a2489c19ecf98bbe86a7bf6f0edcb071; YF-Page-G0=416186e6974c7d5349e42861f3303251; YF-Ugrow-G0=1eba44dbebf62c27ae66e16d40e02964; login_sid_t=d6699aedc95165e8b59b7ec2702e9657; UOR=,,login.sina.com.cn; myuid=1789397551; WBtopGlobal_register_version=d0bee671faf5f116; SUP=cv%3D1%26bt%3D1452515437%26et%3D1452601837%26d%3Dc909%26i%3Dbc04%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D1789397551%26name%3Dfengkaibnu%2540sina.cn%26nick%3D%25E5%25A4%25A7%25E7%25AC%25A8%26fmp%3D%26lcp%3D; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhYEKY_bHIOC5Tm2zLZlMBd5JpX5K2t; SUHB=02M-goahrG8WQw; ALF=1453120237; SSOLoginState=1452515437; un=fengkaibnu@sina.cn'}
        url = url +urllib.urlencode(getWeiboPage.body)
#         req = urllib2.Request(url, headers=headers)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        print text
        self.writefile('./output/text1',text)        
        self.writefile('./output/result1',eval("u'''"+text+"'''"))
        
    def get_secondpage(self,url):
        getWeiboPage.body['count'] = '15'
    #    getWeiboPage.body['end_id'] = '3490160379905732'
    #    getWeiboPage.body['max_id'] = '3487344294660278'
        getWeiboPage.body['pagebar'] = '0'
        getWeiboPage.body['pre_page'] = getWeiboPage.body['page']

        url = url +urllib.urlencode(getWeiboPage.body)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        self.writefile('./output/text2',text)        
        self.writefile('./output/result2',eval("u'''"+text+"'''"))
    def get_thirdpage(self,url):
        getWeiboPage.body['count'] = '15'
        getWeiboPage.body['pagebar'] = '1'
        getWeiboPage.body['pre_page'] = getWeiboPage.body['page']

        url = url +urllib.urlencode(getWeiboPage.body)
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        text = result.read()
        self.writefile('./output/text3',text)        
        self.writefile('./output/result3',eval("u'''"+text+"'''"))
    def get_url(self,uid):
        url = 'http://weibo.com/' + uid + '?from=otherprofile&wvr=3.6&loc=tagweibo'
        return url
    def get_uid(self,filename):
        fread = file(filename)
        for line in fread:
            getWeiboPage.uid_list.append(line)
            print line
            time.sleep(1)
    def writefile(self,filename,content):
        fw = file(filename,'w')
        fw.write(content)
        fw.close()