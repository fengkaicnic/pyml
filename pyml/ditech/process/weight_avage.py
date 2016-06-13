import utils
import traceback
import numpy as np

wedct = { 46:[0.28607274374772995, 0.5087416766984331, 0.5769828307026721],
          58:[0.09569064137048533, 0.050930189263226344, 0.8812077694459185],
          70:[0.3613283533785241, 0.4071977408487927, 0.4702037421260049],
          82:[0.1823497941884067, 0.16381218874299341, 0.7959606315082155],
          94:[0.0435486871253602, 0.005141145536468605, 0.09306058598489708],
          106:[0.15183960886384784, 0.5067202087705133, 0.6739096218838899],
          118:[0.21234428027817198, 0.4191105018550335, 0.5101441374760481],
          130:[0.20487059848782752, 0.3173551669474114, 0.5280919420996816],
          142:[0.12167453236459091, 0.2379181848610189, 0.5065806691054171]}

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
        a1 = np.array([int(lst[8]), int(lst[6]), int(lst[4])])
        rst.append(max(np.sum(wedct[int(lst[2].split('-')[-1])]*a1)/2.0, 1))

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
    with open('d:/ditech/result_last_106_weight.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print num
except:
    traceback.print_exc()

