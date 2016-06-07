#change ratio
import pdb
import time

start = time.time()

with open('d:/ditech/citydata/read_me_1.txt', 'r') as file:
    lines = file.readlines()
splice_lst = []
for line in lines:
    line = line.strip()
    splice_lst.append(line.split('-')[-1])
work = [4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21]
week = [8, 9, 15, 16]
splice_lst = list(set(splice_lst))

with open('d:/ditech/all_date_splice_order.csv', 'r') as file:
    lines = file.readlines()

ratio_dct = {}
for line in lines:
    line = line.strip()
    lst = line.split(',')

    if int(lst[1].split('-')[-1]) in work:
        type = 'work'
    elif int(lst[1].split('-')[-1]) in week:
        type = 'week'
    else:
        continue
    if not ratio_dct.has_key(lst[0]):
        ratio_dct[lst[0]] = {}
        for splice in splice_lst:
            ratio_dct[lst[0]][splice+'-'+type] = [(lst[int(splice)-1], lst[int(splice)], lst[int(splice)+1])]
    else:
        for splice in splice_lst:
            if not ratio_dct[lst[0]].has_key(splice+'-'+type):
                ratio_dct[lst[0]][splice+'-'+type] = [(lst[int(splice)-1], lst[int(splice)], lst[int(splice)+1])]
            else:
                ratio_dct[lst[0]][splice+'-'+type].append((lst[int(splice)-1], lst[int(splice)], lst[int(splice)+1]))

with open('d:/ditech/result_3_inter', 'r') as file:
    rlines = file.readlines()

week1 = [24, 30]
work1 = [22, 26, 28]

for line in rlines:
    line = line.strip()
    lst = line.split(',')

    if int(lst[2].split('-')[-2]) in work1:
        print lst[6], lst[4]
        print ratio_dct[lst[0]][lst[2].split('-')[-1]+'-'+'work']
    else:
        print lst[6], lst[4]
        print ratio_dct[lst[0]][lst[2].split('-')[-1]+'-'+'week']

ed = time.time()

print ed - start
