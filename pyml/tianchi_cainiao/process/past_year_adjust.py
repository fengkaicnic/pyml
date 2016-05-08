import utils
import traceback
import pdb
import time

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    mlsql = 'select item_id, store_code, more, less from config'
    cur.execute(mlsql)
    mlrst = cur.fetchall()
    mlct = {}
    for rs in mlrst:
        mlct[str(rs[0]) + '-' + rs[1]] = [rs[2], rs[3]]

    store_all_dct = {}
    past_year_dct = {}
    with open('d:/tianchi/test_tem_p_14', 'r') as file:
        lines = file.readlines()
    pdb.set_trace()
    for line in lines:
        lst = line.strip().split(',')
        past_year_dct[lst[-1] + '-' + lst[-2]] = lst
        store_all_dct[lst[-1] + '-all'] = 0

    with open('d:/tianchi/result_last_two_week-direct-adj.csv', 'r') as file:
        tlines = file.readlines()

    num = 0
    results = []
    all_sum = 0
    pdb.set_trace()
    for line in tlines:
        tlst = line.strip().split(',')
        # pdb.set_trace()
        if past_year_dct.has_key(tlst[0] + '-' + tlst[1]):
            lts = past_year_dct[tlst[0] + '-' + tlst[1]]
            mls = mlct[tlst[0] + '-' + tlst[1]]
            mlsts = mlct[tlst[0] + '-all']
            
            if lts[0] > lts[1] :
                if mls[0]/mls[1] >= 1.8:
                    # pdb.set_trace()
                    # all_sum += 2 * float(mls[0])
                    tlst[2] = float(tlst[2]) * 1.5 + 1
                    store_all_dct[tlst[0] + '-all'] += float(tlst[2]) * 0.5 + 1
                    all_sum += (float(tlst[2]) * 0.1 + 1) * float(mlsts[0])
                    print lts[0],lts[1],mls[0],mls[1],tlst[2]
                    num += 1
                    print num
                else:
                    tlst[2] = float(tlst[2]) + 2
                    store_all_dct[tlst[0] + '-all'] += 2
                    all_sum += 2
                    print lts[0],lts[1],mls[0],mls[1],tlst[2]
                    num += 1
                    print num
            elif lts[0] < lts[1] :
                if mls[1]/mls[0] >= 1.8:
                    tlst[2] = float(tlst[2]) * 0.75 + 1
                    store_all_dct[tlst[0] + '-all'] -= float(tlst[2]) * 0.25 + 1
                    all_sum += (float(tlst[2]) * 0.1 + 1) * float(mlsts[0])
                    print lts[0],lts[1],mls[0],mls[1],tlst[2]
                    num += 1
                    print num
                else:
                    tlst[2] = float(tlst[2]) * 0.75
                    store_all_dct[tlst[0] + '-all'] -= float(tlst[2]) * 0.25
                    all_sum += (float(tlst[2]) * 0.1 + 1) * float(mlsts[0])
                    print lts[0],lts[1],mls[0],mls[1],tlst[2]
                    num += 1
                    print num
        if not 'all' in tlst:
            results.append(','.join(map(lambda x:str(x), tlst)))

    print all_sum
    for line in tlines:
        tlst = line.strip().split(',')
        if 'all' in tlst:
            if store_all_dct.has_key(tlst[0] + '-all'):
                tlst[2] = float(tlst[2]) + store_all_dct[tlst[0] + '-all']
            results.append(','.join(map(lambda x:str(x), tlst)))


    with open('d:/tianchi/past_year_adjust1.csv', 'wb') as file:
        file.writelines('\n'.join(results))

    conn.close()
except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start
