import utils
import traceback

try:
    with open('d:/ditech/result_3_inter', 'r') as file:
        lines = file.readlines()
    
    results = []
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        rst = []
        rst.append(lst[1])
        rst.append(lst[2])
        rst.append(int(lst[4])/5 + 1)
        
        results.append(','.join(map(lambda x:str(x), rst)))
        
    with open('d:/ditech/result_last_5.csv', 'wb') as file:
        file.writelines('\n'.join(results))
    
except:
    traceback.print_exc()
    