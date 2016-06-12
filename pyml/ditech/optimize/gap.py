# -*-  coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import random
import math
import pdb
"""
宿舍分配问题，属于搜索优化问题。优化方法使用optimization.py中使用的
随机搜索、爬山法、模拟退火法、遗传算法等. 但题解的描述比之前的问题复杂
"""


class dorm:
    def __init__(self):
        # 代表宿舍，每个宿舍有两个隔间可用
        self.dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

        # 代表选择，第一列代表人名，第二列和第三列代表该学生的首选和次选
        self.prefs = [('Toby', ('Bacchus', 'Hercules')),
                      ('Steve', ('Zeus', 'Pluto')),
                      ('Karen', ('Athena', 'Zeus')),
                      ('Sarah', ('Zeus', 'Pluto')),
                      ('Dave', ('Athena', 'Bacchus')),
                      ('Jeff', ('Hercules', 'Pluto')),
                      ('Fred', ('Pluto', 'Athena')),
                      ('Suzie', ('Bacchus', 'Hercules')),
                      ('Laura', ('Bacchus', 'Hercules')),
                      ('James', ('Hercules', 'Athena'))]

        # 题解的表示法：
        # 设想每个宿舍有两个槽，本例中共有5个宿舍，则共有10个槽，我们将每名学生依序安置于各空槽
        # 内————则第一名学生有10种选择，解的取值范围为0-9；第二名学生有9种选择，解的取值范围为
        # 0-8，第三名学生解的取值范围是0-7，以此类推，最后一名学生只有一个可选。
        # 按照上述题解的表示法初始化题解范围：
        self.domain = [(0, 2*len(self.dorms)-1-i) for i in range(len(self.prefs))]

    # 根据题解序列vec打印出最终宿舍分配方案
    # 注意，输出一个槽后表明该槽已经用过，需将该槽删除
    def printsolution(self, vec):
        slots = []
        # slots = [0,0,1,1,2,2,3,3,4,4]
        for i in range(len(self.dorms)):
            slots.append(i)
            slots.append(i)
        # 循环题解
        print "选择方案是："
        for i in range(len(vec)):
            index = slots[vec[i]]
            print self.prefs[i][0], self.dorms[index]
            del slots[vec[i]]

    # 代价函数: 如果学生当前安置的宿舍使其首选则代价为0，是其次选则代价为1，否则代价为3
    # 注意，输出一个槽后表明该槽已经用过，需将该槽删除
    def dormcost(self, vec):
        cost = 0
        # 建立槽
        slots = []
        for i in range(len(self.dorms)):
            slots.append(i)
            slots.append(i)
        # 循环题解
        for i in range(len(vec)):
            index = slots[vec[i]]
            if self.dorms[index] == self.prefs[i][1][0]:
                cost += 0
            elif self.dorms[index] == self.prefs[i][1][1]:
                cost += 1
            else:
                cost += 3
            del slots[vec[i]]
        return cost

    """
    下列函数与 optimization 中函数相同，只不过代价函数和输出函数用本问题的输出函数
    """
    # 搜索方法1: 随机搜索算法
    # 函数会作1000次随机猜测，记录总代价最低的方法. domain为航班号的范围（0-9），共有5个人，因此共有10项
    def randomoptimize(self, domain):
        best_sol = []
        bestcost = 99999
        for i in range(1000):
            sol = [0] * len(domain)
            for j in range(len(domain) / 2):  # 人数
                sol[2 * j] = random.randint(domain[2 * j][0], domain[2 * j][1])
                sol[2 * j + 1] = random.randint(domain[2 * j + 1][0], domain[2 * j + 1][1])

            print sol[:]
            newcost = self.dormcost(sol)
            if newcost < bestcost:
                bestcost = newcost
                best_sol = sol
            else:
                continue
        self.printsolution(best_sol)
        print "随机搜索算法的结果的最小代价是：", bestcost
        return best_sol

    # 搜索算法2：爬山法
    # 首先随机选择一个解作为种子解，每次寻找这个种子相近的解，如果相近的解有代价更小的解，则把这个新的解作为种子
    # 依次循环进行，当循环到某种子附近的解都比该种子的代价大时，说明到达了局部极小值点，搜索结束
    def hillclimb(self, domain):
        # 随机产生一个航班序列作为初始种子
        seed = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        while 1:
            neighbor = []
            # 循环改变解的每一个值产生一个临近解的列表
            for i in range(len(domain)):
                # 下列判断是为了将某一位加减1后不超出domain的范围
                # print seed
                if seed[i] > domain[i][0]:
                    newneighbor = seed[0:i] + [seed[i] - 1] + seed[i + 1:]
                    # print newneighbor[:]
                    neighbor.append(newneighbor)
                if seed[i] < domain[i][1]:
                    newneighbor = seed[0:i] + [seed[i] + 1] + seed[i + 1:]
                    # print newneighbor[:]
                    neighbor.append(newneighbor)

            # 对所有的临近解计算代价，排序，得到代价最小的解
            neighbor_cost = sorted(
                [(s, self.dormcost(s)) for s in neighbor], key=lambda x: x[1])

            # 如果新的最小代价 > 原种子代价，则跳出循环
            if neighbor_cost[0][1] > self.dormcost(seed):
                break

            # 新的代价更小的临近解作为新的种子
            seed = neighbor_cost[0][0]
            print "newseed = ", seed[:], " 代价：", self.dormcost(seed)
        # 输出
        self.printsolution(seed)
        print "爬山法得到的解的最小代价是", self.dormcost(seed)
        return seed

    # 搜索算法4：模拟退火算法
    # 参数：T代表原始温度，cool代表冷却率，step代表每次选择临近解的变化范围
    # 原理：退火算法以一个问题的随机解开始，用一个变量表示温度，这一温度开始时非常高，而后逐步降低
    #      在每一次迭代期间，算啊会随机选中题解中的某个数字，然后朝某个方向变化。如果新的成本值更
    #      低，则新的题解将会变成当前题解，这与爬山法类似。不过，如果成本值更高的话，则新的题解仍
    #      有可能成为当前题解，这是避免局部极小值问题的一种尝试。
    # 注意：算法总会接受一个更优的解，而且在退火的开始阶段会接受较差的解，随着退火的不断进行，算法
    #      原来越不能接受较差的解，直到最后，它只能接受更优的解。
    # 算法接受较差解的概率 P = exp[-(highcost-lowcost)/temperature]
    def annealingoptimize(self, domain, T=10000.0, cool=0.98, step=1):
        # 随机初始化值
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

        # 循环
        while T > 0.1:
            # 选择一个索引值
            i = random.randint(0, len(domain) - 1)
            # 选择一个改变索引值的方向
            c = random.randint(-step, step)  # -1 or 0 or 1
            # 构造新的解
            vecb = vec[:]
            vecb[i] += c
            if vecb[i] < domain[i][0]:  # 判断越界情况
                vecb[i] = domain[i][0]
            if vecb[i] > domain[i][1]:
                vecb[i] = domain[i][1]

            # 计算当前成本和新的成本
            cost1 = self.dormcost(vec)
            cost2 = self.dormcost(vecb)

            # 判断新的解是否优于原始解 或者 算法将以一定概率接受较差的解
            if cost2 < cost1 or random.random() < math.exp(-(cost2 - cost1) / T):
                vec = vecb

            T = T * cool  # 温度冷却
            print vecb[:], "代价:", self.dormcost(vecb)

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
    def geneticoptimize(self, domain, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=1000):
        # 变异操作的函数
        def mutate(vec):
            i = random.randint(0, len(domain) - 1)
            res = []
            if random.random() < 0.5 and vec[i] > domain[i][0]:
                res = vec[0:i] + [vec[i] - step] + vec[i + 1:]
            elif vec[i] < domain[i][1]:
                res = vec[0:i] + [vec[i] + step] + vec[i + 1:]
            else:
                res = vec
            return res

        # 交叉操作的函数（单点交叉）
        def crossover(r1, r2):
            i = random.randint(0, len(domain) - 1)
            return r1[0:i] + r2[i:]

        pdb.set_trace()
        # 构造初始种群
        pop = []
        for i in range(popsize):
            vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
            pop.append(vec)
        pdb.set_trace()
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
            pdb.set_trace()
            scores.sort()
            ranked = [v for (s, v) in scores]  # 解按照代价由小到大的排序

            pdb.set_trace()
            # 优质解遗传到下一代
            pop = ranked[0: topelite]
            # 如果当前种群数量小于既定数量，则添加变异和交叉遗传
            while len(pop) < popsize:
                # 随机数小于 mutprob 则变异，否则交叉
                if random.random() < mutprob:  # mutprob控制交叉和变异的比例
                    # 选择一个个体
                    c = random.randint(0, topelite)
                    # 变异
                    pdb.set_trace()
                    if len(ranked[c]) == len(self.prefs):
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
    #sol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #dormsol.printsolution(sol)
    #dormsol.dormcost(sol)

    domain = dormsol.domain

    # 方法1：随机猜测
    # dormsol.randomoptimize(domain)

    # 方法2：爬山法
    # dormsol.hillclimb(domain)

    # 方法3：模拟退火法
    # dormsol.annealingoptimize(domain)

    # 方法4：遗传算法
    dormsol.geneticoptimize(domain)
