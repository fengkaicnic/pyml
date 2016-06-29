#coding:utf8
import random

tests = []
with open('data/traindata', 'r') as file:
    lines = file.readlines()

trains = []

num = 0

for index, line in enumerate(lines):
    if index > 192:
        break
    num += 1
    # if num == 5721:
    #     break
    if random.randint(1, 3) == 1:
        tests.append(line.strip())
    else:
        trains.append(line.strip())

with open('d:/naren/recommend/train-data', 'wb') as file:
    file.writelines('\n'.join(trains))

with open('d:/naren/recommend/test-data', 'wb') as file:
    file.writelines('\n'.join(tests))