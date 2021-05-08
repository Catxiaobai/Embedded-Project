#encoding:UTF-8
from __future__ import division     #ensure that float number when divide

import random
from random import choice

import obtain_efsm_info

def crossover(selectedchrolist,pc):
    crossedchrolist = []
    for i in range(0,len(selectedchrolist),2):    #每两个个体作为一对父母
        momchro=selectedchrolist[i]
        dadchro=selectedchrolist[i+1]
        randnum=random.uniform(0,1)       #随机数决定是否执行交叉
        #print randnum     # for test
        if randnum <= pc:
            traninforlist = obtain_efsm_info.obtain_tran_info()  # 得到全部transition信息

            for num in range(5):  #最多重选5次，如果仍找不到可交叉的子path，则不进行交叉
                crosstran = choice(momchro)  # 在mom path 中随机选择一个 交叉transition
                tran_index = momchro.index(crosstran)  # 获得该transition的位置

                temp1=momchro[0:tran_index] #将mom拆分成两部分
                temp2=momchro[tran_index:]

                samesrc_tranlist=[]   #存放crosstran的兄弟迁移
                for item in traninforlist:
                    if item.name == crosstran:
                        src_state=item.src.name
                        for i in traninforlist:
                            if i.src.name == src_state:
                                samesrc_tranlist.append(i.name)
                        break

                intersectionlist=list(set(samesrc_tranlist).intersection(set(dadchro))) #dad path与兄弟迁移的交集
                if len(intersectionlist) != 0:
                    crosstran_indad=choice(intersectionlist)
                    index_indad=dadchro.index(crosstran_indad)  #若该tran在dad中是重复出现的，只能每次选靠前的那一个作为交叉点
                    temp3=dadchro[0:index_indad]
                    temp4=dadchro[index_indad:]

                    newpath1=temp1+temp4   # 得到交叉后的两个path
                    newpath2=temp3+temp2
                    crossedchrolist.append(newpath1)  #将交叉后的path存入新种群中
                    crossedchrolist.append(newpath2)
                    #print '交叉成功'
                    break
                if num == 4:
                    crossedchrolist.append(momchro)
                    crossedchrolist.append(dadchro)
                    #print '交叉失败'
        else:   #不进行交叉的情况
            crossedchrolist.append(momchro)
            crossedchrolist.append(dadchro)
            #print '不交叉'

    return crossedchrolist


if __name__ == '__main__':
    selectedpop=[['T1', 'T2', 'T2', 'T2', 'T4', 'T5', 'T23'],
                 ['T1', 'T2', 'T2', 'T4', 'T6', 'T23'],
                 ['T1', 'T4', 'T5', 'T7', 'T9', 'T8', 'T17', 'T22', 'T10', 'T23'],
                 ['T1', 'T2', 'T4', 'T6', 'T7', 'T9', 'T23'],
                 ['T1', 'T4', 'T5', 'T8', 'T10', 'T23'],
                 ['T1', 'T2', 'T4', 'T6', 'T7', 'T9', 'T7', 'T13', 'T15', 'T9', 'T8', 'T20', 'T22', 'T10', 'T7', 'T9', 'T23']]

    crossedresult=crossover(selectedpop,0.8)
    print crossedresult
    print selectedpop



