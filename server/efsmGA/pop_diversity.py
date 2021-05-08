#encoding:UTF-8
from __future__ import division     #ensure that float number when divide

def path_Dice_diversity(first,second):   #计算两path的 Dice 距离，Dice越大，相似度越大
    a = len(list(set(first).intersection(set(second))))  # intersection
    b = len(list(set(first).union(set(second))))  # union
    dice=a/(a+(b-a)/2)
    return 1/dice

def path_leven_diversity(first,second):
    match = 0
    mismatch = 0
    gap = abs(len(first) - len(second))
    for i in range(min(len(first), len(second))):
        if first[i] == second[i]:
            match = match + 1
        else:
            mismatch = mismatch + 1
    leven = match * 1 + mismatch * 0 + gap * 0
    # print match,mismatch,gap
    return 1/leven

def levenshtein(first, second):
        if len(first) > len(second):
            first, second = second, first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [range(second_length) for x in range(first_length)]
        # print distance_matrix
        for i in range(1, first_length):
            for j in range(1, second_length):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion, deletion, substitution)
        #print distance_matrix
        return distance_matrix[first_length - 1][second_length - 1]

def suite_diversity(list):
    sum=0
    for i in range(len(list)-1):
        for j in range(i+1,len(list)):
            dice = path_Dice_diversity(list[i], list[j])
            #print "dice of two:",dice
            sum = sum + dice
    return sum

def suite_diversity_leven(list):
    sum = 0
    for i in range(len(list) - 1):
        for j in range(i + 1, len(list)):
            leven = levenshtein(list[i], list[j])
            #print "leven of two:",leven
            sum = sum + leven
    return sum

def suite_deversity_levenmatch(list):
    sum = 0
    for i in range(len(list) - 1):
        for j in range(i + 1, len(list)):
            leven =  path_leven_diversity(list[i], list[j])
            #print "levenmatch of two",leven
            sum = sum + leven
    return sum

if __name__ == '__main__':
    pop=  [['T1', 'T2', 'T10', 'T14', 'T10', 'T14', 'T6', 'T4', 'T3', 'T5', 'T9', 'T12', 'T6', 'T6', 'T3', 'T8', 'T14', 'T7', 'T15'], ['T1', 'T2', 'T4', 'T3', 'T8', 'T13', 'T7', 'T9', 'T12', 'T9', 'T11', 'T3', 'T15'], ['T1', 'T2', 'T4', 'T4', 'T7', 'T6', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15'], ['T1', 'T2', 'T4', 'T4', 'T7', 'T4', 'T4', 'T7', 'T6', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15'], ['T1', 'T2', 'T4', 'T4', 'T7', 'T6', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15'], ['T1', 'T2', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15'], ['T1', 'T2', 'T4', 'T4', 'T7', 'T6', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15'], ['T1', 'T2', 'T4', 'T4', 'T7', 'T4', 'T4', 'T7', 'T6', 'T10', 'T14', 'T6', 'T4', 'T3', 'T6', 'T8', 'T12', 'T8', 'T17'], ['T1', 'T2', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15'], ['T1', 'T2', 'T4', 'T4', 'T7', 'T6', 'T10', 'T14', 'T6', 'T4', 'T3', 'T8', 'T14', 'T6', 'T4', 'T3', 'T8', 'T12', 'T7', 'T6', 'T15']]

    print 'size:',len(pop)
    sum=suite_diversity(pop)
    print 'dice distance:',sum
    sum1=suite_diversity_leven(pop)
    print 'leven distance:',sum1
    sum3=suite_deversity_levenmatch(pop)
    print 'levenmatch distance:',sum3
    #print levenshtein('GUMBOsdafsadfdsafsafsadfasfadsfasdfasdfs', 'GAMBOL00000000000dfasfasfdafsafasfasdfdsa')