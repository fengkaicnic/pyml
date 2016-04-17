import os
import time

start = time.time()

store_code_lst = [1, 2, 3, 4, 5, 'all']

import store_gbdt

result = []

for code in store_code_lst:
    lst = store_gbdt.predict_data(code)
    result = result + lst

print len(result)

with open('d:/tianchi/result.csv', 'wb') as file:
    file.writelines('\n'.join(result))
    
end = time.time()

print (end - start)