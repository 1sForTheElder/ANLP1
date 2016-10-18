# -*- coding: utf-8 -*-
# problem5
# Write a function or method called generate from LM that uses a language
# model to generate random output sequences. That is, the sequences should be generated
# according to the probabilities in the language model.

import re
import numpy as np
import operator
import random
from numpy.random import random_sample
import math
import problem_2 as p2
import problem_4 as p4


#def get_distrubution(so1,so2): #caculate distribution of normalized probability (e.g : {P(a|bb), 0.5})
#    prob1 = 0
#    distribution1 = {}
#    so1 = sorted(so1.items(),key=operator.itemgetter(1),reverse=True)
#    so2 = sorted(so2.items(),key=operator.itemgetter(1),reverse=True)
#    for a in range(0,len(so1),1):
#        for b in range(0, len(so2),1):
#            if so1[a][0][0] == so2[b][0][0] and so1[a][0][1] == so2[b][0][1]:
#                prob = (float(so1[a][1])+1)/(so2[b][1]+p2.length/2) #�������
#                distribution1[so1[a][0]] = prob
#    return distribution1

def random_sample_random_sequence(distribution5, N):

    outcomes = np.array(distribution5.keys())
    probss = np.array(distribution5.values())
    print('probss:::',probss)
    bins = np.cumsum(probss)
    print('bins:::',bins)
    return list(outcomes[np.digitize(random_sample(N), bins)-1])

def compute_distribution(content):

    trigram2 = p4.getNgrams(content,3)
    bigram2 = p4.getNgrams(content,2)
    trigram2_prob = get_distrubution(trigram2,bigram2)
    return trigram2_prob

def generate_sample(test,N):
    probs = compute_distribution(test)
    distribution = random_sample_random_sequence(probs,N)

    return distribution

def read_model(input):
    f=open(input)
    Given_model = {}
    for line in f:
        Given_model[line[0]+line[1]+line[2]] = float(line[4:])
    Given_model = sorted(Given_model.items(),key=operator.itemgetter(0))
    Given_model = p4.Append_SpecialCase(Given_model)
    return Given_model
        
def generate_sample(model,N):
    result = '##'
    vacabulary = np.array([' ','#','.','0','a','b','c','d','e','f',
                       'g','h','i','j','k','l','m','n','o','p',
                       'q','r','s','t','u','v','w','x','y','z','z'])
    for i in range(2,N):
        prob = np.zeros(30)
        for j in range(0,30):
            if model[900*j][0][0]==result[i-2]:
                for k in range(0,30):
                    if model[900*j+30*k][0][1]==result[i-1]:
                        for l in range(0,30):
                            prob[l] = model[900*j+30*k+l][1]
                        bins = np.cumsum(prob)
                        letter = vacabulary[np.digitize(np.array([random.random()]), bins,right=True)]
                        result = result + letter[0]
                        break
                break
    return result
#            else if model[j][0][0]!=result[i-2] and model[j][0][1]!=result[i-1] and flag==1:
#                break
                
                
##########################  test ##################################
#random_result = generate_sample("training.de",300)
My_model = p4.Trigram_training('training.en')
Given_model = read_model('model-br.en')
result = generate_sample(My_model,1000)
#for i in range(0,len(My_model)):
#    if My_model[i][0] != Given_model[i][0]:
#        print My_model[i][0]
#        break
print result
#integrate = ""
#for i in random_result:
#    integrate += i
#
#
#
#print ('random_result',random_result)
#print integrate
#print p2.length
aaa = '##'
# for i in range(0,300):
#     if My_model[i][0][0] == aaa[i-2]:
#         print 'hjahahaha'
#     else:
#         print '00000000000000000000'
