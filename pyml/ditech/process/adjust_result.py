import utils
import traceback

try:
    with open('d:/ditech/gbdt_model_result.csv', 'r') as file:
        lines = file.readlines()

    results = []
    num = 0
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        rst = []
        rst.append(lst[0])
        rst.append(lst[1])
        num = int(float(lst[2])/3)
        if not num:
            num = 1
        rst.append(num)

        results.append(','.join(map(lambda x:str(x), rst)))

    with open('d:/ditech/gbdt_result_3nt.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print num
except:
    traceback.print_exc()

