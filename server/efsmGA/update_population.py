#encoding:UTF-8

import cal_chrofitness
import feasibility
import Difference

def update_cov(parent,child,popsize):  #选择覆盖迁移多的个体组成规模为M的新种群
    #list1=feasibility.is_feasible_list(parent)
    #list2=feasibility.is_feasible_list(child)

    #print 'update内parent可行性：',list1
    #print 'update内child可行性：',list2
    p_fitnesslist=cal_chrofitness.pop_fitlist_cov(parent)
    c_fitnesslist=cal_chrofitness.pop_fitlist_cov(child)

    for i in range(len(child)):   #对过长的path的适应度惩罚，避免其进入下一代
        if len(child[i])>10:
            c_fitnesslist[i]=c_fitnesslist[i]-(len(child[i])-10)

    all_fitlist=p_fitnesslist+c_fitnesslist #合并parent，child的 覆盖迁移数（fitness）
    #print all_fitlist
    all_pop=parent+child #合并parent，child种群
    #print all_pop

    newpop=[]
    for i in range(popsize):
        maxfit=max(all_fitlist)
        #print maxfit
        maxfit_index=all_fitlist.index(maxfit)
        newpop.append(all_pop[maxfit_index])
        all_fitlist[maxfit_index]=(-100)  #避免选过的最优个体再次被选
    return newpop

#==============================================================================

def update_covdiv(parent,child,popsize):
    p_fitnesslist = cal_chrofitness.pop_fitlist_cov(parent)   #父种群所有个体的cov list
    c_fitnesslist = cal_chrofitness.pop_fitlist_cov(child)    #子种群所有个体的cov list
    #p_divlist=cal_chrofitness.chromdiv(parent)   #父种群所有个体的leven div list
    #c_divlist=cal_chrofitness.chromdiv(child)    #子种群所有个体的leven div list

    p_divlist = cal_chrofitness.chromdiv_dice(parent)  # 父种群所有个体的dice div list
    c_divlist = cal_chrofitness.chromdiv_dice(child)  # 子种群所有个体的dice div list

    for i in range(len(child)):  # 对过长的path的适应度惩罚，避免其进入下一代
        if len(child[i]) > 20:
            c_fitnesslist[i] = c_fitnesslist[i] - (len(child[i]) - 20)

    p_covdivlist=map(lambda (a,b):a+b,zip(p_fitnesslist,p_divlist))
    c_covdivlist = map(lambda (a, b): a + b, zip(c_fitnesslist, c_divlist))



    all_fitlist = p_covdivlist + c_covdivlist  # 合并parent，child的 覆盖迁移数（fitness）
    #print all_fitlist
    all_pop = parent + child  # 合并parent，child种群
    #print all_pop


    newpop = []
    for i in range(popsize):
        maxfit = max(all_fitlist)
        # print maxfit
        maxfit_index = all_fitlist.index(maxfit)
        newpop.append(all_pop[maxfit_index])
        all_fitlist[maxfit_index] = (-100)  # 避免选过的最优个体再次被选
    return newpop

#=======================================================================================

def update_div(parent,child,popsize):
    p_fitnesslist = cal_chrofitness.chromdiv_dice(parent)
    c_fitnesslist = cal_chrofitness.chromdiv_dice(child)

    for i in range(len(child)):  # 对过长的path的适应度惩罚，避免其进入下一代
        if len(child[i]) > 15:
            c_fitnesslist[i] = c_fitnesslist[i] - (len(child[i]) - 15)

    all_fitlist = p_fitnesslist + c_fitnesslist  # 合并parent，child的 覆盖迁移数（fitness）
    # print all_fitlist
    all_pop = parent + child  # 合并parent，child种群
    # print all_pop

    newpop = []
    for i in range(popsize):
        maxfit = max(all_fitlist)
        # print maxfit
        maxfit_index = all_fitlist.index(maxfit)
        newpop.append(all_pop[maxfit_index])
        all_fitlist[maxfit_index] = (-100)  # 避免选过的最优个体再次被选
    return newpop

#===========2018.1.5添加，新的种群更新策略=======================================

def no_repaeat(all):
    no_repeat_pop = []  # 去重
    for i in all:
        if not i in no_repeat_pop:
            no_repeat_pop.append(i)
    return no_repeat_pop

#构造差异度矩阵，对称矩阵，矩阵中每个值为对应两个path的差异度Diffference,另一半全为1000
def DifferMatrix_1000(parent,child):
    all = parent + child
    no_repeat_pop = no_repaeat(all)

    matrix = []
    for line in range(len(no_repeat_pop)):
        differ_score = []
        for row in range(len(no_repeat_pop)):
            if row <= line :
                differ_score.append(1000)
            else:
                differ_score.append(Difference.Difference(no_repeat_pop[line],no_repeat_pop[row]))
        matrix.append(differ_score)
    return matrix

#构造差异度矩阵，对称矩阵，矩阵中每个值为对应两个path的差异度Diffference,另一半全为0
def DifferMatrix_0(parent,child):
    all = parent + child
    no_repeat_pop = no_repaeat(all)

    matrix = []
    for line in range(len(no_repeat_pop)):
        differ_score = []
        for row in range(len(no_repeat_pop)):
            if row <= line :
                differ_score.append(0)
            else:
                differ_score.append(Difference.Difference(no_repeat_pop[line],no_repeat_pop[row]))
        matrix.append(differ_score)
    return matrix

#更新策略一：依次删除矩阵中最小值对应的两个path中的其中一个，直到剩余path规模等于popsize
def update_deleteSim(parent,child,popsize):
    all = parent + child
    no_repeat_pop = no_repaeat(all)
    size = len(no_repeat_pop)
    if size == popsize:  #不可能再删除个体，需全部进入下一代
        return no_repeat_pop
    else:                              #需要删除个体，选择一部分进入下一代
        matrix = DifferMatrix_1000(parent,child)  # 获得差异度矩阵

        delete_path_index = []
        for i in range(size-popsize):
            minimum_list = []
            minimumIndex_list = []
            for line in range(size - 1):
                minimum = min(matrix[line])
                minimum_list.append(minimum)
                minimumIndex_list.append(matrix[line].index(minimum))
            target1 = minimum_list.index(min(minimum_list))    #确定了最小值对应的行
            target2 = minimumIndex_list[target1]  #确定了最小值对应的列
            coverage1 = cal_chrofitness.covfitness(no_repeat_pop[target1])
            coverage2 = cal_chrofitness.covfitness(no_repeat_pop[target2])
            if coverage1 > coverage2:
                delete_path_index.append(target2)   #将需要删除的path的index存入一个list中
            else:
                delete_path_index.append(target1)
            for p in range(size):
                matrix[delete_path_index[i]][p] = 1000
            for q in range(size):
                matrix[q][delete_path_index[i]] = 1000
        newpop = []
        for i in range(len(no_repeat_pop)):
            if i not in delete_path_index:
                newpop.append(no_repeat_pop[i])

    return newpop

#更新策略二：选择与已选个体差异最大的个体放进来
def update_chooseDiff(parent,child,popsize):
    all = parent + child
    no_repeat_pop = no_repaeat(all)
    size = len(no_repeat_pop)
    if size == popsize:  # 不可能再删除个体，需全部进入下一代
        return no_repeat_pop
    else:  # 需要删除个体，选择一部分进入下一代
        matrix = DifferMatrix_0(parent, child)  # 获得差异度矩阵




if __name__ == '__main__':
    parent=[
        ['T1', 'T4', 'T5', 'T8', 'T10', 'T23'],
        ['T1', 'T2', 'T2', 'T4', 'T6', 'T23','T23', 'T23', 'T23', 'T23', 'T23', 'T23', 'T23', 'T23', 'T23', 'T23', 'T23'],
        ['T1', 'T4', 'T6', 'T8', 'T18', 'T21', 'T18', 'T22', 'T10', 'T7', 'T9', 'T23'],
        ['T1', 'T4', 'T6', 'T7', 'T11', 'T16', 'T11', 'T15', 'T12', 'T15', 'T13', 'T16', 'T12', 'T15', 'T9', 'T23'],
        ['T1', 'T2', 'T4', 'T5', 'T7', 'T11', 'T16', 'T9', 'T7', 'T13', 'T15', 'T9', 'T23'],
        ['T1', 'T4', 'T5', 'T8', 'T10', 'T7', 'T11', 'T15', 'T11', 'T15', 'T11', 'T16', 'T9', 'T23']]
    child=[
        ['T1', 'T2', 'T2', 'T4', 'T6', 'T23'],
        ['T1', 'T4', 'T5', 'T7', 'T9', 'T8', 'T17', 'T22', 'T10', 'T23']]

    a = DifferMatrix(parent,child)
    print a
    print len(update_deleteSim(parent,child,6))
    #newpop=update_covdiv(parent,child,6)
    #print newpop
    #print cal_chrofitness.pop_coverage(newpop)