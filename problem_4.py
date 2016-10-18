# -*- coding: utf-8 -*-

#   the target of this class is to build your own trigram character language model. You will
#   need to read in a training file, collect counts, estimate probabilities, and write the model
#   probabilities into a file.
############################################################################################################################################################

import re
import numpy as np
import problem_2 as p2  #    so that I can use the function in file problem_2.py
import operator

def generate_Ngrams_list():
    vacabulary = np.array([' ','#','.','0','a','b','c','d','e','f',
                           'g','h','i','j','k','l','m','n','o','p',
                           'q','r','s','t','u','v','w','x','y','z'])
    Ngrams_list = {}
    for a in vacabulary:
        for b in vacabulary:
            if (a!='#' and b=='#'):
                continue
            for c in vacabulary:
                if a=='#' and c=='#':
                    continue
                Ngrams_list[a+b+c] = 0
    return Ngrams_list

def get_Ngrams(input, Ngrams_list, n):    #   function to make a Ngrams model
    input = p2.process_line(input)     #    use the cleanText function to pre
#    output = {} # create a new dictionary
    for i in range(len(input)-n+1):     #   divide them into groups with 3 characters.
        ngramTemp = "".join(input[i:i+n])
        if ngramTemp[0] == '#' or ngramTemp[1] != '#':
            Ngrams_list[ngramTemp] += 1
    return Ngrams_list

def get_Count_List(Ngrams_list):
    Count_List = {}
    for i in Ngrams_list:
        if Ngrams_list[i] not in Count_List:
            Count_List[Ngrams_list[i]] = 0;
        Count_List[Ngrams_list[i]] +=1
    Count_List = sorted(Count_List.items(),key=operator.itemgetter(0))
    return Count_List

def part_Good_Turing(Count_list):
    Turing_List = np.zeros((len(Count_list),3))
    flag = 0
    for i in range(0,len(Count_list)):
        if flag == 0:
            #Tured_List.append(np.array([Count_list[i][0],float((i+1))*Count_list[i+1][1]/Count_list[i][1],Count_list[i][1]]))
            #Tured_List[Count_list[i][0]] = float((i+1))*Count_list[i+1][1]/Count_list[i][1]
            Turing_List[i][0] = Count_list[i][0]
            Turing_List[i][1] = float((i+1))*Count_list[i+1][1]/Count_list[i][1]
            Turing_List[i][2] = Count_list[i][1]
            if Count_list[i+2][0] != i+2:
                flag = 1
        else:
            #Tured_List.append(np.array([Count_list[i][0],Count_list[i][0],Count_list[i][1]]))
            Turing_List[i][0] = Count_list[i][0]
            Turing_List[i][1] = Count_list[i][0]
            Turing_List[i][2] = Count_list[i][1]
    return Turing_List

def Sum(Turing_list):
    Total_Count = 0.0
    for i in Turing_list:
        Total_Count += i[1]*i[2]
    return Total_Count

def GT_prob(Turing_list, Total_Count):
    GT_prob_list = {}
    for i in range(0,len(Turing_list)):
        #GT_prob_list[i][0] = Turing_list[i][0]
        GT_prob_list[Turing_list[i][0]] = Turing_list[i][1]/Total_Count
    return GT_prob_list
        
def Ngram_prob(Ngrams_list, GT_prob_list):
    Ngrams_prob_list = {}
    for i in Ngrams_list:
        Ngrams_prob_list[i] = GT_prob_list[Ngrams_list[i]]
    Ngrams_prob_list = sorted(Ngrams_prob_list.items(),key=operator.itemgetter(0))
    
    
    flag = ''
    prob_sum = 0.0
    for i in range(0,len(Ngrams_prob_list)):
        if Ngrams_prob_list[i][0][0:2]!=flag:
            flag = Ngrams_prob_list[i][0][0:2]
            prob_sum = 0
            for j in range(i,len(Ngrams_prob_list)):
                if Ngrams_prob_list[j][0][0:2]!=flag:
                    break
                prob_sum += Ngrams_prob_list[j][1]
        Ngrams_prob_list[i] = (Ngrams_prob_list[i][0],Ngrams_prob_list[i][1]/prob_sum)
    return Ngrams_prob_list
    
#############################################################################
def Append_SpecialCase(Ngrams_prob_list):
    insert_string = np.array(['#','#','#'])
    vacabulary = np.array([' ','#','.','0','a','b','c','d','e','f',
                           'g','h','i','j','k','l','m','n','o','p',
                           'q','r','s','t','u','v','w','x','y','z'])
    
    for i in vacabulary:
        insert_string[1]=i
        Ngrams_prob_list.append((insert_string[0]+insert_string[1]+insert_string[2],0.0))
    
    insert_string[1]='#'
    for i in vacabulary:
        if i=='#':
            continue
        insert_string[0]=i
        for j in vacabulary:
            insert_string[2]=j
            if j=='#':
                Ngrams_prob_list.append((insert_string[0]+insert_string[1]+insert_string[2],1.0))
            else:
                Ngrams_prob_list.append((insert_string[0]+insert_string[1]+insert_string[2],0.0))
    Ngrams_prob_list.sort(key=operator.itemgetter(0))
    return Ngrams_prob_list

###############################################################
###############################################################
def compute_probs(so1,so2): #caculate probability of normalized probability (e.g : {P(a|bb), 0.5})
    prob1 = 0
    output1 = {}
    so1 = sorted(so1.items(),key=operator.itemgetter(1),reverse=True)
    so2 = sorted(so2.items(),key=operator.itemgetter(1),reverse=True)
    for a in range(0,len(so1),1):
        for b in range(0, len(so2),1):
            if so1[a][0][0] == so2[b][0][0] and so1[a][0][1] == so2[b][0][1]:
                prob = (float(so1[a][1])+0.5)/(so2[b][1]+30/2)

                # print so1[a],so2[b]
                # print prob
                key = 'P('+ so1[a][0][2] + "|" + so1[a][0][0]+so1[a][0][1] + ")"
                output1[key] = prob
    return output1

def probs(content):

    trigram2 = getNgrams(content,3)
    bigram2 = getNgrams(content,2)
    trigram2_prob = compute_probs(trigram2,bigram2)
    return trigram2_prob

def write_into_file(probs,filename):    #write it into a file
    f = open(filename, 'w')   # the file call prob.txt
    for key in probs:
        f.write(key)
        f.write('\t')
        for key2 in str(probs[key]):

            f.write(key2)

            # f.write('\t'.join(str(probs[key][key2])))
            # f.write('\n')
        f.write('\n')

    f.close()

def Test_Sum(Prob_List, Turing_list):
    result = 0
    for i in range(0,len(Prob_List)):
        result += Prob_List[Turing_list[i][0]]*Turing_list[i][2]
    return result
                                    # Test below #
############################################################################
def Trigram_training(input):
    Ngrams_list = generate_Ngrams_list()
    Ngrams_list = get_Ngrams(input,Ngrams_list,3)
    Count_list = get_Count_List(Ngrams_list)
    Turing_list = part_Good_Turing(Count_list)
    Sum_Count = Sum(Turing_list)
    Prob_list = GT_prob(Turing_list, Sum_Count)
    Ngrams_prob_list = Ngram_prob(Ngrams_list, Prob_list)
    Ngrams_prob_list = Append_SpecialCase(Ngrams_prob_list)
    
    return Ngrams_prob_list
##############################################################################


#result = Test_Sum(Prob_list, Turing_list)

Ngrams_prob_list = Trigram_training('training.de')

#result = 0
#for i in range(930,959):
#    result = result + Ngrams_prob_list[i][1]

print('result',len(Ngrams_prob_list))

print test_getCaculateProbs #print the model

print ('test_getNgrams:::',test_getNgrams)
print p2.length