# encoding:utf-8
import random
import EFSM
import obtain_efsm_info
import protocol
import INTBYTE

modelfiledir = '../subjects/'
#模型
modelfile = "EFSM_ATM.txt"
inputfile = modelfiledir + modelfile
SM = EFSM.efsmFromFile(inputfile)    #对efsm类实例化
SM.allPathNum()
#获得路径上的变量名
def obtain_var_from_path(SM, currPathT):
    SM.repeatTranVarDict = {}
    SM.repeatTranFuncDict = {}  ####store repeat transition
    SM.currPathTranVarDict = {}
    SM.currPathTranFuncDict == {}
    SM.copyPathInfo()
    for tran in currPathT:  # change the varibale name for the same T
        if currPathT.count(tran) > 1:
            SM.repeatTrans(currPathT)
            break
    SM.pathInputVar(currPathT)  # identify input variable in events relating to the current path
    SM.pathProProcess(currPathT)  # rewrite identical variables, ---stored in self.pathDefVar
    varname = SM.originalDef
    return varname

#根据变量名获得变量的类型
def obtain_vartype_from_varname(SM, varnme):
    pathVarType={}
    for i in range(len(varnme)):
        pathVarType[i]=('INT16')
    return pathVarType

def random_int(l,r):
    return  random.randint( l, r)

def Initial_data(SM,currPath, varname, pathVarType, populationSize):#根据GA进行测试数据生成
    noInputVar=0
    gaSample = EFSM.GA(populationSize, len(SM.pathDefVar))
    population = gaSample.creatStartPopulation(pathVarType)  ###initiate Population according to input variable number
    j = 1
    data = []
    while 1:
        oldInvidualFit = SM.obtainIndividualFitness(currPath, population, populationSize, noInputVar,varname)
        if oldInvidualFit[0] == 0:
            print 'No' + '\tsuccessGeneration\t', j
            #SM.outputTestData(currPath, pathVarType, 0)
            data.append(SM.pathVarValue)
            break  # break for j loop
        j += 1
        population = gaSample.GeneticAlgorithm(oldInvidualFit, population, pathVarType)
        invidualFitness = SM.obtainIndividualFitness(currPath, population, populationSize, noInputVar,varname)
        if invidualFitness[0] == 0:
            print 'No' + '\tsuccessGeneration\t', j
            #SM.outputTestData(currPath, pathVarType, 0)
            data.append(SM.pathVarValue)
            break  # break for j loop
        population = gaSample.basicSurvive(oldInvidualFit, invidualFitness, population)
        if  j >= 20000:
            print 'this path is not feasible'
            return []

    return data

def testProcee(SM, currPathT):
    coverage = 0
    populationSize=20
    varname = obtain_var_from_path(SM, currPathT)  #获得序列上的变量名
    pathVarType=obtain_vartype_from_varname(SM, varname)#获得变量类型
    if len(SM.originalDef) > 0:  ##There exist input variables on the path
        vecdata = Initial_data( SM, currPathT, varname, pathVarType, populationSize)  #测试数据生成
        #vecdata[0].read()
        data = vecdata
    else:
        print"The path has no variables"
        data = []
        SM.executePath(currPathT, 1)
    return varname,data[0]


if __name__ == '__main__':
    traninfolist = obtain_efsm_info.obtain_tran_info()  # 迁移信息全部在这
    path = ['T1', 'T2', 'T7', 'T11', 'T19']
    vername,data = testProcee(SM, path)
    print vername
    print data
