#Here are some libraries you're likely to use. You might want/need others as well.
from __future__ import division
import re
import sys
from random import random
from math import log
from collections import defaultdict
import numpy as np
from numpy.random import random_sample


def generate_random_sequence(distribution, N):
    ''' generate_random_sequence takes a distribution (represented as a
    dictionary of outcome-probability pairs) and a number of samples N
    and returns a list of N samples from the distribution.
    This is a modified version of a sequence generator by fraxel on
    StackOverflow:
    http://stackoverflow.com/questions/11373192/generating-discrete-random-variables-with-specified-weights-using-scipy-or-numpy
    '''
    #As noted elsewhere, the ordering of keys and values accessed from
    #a dictionary is arbitrary. However we are guaranteed that keys()
    #and values() will use the *same* ordering, as long as we have not
    #modified the dictionary in between calling them.
    outcomes = np.array(distribution.keys())
    probs = np.array(distribution.values())
    #make an array with the cumulative sum of probabilities at each
    #index (ie prob. mass func)
    bins = np.cumsum(probs)
    #create N random #s from 0-1
    #digitize tells us which bin they fall into.
    #return the sequence of outcomes associated with that sequence of bins
    #(we convert it from array back to list first)
    return list(outcomes[np.digitize(random_sample(N), bins)])

sentences = []
trigram = {}
f = open("model-br.en")
# print f

for line in f:
    line = line.strip('\n').split("\t")
    sentences.append(line)
print sentences[1:100]


for line in range(len(sentences)-1):
    key = sentences[line][0]
    trigram[key] = float(sentences[line][1])
# print trigram

str_list = generate_random_sequence(trigram,10000) #generate random sequence
print trigram
print str_list
