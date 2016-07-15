
def find_split(seq):
    low = 0
    high = len(seq) - 1
    while high-low > 1:
        mid = (high+low)/2
        if seq[mid] <= seq[high]:
            high = mid
        else:
            low = mid
    return low, high

def find_num(seq, num):
    low, high = find_split(seq)
    if num > seq[-1]:
        start = 0
        end = low
        while start < end:
            mid = (start+end)/2
            if num == seq[mid]:
                return mid
            elif num < seq[mid]:
                end = mid-1
            else:
                start = mid+1
        return start
    else:
        start = high
        end = len(seq) - 1
        while start < end:
            mid = (start+end)/2
            if num == seq[mid]:
                return mid
            elif num < seq[mid]:
                end = mid-1
            else:
                start = mid+1
        return start


if __name__ == '__main__':
    seq = [6, 7, 7, 7, 8, 1, 2, 2, 3, 4, 5]
    find_split(seq)
    index = find_num(seq, 3)
    print index
