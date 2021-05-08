# encoding:UTF-8
from __future__ import division

import copy
import json
from collections import OrderedDict
from datetime import datetime

import cal_chrofitness
import crossover
import delete_repeat
import feasibility
import initial_population
import mutation
import obtain_efsm_info
import selection
import update_population

ind_history = []
history = []


def pop_history(pop, flag):  # 精英策略
    ind_flag = 0
    if flag == 2:
        for ind in pop:
            for tran in ind:
                if tran not in history:
                    history.append(tran)
                    ind_flag = 1
            if ind_flag:
                ind_history.append(ind)
    elif flag == 1:
        traninfolist = obtain_efsm_info.obtain_tran_info()
        for ind in pop:
            ind_flag = 0
            for tran in ind:
                tran = tran.strip('T')
                index = int(tran) - int('0') - 1
                if traninfolist[index].tgt.name not in history:
                    history.append(traninfolist[index].tgt.name)
                    ind_flag = 1
                if traninfolist[index].src.name not in history:
                    history.append(traninfolist[index].src.name)
                    ind_flag = 1
            if ind_flag:
                ind_history.append(ind)


def GA(pop, pc, pm, popsize, flag):
    # print
    # 'parent pop:', pop
    temp = copy.deepcopy(pop)
    covlist = cal_chrofitness.pop_fitlist_cov(pop, flag)  # flag=1,全状态覆盖，=2，迁移覆盖
    selectedpop = selection.RouletteSelection(pop, flag)  # 验证 select功能
    crossedpop = crossover.crossover(selectedpop, pc)  # 验证crossover功能
    mutantedpop = mutation.mutantion(crossedpop, pm)  # 验证mutant功能
    childpop_repeat = delete_repeat.delete_repeat_chrom(mutantedpop)
    newpop = update_population.update_deleteSim(temp, childpop_repeat, popsize)  ## 验证update功能
    # print
    # 'update result:', newpop
    list = feasibility.is_feasible_list(newpop)
    if len(list) < popsize:
        for i in range(len(list)):
            if list[i] == False:
                newpop[i] = pop[i]
    return newpop


if __name__ == '__main__':
    filepath = './efsmGA/files/'
    fo = open(filepath + 'input.txt', 'r')
    setting = json.load(fo)
    fo.close()
    popsize = 10
    pc = 0.9
    pm = 0.3
    # flag=1,全状态覆盖，=2，迁移覆盖
    startTime = datetime.now()  # 记录开始时间
    pop = initial_population.initalpop_new(popsize)
    count = 0
    flag = 0
    flag = int(setting['type'])
    end_need_num = 0
    if flag == 1:
        end_need_num = obtain_efsm_info.state_number()
    elif flag == 2:
        end_need_num = obtain_efsm_info.tran_number()
    while 1:
        pop_history(pop, flag)
        if (len(history) >= end_need_num) or (count == 400):
            print
            '======================================================='
            print
            'geneneration:', count
            break
        pop = GA(pop, pc, pm, popsize, flag)
        count = count + 1
    endTime = datetime.now()
    during = endTime - startTime
    # print
    # during
    path = OrderedDict()
    if flag == 2:
        path['name'] = "全迁移"
        print
        '=====================' + str(len(history)) + '条迁移全覆盖==========================='
    elif flag == 1:
        path['name'] = "全状态"
        print
        '=====================' + str(len(history)) + '个状态全覆盖==========================='
    for i in range(len(ind_history)):
        path["path" + str(i + 1)] = ind_history[i]
    with open(filepath + 'output.txt', 'w+') as f:
        json.dump(path, f, indent=4, ensure_ascii=False)
        print("路径写入json文件完成...")
