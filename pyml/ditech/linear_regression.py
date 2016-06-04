import numpy as np 
from sklearn import linear_model
import time

start = time.time()

clf = linear_model.LinearRegression()

splice_lst = []
with open('d:/ditech/citydata/read_me_1.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        splice_lst.append(int(line.strip().split('-')[-1]))

splice_lst = list(set(splice_lst))

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    lines = file.readlines()

for splice in splice_lst:
    result = []
    hash_lst = []
    print splice
    for line in lines:
        line = line.strip()
        rlst = line.split(',')
        lst = map(lambda x:int(x), rlst[splice-2:splice+2])
        if np.mean(lst) > 10:
            result.append(lst)
            hash_lst.append(rlst[:2])
    
    rst = np.array(result)
    clf.fit(rst[:,:-1], rst[:,-1])
    print clf.coef_, clf.intercept_
    num = 0
    if splice == 70:
        for index, rs in enumerate(rst):
            print rs, hash_lst[index]
            print clf.predict(rs[:-1])
            num += 1
        print num
        print '======================================================================'
        
en = time.time()

print en - start
