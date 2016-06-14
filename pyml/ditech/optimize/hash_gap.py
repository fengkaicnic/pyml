# -*-  coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import random
import math
import time
import utils
import pdb
import pickle
"""
宿舍分配问题，属于搜索优化问题。优化方法使用optimization.py中使用的
随机搜索、爬山法、模拟退火法、遗传算法等. 但题解的描述比之前的问题复杂
"""

st = time.time()

class dorm:
    def __init__(self, splice=None):

        splice_lst = [46, 58, 70, 82, 94, 106, 118, 130, 142]
        try:
            conn = utils.persist.connection()
            cur = conn.cursor()
            sql = 'select * from cluster_map'
            cur.execute(sql)
            rst = cur.fetchall()
            hash_lst = []
            for rs in rst:
                hash_lst.append(rs[0])
            conn.close()
        except:
            conn.close()
        self.hash_splice_dct = {}
        with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
            lines = file.readlines()

        for line in lines:
            lst = line.strip().split(',')
            if not self.hash_splice_dct.has_key(lst[0]):
                self.hash_splice_dct[lst[0]] = {}
                for splice in splice_lst:
                    self.hash_splice_dct[lst[0]][splice] = [[int(lst[splice-2]), int(lst[splice-1]), int(lst[splice]), int(lst[splice+1])]]
            else:
                for splice in splice_lst:
                    self.hash_splice_dct[lst[0]][splice].append([int(lst[splice-2]), int(lst[splice-1]), int(lst[splice]), int(lst[splice+1])])

            # self.rst.append([int(lst[splice-2]), int(lst[splice-1]), int(lst[splice]), int(lst[splice+1])])


    def train(self, method='hillclimb'):
        methods = {'hillclimb':self.hillclimb}
        method = methods[method]
        hash_splice_param = {}
        num = 0
        total = 0
        totalcost = 0.0
        for key in self.hash_splice_dct.keys():
            hash_splice_param[key] = {}
            # pdb.set_trace()
            for key1 in self.hash_splice_dct[key].keys():
                rst = self.hash_splice_dct[key][key1]
                weg, cost = method(rst)
                total += 1
                totalcost += cost
                hash_splice_param[key][key1] = weg
            num += 1
            print num
        for key in hash_splice_param.keys():
            for key1 in hash_splice_param[key].keys():
                print key, key1, hash_splice_param[key][key1]

        print totalcost / total

    # 根据题解序列vec打印出最终宿舍分配方案
    # 注意，输出一个槽后表明该槽已经用过，需将该槽删除
    def printsolution(self, vec):
        print vec


    # 代价函数: 如果学生当前安置的宿舍使其首选则代价为0，是其次选则代价为1，否则代价为3
    # 注意，输出一个槽后表明该槽已经用过，需将该槽删除
    def dormcost(self, vec, rst):

        mape = 0.0
        total = 0
        for rs in rst:
            if not rs[-1]:
                total += 1
            else:
                mape += abs(max(((rs[0]*vec[0] + rs[1]*vec[1] + rs[2]*vec[2])/2), 1) - rs[3])/float(rs[3])
                total += 1

        return mape/total


    """
    下列函数与 optimization 中函数相同，只不过代价函数和输出函数用本问题的输出函数
    """
    # 搜索方法1: 随机搜索算法
    # 函数会作1000次随机猜测，记录总代价最低的方法. domain为航班号的范围（0-9），共有5个人，因此共有10项
    def randomoptimize(self, num):
        best_sol = []
        bestcost = 99999
        for i in range(num):
            sol = [random.random(), random.random(), random.random()]

            # print sol[:]
            newcost = self.dormcost(sol)
            if newcost < bestcost:
                bestcost = newcost
                best_sol = sol
                print best_sol, bestcost
            else:
                continue
        self.printsolution(best_sol)
        print "随机搜索算法的结果的最小代价是：", bestcost
        return best_sol

    # 搜索算法2：爬山法
    # 首先随机选择一个解作为种子解，每次寻找这个种子相近的解，如果相近的解有代价更小的解，则把这个新的解作为种子
    # 依次循环进行，当循环到某种子附近的解都比该种子的代价大时，说明到达了局部极小值点，搜索结束
    def hillclimb(self, rst):
        # 随机产生一个航班序列作为初始种子
        seed = [random.random(), random.random(), random.random()]
        step = 1
        alpha = 0.005
        while 1:
            neighbor = []
            for i in range(100):
                newneighbor = [seed[0]+random.randint(-step, step)*alpha, seed[1]+\
                                random.randint(-step, step)*alpha, seed[2]+random.randint(-step, step)*alpha]
                neighbor.append(newneighbor)

            neighbor_cost = sorted([(s, self.dormcost(s, rst)) for s in neighbor], key=lambda x:x[1])

            if neighbor_cost[0][1] >= self.dormcost(seed, rst):
                break

            seed = neighbor_cost[0][0]
            # print "newseed = ", seed[:], " 代价：", self.dormcost(seed, rst)

        self.printsolution(seed)
        print "爬山法得到的解的最小代价是", self.dormcost(seed, rst)
        return seed, self.dormcost(seed, rst)


    # 搜索算法4：模拟退火算法
    # 参数：T代表原始温度，cool代表冷却率，step代表每次选择临近解的变化范围
    # 原理：退火算法以一个问题的随机解开始，用一个变量表示温度，这一温度开始时非常高，而后逐步降低
    #      在每一次迭代期间，算啊会随机选中题解中的某个数字，然后朝某个方向变化。如果新的成本值更
    #      低，则新的题解将会变成当前题解，这与爬山法类似。不过，如果成本值更高的话，则新的题解仍
    #      有可能成为当前题解，这是避免局部极小值问题的一种尝试。
    # 注意：算法总会接受一个更优的解，而且在退火的开始阶段会接受较差的解，随着退火的不断进行，算法
    #      原来越不能接受较差的解，直到最后，它只能接受更优的解。
    # 算法接受较差解的概率 P = exp[-(highcost-lowcost)/temperature]
    def annealingoptimize(self, T=10000.0, cool=0.99, step=10):
        # 随机初始化值
        # vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        vec = [random.random(), random.random(), random.random()]

        # 循环
        while T > 0.1:
            # 选择一个索引值
            i = random.randint(0, 2)
            # 选择一个改变索引值的方向
            c = random.randint(-step, step) * 0.015  # -1 or 0 or 1
            # 构造新的解
            vecb = vec[:]
            vecb[i] += c
            vecb[i] = max(vecb[i], 0)

            # 计算当前成本和新的成本
            cost1 = self.dormcost(vec)
            cost2 = self.dormcost(vecb)

            # 判断新的解是否优于原始解 或者 算法将以一定概率接受较差的解
            if cost2 < cost1 or random.random() < math.exp(-(cost2 - cost1)*25 / T):
            # if cost2 < cost1:
                vec = vecb

            T = T * cool  # 温度冷却
            print vec[:], "代价:", self.dormcost(vec)

        self.printsolution(vec)
        print "模拟退火算法得到的最小代价是：", self.dormcost(vec)
        return vec

    # 搜索算法5： 遗传算法
    # 原理： 首先随机生成一组解，我们称之为种群，在优化过程的每一步，算法会计算整个种群的成本函数，
    #       从而得到一个有关题解的有序列表。随后根据种群构造进化的下一代种群，方法如下：
    #       遗传：从当前种群中选出代价最优的一部分加入下一代种群，称为“精英选拔”
    #       变异：对一个既有解进行微小的、简单的、随机的修改
    #       交叉：选取最优解中的两个解，按照某种方式进行交叉。方法有单点交叉，多点交叉和均匀交叉
    # 一个种群是通过对最优解进行随机的变异和配对处理构造出来的，它的大小通常与旧的种群相同，尔后，这一过程会
    #       一直重复进行————新的种群经过排序，又一个种群被构造出来，如果达到指定的迭代次数之后题解都没有得
    #       改善，整个过程就结束了
    # 参数：
    # popsize-种群数量 step-变异改变的大小 mutprob-交叉和变异的比例 elite-直接遗传的比例 maxiter-最大迭代次数
    def geneticoptimize(self, popsize=50, step=1, mutprob=0.5, elite=0.2, maxiter=200):
        # 变异操作的函数
        def mutate(vec):
            res = []
            # if random.random() < 0.34:
            #     res = [vec[0]-0.1, vec[1], vec[2]+0.1]
            #
            # elif random.random() < 0.67:
            #     res = [vec[0]+0.1, vec[1], vec[2]-0.1]
            # else:
            #     res = [vec[0]-0.1, vec[1]+0.1, vec[2]]
            res = [random.random(), random.random(), random.random()]
            return res

        # 交叉操作的函数（单点交叉）
        def crossover(r1, r2):
            i = random.randint(0, len(r1) - 1)
            return r1[0:i] + r2[i:]

        # 构造初始种群
        pop = []
        for i in range(popsize):
            # vec = [random.random()/3, random.random()/2, random.random()]
            vec = [random.random(), random.random(), random.random()]
            pop.append(vec)
        # 每一代中有多少胜出者
        topelite = int(elite * popsize)

        # 主循环
        for i in range(maxiter):
            if [] in pop:
                print "***"
            try:
                scores = [(self.dormcost(v), v) for v in pop]
            except:
                print "pop!!", pop[:]
            scores.sort()
            # pdb.set_trace()
            ranked = [v for (s, v) in scores]  # 解按照代价由小到大的排序


            # 优质解遗传到下一代
            pop = ranked[0: topelite]
            # 如果当前种群数量小于既定数量，则添加变异和交叉遗传
            while len(pop) < popsize:
                # 随机数小于 mutprob 则变异，否则交叉
                if random.random() < mutprob:  # mutprob控制交叉和变异的比例
                    # 选择一个个体
                    c = random.randint(0, topelite)
                    # 变异

                    temp = mutate(ranked[c])
                    if temp == []:
                        print "******", ranked[c]
                    else:
                        pop.append(temp)

                else:
                    # 随机选择两个个体进行交叉
                    c1 = random.randint(0, topelite)
                    c2 = random.randint(0, topelite)
                    pop.append(crossover(ranked[c1], ranked[c2]))
            # 输出当前种群中代价最小的解
            print scores[0][1], "代价：", scores[0][0]
        self.printsolution(scores[0][1])
        print "遗传算法求得的最小代价：", scores[0][0]
        return scores[0][1]

if __name__ == '__main__':
    dormsol = dorm()
    dormsol.train()
    #sol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #dormsol.printsolution(sol)
    #dormsol.dormcost(sol)

    # 方法1：随机猜测
    # dormsol.randomoptimize(50000)

    # 方法2：爬山法
    # dormsol.hillclimb()

    # 方法3：模拟退火法
    # dormsol.annealingoptimize()

    # 方法4：遗传算法
    # vec = dormsol.geneticoptimize(mutprob=0.8, maxiter=1000)
    # vec = [0.17, 0.34, 0.34]
    # vec1 = [0.15809659303455248, 0.31596469436756436, 0.3890133104417647]
    #
    # print dormsol.dormcost(vec)

ed = time.time()
print ed - st
