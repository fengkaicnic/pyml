#coding:utf-8
#!/usr/bin/python
import json
#Function:Analyze jsons script
#Json is a script can descript data structure as xml, 
#for detail, please refer to "http://jsons.org/jsons-zh.html".

#Note:
#1.Also, if you write jsons script from python,
#you should use dump instead of load. pleaser refer to "help(jsons)".

#jsons file:
#The file content of temp.jsons is:
#{
# "name":"00_sample_case1",
# "description":"an example."
#}
#f = file("temp.jsons");
#s = jsons.load(f)
#print s
#f.close
with open('d:/practice.json') as file:
    sc = file.readline()
    s = json.loads(sc)
    #print s.keys()
    #for key in s.keys():
        #print key
        #print s[key]
    for key in s["workExperienceList"][0].iterkeys():
        print key + ':'
        print s["workExperienceList"][0][key]
    
