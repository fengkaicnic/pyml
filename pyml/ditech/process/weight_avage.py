import utils
import traceback

try:
    with open('d:/ditech/result_3_inter', 'r') as file:
        lines = file.readlines()
    
    results = []
    num = 0
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        rst = []
        rst.append(lst[1])
        rst.append(lst[2])

        rst.append(max((int(lst[4])*0.65 + int(lst[6])*0.2 + int(lst[8])*0.15), 1))
#         else:
#             rst.append(int(lst[4]))
#             print lst[3:]
        
        results.append(','.join(map(lambda x:str(x), rst)))
        
    with open('d:/ditech/result_last_weight.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print num
except:
    traceback.print_exc()

