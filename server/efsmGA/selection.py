#encoding:UTF-8
from __future__ import division     #ensure that float number when divide

import random

import cal_chrofitness

def sumfitness(fitlist):       #种群中全部个体的fitness之和
    total=0
    for i in range(len(fitlist)):
        total=total+fitlist[i]
    return total

def cumcomfit(fitlist):   #将种群中每个fitness标准化，得到累积fitness列表，为 轮盘赌 做准备
    norfitlist=[]
    for i in range(len(fitlist)):
        norfitlist.append(fitlist[i]/sumfitness(fitlist))
    cumfitlist = []
    for i in range(len( norfitlist)):
        t = 0
        j = 0
        while (j <= i):
            t +=  norfitlist[j]
            j = j + 1
        cumfitlist.append(t)
    return cumfitlist

def fitprocess_before_RS(pop, flag):     #将 种群的 fitness计算和累积fitness合并到一个函数，在 轮盘赌 中调用
    fit_list = cal_chrofitness.pop_fitlist_cov(pop,flag)  # 以 coverage
    #print fit_list   #for test
    cumfit_list=cumcomfit(fit_list)
    return cumfit_list

def RouletteSelection(pop, flag):    #以适应度来选择个体，轮盘赌

    selectedchrolist=[]
    templist=fitprocess_before_RS(pop,flag)
    #print templist                  #for test
    for i in range(len(pop)):   #若种群大小为M，则用随机数选择M次，将这些父母按被选择的顺序存入selectedchro列表中，父母会重复被选择
        randnum = random.uniform(0, 1)
        #print randnum                  #for test
        for j in range(len(pop)):
            if randnum<=templist[j]:
                selectedchrolist.append(pop[j])
                break

    #print '选择后的种群：',selectedchrolist
    return selectedchrolist


if __name__ == '__main__':
    pop = [['T1', 'T4', 'T5', 'T8', 'T20', 'T22', 'T10', 'T23'],
           ['T1', 'T2', 'T4', 'T5', 'T8', 'T10', 'T8', 'T19', 'T22', 'T10', 'T7', 'T9', 'T23'],
           ['T1', 'T2', 'T4', 'T6', 'T8', 'T17', 'T21', 'T10', 'T23'],
           ['T1', 'T2', 'T2', 'T4', 'T6', 'T8', 'T19', 'T21', 'T20', 'T22', 'T18', 'T22', 'T10', 'T7', 'T9', 'T23'],
           ['T1', 'T2', 'T2', 'T4', 'T5', 'T23']]

    #print fitprocess_before_RS(pop)
    print pop
    RouletteSelection(pop)
    print pop