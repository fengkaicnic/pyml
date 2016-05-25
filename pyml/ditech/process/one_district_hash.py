import utils
import traceback
import pdb
import time

start = time.time()

def get_all_hash():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select * from cluster_map'
        cur.execute(sql)
        rst = cur.fetchall()
        hsh_ls = []
        for rs in rst:
            hsh_ls.append(rs[0])
        return hsh_ls
        conn.close()
    except:
        traceback.print_exc()
        conn.close()

def generate_one_hash(hasho):
    try:
        start_district_hash = hasho
        with open('d:/ditech/citydata/read_me_1.txt', 'r') as file:
            lines = file.readlines()
        splice_lst = []
        for line in lines:
            splice_lst.append(line.strip().split('-')[-1])

        splice_lst = list(set(splice_lst))
        splice_lst = map(lambda x:int(x), splice_lst)

        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select date, splice, count(*) from order_data where start_district_hash = "%s" \
                group by date, splice order by date, splice' % start_district_hash
        cur.execute(sql)
        rst = cur.fetchall()
        results = []
        rsult = []
        datestr = ''
        for rs in rst:
            if datestr != rs[0]:
                if not rsult:
                    datestr = rs[0]
                    rsult.append(start_district_hash)
                    rsult.append(rs[0])
                    rsult.append(rs[2])
                else:
                    results.append(','.join(map(lambda x:str(x), rsult)))
                    rsult = [start_district_hash, rs[0], rs[2]]
                    datestr = rs[0]
            else:
                rsult.append(rs[2])

        results.append(','.join(map(lambda x:str(x), rsult)))
        # with open('d:/ditech/all_date_splice.csv', 'wb') as file:
        #     file.writelines('\n'.join(results))
        return results
        conn.close()
    except:
        traceback.print_exc()
        conn.close()

if __name__ == '__main__':
    hsh_lst = get_all_hash()
    results = []
    num = 0
    for hasho in hsh_lst:
        num += 1;print num
        rst = generate_one_hash(hasho)
        results += rst
    with open('d:/ditech/all_date_splice.csv', 'wb') as file:
        file.writelines('\n'.join(results))

end = time.time()
print end - start
