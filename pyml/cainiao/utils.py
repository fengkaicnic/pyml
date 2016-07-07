
import numpy as np

R = 6378137
pie = 3.14
def compute_tm(wangdian, songdian):
    # pdb.set_trace()
    lng = wangdian[0]
    lat = wangdian[1]
    lng1 = songdian[0]
    lat1 = songdian[1]
    deltalat = (lat - lat1)/2
    deltalng = (lng - lng1)/2
    S = 2*R*np.arcsin(np.sqrt(np.sin(pie*deltalat/180)**2 + np.cos(pie*lat/180)*np.cos(pie*lat1/180)*np.sin(pie*deltalng/180)*np.sin(pie*deltalng/180)))
    # pdb.set_trace()
    tm = S/250
    return (songdian, tm)


wangdian_dct = {}
peisongdian_dct = {}
shanghu_dct = {}

def get_didian():
    with open('d:/cainiao/wangdian.csv', 'r') as file:
        lines = file.readlines()
        lines = lines[0].strip().split('\r')
        for line in lines[1:]:
            lst = line.strip().split(',')
            wangdian_dct[lst[0]] = [(float(lst[1]), float(lst[2]))]

    with open('d:/cainiao/peisongdian.csv', 'r') as file:
        lines = file.readlines()
        lines = lines[0].strip().split('\r')
        for line in lines[1:]:
            lst = line.strip().split(',')
            peisongdian_dct[lst[0]] = [float(lst[1]), float(lst[2])]

    with open('d:/cainiao/shanghu.csv', 'r') as file:
        lines = file.readlines()
        lines = lines[0].strip().split('\r')
        for line in lines[1:]:
            lst = line.strip().split(',')
            shanghu_dct[lst[0]] = [float(lst[1]), float(lst[2])]


def encode_didian():

    pass
