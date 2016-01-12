#encoding:utf8
 
import re
import pdb
  
pdb.set_trace()
p = re.compile(u"[\u4e00-\u9fa5]*")
  
with open('output/text1') as f:
    for line1 in f.readlines():
        line = line1.decode('utf8') 
        results = p.findall(line)
        for index, result in enumerate(results):
            if result:
                print result
        print '============the ', index, '================'

# import re  
# import pdb
# pdb.set_trace()
# source = "s2f程序员杂志一2d3程序员杂志二2d3程序员杂志三2d3程序员杂志四2d3"  
# temp = source.decode('utf8')  
# xx=u"[\u4e00-\u9fa5]*"  
# pattern = re.compile(xx)  
# results =  pattern.findall(temp)  
# for result in results :  
#     if result:
#         print result 