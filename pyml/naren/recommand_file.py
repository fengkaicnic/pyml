import os
import json
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf8')

path_confirm = 'd:/naren/data/confirm/'
path_read = 'd:/naren/data/read/'
path_recommand = 'd:/naren/data/recommend/'
company_path = 'd:/naren/data/search.json'

company_confirm = {}
company_read = {}
company_recommand = {}
company_info = {}
company_per = {}

def load_company(company_path):
    with open(company_path, 'r') as file:
        lines = file.readlines()
        listobj = ''.join(lines)
        listobj = eval(listobj)
    for comp_dct in listobj:
        company_info[comp_dct['position_id']] =comp_dct['position_name']

def stastic_data(path, dct):
    for fname in os.listdir(path):
        company_id = fname.split('-')[0]
        profile_id = fname.split('-')[1]
        profile_id = profile_id.split('.')[0]
        if not dct.has_key(company_id):
            dct[company_id] = 1
        else:
            dct[company_id] += 1

stastic_data(path_recommand, company_recommand)
stastic_data(path_read, company_read)
stastic_data(path_confirm, company_confirm)

for key in company_confirm.iterkeys():
    print key,':',company_confirm[key]

for key in company_recommand.iterkeys():
    print key,':',company_recommand[key]


load_company(company_path)


num = 0
recom_set = set()
for key in company_read.iterkeys():
    num += 1
    print key,':',company_read[key],'|',company_recommand.get(key, 0),'|',company_confirm.get(key, 0)
    # pdb.set_trace()
    company_per[key] = [float(company_recommand.get(key, 0))/float(company_read.get(key, 0.001)),\
                        float(company_confirm.get(key, 0))/float(company_recommand.get(key, 0.001)),\
                        company_read.get(key, 0.001), company_recommand.get(key, 0.001), company_confirm.get(key, 0)]
    print company_per[key]
    print company_info.get(int(key), 'None')
    recom_set.add(company_info.get(int(key), 'None'))

company_sortper = sorted(company_per.items(), key=lambda item:item[1][1], reverse=True )

for item in company_sortper:
    print company_info.get(int(item[0]), 'None'), item[1]
print num
print len(recom_set)

items = company_info.items()
print len(items)
com_set = set()
for item in items:
    com_set.add(item[1].lower())

print len(com_set)
