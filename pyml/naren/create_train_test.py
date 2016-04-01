#coding:utf8
import random

tests = []
with open('d:/naren/recommend/data', 'r') as file:
    lines = file.readlines()

trains = []

for line in lines:
    if random.randint(1, 3) == 1:
        tests.append(line.strip())
    else:
        trains.append(line.strip())

with open('d:/naren/recommend/train-data', 'wb') as file:
    file.writelines('\n'.join(trains))

with open('d:/naren/recommend/test-data', 'wb') as file:
    file.writelines('\n'.join(tests))