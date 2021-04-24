# -*- coding: utf-8 -*-
import json
import codecs
import re

def combination():
    filepath = './file/'
    wf = codecs.open(filepath + "result.txt", 'w', encoding="utf-8")
    state = dict(json.load(open(filepath + "S2.txt", 'r', encoding="utf-8")))

    wf1 = codecs.open(filepath + "resultModel.txt", 'w', encoding="utf-8")

    for key in sorted(state.keys(), key=lambda x: int(x[1:])):
        if key == 'S0':
            wf1.write("State:\n\tname=" + 'START' + '\n')
        else:
            wf1.write("State:\n\tname=" + key + '\n')
        wf.write("State:\n\tlabel=" + key + '\n\t' + "name=" + state[key] + '\n')
    details = codecs.open(filepath + "T6.txt", 'r', encoding="utf-8").readlines()
    for line in details:
        fields = line.split(";", 5)
        if fields[4].strip().split('=')[1] == "null":
            fields[4] = "condition="
        else:
            lastCond = fields[4].strip().split('=', 1)[1]
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
            fields[4] = "condition=" + " & ".join(lastCond1)
        fields[5] = fields[5].replace(',', ';')
        wf.write("Transition:\n\tname=" + fields[0] + '\n\tsrc=' + fields[1] + '\n\ttgt=' + fields[2] + '\n\t' + fields[
            3] + '\n\t' + fields[4] + '\n\t' + fields[5])
        if int(fields[1][1:]) == 0 and int(fields[2][1:]) == 0:
            wf1.write(
                "Transition:\n\tname=" + fields[0] + '\n\tsrc=' + 'START' + '\n\ttgt=' + 'START' + '\n\t' + fields[
                    3] + '\n\t' + fields[4] + '\n\t' + fields[5])
        elif fields[1] == 'S0':
            wf1.write(
                "Transition:\n\tname=" + fields[0] + '\n\tsrc=' + 'START' + '\n\ttgt=' + fields[2] + '\n\t' + fields[
                    3] + '\n\t' + fields[4] + '\n\t' + fields[5])
        elif fields[2] == 'S0':
            wf1.write(
                "Transition:\n\tname=" + fields[0] + '\n\tsrc=' + fields[1] + '\n\ttgt=' + 'START' + '\n\t' + fields[
                    3] + '\n\t' + fields[4] + '\n\t' + fields[5])
        else:
            wf1.write(
                "Transition:\n\tname=" + fields[0] + '\n\tsrc=' + fields[1] + '\n\ttgt=' + fields[2] + '\n\t' + fields[
                    3] + '\n\t' + fields[4] + '\n\t' + fields[5])
    wf.close()
    wf1.close()
