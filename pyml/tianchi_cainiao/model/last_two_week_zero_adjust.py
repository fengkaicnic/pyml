import utils
import traceback
import pdb

with open('d:/tianchi/result_last_two_week-direct-adj.csv', 'r') as file:
    lines = file.readlines()

result_lst = [] 

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
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
                else:
                    result_lst.append(line)
    
    
    with open('d:/tianchi/last_two_week_zero_adjust.csv', 'wb') as file:
        file.writelines('\n'.join(result_lst))
    
    conn.close() 
            
except:
    traceback.print_exc()
    conn.close()
    