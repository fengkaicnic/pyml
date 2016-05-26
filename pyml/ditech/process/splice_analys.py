import utils
import traceback

splice_lst = []
with open('d:/ditech/citydata/read_me_1', 'r') as file:
    slines = file.readlines()
    for line in slines:
        splice_lst.append(line.strip().split('-')[-1])

splice_lst = map(lambda x:int(x), splice_lst)

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    lines = file.readlines()

for line in lines:
    lst = line.strip().split(',')

