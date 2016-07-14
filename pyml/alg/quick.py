
l = [5, 1, 3, 8, 9, 4, 7, 6]

def path_sort(list, start_index, end_index):
    flag = list[end_index]
    i = start_index - 1
    for j in range(start_index, end_index):
        if list[j] > flag:
            pass
        else:
            i += 1
            tmp = list[i]
            list[i] = list[j]
            list[j] = tmp
    tmp = l[end_index]
    l[end_index] = l[i+1]
    l[i+1] = tmp
    return i+1

def Quick_sort(list,start_index,end_index):
    if start_index >= end_index:
        return
    middle = path_sort(list, start_index, end_index)
    Quick_sort(list, start_index, middle-1)
    Quick_sort(list, middle+1, end_index)
    print(l)
Quick_sort(l, 0, len(l)-1)
