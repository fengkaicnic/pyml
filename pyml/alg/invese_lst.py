#invese seq

def invese_lst(seq, p):
    if not seq:
        print 'seq is null'
        return

    p2 = -1
    p1 = -1
    while p != -1:
        p1 = lst[p][1]  #p1 = p.next
        lst[p][1] = p2  #p.next = p2
        p2 = p          #p2 = p
        p = p1          #p = p1
    print seq
    while p2 != -1:
        print lst[p2][0]
        p2 = lst[p2][1]

if __name__ == '__main__':

    lst = [[1, 1], [2, 3], [3, 4], [4, 2], [5, -1]]
    p = 0
    while p != -1:
        print lst[p][0]
        p = lst[p][1]
    invese_lst(lst, 0)
