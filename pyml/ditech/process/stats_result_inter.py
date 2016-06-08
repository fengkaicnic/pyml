# stats result inter

import numpy as np

with open('d:/ditech/result_3_inter', 'r') as file:
    lines = file.readlines()

splice = 46

num = 0
for line in lines:
    lst = line.strip().split(',')

    if lst[2].split('-')[-1] == str(splice):
        if np.mean([int(lst[4]), int(lst[6]), int(lst[8])]) > 5:
            num += 1
            print lst[8], lst[6], lst[4]

print num
