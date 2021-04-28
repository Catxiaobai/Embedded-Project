#encoding:UTF-8
from __future__ import division     #ensure that float number when divide
from collections import Counter
import obtain_efsm_info

def EditDist(first, second):   # 编辑距离,该值>1，权重为1
    matrix = [[i + j for j in range(len(second) + 1)] for i in range(len(first) + 1)]

    for i in xrange(1, len(first) + 1):
        for j in xrange(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    EditNum=matrix[len(first)][len(second)]
    return EditNum

def TranFreq(first,second): #重复迁移覆盖次数差异，该值<1，权重为1
    fre_diff_list=[]
    templist = list(set(first).intersection(set(second)))  # 把两path重复的迁移，构成集合list
    for i in range(len(templist)):
        freqdiff = abs(first.count(templist[i])-second.count(templist[i]))
        fre_diff_list.append(freqdiff)
    fen_zi = sum(fre_diff_list)  #分子
    #print fen_zi
    fen_mu = 1 * obtain_efsm_info.tran_number()  #分母(模型迁移总数)，其中kmax暂定为1
    #fen_mu = 1 * (len(first)+len(second))   #分母（两path的迁移个数和），其中kmax暂定为1
    #print fen_mu
    freDiff = fen_zi / fen_mu
    return freDiff

def Difference(first,second):
    editdis = EditDist(first, second)
    tranfreq = TranFreq(first,second)
    differ = 1 * editdis + 1 * tranfreq
    return differ

if __name__ =='__main__':
    first = ['T1','T2','T3','T4']
    second = ['T1','T3','T2','T5','T7','T3','T2','T2']
    print EditDist(first,second)
    print TranFreq(first,second)
    print Difference(first,second)