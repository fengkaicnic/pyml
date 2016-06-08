#date gap plot to show

import numpy as np
import time
import matplotlib.pyplot as plt
import pdb

st = time.time()

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    lines = file.readlines()

splice_dct = {}

for line in lines:
    line = line.strip()
    lst = line.split(',')

    if splice_dct.has_key(lst[0]):
        splice_dct[lst[0]].append(map(lambda x:int(x), lst[2:]))
    else:
        splice_dct[lst[0]] = [map(lambda x:int(x), lst[2:])]

show_hash = '929ec6c160e6f52c20a4217c7978f681'

works = [4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21]
weeks = [8, 9, 15, 16]

x_label = [i for i in range(1, 145)]
plt.figure(figsize=(144, 5))
for index, rs in enumerate(splice_dct[show_hash]):
    if index not in works:
        continue
    plt.plot(x_label, rs)

plt.xlabel('time')
plt.ylabel('Num')
plt.legend()
plt.show()

ed = time.time()

print ed - st
