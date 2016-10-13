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
distribution1 = {}


#�޳������ֺ���
def isCommon(ngram):
    commonWords = [ "well"]

    if ngram in commonWords:
        return True
    else:
        return False


#begin to deal with the test.txt #add hash before and after the line
def add_hash(txt):
    b='#'
    f=open('test1.txt','w')    # r只读，w可写，a追加
    g = open(txt)
    for line in g:
        line = b + b + line[:-1] + b
        f.write(line)
    f.close()
    gg5 = open("test1.txt").read()
    return gg5


def cleanText(input):
    # input = re.sub('[^#]', " " ,input)

    input = re.sub('[^a-zA-Z0-9^#^ ]', '', input)
    # print input
    input = input.lower()
    input = re.sub('\d', '0', input)
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
        # item = item.strip(string.punctuation) # string.punctuation��ȡ���б�����
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

# #��ȡ���Ĵ��ڵľ���
# def getFirstSentenceContaining(ngram, content):
#     #print(ngram)
#     sentences = content.split(".")
#     for sentence in sentences:
#         if ngram in sentence:
#             return sentence
#     return ""

b = '#'
def write_into_file(list):   #write lines into a file
    preinput = ''
    for l in list:
        preinput += l
    print preinput
    for i in range(0,len(preinput)-1,1):
        # print preinput[0]
        if preinput[i] == 'e':
            print preinput[i]
            # preinput = preinput[0:i] + '\r\n' + preinput[:-1]
            preinput[i] += 'a'
    return preinput
    f = open('test4.txt','w')  # r只读，w可写，a追加
    for line in preinput:
        f.write(preinput)
    f.close()


def compute_probs(so1,so2,n,h): #caculate probability of normalized probability (e.g : {P(a|bb), 0.5})


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
                distribution1[so1[a][0]] = prob #�����и��ʵ�trigram�ֵ��Ա�����
                output1[key] = prob #��key��value�����ֵ�
                NGList.append(prob)

    return output1

def distribution(so1,so2,n,h): #caculate distribution(N-gram) by using its Ngram probabiliyu over N-1 Gram probability


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
                distribution1[so1[a][0]] = prob #�����и��ʵ�trigram�ֵ��Ա�����

                output1[key] = prob #��key��value�����ֵ�
                NGList.append(prob)

    return distribution1

def random_sample_random_sequence(distribution5, N):
    output2 = {}
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
    outcomes = np.array(distribution5.keys())
    print distribution5.values()
    probss = np.array(distribution5.values())
    #make an array with the cumulative sum of probabilities at each
    #index (ie prob. mass func)
    bins = np.cumsum(probss)
    print ('bins::',bins)
    # for i in outcomes:
    #     output2[outcomes] = probss
    #
    # print output2
    #create N random #s from 0-1
    #digitize tells us which bin they fall into.
    #return the sequence of outcomes associated with that sequence of bins
    #(we convert it from array back to list first)
    return list(outcomes[np.digitize(random_sample(N), bins)-1])

def caculate_perplexity(distribution): #caculate perplexity function by using distribution.values
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

# print sorted_probability # ��ӡ��������ĸ����ֵ�
# for a in ggg.values(): #caculate total probability
#     total_probability += a

# str_list = random_sample_random_sequence(distribution, 300) #���Լ���ģ�����������ĸ
# print distribution
#content3 = open("model-br.en").read()
#print content3
# gg = get_probability("model-br.en")
# print total_probability
# print NGList
# print wordcounts1

# print str_list #��ӡ�Լ������������ĸ

ab = "sdfgfsdgfdsgfdgfdfdgfgfdgfgsgsfdsgfdgfsd"  #test
for i in range(0,len(ab)-1,1):
    if ab[i] == 'g':
        ab = ab[:i] + '\r\n' + ab[i:]
print ab




def probs(content):
# print(content5)
    trigram2 = getNgrams(content,3)
    bigram2 = getNgrams(content,2)
    trigram2_prob = compute_probs(trigram2,bigram2,0,0)
    return trigram2_prob

def compute_distribution(content):
# print(content5)
    trigram2 = getNgrams(content,3)
    bigram2 = getNgrams(content,2)
    trigram2_prob = distribution(trigram2,bigram2,0,0)
    return trigram2_prob






content = add_hash("training.de")

ngrams = getNgrams(content, 3)



wordcounts1 = len(cleanText(content))

content2 = add_hash("training.de")

bigram = getNgrams(content2,2)

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

sorted_probability = sorted(ggg.items(),key = operator.itemgetter(1))

ttt = add_hash("test.txt")
aaa = compute_distribution(ttt)
print aaa
str_list2 = random_sample_random_sequence(aaa,3)
# write_into_file(str_list2)
print(str_list2)
# perplexity_of_list_generated_by_test = caculate_perplexity(gf)
# print perplexity_of_list_generated_by_test
ggg = []
testprob1 = {} #training test.txt
testprob = add_hash("test.txt")
trigrammm = probs(testprob)
trigrammm1 = compute_distribution(testprob)
ppt = caculate_perplexity(trigrammm)

print trigrammm1
print ('woeijfnwr::::',trigrammm1.keys())
# ggg = np.random.binomial(10,trigrammm1.values(),len(trigrammm1.values()))
# print ggg


ggg = random_sample_random_sequence(trigrammm1,100)
print ('ggg:',ggg)

# print trigrammm



end = time.clock()

print ('Running time: %s Seconds'%(end-start))




