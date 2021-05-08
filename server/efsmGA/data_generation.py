# encoding:utf-8
import random
import EFSM
import obtain_efsm_info
import protocol
import time
import INTBYTE
path = './efsmGA/files/'
fo=open(path+'input.txt','r')
lines=fo.readlines()
fo.close()
setting={}
for line in lines:
    line=line.strip()
    if '"' not in line:
        continue
    line=line.replace('"','')
    index=line.find(':')
    key=line[:index]
    value=line[index+1:]
    setting[key]=value
modelfiledir = './efsmGA/files/'
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
            data.extend(SM.pathVarValue)
            break  # break for j loop
        j += 1
        population = gaSample.GeneticAlgorithm(oldInvidualFit, population, pathVarType)
        invidualFitness = SM.obtainIndividualFitness(currPath, population, populationSize, noInputVar,varname)
        if invidualFitness[0] == 0:
            data.extend(SM.pathVarValue)
            break  # break for j loop
        population = gaSample.basicSurvive(oldInvidualFit, invidualFitness, population)
        if  j >= 20000:
            print 'this path is not feasible'
            return []
    return data
def dfs(data,tmp,k):
    if k==len(data):
        fo = open(path+'output.txt', 'a')
        for i in range(len(tmp)):
            fo.write(tmp[i])
            if i <len(tmp)-1:
                fo.write(' ')
        fo.write("\n")
        fo.close()
        return None
    for i in [0,1]:
        if i==0:
            tmp.append(('\"F\":\"')+str(data[k]['ctr'][i])+'"')
        else:
            tmp.append(('\"T\":\"') + str(data[k]['ctr'][i]) + '"')
        dfs(data,tmp,k+1)
        tmp.pop()

def testProcee(SM, currPathT,flag,num=0,accuracy=1,TIME=0):
    coverage = 0
    populationSize=20
    varname = obtain_var_from_path(SM, currPathT)  #获得序列上的变量名
    pathVarType=obtain_vartype_from_varname(SM, varname)#获得变量类型
    if len(SM.originalDef) ==0:
        print"The path has no variables"
        data = []
        SM.executePath(currPathT, 0)
    elif flag==1:  ##There exist input variables on the path
        vecdata = []
        if num>0:
            while (num > 0):
                vecdata.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize))  # 测试数据生成
                num -= 1
        elif TIME>0:
            startTime = time.time()
            while(time.time()-startTime<TIME):
                vecdata.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize))  # 测试数据生成
        #vecdata[0].read()
        fo = open(path+'output.txt', 'w')
        fo.write('{\n\"name\":\"random test data generation\"')
        data=vecdata
        for i in range(len(data)):
            strf='\n"'+"测试用例"+str(i+1)+'"'
            fo.write(strf)
            k = 0
            for currTrans in currPathT:
                strf='\n'+currTrans
                fo.write(strf)
                for ftran, fdict in SM.currPathTranFuncDict.iteritems():
                    if ftran == currTrans:
                        ###########deal with event variables#############################
                        if SM.tranVarDict[currTrans]['eventVdef'] != []:
                            for var in SM.tranVarDict[currTrans]['eventVdef']:
                                strf=' "'+ str(var) +'_var'+currTrans[1:]+'"'+':'+'"'+str(data[i][k])+'"'
                                fo.write(strf)
                                k += 1
        fo.write('\n}')
        fo.close()
    elif flag==2 :
        data=SM.bianJie(currPathT,pathVarType,accuracy,1)
        fo = open(path+'output.txt', 'w')
        fo.write('{\n\"name\":\"边界值 test data generation\"')
        k = 0
        for currTrans in currPathT:
            strf = '\n' + currTrans
            fo.write(strf)
            for ftran, fdict in SM.currPathTranFuncDict.iteritems():
                if ftran == currTrans:
                    ###########deal with event variables#############################
                    if SM.tranVarDict[currTrans]['eventVdef'] != []:
                        for var in SM.tranVarDict[currTrans]['eventVdef']:
                            strf = ' "' + str(var) + '_var' + currTrans[1:] + '"' + ':' + '"' + str(data[k][var]) + '"'
                            fo.write(strf)
                        k += 1
        fo.write('\n}')
        fo.close()
    elif flag==3:#逐渐增加
        ans = []
        vecdata = []
        while(num>0):
            vecdata.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize))  # 测试数据生成
            num-=1
        for j in range(len(vecdata[0])):
            ans.append([])
            for i in range(len(vecdata)):
                ans[j].append(vecdata[i][j])
            ans[j].sort()
        data=ans
        k = 0
        fo = open(path+'output.txt', 'w')
        fo.write('{\n\"name\":\"increase test data generation\"')
        for currTrans in currPathT:
            strf = '\n' + currTrans
            fo.write(strf)
            for ftran, fdict in SM.currPathTranFuncDict.iteritems():
                if ftran == currTrans:
                    ###########deal with event variables#############################
                    if SM.tranVarDict[currTrans]['eventVdef'] != []:
                        for var in SM.tranVarDict[currTrans]['eventVdef']:
                            strf = ' "' + str(var) + '_var' + currTrans[1:] + '"' + ':' + '"' + str(data[k]) + '"'
                            fo.write(strf)
                            k += 1
        fo.write('\n}')
        fo.close()
    elif flag == 4:  # 逐渐减少
        ans = []
        vecdata = []
        while (num > 0):
            vecdata.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize))  # 测试数据生成
            num -= 1
        for j in range(len(vecdata[0])):
            ans.append([])
            for i in range(len(vecdata)):
                ans[j].append(vecdata[i][j])
            ans[j].sort(reverse=True)
        data = ans
        k = 0
        fo = open(path+'output.txt', 'w')
        fo.write('{\n\"name\":\"descending test data generation\"')
        for currTrans in currPathT:
            strf = '\n' + currTrans
            fo.write(strf)
            for ftran, fdict in SM.currPathTranFuncDict.iteritems():
                if ftran == currTrans:
                    ###########deal with event variables#############################
                    if SM.tranVarDict[currTrans]['eventVdef'] != []:
                        for var in SM.tranVarDict[currTrans]['eventVdef']:
                            strf = ' "' + str(var) + '_var' + currTrans[1:] + '"' + ':' + '"' + str(data[k]) + '"'
                            fo.write(strf)
                            k += 1
        fo.write('\n}')
        fo.close()
    elif flag == 5:  #CDMD
        tmp=[]
        data = SM.CDMD(currPathT,pathVarType, 1)
        fo = open(path+'output.txt', 'w')
        fo.write('{\n\"name\":\"MC/DC test data generation\"\n')
        for i in currPathT:
            fo.write('   \"'+i+'\"   ')
        fo.write("\n")
        fo.close()
        dfs(data,tmp,0)
        fo = open(path+'output.txt', 'a')
        fo.write("}")
        fo.close()
    return varname,data

if __name__ == '__main__':
    flag =int(setting['type'])
    traninfolist = obtain_efsm_info.obtain_tran_info()  # 迁移信息全部在这
    pathstr=setting['path']
    pathstr = pathstr.lstrip('[')
    pathstr = pathstr.rstrip(']')
    path = pathstr.split(',')

    num=int(setting['amount'])
    TIME=int(setting['time'])
    precision = float(setting['precision'])
    vername,data = testProcee(SM, path,flag,num,precision,TIME)
