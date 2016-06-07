#stats splice
import datetime
import pdb

tdct = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

def discriminate_series(lst):
    typedct = {0.5:1, 0.3:2, 2.0:3, 0.7:4, 3.0:5, 1.5:6}
    nlst = []
    for index, r in enumerate(lst):
        nlst.append((index+1, r))
    nlst = sorted(nlst, key=lambda x:x[1], reverse=True)
    # pdb.set_trace()
    return typedct[round(float(nlst[0][0])/nlst[1][0], 1)]


with open('d:/ditech/all_date_gap_id_splice.csv', 'r') as file:
    lines = file.readlines()

num = 106
t_num = 0
work_num = 0
for line in lines:
    line = line.strip()
    lst = line.split(',')
    tm = datetime.datetime.strptime(lst[2], '%Y-%m-%d')
    # pdb.set_trace()
    tpnum = discriminate_series(lst[num-1:num+2])
    tdct[tpnum] += 1
    if tm.weekday() < 5:
        work_num += 1
    else:
        continue

    if int(lst[num + 2]) >= int(lst[num+1]) :
        # pdb.set_trace()
        t_num += 1
    else:

        print lst[1], lst[num-1:num+6], tm.weekday(), lst[2]

print t_num
print work_num
print tdct
