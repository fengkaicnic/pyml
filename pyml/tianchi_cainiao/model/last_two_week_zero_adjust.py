import utils
import traceback
import pdb

import time

start = time.time()

with open('d:/tianchi/result_last_two_week-direct-adj.csv', 'r') as file:
    lines = file.readlines()

result_lst = [] 

def direct_adjust():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        num = 0
        for line in lines:
            line = line.strip()
            lst = line.split(',')
            if float(lst[2]) != 0.0:
                result_lst.append(line)
            else:
                item_id = lst[0]
                store_code = lst[1]
                sql = 'select more, less from config where item_id = %s and store_code = "%s"' % (item_id, store_code)
                cur.execute(sql)
                rst = cur.fetchall()
                for rs in rst:
                    more = rs[0]
                    less = rs[1]
                    if less > more:
                        result_lst.append(item_id + ',' + store_code + ',5.0')
                        num += 1
                        print less,more
                        print num
                    else:
                        result_lst.append(line)

        with open('d:/tianchi/last_two_week_zero_adjust.csv', 'wb') as file:
            file.writelines('\n'.join(result_lst))

        conn.close()

    except:
        traceback.print_exc()
        conn.close()


def four_week_adjust():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select item_id, store_code, twnum0, twnumd0, twnum1, twnumd1 from config_two'
        cur.execute(sql)
        rst = cur.fetchall()
        result_lst = []
        for rs in rst:
            item_id = rs[0]
            store_code = rs[1]
            if rs[2] != 0:
                result_lst.append(','.join([str(item_id), store_code, str(rs[2])]))
            elif rs[4] != -1:
                result_lst.append(','.join([str(item_id), store_code, str(round((rs[2] + rs[4])/2))]))
            else:
                result_lst.append(','.join([str(item_id), store_code, '0']))

        conn.close()

        with open('d:/tianchi/last_two_week_adjust_four.csv', 'wb') as file:
            file.writelines('\n'.join(result_lst))

    except:
        traceback.print_exc()
        conn.close()

if __name__ == '__main__':
    four_week_adjust()

end = time.time()

print end - start

