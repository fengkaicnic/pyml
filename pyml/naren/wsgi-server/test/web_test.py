# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:24:02 2015

@author: yugang.zhou
"""

import requests,json
import urllib2
import urllib
import time

def web_test(service, test_value):
    #url = "http://121.40.251.226:9301/"
    url = "http://%s/" % service
    if test_value == 1:
        text = "结巴分词测试"
        #method为cut为普通分词，posseg_cut为带有词性标注的分词
        data = {'text': text,'method':'posseg_cut'}
        url = url+"poscut"
    elif test_value == 2:
        text = "具有较强的英文口语和写作能力，熟练使用Microsoft office办公软件；工作认真，善于沟通"
        data = {'text': text}
        url = url+"resumeindex"
    elif test_value == 3:
        text = "具有较强的英文口语和写作能力，熟练使用Microsoft office办公软件"
        data = {'text': text}
        url = url+"jobdespindex"
    elif test_value == 4:
        text = "具有较强的英文口语和写作能力，熟练使用Microsoft office办公软件"
        data = {'text': text}
        url = url+"infoextract"
    elif test_value == 5:
        textlist =  ["具有较强的英文口语和写作能力，熟练使用Microsoft office办公软件；工作认真，善于沟通，重视团队合作中的反复探讨，沟通和协作，从中我不但可以得到收获的喜悦，更能够在一次次的实践中不断得到提高。",  "dsdsdsd"]
        text = "熟悉办公软件"
        data = {'text': text, 'textlist': textlist}
        url = url+"matchtext"
    elif test_value == 6:
        jd1 = "熟练使用Office"
        jd2 = "熟悉办公软件"
        data = {'jd1': jd1, 'jd2': jd2}
        url = url+"jobdespmatch"
    elif test_value == 7:
        job = "销售经理（母婴/快消品/奶粉/婴童）"
        work = '市场销售经理'
        data = {'job':job,'work':work,'high':1.0,'low':0.0}
        url = url+"positionmatch"
    elif test_value == 8:
        position_name = "北京-java工程师"
        data = {'position_name': position_name}
        url = url+"positionclean"
    elif test_value == 9:
        position_name = "我需要北京java工程师"
        data = {'position_name': position_name}
        url = url+"positionproject"
    elif test_value == 10:
        position_name = "java工程师"
        data = {'position_name': position_name}
        url = url+"positionindex"
    elif test_value == 11:
        position_name = "java工程师"
        data = {'position_name': position_name}
        url = url+"positionskill"
    elif test_value == 12:
        corp_name = "纳人网络公司"
        corp_data = '从事招聘的技术服务公司'
        data = {'corp_name': corp_name,'corp_data': corp_data}
        url = url+"corpindex"
    elif test_value == 13:
        corp_name = "前程无忧网络公司"
        corp_data = '从事招聘的技术服务公司'
        job_name = "微软销售工程师"
        job_data = '熟练掌握java，熟悉spring框架'
        data = {'job_name': job_name,'job_data': job_data,'corp_name': corp_name,'corp_data': corp_data}
        url = url+"retrieveterms"
    elif test_value == 14:
        corp_name = "前程无忧网络公司"
        corp_data = '从事招聘的技术服务公司'
        job_name = "java工程师"
        job_data = '熟练掌握java，熟悉spring框架'
        data = {'job_name': job_name,'job_data': job_data,'corp_name': corp_name,'corp_data': corp_data}
        url = url+"searchterms"
    elif test_value == 100:  #it last long time,test separately
        corp_name = "纳人网络公司"
        corp_data = '从事招聘的技术服务公司'
        data = {'corp_name': corp_name,'corp_data': corp_data}
        url = url+"corpsimilar"
    else:
        return
        
    res = requests.post(url, data)
    
    print 'connect',test_value,res.status_code
    jret = json.loads(res.content,encoding='utf8')
    
    for item in jret:
        print 'post test',item,jret[item]


def rpc_test():
    import jsonrpclib
    server1 = jsonrpclib.Server('http://121.40.251.226:4000')
    
    result = server1.echo('hello')
    
    print len(result)
    

def package_test():
    sys.path.append('..')
    import match_base
    
    corp_name = "去哪儿网"
    corp_data = '从事招聘的技术服务公司'
    job_name = "微软销售工程师"
    job_data = '熟练掌握java，熟悉spring框架'
    
    #result = match_base.retrieve_terms_api(job_name,job_data,corp_name,corp_data)
    result = match_base.posseg_cut(job_name)
    result = match_base.info_extract_api(job_data)
    
    print 'end test',result
    
# web_test.py 42.120.18.245:9301
if __name__ == "__main__":
    import sys
    #service = sys.argv[1]
    service = '121.40.251.226:9301'
    
    for i in xrange(1, 16):
        time1 = time.time()
        web_test(service, i)
        print 'time',time.time()-time1
        
    #rpc_test()
    #package_test()
    
    