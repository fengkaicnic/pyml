import os
import time

start = time.time()

store_code_lst = [1, 2, 3, 4, 5, 'all']

import store_gbdt

result = []
period = 14

for code in store_code_lst:
    lst = store_gbdt.predict_data(code, period)
    result = result + lst

print len(result)

with open('d:/tianchi/result_jhs_per_%d.csv' % period, 'wb') as file:
    file.writelines('\n'.join(result))
    
end = time.time()

print (end - start)