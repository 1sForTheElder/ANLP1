# -*- coding: utf-8 -*-
import urllib2
import re
import string
import time
import operator
import numpy as np
from numpy.random import random_sample
import math


start = time.clock()
wordcounts1 = 0
haha = {}
gaga = {}
NGList = []
total_probability = 0
distribution = {}


#�޳������ֺ���
def isCommon(ngram):
    commonWords = [ "well"]

    if ngram in commonWords:
        return True
    else:
        return False

def cleanText(input):
    input = re.sub('[^a-zA-Z]', ' ', input)
    input = input.lower()
    input = re.sub('\d', ' ', input)
    input = bytes(input)  # .encode('utf-8') # ������ת����utf-8��ʽ������ת���ַ�
    #input = re.sub('\n+', " ", input).lower() # ƥ�任���ÿո��滻�ɿո�
    #input = re.sub('\[[0-9]*\]', "", input) # �޳�����[1]���������ñ��

    #input = re.sub(' +', " ", input) #  ����������ո��滻��һ���ո�

    #input = input.decode("ascii", "ignore")
    # print input
    return input

def cleanInput(input):
    input = cleanText(input)
    cleanInput = []
    #input = input.split(' ') #�Կո�Ϊ�ָ����������б�


    for item in input:
        item = item.strip(string.punctuation) # string.punctuation��ȡ���б�����

        if len(item) == 1: #or (item.lower() == 'a' or item.lower() == 'i'): #�ҳ����ʣ�����i,a�ȵ�������
            cleanInput.append(item)
    return cleanInput

def getNgrams(input, n):
    input = cleanInput(input)

    output = {} # �����ֵ�
    for i in range(len(input)-n+1):
        ngramTemp = "".join(input[i:i+n])#.encode('utf-8')


        if ngramTemp not in output: #��Ƶͳ��
            output[ngramTemp] = 0 #���͵��ֵ����
        output[ngramTemp] += 1

    return output

#��ȡ���Ĵ��ڵľ���
def getFirstSentenceContaining(ngram, content):
    #print(ngram)
    sentences = content.split(".")
    for sentence in sentences:
        if ngram in sentence:
            return sentence
    return ""

def compute_probs(so1,so2,n,h):


    output1 = {} #�����ֵ�
    so1 = sortedNGrams
    so2 = sortedBigram
#    for a in so1:
#        haha[n] = a[0]
#        n +=1
#    for g in so2:
#        gaga[h] = g[0]
#        h +=1
#    print so1[0][0][1] #��һ�����������Ƶ�ʵ����У��ڶ�������0��ȡ����ĸ������������1��ȡ�����ĵ�һ����ĸ
    for a in range(0,len(so1),1):  #ѭ���������һ���͵ڶ�����ĸ��ͬ��NN��
        for b in range(0, len(so2),1):
            if so1[a][0][0] == so2[b][0][0] and so1[a][0][1] == so2[b][0][1]:
                prob = (float(so1[a][1])+1)/(so2[b][1]+163898) #�������

                # print so1[a],so2[b]
                # print prob
                key = 'P('+ so1[a][0][2] + "|" + so1[a][0][0]+so1[a][0][1] + ")"  #����keyֵ
                distribution[so1[a][0]] = prob #�����и��ʵ�trigram�ֵ��Ա�����
                output1[key] = prob #��key��value�����ֵ�
                NGList.append(prob)

    return output1

def random_sample_random_sequence(distribution, N):
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

def caculate_perplexity(distribution):
    value = np.array(distribution.values())
    b = 1
    for a in value:
        a *= a
    b = math.log(a,2)
    return b
# def get_probability(input): #try to read the document
#     model = {}
#     after_process = input.strip().split(' ')
#     print after_process
#     for a in input:
#
#         model.keys().append(a)
#
#
#     print model
#     haha = 0
#     return haha
#
# def caculate_perplexity(dict):
#
#     l
#     output2 = {}
#
#
#
#     return output2



#����һ������ҳֱ�ӽ��ж�ȡ
#content = urllib2.urlopen(urllib2.Request("http://pythonscraping.com/files/inaugurationSpeech.txt")).read()
#�Ա����ļ��Ķ�ȡ������ʱ���ã���Ϊ��������

content = open("training.de").read()
ngrams = getNgrams(content, 3)

wordcounts1 = len(cleanText(content))

context2 = open("training.de").read()
bigram = getNgrams(context2,2)

sortedBigram =  sorted(bigram.items(),key=operator.itemgetter(1),reverse=True)

sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True) # reverse=True ��������

# tt = sortedBigram[1]
# gg = tt[0]
# yy = gg[0]
# print gg
# print yy
# print tt
print(sortedNGrams)
print (sortedBigram)
ggg = compute_probs(sortedNGrams,sortedBigram,0,0)
# print ggg

# print distribution
sorted_probability = sorted(ggg.items(),key = operator.itemgetter(1))
# print sorted_probability # ��ӡ��������ĸ����ֵ�
# for a in ggg.values(): #caculate total probability
#     total_probability += a

str_list = random_sample_random_sequence(distribution, 27000) #���Լ���ģ�����������ĸ
print distribution
#content3 = open("model-br.en").read()
#print content3
# gg = get_probability("model-br.en")
# print total_probability
# print NGList
# print wordcounts1
end = time.clock()
# print str_list #��ӡ�Լ������������ĸ

#begin to deal with the test.txt
def probs(content):
    content5 = open(content).read()
# print(content5)
    trigram2 = getNgrams(content5,3)
    bigram2 = getNgrams(content5,2)
    trigram2_prob = compute_probs(trigram2,bigram2,0,0)
    return trigram2_prob

gf = probs("test.txt")
str_list2 = random_sample_random_sequence(distribution,10000)
print(str_list2)
perplexity_of_list_generated_by_test = caculate_perplexity(gf)
print perplexity_of_list_generated_by_test

print ('Running time: %s Seconds'%(end-start))



#for top3 in range(3):
#    print "###"+getFirstSentenceContaining(sortedNGrams[top3][0],content.lower())+"###"























# �ɽ���
# �����ǣ���staff.txt��1 zhangsan IT 13052359323�����1��Ϊkey,ʣ�µ�Ϊvalue�洢���ֵ��С�
# python <wbr>���ļ����ݴ洢���ֵ���python <wbr>���ļ����ݴ洢���ֵ�������һ��������Ҳʵ����Ŀ�ġ������Ǹо�̫�鷳�ˡ�
# #!/usr/bin/env python
# staff_dic = {}
# value_list = []
# f = open('staff.txt','a+')
# d = f.readlines()
# f.close()
# for line in d:
#     key_ = int(line.split()[0])
#     value_1 = line.split()[1]
#     value_2 = line.split()[2]
#     value_3 = line.split()[3]
#     staff_dic[key_] = value_1 + ' ' + value_2 + ' ' + value_3
# print staff_dic
#
# -------------------------------------------------------------------------------------
# ����key��intΪ������
# -------------------------------------------------------------------------------------
# ���ּ򵥵ķ���
# #!/usr/bin/env python
# staff_dic = {}
# value_list = []
# f = open('staff.txt','a+')
# d = f.readlines()
# f.close()
# for line in d:
#     key_ = int(line.split()[0])
#     value_ = line.split()[1:]
#     staff_dic[key_] = value_
# print staff_dic
