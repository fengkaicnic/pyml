#coding:utf8

import os
import shutil

import time

data_path = 'd:/naren/data/'
new_data_path = 'd:/naren/new-data/resumes/'
start = time.time()
new_data_read = 'd:/naren/new-data/read/'
new_data_reco = 'd:/naren/new-data/recommend/'
new_data_con = 'd:/naren/new-data/confirm/'

read_dct = {}
confirm_dct = {}
recommend_dct = {}

for name in os.listdir(data_path + 'read'):
    read_dct[name] = 0

for name in os.listdir(new_data_path + 'read'):
    if not read_dct.has_key(name):
        shutil.copyfile(new_data_path + 'read/' +name, new_data_read + name)

for name in os.listdir(data_path + 'recommend'):
    recommend_dct[name] = 0

for name in os.listdir(new_data_path + 'recommend'):
    if not recommend_dct.has_key(name):
        shutil.copyfile(new_data_path + 'recommend/' + name, new_data_reco + name)

for name in os.listdir(data_path + 'confirm'):
    confirm_dct[name] = 1

for name in os.listdir(new_data_path + 'confirm'):
    if not confirm_dct.has_key(name):
        shutil.copyfile(new_data_path + 'confirm/' + name, new_data_con + name)

end = time.time()

print (end - start)