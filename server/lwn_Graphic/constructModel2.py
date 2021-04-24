# incoding:UTF-8
import codecs
import copy
import json
import copy
import os
import sys
import json
import numpy as np
from graphviz import Digraph

# 获取状态集跟迁移集
# sys.path.append("")
# writepath = r''
filepath = './file/'
# filename1 = "Trace.txt"


def getTransState1(inputfile):
    # with open(r"Trace.txt", 'r', encoding='utf-8') as file:       #读取生成的模型文件，对模型进行完整性验证和补全
    #     lines = file.readlines()  # 读取所有行并返回列表
    lines = open(filepath + inputfile, 'r', encoding="utf-8").readlines()
    states_label = []
    source, event, condition, action, target = "", "", "", "", ""
    count = 0
    TransSet = []
    k = 0
    # 状态列表
    StateSet = {}
    # Trace集合
    TraceSet = []
    Trace = []
    for line in lines:
        if line.strip() == "Trace:":  # ignore
            if len(Trace) > 0:
                TraceSet.append(Trace)
                Trace = []
            Trace.append("Trace:")
            continue
        line = line.strip()
        fileds = line.split(':', 1)
        if fileds[0] == "source":
            Trace.append(line)
            source = fileds[1].split(":")[1]
            label = fileds[1].split(":")[0]
            if label not in states_label:
                states_label.append(label)
                StateSet[label] = source
                k += 1
        elif fileds[0] == 'event':
            Trace.append(line)
            event = "event=" + fileds[1]
        elif fileds[0] == 'condition':
            Trace.append(line)
            condition = "condition=" + fileds[1]
        elif fileds[0] == 'action':
            Trace.append(line)
            action = "action=" + fileds[1]
        elif fileds[0] == 'target':
            Trace.append(line)
            if ":" in fileds[1]:
                target = fileds[1].split(":")[1]
                label = fileds[1].split(":")[0]
            else:
                target = "null"
                label = fileds[1]
            if label not in states_label:
                states_label.append(label)
                StateSet[label] = target
                k = k + 1
            count += 1
            TransLable = "T" + str(count)
            TransSet.append([TransLable, states_label[k - 2], states_label[k - 1], event, condition, action])
            source, event, condition, action, target = "", "", "", "", ""
    TraceSet.append(Trace)
    output = open(filepath + 'TraceSet2.txt', 'w+')
    for i in range(len(TraceSet)):
        for j in range(len(TraceSet[i])):
            output.write(str(TraceSet[i][j]))
            output.write(' ')
        output.write('\n')
    output.close()
    with open(filepath + 'StateSet2.txt', 'w') as f:
        json_str = json.dumps(StateSet, ensure_ascii=False, indent=0)
        f.write(json_str)
        f.write('\n')
    output = open(filepath + 'TransSet2.txt', 'w+')
    for i in range(len(TransSet)):
        for j in range(len(TransSet[i])):
            output.write(str(TransSet[i][j]))
            output.write(' ')
        output.write('\n')
    output.close()
    return TraceSet, StateSet, TransSet


def constructModel1(inputfile):
    TraceSet, StateSet, TransSet = getTransState1(inputfile)
    Tr = copy.deepcopy(TransSet)
    # 去除state字典中的值重复项
    func = lambda State: dict([(x, y) for y, x in State.items()])
    State2 = func(func(StateSet))
    # 修改状态编号使状态编号较小
    State3 = {}
    i = 0
    s = ""
    flagValue = ""
    for value in State2.values():
        if value == "Start":
            s = "S0"
            State3[value] = s
        if value == "End":
            flagValue = value
            continue
        s = "S" + str(i)
        State3[value] = s
        i += 1
    if flagValue:
        s = "S" + str(i)
        State3[flagValue] = s
    with open(filepath + 'S12.txt', 'w') as f:
        json_str = json.dumps(State3, ensure_ascii=False, indent=0)
        f.write(json_str)
        f.write('\n')
    # 获得标号-》名称一一对应
    State4 = {}
    for key, value in State3.items():
        State4[value] = key
    with open(filepath + 'S22.txt', 'w') as f:
        json_str = json.dumps(State4, ensure_ascii=False, indent=0)
        f.write(json_str)
        f.write('\n')
    # 合并迁移中状态相等的
    for k in range(0, len(Tr) - 1):
        m = Tr[k][1]
        n = Tr[k][2]
        for i in range(k + 1, len(Tr)):
            if StateSet[m] == StateSet[Tr[i][1]]:
                Tr[i][1] = m
            if StateSet[m] == StateSet[Tr[i][2]]:
                Tr[i][2] = m
            if StateSet[n] == StateSet[Tr[i][1]]:
                Tr[i][1] = n
            if StateSet[n] == StateSet[Tr[i][2]]:
                Tr[i][2] = n
    # output = open('T1.txt', 'w+')
    # for i in range(len(Tr)):
    #     for j in range(len(Tr[i])):
    #         output.write(str(Tr[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # 修改迁移中的状态标号使其标号为较小的标号
    for k in range(0, len(Tr)):
        m = Tr[k][1]
        n = Tr[k][2]
        Tr[k][1] = State3[StateSet[m]]
        Tr[k][2] = State3[StateSet[n]]
    # output = open('T2.txt', 'w+')
    # for i in range(len(Tr)):
    #     for j in range(len(Tr[i])):
    #         output.write(str(Tr[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # # 识别各个元素相同的迁移并标识为相同的编号
    for i in range(0, len(Tr) - 1):
        t = Tr[i][0]
        src1 = Tr[i][1]
        tgt1 = Tr[i][2]
        event1 = Tr[i][3]
        cond1 = Tr[i][4]
        action1 = Tr[i][5]
        for j in range(i + 1, len(Tr)):
            if src1 == Tr[j][1] and tgt1 == Tr[j][2] and event1 == Tr[j][3] and cond1 == Tr[j][4] and action1 == Tr[j][
                5]:
                Tr[j][0] = t
    # output = open('T3.txt', 'w+')
    # for i in range(len(Tr)):
    #     for j in range(len(Tr[i])):
    #         output.write(str(Tr[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    # 去除迁移列表中的重复迁移
    T2 = np.array(Tr)
    list3 = np.array(list(set([tuple(t) for t in T2])))
    k = 1
    Trans2 = []
    for i in list3:
        list3 = list(i)
        k += 1
        Trans2.append(list3)
    # output = open('T4.txt', 'w+')
    # for i in range(len(Trans2)):
    #     for j in range(len(Trans2[i])):
    #         output.write(str(Trans2[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    T1 = mergeTrans(Trans2, State4)
    wf = codecs.open(filepath + "result2.txt", 'w', encoding="utf-8")
    wf1 = codecs.open(filepath+"resultModel2.txt", 'w', encoding="utf-8")
    for key in sorted(State4.keys(), key=lambda x: int(x[1:])):
        if key == 'S0':
            wf1.write("State:\n\tname=" + 'START' + '\n')
        else:
            wf1.write("State:\n\tname=" + key + '\n')
        wf.write("State:\n\tlabel=" + key + '\n\t' + "name=" + State4[key] + '\n')
    for line in T1:
        if line[4].strip().split('=')[1] == "null" or not line[4].strip().split('=')[1]:
            line[4] = "condition="
        else:
            lastCond = line[4].strip().split('=', 1)[1]
            lastCond1 = lastCond.strip().split(',')
            # num_con = len(con)
            i = 0
            for j in range(0, len(lastCond1)):
                if "!=" not in lastCond1[j] and ">=" not in lastCond1[j] and "<=" not in lastCond1[j] and "=" in \
                        lastCond1[j]:
                    lastCond1[j] = lastCond1[j].replace("=", "==")
                if "<=" in lastCond1[j]:
                    re = lastCond1[j].split("<=")
                    if len(re) > 2:
                        lastCond1[j] = re[1] + ">=" + re[0] + ") & (" + re[1] + "<=" + re[2]
                    else:
                        lastCond1[j] = re[0] + "<=" + re[1]
                lastCond1[j] = "(" + lastCond1[j] + ")"
                # print(lastCond1)
            line[4] = "condition=" + " & ".join(lastCond1)
        action = line[5].replace(",", ";")
        if "(" in action and ")" in action and "()" not in action:
            t = action.split("(")
            t2 = t[1].split(")")
            # print(t2)
            if ";" in t2[0]:
                t2[0] = t2[0].replace(";", ",")
            if t2[1]:
                action = t[0] + "(" + t2[0] + ")" + t2[1]
            else:
                action = t[0] + "(" + t2[0] + ")"
        line[5] = action
        wf.write("Transition:\n\tname=" + line[0] + '\n\tsrc=' + line[1] + '\n\ttgt=' + line[2] + '\n\t' + line[
            3] + '\n\t' + line[4] + '\n\t' + line[5] + "\n")
        if int(line[1][1:]) == 0 and int(line[2][1:]) == 0:
            wf1.write(
                "Transition:\n\tname=" + line[0] + '\n\tsrc=' + 'START' + '\n\ttgt=' + 'START' + '\n\t' + line[
                    3] + '\n\t' + line[4] + '\n\t' + line[5]+"\n")
        elif line[1] == 'S0':
            wf1.write(
                "Transition:\n\tname=" + line[0] + '\n\tsrc=' + 'START' + '\n\ttgt=' + line[2] + '\n\t' + line[
                    3] + '\n\t' + line[4] + '\n\t' + line[5]+"\n")
        elif line[2] == 'S0':
            wf1.write(
                "Transition:\n\tname=" + line[0] + '\n\tsrc=' + line[1] + '\n\ttgt=' + 'START' + '\n\t' + line[
                    3] + '\n\t' + line[4] + '\n\t' + line[5]+"\n")
        else:
            wf1.write(
                "Transition:\n\tname=" + line[0] + '\n\tsrc=' + line[1] + '\n\ttgt=' + line[2] + '\n\t' + line[
                    3] + '\n\t' + line[4] + '\n\t' + line[5]+"\n")
    wf1.close()
    wf.close()
    # # 画成png图
    # with open(r"" + filename2 + '.dot', 'w+') as fout:
    #     fout.writelines("digraph g {\n")
    #     st = list()
    #     for i in range(0, len(T1)):
    #         name = T1[i][0]
    #         src = T1[i][1]
    #         tgt = T1[i][2]
    #         event = T1[i][3]
    #         cond = T1[i][4]
    #         action = T1[i][5]
    #         fout.writelines(" " + src + " -> " + tgt + ' [ label="' + name)
    #         if event != None:
    #             fout.writelines('\n' + event)
    #         if cond != None:
    #             fout.writelines('\n' + cond)
    #         # if action!= None:
    #         #     fout.writelines('\n' + action)
    #         fout.writelines('" ];\n')
    #         if src not in st:
    #             st.append(src)
    #             print(src + "->" + State4[src])
    #     fout.writelines("}\n")
    # os.popen("dot -Tpng {}.dot -o {}.png".format(filename2, filename2))
    # 生成PDF图
    # f = Digraph('digraph g', filename=filepath + "efsm1.gv")
    # s = ""
    # for i in range(0, len(T1)):
    #     src = T1[i][1]
    #     if src == "S0":
    #         s = src
    # f.attr('node', shape='doublecircle')
    # f.node(s)
    # f.attr('node', shape='circle')
    # st = list()
    # for i in range(0, len(T1)):
    #     name = T1[i][0]
    #     src = T1[i][1]
    #     tgt = T1[i][2]
    #     event = T1[i][3]
    #     cond = T1[i][4]
    #     action = T1[i][5]
    #     if src not in st:
    #         st.append(src)
    #         print(src + "->" + State4[src])
    #     if tgt not in st:
    #         st.append(tgt)
    #         print(tgt + "->" + State4[tgt])
    #     f.edge(src, tgt, label=event + '\n' + cond + '\n' + action)
    # f.view()
    return State4, T1


# 获取迁移中的计数变量集
def findcountVar(Trans2):
    countVarSet = set()
    for i in range(0, len(Trans2)):
        cond = Trans2[i][4]
        cond1 = cond.split("condition=")[1].split(",")
        for j in range(0, len(cond1)):
            if cond1[j] != "null" and "=" in cond1[j]:
                varName = cond1[j].split("=")[0]
                varValue = cond1[j].split("=")[1]
                if varValue.isdigit() == True:
                    countVarSet.add(varName)
    countVarSet = list(countVarSet)
    return countVarSet


def findSameT(Trans2):
    # 将计数变量不同，其余均相同的迁移标为同一条迁移，以便合并
    sameTLabel = []
    sameT = []
    for i in range(0, len(Trans2) - 1):
        t = Trans2[i][0]
        src1 = Trans2[i][1]
        tgt1 = Trans2[i][2]
        event1 = Trans2[i][3]
        cond1 = Trans2[i][4]
        action1 = Trans2[i][5]
        for j in range(i + 1, len(Trans2)):
            if src1 == Trans2[j][1] and tgt1 == Trans2[j][2] and event1 == Trans2[j][3] and action1 == Trans2[j][5]:
                Trans2[j][0] = t
                sameTLabel.append(t)
                if Trans2[i] not in sameT:
                    sameT.append(Trans2[i])
                if Trans2[j] not in sameT:
                    sameT.append(Trans2[j])
    sameTLabel = list(set(sameTLabel))
    # print(sameTLabel)
    # print(sameT)
    # 将标号不同的迁移从1标号并加入到1
    T1 = []
    j = 1
    for i in range(0, len(Trans2)):
        t = Trans2[i][0]
        if t not in sameTLabel:
            Trans2[i][0] = "t" + str(j)
            T1.append(Trans2[i])
            j += 1
    # output = open('T5.txt', 'w+')
    # for i in range(len(T1)):
    #     for j in range(len(T1[i])):
    #         output.write(str(T1[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    return sameT, T1


def mergeTrans(Trans2, State4):
    countVarSet = findcountVar(Trans2)
    # 合并相同标号的迁移，确定计数变量的取值范围
    # for k in range(0,len(countVarSet)):
    sameT, T1 = findSameT(Trans2)
    # output = open('sameT.txt', 'w+')
    # for i in range(len(sameT)):
    #     for j in range(len(sameT[i])):
    #         output.write(str(sameT[i][j]))
    #         output.write(' ')
    #     output.write('\n')
    # output.close()
    countVarSet = findcountVar(Trans2)
    # 存储相同标号的迁移的标号与其合并了的数值变量的条件
    mergeCond = {}
    i = 0
    while i < len(sameT) - 1:
        t = sameT[i][0]
        cond = sameT[i][4]
        cond1 = cond.split("condition=")[1].split(",")
        # print(cond1)
        # i+=1
        # 相同标号迁移的计数变量与其最大最小值对应
        varValue = {}
        for j in range(0, len(cond1)):
            if cond1[j] != "null" and "=" in cond1[j]:
                varName = cond1[j].split("=")[0]
                if varName in countVarSet:
                    # print(varName)
                    # 某一时钟的最大最小值
                    varValueRange = []
                    var = varName + "="
                    if var in cond:
                        numAttempts1 = int(cond.split(var)[1].split(",")[0])
                        # print(numAttempts1)
                        minN = maxN = numAttempts1
                        k = i + 1
                        while k < len(sameT):
                            if sameT[k][0] == t:
                                cond2 = sameT[k][4]
                                # condition = p != pin, attempts=0
                                # condition = p != pin, attempts=1
                                if var in cond2:
                                    numAttempts2 = int(cond2.split(var)[1].split(",")[0])
                                    # print(numAttempts2)
                                    if minN > numAttempts2:
                                        minN = numAttempts2
                                    if maxN < numAttempts2:
                                        maxN = numAttempts2
                                k += 1
                            else:
                                break
                        if minN == maxN:
                            varValueRange.append(minN)
                        else:
                            varValueRange.append(minN)
                            varValueRange.append(maxN)
                        # print(varValueRange)
                        varValue[varName] = varValueRange
        # print(varValue)
        mergeCondValue = "condition="
        for item in cond1:
            flag = 0
            for key in varValue.keys():
                if key in item:
                    flag = 1
            if flag == 0:
                mergeCondValue += item + ","
            # 表示某一变量的式子
        for key, value in varValue.items():
            if len(value) == 1:
                varFormula = key + "=" + str(value[0])
            else:
                varFormula = str(value[0]) + "<=" + key + "<=" + str(value[1])
            mergeCondValue += varFormula + ","
        mergeCondValue = list(mergeCondValue)[:-1]
        mergeCondValue = "".join(mergeCondValue)
        # print(mergeCondValue)
        mergeCond[t] = mergeCondValue
        i = k
    # print(mergeCond)
    # 合并相同标号迁移,并加入模型迁移集：
    k = len(T1)
    for key, value in mergeCond.items():
        for i in range(0, len(sameT)):
            if sameT[i][0] == key:
                mergeT = sameT[i]
                break
        mergeSame = []
        src1 = mergeT[1]
        tgt1 = mergeT[2]
        event1 = mergeT[3]
        action1 = mergeT[5]
        t = "t" + str(k + 1)
        mergeSame.append(t)
        mergeSame.append(src1)
        mergeSame.append(tgt1)
        mergeSame.append(event1)
        mergeSame.append(value)
        mergeSame.append(action1)
        # print(mergeSame)
        T1.append(mergeSame)
        k += 1
    output = open(filepath + 'T62.txt', 'w+')
    for i in range(len(T1)):
        for j in range(len(T1[i])):
            output.write(str(T1[i][j]))
            output.write(';')
        output.write('\n')
    output.close()
    return T1


def main():
    import time
    t0 = time.perf_counter()
    constructModel1('Trace2.txt')
    elapsed = time.perf_counter() - t0
    # print("Time used:", elapsed)

if __name__ == '__main__':
    import time
    t0 = time.perf_counter()
    constructModel1('Trace2.txt')
    elapsed = time.perf_counter() - t0
    print("Time used:", elapsed)
