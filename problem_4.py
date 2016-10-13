# -*- coding: utf-8 -*-

#   the target of this class is to build your own trigram character language model. You will
#   need to read in a training file, collect counts, estimate probabilities, and write the model
#   probabilities into a file.
############################################################################################################################################################

import re
import numpy as np
import problem_2 as p2  #    so that I can use the function in file problem_2.py
import operator

def getNgrams(input, n):    #   function to make a Ngrams model
    input = p2.process_line(input)     #    use the cleanText function to pre
    print input

    output = {} # create a new dictionary
    for i in range(len(input)-n+1):     #   divide them into groups with 3 characters.
        ngramTemp = "".join(input[i:i+n])


        if ngramTemp not in output:     #   add it into the dictionary
            output[ngramTemp] = 0
        output[ngramTemp] += 1

    return output

def compute_probs(so1,so2): #caculate probability of normalized probability (e.g : {P(a|bb), 0.5})


    output1 = {} #�����ֵ�
    so1 = sorted(so1.items(),key=operator.itemgetter(1),reverse=True)
    so2 = sorted(so2.items(),key=operator.itemgetter(1),reverse=True)
    for a in range(0,len(so1),1):
        for b in range(0, len(so2),1):
            if so1[a][0][0] == so2[b][0][0] and so1[a][0][1] == so2[b][0][1]:
                prob = (float(so1[a][1])+1)/(so2[b][1]+163898)

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
test_getCaculateProbs = probs("training.de") #read in a training file and try to estimate probability, finally generate a model.

write_into_file(test_getCaculateProbs,'prob1.txt')

getContent = open('prob1.txt')    #print the file which is just created
for i in getContent:
    print i

print test_getCaculateProbs #print the model

print test_getNgrams
