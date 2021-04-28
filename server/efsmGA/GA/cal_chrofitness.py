#encoding:UTF-8
from __future__ import division     #ensure that float number when divide
import math
import obtain_efsm_info

def covfitness(chro):   #计算个体(path)的覆盖的迁移个数
    coveredtran=len(set(chro))
    return coveredtran
def statecovfitness(pop):
    traninfolist = obtain_efsm_info.obtain_tran_info()
    index=0
    state=[]
    fitlist=[]
    for ind in pop:
        state=[]
        for tran in ind:
            tran=tran.strip('T')
            index=int(tran)-int('0')-1
            if traninfolist[index].tgt.name not in state:
                state.append(traninfolist[index].tgt.name)
            if traninfolist[index].src.name not in state:
                state.append(traninfolist[index].src.name)
        fitlist.append(len(state))
    return fitlist

def pop_fitlist_cov(pop,flag):  #种群中全部个体的coverage的list
    fitlist=[]
    if flag == 1:
        for i in range(len(pop)):
            fitlist.append(covfitness(pop[i]))
    elif flag==2:
        fitlist=statecovfitness(pop)

    return fitlist

def pop_coverage(pop):  #给出一个population，计算种群覆盖的迁移数
    num=0
    if len(pop) == 1:
        num = len(set(pop[0]))
    else:
        templist=pop[0]
        for i in range(1,len(pop)):
            templist= list(set(templist).union(set(pop[i])))
            #print templist
        num = len(templist)
    return num

def best_chro(pop):  #得到种群中覆盖迁移最多的个体（path）
    fitlist=pop_fitlist_cov(pop)
    maxvalue = max(fitlist)
    best_index = fitlist.index(maxvalue)
    bestchro = pop[best_index]
    return bestchro

def levediv(first, second):   # 编辑距离，计算两个个体（path）的差异度   该值>1
    matrix = [[i + j for j in range(len(second) + 1)] for i in range(len(first) + 1)]

    for i in xrange(1, len(first) + 1):
        for j in xrange(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    EditNum=matrix[len(first)][len(second)]
    #Leven=EditNum/max(len(first),len(second))  # 使用编辑距离，公式为Leven_divmax
    return EditNum

def chromdiv(pop):   #计算一个个体（path）与种群中其他个体比较后的div_fitness
    allpath_div=[]
    for i in range(len(pop)):
        difflist=[]
        for j in range(len(pop)):
            diff=levediv(pop[i],pop[j])   #计算pop[i]与其他path的差异度
            if diff != 0:
                difflist.append(diff)
        #print difflist
        if len(difflist) != 0:
            div_fitness = min(difflist)  # 选择与其他path差异度的最小值作为该path的div_fitness
        else:
            div_fitness=0
        #print div_fitness
        allpath_div.append(div_fitness)  #将种群中所有个体的div_fitness放入一个list中，值越大的个体说明与其他path差异越大，越应保留到下一代
    return allpath_div
#==================================================================================================
def path_Dice_diversity(first,second):   #计算两path的 Dice 距离，Dice越大，相似度越大【大于1】
    a = len(list(set(first).intersection(set(second))))  # intersection
    b = len(list(set(first).union(set(second))))  # union
    dice=a/(a+(b-a)/2)
    return 1/dice

def chromdiv_dice(pop):   #计算一个个体（path）与种群中其他个体比较后的div_fitness
    allpath_div=[]
    for i in range(len(pop)):
        difflist=[]
        for j in range(len(pop)):
            diff=path_Dice_diversity(pop[i],pop[j])   #计算pop[i]与其他path的差异度
            if diff != 1.0:
                difflist.append(diff)
        #print difflist
        if len(difflist) != 0:
            div_fitness = min(difflist)  # 选择与其他path差异度的最小值作为该path的div_fitness
        else:
            div_fitness=0

        #print div_fitness
        allpath_div.append(div_fitness)  #将种群中所有个体的div_fitness放入一个list中，值越大的个体说明与其他path差异越大，越应保留到下一代
    return allpath_div


if __name__ =='__main__':


    chro=['T1', 'T4', 'T5', 'T7', 'T13', 'T16', 'T11', 'T16', 'T14', 'T16', 'T14', 'T15', 'T9', 'T23']
    pop1=[[1,2,3],[1,2,3],[1,2,3]]
    pop=[['T1', 'T4', 'T5', 'T8', 'T19', 'T22', 'T17', 'T21', 'T18', 'T21', 'T10', 'T23'], ['T1', 'T4', 'T5', 'T7', 'T12', 'T15', 'T11', 'T16', 'T11', 'T15', 'T12', 'T16', 'T14', 'T16', 'T9', 'T23'], ['T1', 'T4', 'T5', 'T7', 'T14', 'T16', 'T9', 'T7', 'T12', 'T15', 'T13', 'T15', 'T9', 'T23'], ['T1', 'T4', 'T6', 'T8', 'T10', 'T8', 'T17', 'T22', 'T10', 'T7', 'T9', 'T23'], ['T1', 'T4', 'T5', 'T7', 'T9', 'T8', 'T10', 'T8', 'T19', 'T21', 'T10', 'T23'], ['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T8', 'T19', 'T21', 'T10', 'T23'], ['T1', 'T4', 'T6', 'T7', 'T14', 'T16', 'T9', 'T23'], ['T1', 'T2', 'T4', 'T5', 'T8', 'T10', 'T8', 'T10', 'T23'], ['T1', 'T2', 'T4', 'T5', 'T8', 'T10', 'T8', 'T10', 'T23'], ['T1', 'T4', 'T6', 'T8', 'T10', 'T23'], ['T1', 'T4', 'T6', 'T7', 'T9', 'T23'], ['T1', 'T4', 'T6', 'T8', 'T10', 'T23'], ['T1', 'T2', 'T4', 'T6', 'T23'], ['T1', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T4', 'T6', 'T23'], ['T1', 'T2', 'T2', 'T4', 'T6', 'T23'], ['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T4', 'T6', 'T23'], ['T1', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T23'], ['T1', 'T2', 'T2', 'T4', 'T6', 'T23'], ['T1', 'T4', 'T5', 'T23'], ['T1', 'T4', 'T6', 'T23'], ['T1', 'T4', 'T5', 'T23'], ['T1', 'T4', 'T5', 'T23'], ['T1', 'T4', 'T6', 'T23'], ['T1', 'T4', 'T6', 'T23']]

    first=['T1', 'T4', 'T5', 'T8', 'T20', 'T22', 'T10', 'T23']
    second=['T1', 'T4', 'T5', 'T8', 'T20', 'T22', 'T10', 'T23']
    test=['T1', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2', 'T2','T23']
    updateresult=[['T1', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T2', 'T2', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T2', 'T2', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T2', 'T2', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T2', 'T2', 'T3', 'T12', 'T13', 'T4', 'T5', 'T6', 'T7', 'T16', 'T17', 'T19', 'T20'], ['T1', 'T3', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T9', 'T10', 'T11'], ['T1', 'T3', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T9', 'T10', 'T11'], ['T1', 'T3', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T3', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T3', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T3', 'T16', 'T17', 'T19', 'T21', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8'], ['T1', 'T3', 'T12', 'T13', 'T4', 'T9', 'T15', 'T16', 'T17', 'T18', 'T12', 'T13', 'T4', 'T5', 'T6', 'T8']]

    #print len(chro)
    #print pop_fitlist_cov(updateresult)
    print pop_coverage(updateresult)
    print chromdiv(pop)
    print chromdiv_dice(pop)
    print levediv(first,second)