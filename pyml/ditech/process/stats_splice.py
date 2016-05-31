#stats splice
import datetime
import pdb

with open('d:/ditech/all_date_gap_id_splice.csv', 'r') as file:
    lines = file.readlines()

num = 70
t_num = 0
work_num = 0
for line in lines:
    line = line.strip()
    lst = line.split(',')
    tm = datetime.datetime.strptime(lst[2], '%Y-%m-%d')
    # pdb.set_trace()
    if tm.weekday() < 5:
        work_num += 1
    else:
        continue
    if int(lst[num + 2]) >= int(lst[num+1]) :
        t_num += 1
    else:
        print lst[1], lst[num-1:num+6], tm.weekday(), lst[2]

print t_num
print work_num
