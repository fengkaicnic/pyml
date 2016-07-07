import utils
import numpy as np

utils.get_didian()
wangdian_dct = utils.wangdian_dct
peisongdian_dct = utils.peisongdian_dct
shanghu_dct = utils.shanghu_dct

couriers = np.array((300, 3))

with open('d:/cainiao/tongcheng.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].split('\r')
    for line in lines:
        lst = line.strip().split(',')


