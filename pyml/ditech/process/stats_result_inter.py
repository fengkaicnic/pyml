# stats result inter

import numpy as np
import pdb

def count_all_num():
    with open('d:/ditech/result_3_inter', 'r') as file:
        lines = file.readlines()

    splice = 46

    num = 0
    hash_dct = {}
    for line in lines:
        lst = line.strip().split(',')

        if np.sum([int(lst[4]), int(lst[6]), int(lst[8])]) > 15:
            num += 1
            if not hash_dct.has_key(lst[0]):
                hash_dct[lst[0]] = {int(lst[2].split('-')[-1]):1}
            else:
                if not hash_dct[lst[0]].has_key(int(lst[2].split('-')[-1])):
                    hash_dct[lst[0]][int(lst[2].split('-')[-1])] = 1
                else:
                    hash_dct[lst[0]][int(lst[2].split('-')[-1])] += 1
    results = []
    for key in hash_dct.keys():
        for key1 in hash_dct[key].keys():
            results.append((key, key1, hash_dct[key][key1]))

    pdb.set_trace()
    results = sorted(results, key=lambda x:int(x[2]), reverse=True)
    for result in results:
        print result

def count_mean():

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


if __name__ == '__main__':

    # count_all_num()
    count_mean()
