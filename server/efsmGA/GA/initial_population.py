#encoding:UTF-8
import random
from random import choice
from collections import Counter
import obtain_efsm_info
import delete_repeat


def validpath_matrix():    #将efsm迁移关系存储在矩阵中
    traninfolist=obtain_efsm_info.obtain_tran_info()
    #print traninfolist
    matrix=[]
    for line in range(len(traninfolist)):
        temp=[]
        for row in range(len(traninfolist)):
            if traninfolist[line].tgt.name == traninfolist[row].src.name:
                temp.append(1)
            else:
                temp.append(0)
        matrix.append(temp)
    return matrix
def get_endtran_from_matrix():  #行全0的为end transition
    m=validpath_matrix()
    endtran = []
    for i in range(len(m)):
        if 1 not in m[i]:
            endtran.append(i)  #+1为了直观看出迁移ID
    return endtran

def get_startran_from_matrix():    #列全0的为start transition
    m=validpath_matrix()
    startran = []
    l = map(list, zip(*m))  # 转置矩阵
    for k in range(len(l)):
        if 1 not in l[k]:
            startran.append(k)   #+1为了直观看出迁移ID
    return startran

def random_path():   #从关系矩阵中随机得到一条efsm有效序列
    path=[]
    path_new=[]
    startlist=get_startran_from_matrix()
    endlist=get_endtran_from_matrix()
    print startlist,endlist
    m=validpath_matrix()
    i=choice(startlist)
    path.append(i)
    while 1:
            while 1:
                randnum = random.randint(0, len(m[i]) - 1)
                if (m[i][randnum] == 1) :
                    path.append(randnum)
                    break
            i=randnum
            if i in endlist:
                break
    for index in range(len(path)):
        tran='T'+str(path[index]+1)
        path_new.append(tran)
    return path_new

def random_subpath(transition):  #以给定transition为开始的子path

    tran_matrix_index=int(transition[1:])-1  #将字符串迁移编号转换成矩阵的行号

    path = []
    path_new = []

    endlist = get_endtran_from_matrix()
    m = validpath_matrix()
    i = tran_matrix_index
    path.append(i)
    while 1:
        while 1:
            randnum = random.randint(0, len(m[i]) - 1)
            if (m[i][randnum] == 1):
                path.append(randnum)
                break
        i = randnum
        if i in endlist:
            break
    for index in range(len(path)):
        tran = 'T' + str(path[index] + 1)
        path_new.append(tran)
    return path_new

'''def random_subpath_length(transition):   #对由某tran产生的subpath长度进行限制，不能过长
    while 1:
        subpath_length=random_subpath(transition)
        if len(subpath_length)<17 and len(subpath_length)>1:
            break
    return subpath_length'''

def chromsome():   # 个体=a path，对path的长度、重复迁移个数进行限制
    while 1:
        p=random_path()
        timeslist = Counter(p).values()  # 每个重复出现的迁移的出现次数
        maxtimes = max(timeslist)
        if len(p)<15 and len(p)>2 and maxtimes<15:   #这里的限定需要再做考虑！！
            break
    return p

def initalpop(popsize):  # 初始化种群，即pathlist(不能保证初始种群中没重复个体)
    pop = []
    for k in range(popsize):
        pop.append(chromsome())
    return pop

#==============2018.1.5添加，保证初始种群个体是不重复的=============
#初始化种群，无重复个体
def initalpop_new(popsize):
    pop = []
    count = 0
    while 1:
        c = chromsome()
        if c not in pop:
            pop.append(c)
            count = count + 1
            if count == popsize:
                break
    return pop

def initialpop_feasible(popsize):  #初始化种群，使得种群中全部path 潜在可行
    pop=[]
    for k in range(popsize):
        while 1:
            path = chromsome()
            if is_feasible(path) == True and (path not in pop):
                pop.append(path)
                break
    return pop

def is_feasible(currpath):  #可行性判断
    conflictTran = {}
    conflictTran["T5"] = ["T11", "T16", "T20", "T22"]
    conflictTran["T6"] = ["T12", "T15", "T19", "T21"]
    tempPath = currpath[:]
    while tempPath:
        firstTran = tempPath[0]
        restTranList = tempPath[1:]
        if firstTran in conflictTran.keys():
            for tran in restTranList:
                if tran in conflictTran[firstTran]:
                    return False
        tempPath = restTranList
    return True

if __name__ == '__main__':  # not execute when import as a module
    pop=initalpop_new(22)
    print pop
    print len(delete_repeat.delete_repeat_chrom(pop))
    #pop=initialpop_feasible(20)
    #test=['T1', 'T2', 'T2', 'T4', 'T6', 'T8', 'T18', 'T21', 'T10', 'T7', 'T11', 'T15', 'T13', 'T16', 'T9', 'T8', 'T10', 'T7', 'T11', 'T16', 'T13', 'T16', 'T14', 'T16', 'T9', 'T8', 'T17', 'T22', 'T20', 'T22', 'T10', 'T8', 'T10', 'T23']
    '''print pop
    count=0
    for i in range(len(pop)):
        t=is_feasible(pop[i])
        if t == True:
            count=count+1
    print count'''
    #print is_feasible(test)
    #print random_subpath_length('T5')
    #print chromsome()
    #print get_endtran_from_matrix()
    #print get_startran_from_matrix()
    print random_path()













