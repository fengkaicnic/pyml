import utils
import numpy as np

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    lines = file.readlines()

mslst = []
for line in lines:
    lst = line.strip().split(',')
    mslst.append((np.mean(map(lambda x:int(x), lst[44:])), np.std(map(lambda x:int(x), lst[44:])), lst[0], lst[1]))

mslst = sorted(mslst, key=lambda x:x[0])

for rs in mslst:
    print rs
