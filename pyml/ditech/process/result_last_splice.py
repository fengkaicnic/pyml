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
        if int(lst[4]) < 5:
            num += 1
            rst.append(int(lst[4])/3 + 1)
        else:
            rst.append(int(lst[4]))
            print lst[3:]
        
        results.append(','.join(map(lambda x:str(x), rst)))
        
    with open('d:/ditech/result_last_53.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print num
except:
    traceback.print_exc()

