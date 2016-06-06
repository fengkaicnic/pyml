#coding:utf8
#prepare education
import utils
import traceback

def remove_space():
    with open('d:/naren/college.txt', 'r') as file:
        lines = file.readlines()

    results = []
    result = []
    for line in lines:
        line = line.strip()
        if line:
            if len(result) < 11:
                result.append(line)
            else:
                results.append(','.join(result))
                result = [line]

    results.append(','.join(result))

    with open('d:/naren/newcollege.txt', 'wb') as file:
        file.writelines('\n'.join(results))


def insert_college():
    with open('d:/naren/newcollege.txt', 'r') as file:
        lines = file.readlines()

    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        for line in lines:
            line = line.strip()
            lst = line.split(',')
            sql = 'insert into college(num, name, type, location, total, talent, science, social)\
                    values (%d, "%s", "%s", "%s", %f, %f, %f, %f)' % (int(lst[0]), lst[1], \
                        lst[2], lst[3], float(lst[4]), float(lst[5]), float(lst[6]), float(lst[7]))
            cur.execute(sql)

        conn.commit()
        conn.close()
    except:
        traceback.print_exc()
        conn.close()


if __name__ == '__main__':
    # remove_space()
    insert_college()
