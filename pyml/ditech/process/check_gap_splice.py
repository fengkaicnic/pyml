#gap and splice to check

import pdb

with open('d:/ditech/all_date_splice.csv', 'r') as file:
    lines = file.readlines()

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    rlines = file.readlines()

hash_id = 'd4ec2125aff74eded207d2d915ef682f'
splice = 142

for line in rlines:
    lst = line.strip().split(',')

    if lst[0] == hash_id:
        # pdb.set_trace()
        print lst[splice-2:splice+2]
