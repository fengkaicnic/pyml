#gap and splice to check

import pdb

with open('d:/ditech/all_date_splice.csv', 'r') as file:
    lines = file.readlines()

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    rlines = file.readlines()

hash_id = 'd05052b4bda7662a084f235e880f50fa'
splice = 46

for line in rlines:
    lst = line.strip().split(',')

    if lst[0] == hash_id:
        # pdb.set_trace()
        print lst[splice-2:splice+2]
