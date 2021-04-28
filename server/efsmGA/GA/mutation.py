#encoding:UTF-8
from __future__ import division     #ensure that float number when divide

import random
from random import choice
from collections import Counter
import initial_population
import obtain_efsm_info
import cal_chrofitness


def mutantion(crossedchrolist,pm):
    mutantedchrolist = []
    for i in range(len(crossedchrolist)):
        mutantedchro=crossedchrolist[i]
        randnum = random.uniform(0,1)  # 随机数 决定进行哪个变异算子
        if randnum<=(pm):   # 变异1：随机改变一个子path
            traninforlist = obtain_efsm_info.obtain_tran_info()  # 得到全部transition信息
            endtranlist=obtain_efsm_info.obtain_end_tranlist() #得到终止迁移name list

            for num in range(5):  #最多重选5次，如果仍找不到可变异的子path，则不进行变异
                tran_index=random.randint(0,len(mutantedchro)-2)  # 获得该transition的位置
                mutantran=mutantedchro[tran_index]  #记录该transition的name
                temp1=mutantedchro[0:tran_index] #将原path（个体）拆分成两部分
                #temp2=mutantedchro[tran_index:]
                samesrc_tranlist=[]   #存放mutantran的兄弟迁移
                for item in traninforlist:
                    if item.name == mutantran:
                        src_state=item.src.name
                        for i in traninforlist:
                            if (i.src.name == src_state) and (i.name not in endtranlist):
                                samesrc_tranlist.append(i.name)
                        break
                if len(samesrc_tranlist)!=0:  #有可替换的兄弟迁移，则随机选择一兄弟，随机生成由该兄弟出发的子path
                    newtran=choice(samesrc_tranlist)   #newtran不能为终止迁移之一！

                    while 1:
                        p = initial_population.random_subpath(newtran)
                        if len(p) < 17:
                            break
                    newpath=temp1+p
                    mutantedchrolist.append(newpath)
                    #print '1变异成功'
                    break
                if num == 4:   #始终没找到可以改变的subpath
                    mutantedchrolist.append(mutantedchro)
                    #print '1变异失败'
            continue
        else:  # 不变异情况
           mutantedchrolist.append(mutantedchro)
           #print '不变异'
    return mutantedchrolist
    '''elif randnum<=(pm):  #变异2：随机替换一个同源同目标状态的迁移
            traninforlist = obtain_efsm_info.obtain_tran_info()  # 得到全部transition信息

            for num in range(5):
                mutantran = choice(mutantedchro)  # 随机选择一个 变异transition
                tran_index = mutantedchro.index(mutantran)  # 获得该transition的位置
                src = []  # 存储该迁移的源状态
                tgt = []  # 存储该迁移的目标状态
                for item in traninforlist:
                    if item.name == mutantran:
                        src.append(item.src.name)
                        tgt.append(item.tgt.name)
                        break
                candidate_tran = []  # 用来存储同源同目标的transition
                for item in traninforlist:
                    if (item.src.name == src[0]) and (item.tgt.name == tgt[0]) and (item.name != mutantran):
                        candidate_tran.append(item.name)
                if len(candidate_tran) != 0:
                    r = random.randint(0, len(candidate_tran) - 1)
                    mutantedchro[tran_index]=candidate_tran[r]
                    mutantedchrolist.append(mutantedchro)
                    #print '2变异成功'
                    break
                if num == 4:
                    mutantedchrolist.append(mutantedchro)
                    #print '2变异失败'
            continue'''


    '''elif randnum <=pm:  #变异3：在path末尾随机附加一个迁移，若efsm有终止迁移，该变异无法执行
            endtranlist=obtain_efsm_info.obtain_end_tranlist()  #得到efsm的终止迁移list
            traninforlist = obtain_efsm_info.obtain_tran_info()  # 得到全部transition信息
            path_last=mutantedchro[-1]

            if path_last in endtranlist:
                mutantedchrolist.append(mutantedchro)
            else:
                succ_tranlist=[]
                for item in traninforlist:
                    if item.name == path_last:  #找到该tran的终止状态
                        tgt_tran=item.tgt.name
                        for tran in traninforlist:
                            if tran.src.name == tgt_tran:  #找到从此终止状态出发的所有tran
                                succ_tranlist.append(tran.name)
                        break
                newtran=choice(succ_tranlist)
                mutantedchro.append(newtran)
                mutantedchrolist.append(mutantedchro)
            continue'''






if __name__ == '__main__':
    crossedpop=[['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T23'],
                 ['T1', 'T2', 'T2', 'T4', 'T6', 'T23'],
                 ['T1', 'T4', 'T5', 'T7', 'T9', 'T8', 'T17', 'T22', 'T10', 'T23'],
                 ['T1', 'T2', 'T4', 'T6', 'T7', 'T9', 'T23'],
                 ['T1', 'T4', 'T5', 'T8', 'T10', 'T23'],
                 ['T1', 'T2', 'T4', 'T6', 'T7', 'T9', 'T7', 'T13', 'T15', 'T9', 'T8', 'T20', 'T22', 'T10', 'T7', 'T9', 'T23']]

    crossedpop=[['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T17', 'T22', 'T10', 'T8', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22',
              'T10', 'T8', 'T10', 'T7', 'T11', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T21', 'T20', 'T21', 'T20',
              'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15',
              'T9', 'T23'],
             ['T1', 'T2', 'T4', 'T5', 'T8', 'T20', 'T22', 'T17', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10',
              'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T7', 'T13', 'T15', 'T13', 'T16',
              'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T17', 'T22', 'T10', 'T8', 'T20', 'T21', 'T18', 'T22', 'T20', 'T21',
              'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13',
              'T15', 'T9', 'T23'], ['T1', 'T4', 'T5', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8',
              'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T8', 'T19', 'T21', 'T18', 'T21', 'T17',
              'T22', 'T10', 'T8', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8',
              'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T21', 'T20', 'T22', 'T18',
              'T21', 'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T21', 'T20', 'T22', 'T18',
              'T21', 'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T22', 'T10', 'T7', 'T13', 'T15',
              'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22',
              'T10', 'T8', 'T10', 'T7', 'T9', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T22', 'T10', 'T7', 'T9', 'T7',
              'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8',
              'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22',
              'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T18', 'T22', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8',
              'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22',
              'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8',
              'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T19', 'T21', 'T18', 'T21', 'T17', 'T22', 'T10', 'T7', 'T9', 'T7', 'T13', 'T15',
              'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T22', 'T10', 'T8', 'T10', 'T8',
              'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13',
              'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T17', 'T22', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21',
              'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T7', 'T13',
              'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23'],
             ['T1', 'T4', 'T5', 'T8', 'T17', 'T22', 'T10', 'T8', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22',
              'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23']]
    test=[['T1', 'T4', 'T5', 'T8', 'T17', 'T21', 'T19', 'T21', 'T18', 'T21', 'T17', 'T21', 'T20', 'T21', 'T20', 'T22', 'T18', 'T21', 'T19', 'T22', 'T10', 'T8', 'T10', 'T7', 'T13', 'T15', 'T13', 'T16', 'T13', 'T15', 'T9', 'T23']]

    mutantedpop=mutantion(test,0.9)

    print mutantedpop
    print test


    #p = obtain_efsm_info.find_subpath('T8')  # 得到从该迁移发出的subpath 列表
    #print p


