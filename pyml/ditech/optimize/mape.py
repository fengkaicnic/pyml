
import pdb

splice = 46

def get_mape(splice, vec):
    with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
        lines = file.readlines()

    total = 0
    mape = 0.0
    for line in lines:
        lst = line.strip().split(',')
        if not int(lst[splice + 1]):
            total += 1
            continue
        if splice == 94:
            # mape += abs(max((int(lst[splice - 2])*vec[0] + int(lst[splice - 1])*vec[1] + int(lst[splice])*vec[2])/2, 1) - int(lst[splice + 1]))/float(lst[splice + 1])
            mape += abs(max(int(lst[splice])/5.0, 1) - int(lst[splice+1]))/float(lst[splice+1])
            total += 1
        else:
            # pdb.set_trace()
            mape += abs(max((int(lst[splice - 2])*vec[0] + int(lst[splice - 1])*vec[1] + int(lst[splice])*vec[2])/2, 1) - int(lst[splice + 1]))/float(lst[splice + 1])
            total += 1

    print splice, mape, total, mape/total
    return mape/total

if __name__ == '__main__':
    splict_lst = [46, 58, 70, 82, 94, 106, 118, 130, 142]
    vec = [0.15, 0.25, 0.65]
    # vec = [0.2989177332553331, 0.4789144524381843, 0.5719877603861732]
    # vec = [0.2769052213098251, 0.4946433222314749, 0.5742530454106655]
    # vecdct = {46:[0.28607274374772995, 0.5087416766984331, 0.5769828307026721],
    #           58:[0.09569064137048533, 0.050930189263226344, 0.8812077694459185],
    #           70:[0.3613283533785241, 0.4071977408487927, 0.4702037421260049],
    #           82:[0.1823497941884067, 0.16381218874299341, 0.7959606315082155],
    #           94:[0.0435486871253602, 0.005141145536468605, 0.09306058598489708],
    #           106:[0.15183960886384784, 0.5067202087705133, 0.6739096218838899],
    #           118:[0.21234428027817198, 0.4191105018550335, 0.5101441374760481],
    #           130:[0.20487059848782752, 0.3173551669474114, 0.5280919420996816],
    #           142:[0.12167453236459091, 0.2379181848610189, 0.5065806691054171]}
    mape = 0.0
    for splice in splict_lst:
        # mape += get_mape(splice, vecdct[splice])
        mape += get_mape(splice, vec)

    print mape/len(splict_lst)
