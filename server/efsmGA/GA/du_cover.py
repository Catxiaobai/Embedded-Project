import diversity

'''dulist=[['T1','T7'],
['T1','T11'],
['T1','T12'],
['T1','T2'],
['T1','T14'],
['T1','T13'],
['T1','T6'],
['T1','T9'],
['T1','T8'],
['T1','T5'],
['T1','T10'],
['T1','T15'],
['T1','T16'],
['T1','T17'],
['T2','T4'],
['T2','T11'],
['T2','T13'],
['T2','T3'],
['T2','T9'],
['T2','T12'],
['T2','T14'],
['T2','T8'],
['T2','T5'],
['T2','T10'],
['T6','T4'],
['T6','T11'],
['T6','T13'],
['T6','T3'],
['T6','T9'],
['T6','T12'],
['T6','T14'],
['T6','T8'],
['T6','T5'],
['T6','T10'],
['T6','T7'],
['T7','T4'],
['T7','T11'],
['T7','T13'],
['T7','T3'],
['T7','T9'],
['T7','T12'],
['T7','T14'],
['T7','T8'],
['T7','T5'],
['T7','T10'],
['T9','T9'],
['T9','T14'],
['T10','T10'],
['T10','T14'],
['T11','T11'],
['T11','T14'],
['T12','T12'],
['T12','T14'],
['T13','T13'],
['T13','T14'],
['T14','T14'],
['T15','T15'],
['T16','T16'],
['T17','T17']]'''
#pop= [['T1', 'T2', 'T7', 'T3', 'T6', 'T5', 'T8', 'T11', 'T8', 'T12', 'T9', 'T11', 'T3', 'T10', 'T13', 'T15'], ['T1', 'T2', 'T7', 'T10', 'T12', 'T4', 'T5', 'T5', 'T7', 'T15'], ['T1', 'T2', 'T10', 'T14', 'T7', 'T3', 'T15'], ['T1', 'T2', 'T10', 'T14', 'T7', 'T8', 'T17'], ['T1', 'T2', 'T10', 'T14', 'T7', 'T3', 'T7', 'T3', 'T15'], ['T1', 'T2', 'T8', 'T12', 'T6', 'T7', 'T8', 'T17'], ['T1', 'T2', 'T8', 'T12', 'T6', 'T7', 'T8', 'T17'], ['T1', 'T2', 'T10', 'T14', 'T6', 'T8', 'T17'], ['T1', 'T2', 'T8', 'T12', 'T6', 'T7', 'T8', 'T17'], ['T1', 'T2', 'T10', 'T14', 'T10', 'T14', 'T7', 'T3', 'T15']]
#dulist=[[2,4],[1,4]]
#pop=[[1,1,3],[1,4,6],[2,1,4]]
def ducover(dulist,pop):
    count = 0
    for i in range(len(dulist)):
        element_d = dulist[i][0]
        element_u = dulist[i][1]
        for k in range(len(pop)):

            if (element_d in pop[k]) and (element_u in pop[k]):
                index_d = pop[k].index(element_d)
                index_u = pop[k].index(element_u)
                if index_d < index_u:
                    count = count + 1
                    #print dulist[i]
                    break
                else:
                    continue
            else:
                continue
    print 'covered number:', count
    print 'total dupairs:',len(dulist)
    print '----------------------------------------------------------'
    print 'size:', len(pop)
    print 'dice distance:', diversity.suite_diversity(pop)
    print 'leven distance:', diversity.suite_diversity_leven(pop)
    print 'levenmatch distance:', diversity.suite_deversity_levenmatch(pop)





