# -*- coding: utf-8 -*-
# problem5
# Write a function or method called generate from LM that uses a language
# model to generate random output sequences. That is, the sequences should be generated
# according to the probabilities in the language model.

import re
import numpy as np
import operator
from numpy.random import random_sample
import math
import problem_2 as p2
import problem_4 as p4


def get_distrubution(so1,so2): #caculate distribution of normalized probability (e.g : {P(a|bb), 0.5})
    prob1 = 0
    distribution1 = {}
    so1 = sorted(so1.items(),key=operator.itemgetter(1),reverse=True)
    so2 = sorted(so2.items(),key=operator.itemgetter(1),reverse=True)
    for a in range(0,len(so1),1):
        for b in range(0, len(so2),1):
            if so1[a][0][0] == so2[b][0][0] and so1[a][0][1] == so2[b][0][1]:
                prob = (float(so1[a][1])+1)/(so2[b][1]+p2.length/2) #�������
                distribution1[so1[a][0]] = prob
    return distribution1

def random_sample_random_sequence(distribution5, N):

    outcomes = np.array(distribution5.keys())
    probss = np.array(distribution5.values())
    bins = np.cumsum(probss)
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

##########################  test ##################################
random_result = generate_sample("training.de",30000)
integrate = ""
for i in random_result:
    integrate += i



print random_result
print integrate
print p2.length