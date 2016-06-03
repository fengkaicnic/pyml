#generate district
#mape

import numpy as np

with open('d:/ditech/district_splice_work_gap.csv', 'r') as file:
    lines = file.readlines()

totalgap = 0
for line in lines:
    line = line.strip()
    lst = line.split(',')
    ls = np.array(map(lambda x:int(x), lst[2:]))
    mean = ls.mean()
    if mean < 1:
        mean = 1
    gap = 0
    for tm in ls:
        if tm == 0:
            continue
        gap += abs(mean*0.5 - tm)/tm

    totalgap += gap/len(ls)

print totalgap
print totalgap/len(lines)
