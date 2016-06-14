
import traceback
import pdb

import numpy as np
import pickle

file = open('hash_splice_param', 'r')

hash_splice_dct = pickle.load(file)

try:
    with open('d:/ditech/result_3_inter_test', 'r') as file:
        lines = file.readlines()

    results = []
    tnum = 0
    num = 0
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        rst = []
        rst.append(lst[1])
        rst.append(lst[2])
        # pdb.set_trace()
        vec = hash_splice_dct[lst[0]][int(lst[2].split('-')[-1])]
        a1 = np.array([int(lst[8]), int(lst[6]), int(lst[4])])
        rst.append(max(np.sum(vec*a1)/2.0, 1))

# #         if (lst[2].split('-')[-1] == '146' or lst[2].split('-')[-1] == '106') and np.mean([int(lst[4]), int(lst[6]), int(lst[8])]) > 50:
# #         # if lst[2].split('-')[-1] == '46' or lst[2].split('-')[-1] == '106':
# #             rst.append(max(int(lst[4]), 1))
# #             print lst[8], lst[6], lst[4]
# #             tnum += 1
#
#         if lst[2].split('-')[-1] == '94':
# #             rst.append(max(int(lst[4])/5, 1))
#             rst.append(int(max((int(lst[4])*0.65 + int(lst[6])*0.25 + int(lst[8])*0.15)/6, 1)))
#         else:
#             rst.append(int(max((int(lst[4])*0.65 + int(lst[6])*0.25 + int(lst[8])*0.15)/2, 1)))
# #         else:
# #             rst.append(int(lst[4]))
# #             print lst[3:]

        results.append(','.join(map(lambda x:str(x), rst)))
    with open('d:/ditech/hash_splice_weight.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print num
except:
    traceback.print_exc()

