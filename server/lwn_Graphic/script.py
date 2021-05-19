def main(qianyi):
    jbk = ['ReadL', 'BlockReadL', 'ReadHT', 'BlockReadHT', 'Write', 'Clear', 'Seek', 'BlockSeek', 'Host', 'Getter',
           'Setter', 'PRead', 'PBlockRead', 'FromBytes', 'PWritre', 'PToBytes']
    test0 = []
    for line in open("C:/Users/23789/Desktop/相机模型5.0.txt", "r", encoding='UTF-8'):  # 设置文件对象并读取每一行文件
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
    Tran_name1 = []
    Tran_event1 = []
    for i in range(len(Tran_event)):
        if len(Tran_event[i].split(';', 1)) > 1:
            Tran_name1.append(Tran_name[i])
            Tran_event1.append(Tran_event[i].split(';', 1)[1])
    # print(Tran_event1)
    Tran_event2 = []
    fangfa = []
    for item in Tran_event1:
        Tran_event2.append(item.split("(")[1].split(")")[0])
        fangfa.append(item.split("(")[0])
    # print(Tran_event2)
    road = []
    canshu = []
    for item in Tran_event2:
        road.append(item.split(',', 1)[0])
        canshu.append(item.split(',', 1)[1])
    # print(Tran_name1)
    # print(fangfa)
    # print(road)
    # print(canshu)
    fangfa1 = []
    for item in fangfa:
        if 'ReadL' == item:
            fangfa1.append('Read')
        elif 'BlockReadL' == item:
            fangfa1.append('BlockRead')
        elif 'ReadHT' == item:
            fangfa1.append('Read')
        elif 'BlockReadHT' == item:
            fangfa1.append('BlockRead')
        elif 'PRead' == item:
            fangfa1.append('Read')
        elif 'PBlockRead' == item:
            fangfa1.append('BlockRead')
        elif 'PWrite' == item:
            fangfa1.append('Write')
        elif 'PToBytes' == item:
            fangfa1.append('ToBytes')
        else:
            fangfa1.append(item)
    result = ''
    for i in range(len(Tran_name1)):
        if qianyi == Tran_name1[i] and fangfa[i] in jbk:
            if fangfa1[i] == 'Host':
                result = 'ip=' + str(road[i]) + '.' + 'HostIP' + '\n' \
                         + 'port=' + str(road[i]) + '.' + 'HostPort'

                # print('ip=' + str(road[i]) + '.' + 'HostIP')
                # print('port=' + str(road[i]) + '.' + 'HostPort')
            elif fangfa1[i] == 'Getter':
                # print('v=' + str(road[i]) + '.' + 'Value')
                result = 'v=' + str(road[i]) + '.' + 'Value'
            elif fangfa1[i] == 'Setter':
                result = str(road[i]) + '.' + 'Value' + '=v'
                # print(str(road[i]) + '.' + 'Value' + '=v')
            else:
                # print('array=' + str(road[i]) + '.' + str(fangfa1[i]) + '(' + str(canshu[i]) + ')')
                result = 'array=' + str(road[i]) + '.' + str(fangfa1[i]) + '(' + str(canshu[i]) + ')'
    return result
