# encoding:utf-8
import random
import EFSM
import obtain_efsm_info
import json
import time
import protocol
from collections import OrderedDict
protocolInf=protocol.protocol()
modelfiledir = './efsmGA/files/'
filepath = './efsmGA/files/'
# 模型
modelfile = "efsm_atm.txt"
inputfile = modelfiledir + modelfile
SM = EFSM.efsmFromFile(inputfile)  # 对efsm类实例化
SM.allPathNum()
#获得路径上的变量名
def dfsF2(keys,data,tmp,k,ans,protocol1):
    if k==len(keys):
        protocol1.set(tmp)
        ans.append(protocol1.read())
        return None
    name=keys[k]
    for i in data[keys[k]]:
        if i<0:
            continue
        tmp[name]=i
        dfsF2(keys,data,tmp,k+1,ans,protocol1)
        tmp.pop(name)
def obtain_var_from_path(SM, currPathT):
    SM.repeatTranVarDict = {}
    SM.repeatTranFuncDict = {}  ####store repeat transition
    SM.currPathTranVarDict = {}
    SM.currPathTranFuncDict == {}
    SM.copyPathInfo()
    trans_currPathT=[]
    for tran in currPathT:  # change the varibale name for the same T
        if currPathT.count(tran) > 1:
            SM.repeatTrans(currPathT)
            break
    SM.pathInputVar1(currPathT,trans_currPathT)  # identify input variable in events relating to the current path
    SM.pathProProcess(currPathT)  # rewrite identical variables, ---stored in self.pathDefVar
    varname = SM.originalDef
    return varname,trans_currPathT
#根据变量名获得变量的类型
def obtain_vartype_from_varname(SM, varname):
    pathVarType={}
    for i in range(len(varname)):
        pathVarType[i]=protocolInf.getDataType(varname[i])
    return pathVarType

def random_int(l,r):
    return  random.randint( l, r)

def Initial_data(SM,currPath, varname, pathVarType, populationSize,trans_currPathT):#根据GA进行测试数据生成
    noInputVar=0
    gaSample = EFSM.GA(populationSize, len(SM.pathDefVar))
    population = gaSample.creatStartPopulation(varname,trans_currPathT)  ###initiate Population according to input variable number
    j = 1
    data = []
    #print population
    while 1:
        oldInvidualFit = SM.obtainIndividualFitness(currPath, population, populationSize, noInputVar,varname)
        if oldInvidualFit[0] == 0:
            data.extend(SM.pathVarValue)
            break  # break for j loop
        j += 1
        #print population
        population = gaSample.GeneticAlgorithm(oldInvidualFit, population, varname)
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
        fo = open(filepath + 'output.txt', 'a')
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
    varname,trans_currPathT = obtain_var_from_path(SM, currPathT)  #获得序列上的变量名
    pathVarType=obtain_vartype_from_varname(SM, varname)#获得变量类型
    data = []

    if len(SM.originalDef) ==0:
        print"The path has no variables"
        SM.executePath(currPathT, 0)
    elif flag==1:  ##There exist input variables on the path
        if num>0:
            while (num > 0):
                data.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize,trans_currPathT))  # 测试数据生成
                num -= 1
        elif TIME>0:
            startTime = time.time()
            while(time.time()-startTime<TIME):
                data.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize,trans_currPathT))  # 测试数据生成
    elif flag==2 :
        data=SM.bianJie(currPathT,varname,accuracy,1)
    elif flag==3:#逐渐增加
        ans = []
        while(num>0):
            ans.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize,trans_currPathT))  # 测试数据生成
            num-=1
        for j in range(len(ans[0])):
            data.append([])
            for i in range(len(ans)):
                data[j].append(ans[i][j])
            data[j].sort()
    elif flag == 4:  # 逐渐减少
        ans = []
        while (num > 0):
            ans.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize,trans_currPathT))  # 测试数据生成
            num -= 1
        for j in range(len(ans[0])):
            data.append([])
            for i in range(len(ans)):
                data[j].append(ans[i][j])
            data[j].sort(reverse=True)
    elif flag == 5 or flag==6:  #CDMD
        data = SM.CDMD(currPathT,pathVarType, 1)
    elif flag == 7 :  #接口异常
        data.append(Initial_data(SM, currPathT, varname, pathVarType, populationSize,trans_currPathT))
    return data
def tran_var_macth(currPathT):
    tran_var= OrderedDict()
    for currTrans in currPathT:
        tran_var[currTrans]=[]
        for ftran, fdict in SM.currPathTranFuncDict.iteritems():
            if ftran == currTrans:
                ###########deal with event variables#############################
                if SM.tranVarDict[currTrans]['eventVdef'] != []:
                    for var in SM.tranVarDict[currTrans]['eventVdef']:
                        tran_var[currTrans].append(var)
    return tran_var
def ALLT(data):
    tmp=[]
    flag=""
    for i in data:
        flag+='T'
        for key,value in i.items():
            if 'F' not in key:
                tmp.append(value)
    return flag,tmp


def dfsF3(keys,data,tmp,k,ans,protocol1):
    if k==len(keys):
        protocol1.set(tmp)
        ans.append(protocol1.read())
        return None
    name=keys[k]
    for i in data[k]:
        if i<0:
            continue
        tmp[name]=i
        dfsF3(keys,data,tmp,k+1,ans,protocol1)
        tmp.pop(name)

def i_is_F(data,flag_S,k,tmp,test):
    for key,value in data[k].items():
        if 'F' not in key:
            continue
        else:
            flag=flag_S[:k]+"("+key+")"+flag_S[k+1:]
            tmp[k]=value
            test[flag]=tmp
def dfs_ALL(path,i,noCondition,ans_T_F,tmp,test,flag):
    if i>len(path):
        test[flag]=tmp.copy()
        return None
    f=flag
    currTran = str(path[i - 1])
    if currTran not in noCondition:
        key = currTran + "_" + str(i)
        for k, v in ans_T_F[key].items():
            tmp[key] = v
            if 'F' in k:
                f=flag[:i-1]+k+flag[i:]
            else:
                f=flag[:i-1]+'T'+flag[i:]
            dfs_ALL(path,i+1,noCondition,ans_T_F,tmp,test,f)
            tmp[key] = v
    else:
        dfs_ALL(path, i+1, noCondition, ans_T_F, tmp, test, flag)
def cover_data(path,data,flag):
    protocol1=protocol.protocol()
    tran_var=tran_var_macth(path)
    test = OrderedDict()
    with open(filepath + 'parameter.txt', 'w') as f:
        json.dump(tran_var, f,indent=4,ensure_ascii=False)
        print("数据写入json文件完成...")
    if flag==1:
        test['name']="随机测试"
        for i in range(len(data)):
            k=0
            case = OrderedDict()
            name="case"+str(i+1)
            for tran in path:
                tmp = {}
                for j in tran_var[tran]:
                    tmp[j]=data[i][k]
                    k+=1
                protocol1.set(tmp)
                case[tran]=protocol1.read()
            test[name]=case
    elif flag==2:
        test['name']="边界值测试"
        for i in range(len(path)):
            tmp={}
            ans=[]
            dfsF2(tran_var[path[i]],data[i],tmp,0,ans,protocol1)
            test[path[i]]=ans
    elif flag==3 or flag==4:
        if flag==3:
            test['name'] = "递增测试"
        else:
            test['name'] = "递减测试"
        l=0
        r=0
        for tran in path:
            tmp = {}
            ans = []
            r+=len(tran_var[tran])
            dfsF3(tran_var[tran], data[l:r], tmp, 0, ans, protocol1)
            l=r
            test[tran] = ans
    elif flag == 5 or flag == 6:
        test['name'] = "MC/DC测试"
        noCondition=data["noCondition"]
        ans_T_F={}
        for i in range(1,len(path)+1):
            currTran=str(path[i-1])
            currTran_data = data[currTran + "_" + str(i)]
            tmp = {}
            ans_Tran = {}
            for j in tran_var[currTran]:
                tmp[j] = currTran_data[j][0]
            protocol1.set(tmp)
            ans_Tran["T"] = protocol1.read()
            if currTran not in noCondition:
                for j in tran_var[currTran]:
                    if len(currTran_data[j])==2:
                        tmp[j]=currTran_data[j][1]
                        protocol1.set(tmp)
                        ans_Tran["F_"+j] = protocol1.read()
                        tmp[j] = currTran_data[j][0]
            ans_T_F[currTran+"_"+str(i)]= ans_Tran
        tmp=OrderedDict()
        f=""
        for i in range(1, len(path) + 1):
            currTran = str(path[i - 1])
            f+="T"
            key = currTran + "_" + str(i)
            tmp[key] = ans_T_F[key]['T']
        if flag==5:
            test['T'] = tmp.copy()
            for i in range(1, len(path) + 1):
                currTran = str(path[i - 1])
                if currTran not in noCondition:
                    key=currTran+"_"+str(i)
                    for k,v in ans_T_F[key].items():
                        if k!='T':
                            tmp[key]=v
                            test[key+'_'+k] = tmp.copy()
                            tmp[key]=ans_T_F[key]['T']
        elif flag==6:
            test['name'] = "全条件测试"
            dfs_ALL(path, 1, noCondition, ans_T_F, tmp, test,f)
    elif flag==7:
        test['name'] = "接口异常"
        for i in range(len(data)):
            k=0
            for tran in path:
                case = OrderedDict()
                tmp = {}
                for j in tran_var[tran]:
                    tmp[j]=data[i][k]
                    k+=1
                protocol1.set(tmp)
                case['正常'] = protocol1.read()
                case['帧头异常'] = protocol1.readBadHead(88)
                case['帧尾异常'] = protocol1.readBadEnd(77)
                case['校验和异常'] = protocol1.readBadCrc(90)
                test[tran] = case
    with open(filepath + 'output.txt', 'w') as f:
        json.dump(test, f,indent=4,ensure_ascii=False)
        print("数据写入json文件完成...")
if __name__ == '__main__':
    fo = open(filepath + 'input.txt', 'r')
    setting = json.load(fo)
    fo.close()
    #print setting
    flag =int(setting['type'])
    traninfolist = obtain_efsm_info.obtain_tran_info()  # 迁移信息全部在这
    path=setting['path']

    num=int(setting['amount'])
    TIME=int(setting['time'])
    if '.' in str(setting['precision']):
        precision = float(setting['precision'])
    else:
        precision = int(setting['precision'])
    #print precision
    data = testProcee(SM, path,flag,num,precision,TIME)
    #print "data",data
    cover_data(path,data,flag)

