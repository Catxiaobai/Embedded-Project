#encoding:UTF-8
from __future__ import division
from datetime import datetime
import initial_population
import cal_chrofitness
import selection
import crossover
import mutation
import update_population
import feasibility
import delete_repeat
import pop_diversity
import du_cover
import random

import copy
from collections import Counter

popsize=14
pc=0.9
pm=0.6

def GA(pop,pc,pm,popsize):
    #print 'parent pop:', pop
    #list0 = feasibility.is_feasible_list(pop)
    #print 'parentpop feasibility:', list0
    #parentpopcov=cal_chrofitness.pop_coverage(pop)
    #print 'population covered number:', parentpopcov

    temp = copy.deepcopy(pop)

    covlist = cal_chrofitness.pop_fitlist_cov(pop)
    # print 'cov of everychro:', covlist

    # 验证 select功能
    selectedpop = selection.RouletteSelection(pop)
    #print 'select result:', selectedpop

    # 验证crossover功能
    crossedpop = crossover.crossover(selectedpop, pc)
    #print 'crossover result:', crossedpop

    # 验证mutant功能
    mutantedpop = mutation.mutantion(crossedpop, pm)
    #print 'mutant result:', mutantedpop

    #mut_fit = cal_chrofitness.pop_fitlist_cov(mutantedpop)
    # print 'mutant fit:', mut_fit

    #验证删除子代中不可行path
    #childpop_fealible=feasibility.del_infeasible_after_mutant(mutantedpop)
    #print 'del infeasible path(childpop_feasible):',childpop_fealible
    #print 'fesible删后剩余条数：',len(childpop_fealible)

    #刪除重复个体
    childpop_repeat=delete_repeat.delete_repeat_chrom(mutantedpop)
    #print 'del repeat path(childpop_no_repeat):',childpop_repeat
    #print 'repeat删后剩余条数：',len(childpop_repeat)

    # 验证update功能
    newpop = update_population.update_cov(temp, childpop_repeat, popsize)   #单纯以个体cov更新种群
    #newpop = update_population.update_covdiv(temp,mutantedpop, popsize)   #以cov+div更新
    #newpop=update_population.update_div(temp,mutantedpop, popsize)  #以div更新
    #print 'update result:', newpop

    #list=feasibility.is_feasible_list(newpop)
    #print 'newpop feasibility:',list

    new_fit_cov = cal_chrofitness.pop_fitlist_cov(newpop)
    #print 'update cov fit:', new_fit_cov
    # new_fit_div=calulate_fitness.pop_divalue_list(newpop)
    # print 'update div fit:', new_fit_div

    return newpop

def GA_div(pop,pc,pm,popsize):   #用于GA_mix中
    #print 'parent pop:', pop
    # list0 = feasibility.is_feasible_list(pop)
    # print 'parentpop feasibility:', list0
    # parentpopcov=cal_chrofitness.pop_coverage(pop)
    # print 'population covered number:', parentpopcov

    temp = copy.deepcopy(pop)

    covlist = cal_chrofitness.pop_fitlist_cov(pop)
    # print 'cov of everychro:', covlist

    # 验证 select功能
    selectedpop = selection.RouletteSelection(pop)
    #print 'select result:', selectedpop

    # 验证crossover功能
    crossedpop = crossover.crossover(selectedpop, pc)
    #print 'crossover result:', crossedpop

    # 验证mutant功能
    mutantedpop = mutation.mutantion(crossedpop, pm)
    #print 'mutant result:', mutantedpop

    # mut_fit = cal_chrofitness.pop_fitlist_cov(mutantedpop)
    # print 'mutant fit:', mut_fit

    # 验证删除子代中不可行path
    #childpop_fealible=feasibility.del_infeasible_after_mutant(mutantedpop)
    # print 'del infeasible path(childpop_feasible):',childpop_fealible
    # print 'fesible删后剩余条数：',len(childpop_fealible)

    # 刪除重复个体
    childpop_repeat=delete_repeat.delete_repeat_chrom(mutantedpop)
    # print 'del repeat path(childpop_no_repeat):',childpop_repeat
    # print 'repeat删后剩余条数：',len(childpop_repeat)

    # 验证update功能
    # newpop = update_population.update_cov(temp, mutantedpop, popsize)   #单纯以个体cov更新种群
    # newpop = update_population.update_covdiv(temp,mutantedpop, popsize)   #以cov+div更新
    newpop = update_population.update_div(temp, childpop_repeat, popsize)  # 以div更新
    print 'update result:', newpop

    #list = feasibility.is_feasible_list(newpop)
    #print 'newpop feasibility:', list

    #new_fit_cov = cal_chrofitness.pop_fitlist_cov(newpop)
    #print 'update cov fit:', new_fit_cov
    # new_fit_div=calulate_fitness.pop_divalue_list(newpop)
    # print 'update div fit:', new_fit_div

    return newpop

def GA_mix(pop,pc,pm,popsize):
    newpop1=GA(pop,pc,pm,popsize)
    #newpop2 = GA(newpop1, pc, pm, popsize)
    newpop=GA_div(newpop1,pc,pm,popsize)
    return newpop


startTime = datetime.now()
#pop= initial_population.initialpop_feasible(popsize)   #初始种群可行
pop=initial_population.initalpop(popsize)   #初始种群随机，可能不可行
count=0
while 1:
    pop=GA_mix(pop,pc,pm,popsize)
    count=count+1
    # 输出最优的个体的fitness
    popcov = cal_chrofitness.pop_coverage(pop)
    print 'population covered number:', popcov


    #timeslist = Counter(new_fit).values()
   # maxtimes = max(timeslist)
    #if maxtimes>7:
        #print '================================================'
        #print 'geneneration:', count
        #break

    if popcov== 25:
        print '================================================'
        print 'geneneration:',count
        popdiv = pop_diversity.suite_diversity(pop)
        print 'dice diversity:', popdiv
        popdiv1= pop_diversity.suite_diversity_leven(pop)
        print 'leven diversity:',popdiv1
        break
endTime = datetime.now()
print 'endTime - startTime:\t', endTime - startTime

#对测试序列集乱序10次，每次都找到检测到第一个故障时执行的测试序列个数
indexlist=[]
for i in range(10):
    random.shuffle(pop)
    print "随机排序列表 : ", pop
    for i in range(len(pop)):
        #print pop[i]
        if (('T7' in pop[i]) and ('T20' in pop[i])) or (('T8' in pop[i]) and ('T21' in pop[i])) or (('T9' in pop[i]) and (('T22' in pop[i])or('T23' in pop[i]))):
            index=i+1
            print 'the number which find this fault:',index
            indexlist.append(index)
            break
        elif i==len(pop)-1:
            print 'this suite cannot find this fault!'
            indexlist.append(len(pop))
print indexlist
print sum(indexlist)/10


dulist=[['T1','T20'],  #fuelpump
['T1','T17'],
['T1','T21'],
['T1','T18'],
['T1','T22'],
['T1','T23'],
['T1','T19'],
['T7','T20'],
['T8','T21'],
['T9','T22'],
['T9','T23'],
['T17','T24'],
['T18','T24'],
['T19','T24'],
['T20','T24'],
['T21','T24'],
['T22','T24'],
['T23','T24']]
#ducover=du_cover.ducover(dulist,pop)

'''number=0
for i in range(len(pop)):
    print pop[i]
    if ('T9'in pop[i])and (('T22'in pop[i])or('T23'in pop[i])):
        number=number+1
print 'find fault times:',number'''

