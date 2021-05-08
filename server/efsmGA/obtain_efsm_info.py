# encoding:UTF-8


import EFSM

modelfiledir = './efsmGA/files/'
# 模型
modelfile = "EFSM_ATM.txt"
inputfile = modelfiledir + modelfile
SM = EFSM.efsmFromFile(inputfile)  # 对efsm类实例化
SM.allPathNum()


def obtain_tran_info():  # 得到某efsm的全部迁移信息（name, src, tgt, event, cond, action）
    return SM.transitionList
    # print SM.transitionList[1].src.name


def tran_number():
    return len(SM.transitionList)


def state_number():
    return len(SM.stateList)


def obtain_end_tranlist():  # 得到end transition list
    SM.findEndTransition()
    return SM.endTransitionList


def obtain_start_tranlist():
    SM.findStartTransition()
    return SM.startTransitionList


def obtain_succ():
    SM.initTransitionSuccessor()
    return SM.succDict


def find_subpath(start):  # 得到从某tran出发的的有效sub-path
    obtain_tran_info()
    obtain_succ()

    pathlist = SM.findPath(start)
    return pathlist


def find_allpath():
    obtain_start_tranlist()
    obtain_tran_info()
    obtain_succ()

    pathlist = SM.findAllPath()
    return pathlist


if __name__ == '__main__':  # not execute when import as a module
    print
    "%s has %s states and  %s transitions" % (SM.name, len(SM.stateList), len(SM.transitionList))
    traninfolist = obtain_tran_info()  # 迁移信息全部在这
    path = ['T1', 'T3', 'T6', 'T7', 'T9', 'T10', 'T5', 'T11', 'T19', 'T7', 'T9', 'T10', 'T4']
    SM.testGen()
