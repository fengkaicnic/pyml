#supplement splice zero

def add_zero():
    with open('d:/ditech/splice_series.csv', 'r') as file:
        lines = file.readlines()

    results = []
    for line in lines:
        lst = line.strip().split(',')

        while len(lst) < 23:
            lst.append('0')

        results.append(','.join(lst))

    with open('d:/ditech/splice_series.csv', 'wb') as file:
        file.writelines('\n'.join(results))


def sorted_splice():
    with open('d:/ditech/splice_series.csv', 'r') as file:
        lines = file.readlines()

    results = []
    splice_key = ''
    sorted_lst = []
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        if splice_key != lst[0]:
            if len(sorted_lst) == 0:
                splice_key = lst[0]
                sorted_lst = [lst]
            else:
                sorted_lst = sorted(sorted_lst, key=lambda item:int(item[2]))
                for ls in sorted_lst:
                    results.append(','.join(ls))
                sorted_lst = [lst]
                splice_key = lst[0]
        else:
            sorted_lst.append(lst)

    sorted_lst = sorted(sorted_lst, key=lambda item:int(item[2]))
    for ls in sorted_lst:
        results.append(','.join(ls))

    with open('d:/ditech/splice_sor_series.csv', 'wb') as file:
        file.writelines('\n'.join(results))


if __name__ == '__main__':
    sorted_splice()
