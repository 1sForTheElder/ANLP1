# -*- coding: utf-8 -*-

#   the target of this class is to build your own trigram character language model. You will
#   need to read in a training file, collect counts, estimate probabilities, and write the model
#   probabilities into a file.
############################################################################################################################################################

import re
import numpy as np
import problem_2 as p2  #    so that I can use the function in file problem_2.py
import operator

def number_of_things_we_saw_once(input):
    list = []
    input = sorted(input.items(), key=operator.itemgetter(1))
    for i in range(0,len(input)-1,1):
        if input[i][1] == 1:
            print input[i][1]
    return list

def generate_Ngrams_List(input):

    unseen = np.array([]);
    sentence = ['a','m','n','h','n','t','y','t','r','i','#','0','e','.','f','s','r','s','g','j','y','r','s','d','z']
    inp = ['a','m','n','c','x','s','g','t']
    for a in range(len(input)-2):
        a
voca = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','u','v','w','x','y','z',' ','#','.']

# def number_of_use_of_the_word(token):
#     for i in token
#
#
#     return a
#
# def the_count_words_with_a_frequency_c(token):
#
#     return a
#
# def defaultdict():
#
#
# def add_good_turing(tokens):
#     N = len(tokens) + 1
#     C = number_of_use_of_the_word(tokens)
#     N_c = the_count_words_with_a_frequency_c(list(C.values()))
#     assert(N == sum([k * v for k, v in N_c.items()]))
#     default_value = N_c[1] / N
#     model = defaultdict(lambda: default_value)
#     types = C.keys()
#     B = len(types)
#     for _type in types:
#         c = C[_type]
#         model[_type] = (c + 1) * N_c[c + 1] / (N_c[c] * N)
#     return model

def getNgrams(input, n):    #   function to make a Ngrams model
    input = p2.process_line(input)     #    use the cleanText function to pre
    output = {} # create a new dictionary
    for i in range(len(input)-n+1):     #   divide them into groups with 3 characters.
        ngramTemp = "".join(input[i:i+n])


        if ngramTemp not in output:     #   add it into the dictionary
            output[ngramTemp] = 0
        output[ngramTemp] += 1

    return output

def compute_probs(so1,so2): #caculate probability of normalized probability (e.g : {P(a|bb), 0.5})
    prob1 = 0
    output1 = {}
    so1 = sorted(so1.items(),key=operator.itemgetter(1),reverse=True)
    so2 = sorted(so2.items(),key=operator.itemgetter(1),reverse=True)
    for a in range(0,len(so1),1):
        for b in range(0, len(so2),1):
            if so1[a][0][0] == so2[b][0][0] and so1[a][0][1] == so2[b][0][1]:
                prob = (float(so1[a][1])+1)/(so2[b][1]+p2.length/2)

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

                                    # Test below #
############################################################################

test_getNgrams = getNgrams("training.de",3) #read in a training file and try to collect counts



Num = number_of_things_we_saw_once(test_getNgrams)
# print test_getNgrams['#a0']

# test_getCaculateProbs = probs("woqu.txt") #read in a training file and try to estimate probability, finally generate a model.
#
# write_into_file(test_getCaculateProbs,'prob1.txt')
#
# getContent = open('prob1.txt')    #print the file which is just created
# for i in getContent:
#     print i
#
# print test_getCaculateProbs #print the model
#
# print test_getNgrams
# print p2.length