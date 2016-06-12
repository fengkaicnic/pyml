
splice = 46

def get_mape(splice):
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
            mape += abs(max((int(lst[splice - 2])*0.1 + int(lst[splice - 1])*0.25 + int(lst[splice])*0.65)/6, 1) - int(lst[splice + 1]))/int(lst[splice + 1])
#             mape += abs(max(int(lst[splice])/5.0, 1) - int(lst[splice+1]))/int(lst[splice+1])
            total += 1
        else:
            mape += abs(max((int(lst[splice - 2])*0.1 + int(lst[splice - 1])*0.25 + int(lst[splice])*0.65)/3, 1) - int(lst[splice + 1]))/int(lst[splice + 1])
            total += 1

    print splice, mape, total, mape/total

if __name__ == '__main__':
    splict_lst = [46, 58, 70, 82, 94, 106, 118, 130, 142]
    for splice in splict_lst:
        get_mape(splice)
