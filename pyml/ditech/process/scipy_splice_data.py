import numpy as np 
from sklearn import linear_model
import time
from scipy import stats

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
    total = 0
    t9 = 0
    t1 = 0
    nro = 0
    for line in lines:
        line = line.strip()
        rlst = line.split(',')
        lst = map(lambda x:int(x), rlst[splice-2:splice+2])
        if np.mean(lst) < 5:
            continue
        norm = stats.norm(np.mean(lst), np.std(lst))
        total += 1
#         print lst, norm.cdf(lst[-1])
        nro += norm.cdf(lst[-1])
        if norm.cdf(lst[-1]) > 0.9:
            t9 += 1
        elif norm.cdf(lst[-1]) < 0.1:
            t1 += 1
    
    print total, t9, t1, nro/total
    print '================================================================'
        
#         if np.mean(lst) > 10:
#             result.append(lst)
#             hash_lst.append(rlst[:2])
    
#     rst = np.array(result)
#     clf.fit(rst[:,:-1], rst[:,-1])
#     print clf.coef_, clf.intercept_
#     num = 0
#     if splice == 70:
#         for index, rs in enumerate(rst):
#             print rs, hash_lst[index]
#             print clf.predict(rs[:-1])
#             num += 1
#         print num
#         print '======================================================================'
        
en = time.time()

print en - start
