def main(qianyi, data, file):
    jbk = ['Read', 'BlockRead', 'ReadHT', 'BlockReadHT', 'Write', 'Clear', 'Seek', 'BlockSeek', 'Host',
           'Getter', 'Setter', 'PRead', 'PBlockRead', 'FromBytes', 'PWritre', 'PToBytes']
    test0 = []
    for line in open(file, "r", encoding='UTF-8'):  # 设置文件对象并读取每一行文件
        # line=line.split()[0]
        line = line.rstrip('\n').rstrip(' ')
        test0.append(line)  # 将每一行文件加入到list中

    Tran_name = []
    Tran_src = []
    Tran_tgt = []
    Tran_event = []
    Tran_condi = []
    Tran_action = []
    for index in range(len(test0)):
        if test0[index] == 'Transition:':
            Tran_name.append(test0[index + 1][6:])
            Tran_src.append(test0[index + 2][5:])
            Tran_tgt.append(test0[index + 3][5:])
            Tran_event.append(test0[index + 4][7:])
            Tran_condi.append(test0[index + 5][11:])
            Tran_action.append(test0[index + 6][8:])
    # print(Tran_name)  # 迁移名
    # print(Tran_event)

    fangfa = []
    road = []
    canshu = []
    for item in Tran_event:
        road.append(item.split("_")[1].split("(")[0])
        fangfa.append(item.split("_")[0])
        canshu.append(item.split("(")[1].split(")")[0])

    # print(fangfa)
    # print(road)
    # print(canshu)
    for i in range(len(Tran_name)):
        if qianyi == Tran_name[i] and fangfa[i] in jbk:
            if fangfa[i] == 'Write' or fangfa[i] == 'Clear':
                data = data[1:-1]
                result = 'array=' + road[i] + '.' + fangfa[i] + '(' + data + ')'
                print(result)
            elif ',' in canshu[i]:
                tmp = canshu[i].split(',')
                for j in range(len(tmp)):
                    tmp[j] = '[' + tmp[j] + ']'
                result = road[i] + '.' + fangfa[i] + '(' + ','.join(tmp) + ')'
                print(road[i] + '.' + fangfa[i] + '(' + ','.join(tmp) + ')')
            else:
                result = road[i] + '.' + fangfa[i] + '(' + canshu[i] + ')'
                print(result)
    return result
