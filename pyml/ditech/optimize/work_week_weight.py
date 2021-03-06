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

workdct = { 46:[0.6970239316443556, 0.6829220961645952, 0.6285213414061811],
          58:[0.09811603211675257, 0.04573460863603951, 0.8758033447626098],
          70:[0.38128247184148545, 0.31797696143795984, 0.4219055113416399],
          82:[0.13804072448159976, 0.14899149245302346, 0.8048571668238751],
          94:[0.049138538022894585, 0.0012389551198577209, 0.09368777773838233],
          106:[0.1252937711219112, 0.570023952903327, 0.596114113484878],
          118:[0.3892284731938833, 0.4307510270130258, 0.4027007527125084],
          130:[0.18057690150072836, 0.3331199212925319, 0.5063683158052499],
          142:[0.3266740299543731, 0.28411173631792974, 0.4049409433224077]}

weekdct = { 46:[0.5183245134044023, 0.004816763193546181, 0.24325439959063688],
          58:[0.4099915701290868, 0.20073885514173406, 0.4644344073898218],
          70:[0.10627774585669314, 0.4503189612979237, 0.9560250499130913],
          82:[0.35729520082706834, 0.7519980455496287, 0.2870267003215481],
          94:[0.1221529729026557, 0.265384217868916, 0.8413344927321071],
          106:[0.06862097988983396, 0.4087818426499731, 0.9922674736019262],
          118:[0.18148398052450965, 0.2633687750561846, 0.6722723409611715],
          130:[0.4966871478785856, 0.0037187568237398994, 0.5885138393861615],
          142:[0.08185398899271268, 0.2111388154506827, 0.23710897038531964]}

works = [25, 27, 29]
weeks = [23, 31]

try:
    with open('d:/ditech/result_3_inter_test', 'r') as file:
        lines = file.readlines()
    
    results = []
    tnum = 0
    num = 0
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        if int(lst[2].split('-')[-2]) in works:
            vec = workdct[int(lst[2].split('-')[-1])]
        else:
            vec = weekdct[int(lst[2].split('-')[-1])]
        rst = []
        rst.append(lst[1])
        rst.append(lst[2])
        a1 = np.array([int(lst[8]), int(lst[6]), int(lst[4])])
        rst.append(max(np.sum(vec*a1)/2.0, 1))

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
    with open('d:/ditech/work_week.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    print num
except:
    traceback.print_exc()

