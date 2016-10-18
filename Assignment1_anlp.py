# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:57:33 2016

@author: Cohrii&YiLuo
"""
import time
import re
import numpy as np
import operator
import random

#=====================================Q_2=====================================#
def process_line(input):
    #a function for preprocessing text
    #a already processed file should start with a hash sign
    content_string = '#'
    g = open(input)
    #open the file to be processed by line
    for line in g:
        #use 'for' loop to automatically add '#' at the beginning and at the end of every sentence
        content_string += '#'+line+'#'
    #perfix and sufix the notation of "#" to every sentence. In order to identify the begin and end of a sentence
    content_list = cleanInput(content_string)
    #put the already processed sentence into function(cleanInput)
    return content_list

def cleanText(input):
    #a function for eliminating disturbance and reserve meaningful characters(such as English letters, digits, hash sign and '.')
    input = re.sub('[^a-zA-Z0-9^#^ ^.]', '', input)
    #delete characters except for English letter, #, space, period and digits
    input = re.sub('#.#','',input)
    #remove sequence of '#.#'(which may only be included in training.es) for successful process
    input = input.lower()
    #lowercase all the characters
    input = re.sub('\d', '0', input)
    #replace all digits with '0' according to the requirements
    input = bytes(input)
    #character all of them
    return input

def cleanInput(input):
    #a function for cleaning the text and dividing the content by character.
    #firstly do clean text
    input = cleanText(input)
    cleanInput = []
    #create a list call cleanInput
    for item in input:
        #collect the text letter by letter
        cleanInput.append(item)
    return cleanInput


# =====================================Q_4=====================================#
def generate_Trigram_list():
    #a function for generating all legal trigrams through using vocabulary and special case.
    #firstly, define vocabulary from given conditions
    vocabulary = np.array([' ','#','.','0','a','b','c','d','e','f',
                           'g','h','i','j','k','l','m','n','o','p',
                           'q','r','s','t','u','v','w','x','y','z'])
    trigrams_list = {}
    #define a dictionary for storing
    for a in vocabulary:
    #generate all legal trigrams via some rules
        for b in vocabulary:
            if (a!='#' and b=='#'):
            #when a trigram sequence is not led by '#' but its second character is '#', it should be precluded.
                continue
            for c in vocabulary:
                if a=='#' and c=='#':
                #trigram sequences which led by '#' and end with '#' should be precluded.
                    continue
                trigrams_list[a+b+c] = 0
                #compose the sequence by selected characters
    return trigrams_list

def get_Trigrams(input, Ngrams_list):
    #a function to make a Ngrams model by analyzing given text. The parameter of input means given text, Ngrams_list means array of all legal trigram lists
    input = process_line(input)
    #use the cleanText function to pre-process given text
    for i in range(len(input)-2):
    #divide them into groups with 3 characters.
        ngramTemp = "".join(input[i:i+3])
	    #collect all three character sequences that have appeared in lines.
        if ngramTemp[0] == '#' or ngramTemp[1] != '#':
	    #exclude illegal sequences whose second character is '#' but do not begin with a '#'
            Ngrams_list[ngramTemp] += 1
	        #collect legal sequences and store them into the dictionary by using 'key' as index. When the key can be matched, the value belong the key should add one.
    return Ngrams_list


def get_Count_List(Ngrams_list):
    #a function to get [(c,Nc)]. 'c' means frequency of occurance. 'Nc' means how the number of N-grams that occured c times. Parameter ‘Ngrams_list’ is a given list.
    #create a new dictionary for storing
    Count_List = {}
    for i in Ngrams_list:
    #traverse the Ngram list
        if Ngrams_list[i] not in Count_List:
	    #insert differect counts of occurance into value of Count_List
            Count_List[Ngrams_list[i]] = 0;
            #if the number of count has not come up yet, insert a item with key = Ngrams_list and value = 0 into the dictionary
        Count_List[Ngrams_list[i]] +=1
        #if the number of count has come up once, the value for key of Ngram_list[i] in Count_List should add one
    Count_List = sorted(Count_List.items(),key=operator.itemgetter(0))
    #Sort the new dictionary so that it can change into List data structure, which can be more convenient for latter processes.
    return Count_List


def part_Good_Turing(Count_list):
    #a function to smooth the obtained N-grams by using part_good_turning methon, which means only sequences appeared before the first hollow would be Good_Turning.
    Turing_List = np.zeros((len(Count_list),3))
    #generate an array defined by numpy for the purpose of storing data structure like [c,c*,Nc]. PS: 'c' represents Count,'Nc' represents Count of Counts, 'c*' represents Adjust Count
    flag = 0
    #define a variable for more controllable process
    for i in range(0,len(Count_list)):
    #create a loop to traverse the given Count_List(a N-gram dictionary)
        if flag == 0:
            Turing_List[i][0] = Count_list[i][0]
	        #copy the value of count from Count_list to the new dictionary.
            Turing_List[i][1] = float((i+1))*Count_list[i+1][1]/Count_list[i][1]
	        #the value of Turning_List[i][1] should be Adjust Counts which can be derived through formation of c∗ = (c + 1)(Nc+1)/Nc
            Turing_List[i][2] = Count_list[i][1]
	        #copy the value of Nc from Count_list and save it to Turning_List[i][2]
            if Count_list[i+2][0] != i+2:
	        #change the value of flag from 0 to 1 when we counter a hole, which means discontinuity in the count of occurance.
                flag = 1
        else:
        # Once we counter a hole in the successive value, stop smoothing and just fill c as c*
            Turing_List[i][0] = Count_list[i][0]
            Turing_List[i][1] = Count_list[i][0]
            Turing_List[i][2] = Count_list[i][1]
    return Turing_List


def Sum(Turing_list):
    #a function to sum the number of occurance of all the sequences. That is c* * Nc.
    Total_Count = 0.0
    #define a variable named Total_Count
    for i in Turing_list:
    #use loop for efficient caculation
        Total_Count += i[1]*i[2]
    return Total_Count


def GT_prob(Turing_list, Total_Count):
#a function to caculate joint probabilities of every occurance time of Ngrams
    GT_prob_list = {}
    for i in range(0,len(Turing_list)):
        #GT_prob_list[i][0] = Turing_list[i][0]
        GT_prob_list[Turing_list[i][0]] = Turing_list[i][1]/Total_Count
	#the 'c'(Count) should correspond to probability obtained by Turing_list[i][1]/Total_Count

    return GT_prob_list

def Ngram_prob(Ngrams_list, GT_prob_list):
    #a function to relate Ngram sequences to conditional probabilities that correspond to themselves
    Ngrams_prob_list = {}
    for i in Ngrams_list:
    #use loop to traverse obtained Ngrams_list's keys
        Ngrams_prob_list[i] = GT_prob_list[Ngrams_list[i]]
	#'GT_prob_list[Ngrams_list[i]]' means probabilities corresponse to trigram sequences such as 'aaa'. After obtaining value of the corresponding probability, we insert it into dictionary by key
    Ngrams_prob_list = sorted(Ngrams_prob_list.items(),key=operator.itemgetter(0))

    flag = ''
    prob_sum = 0.0
    for i in range(0,len(Ngrams_prob_list)):
    #traverse all the sequences and their probabilities.
        if Ngrams_prob_list[i][0][0:2]!=flag:
	    #judge whether the first two characters of the item we are processing are equivalent to those whose we stored in flag. If it is, continue the programme.
            flag = Ngrams_prob_list[i][0][0:2]
	        #let the variable flag derive a new value
            prob_sum = 0
            for j in range(i,len(Ngrams_prob_list)):
	        #traverse remaining sequences and their probabilities
                if Ngrams_prob_list[j][0][0:2]!=flag:
		        #try to find the sequence with the same first two characters as flag's defined just now.
                    break
                prob_sum += Ngrams_prob_list[j][1]
		        #if we find it , add it into the prob_sum as a total probability of those sequences with the same first two characters.
        Ngrams_prob_list[i] = (Ngrams_prob_list[i][0],Ngrams_prob_list[i][1]/prob_sum)
        #caculate the Ngrams conditional probabilities correspond to each sequence. Then store it into the dictionary.
    return Ngrams_prob_list


def Append_SpecialCase(Ngrams_prob_list):
    # a function to append special cases that corresponding probability is 0 to the obtained Ngrams_prob_List to make
    insert_string = np.array(['#', '#', '#'])
    # define an array of string for inserting
    vocabulary = np.array([' ', '#', '.', '0', 'a', 'b', 'c', 'd', 'e', 'f',
                           # define a vovabulary
                           'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    for i in vocabulary:
        # append special case with format of '#X#' (p.s 'X' at middle means any characters) so that their probability will not be a hole.
        insert_string[1] = i
        Ngrams_prob_list.append((insert_string[0] + insert_string[1] + insert_string[2], 0.0))

    insert_string[1] = '#'
    for i in vocabulary:
        # traverse vocabulary
        if i == '#':
            continue
        insert_string[0] = i
        for j in vocabulary:
            insert_string[2] = j
            if j == '#':
                Ngrams_prob_list.append((insert_string[0] + insert_string[1] + insert_string[2], 1.0))
            # assign probability value 1.0 to all sequences like '*##',and then insert this sequences couple with its probability into the dictionary
            else:
                Ngrams_prob_list.append((insert_string[0] + insert_string[1] + insert_string[2], 0.0))
                # assign probability value 0.0 to all sequences like '*#*',and then insert this sequences couple with its probability into the dictionary
    Ngrams_prob_list.sort(key=operator.itemgetter(0))
    return Ngrams_prob_list


def write_into_file(data,filename):
    #a function to write the probability that trained by a text into a file. Parameter 'data' means a trained language model. Parameter filename means the name you want to give to the file.
    f = open(filename, 'w')
    #open a file or (if the given filename is not existent) create a file.
    for item in data:
    #use a loop to traverse the language model
        f.write(item[0])
        #write the sequence into the file
        f.write('\t')
        #add a space between sequence and probability
        f.write(str(format(item[1],'.3e')))
        #write probability into the file after scientize it
        f.write('\r\n')
        #add line breaks
    f.close()


def Trigram_training(input, filename):
    #a function to train a model. Parameter 'input' represents name of text you want to train. Parameter 'filename' represents the name of file you want to write result in.
    #invoke functions to complete the procedure from getting text processing to write result into a file
    Ngrams_list = generate_Trigram_list()
    Ngrams_list = get_Trigrams(input,Ngrams_list)
    Count_list = get_Count_List(Ngrams_list)
    Turing_list = part_Good_Turing(Count_list)
    Sum_Count = Sum(Turing_list)
    Prob_list = GT_prob(Turing_list, Sum_Count)
    Ngrams_prob_list = Ngram_prob(Ngrams_list, Prob_list)
    Ngrams_prob_list = Append_SpecialCase(Ngrams_prob_list)
    write_into_file(Ngrams_prob_list, filename)
    return Ngrams_prob_list


# =====================================Q_5=====================================#
def read_model(input,SpecialCase = True):
    #a function to derive clear structure model from given file(such as model-br.en)
    #’SpecialCase == True’ means that special cases need to be inserted into the model.
    f=open(input)
    Given_model = {}
    #define a new dictionary to store processed file
    for line in f:
    #traverse the given language model
        Given_model[line[0]+line[1]+line[2]] = float(line[4:])
	    #consider the first three characters, which represent sequence, of every line in file as key of the dictionary and consider character whose index is larger than 3 as value of the dictionary
    Given_model = sorted(Given_model.items(),key=operator.itemgetter(0))
    if SpecialCase == True:
    #if necessary, add special cases
        Given_model = Append_SpecialCase(Given_model)
    return Given_model

def generate_sample(model, V, N):
    #a function to generate random sample base on language model that is given. Parameter model means given LM, and 'N' means the number or characters you want to generate.
    #According to our comprehension of '#' in the question(please find first paragraph of our report), the generated text should start with '##'.
    result = '##'
    for i in range(2,N):
    #use a loop for generating specific number of characters, and the number will be (N-2).
        prob = np.zeros(V)
	    #define a np.zeros array to temporarily save conditional probabilities.
        for j in range(0,V):
	    #use a loop to traverse the first character
            if model[V*V*j][0][0]==result[i-2]:
		    #when the first character of sequence is corresponding to the penultimate character of generated result
                for k in range(0,V):
	            #use a loop so that we can judge the second character of the sequence
                    if model[V*V*j+V*k][0][1]==result[i-1]:
	                #when the second character of sequence is corresponding to the last character of generated result
                        for l in range(0,V):
	                    #use a loop to traverse the third character
                            prob[l] = model[V*V*j+V*k+l][1]
	                        #save the probability of sequence into prob list
                        bins = np.cumsum(prob[:V-1])
	                    #use cumsum function to caculate cumulative sum of the values in a group of 29 probabilities
                        letter_index = np.digitize(np.array([random.random()]), bins,right=True)
	                    #randomly generate a letter_index among characters in the group by using probabilities just now.
                        letter = model[(V*V*j)+(V*k)+letter_index][0][2]
	                    #according to the index, we can exactly get the letter.
                        result = result+letter
                        break
                break
    return result


# =====================================Q_6=====================================#
def cal_perplexity(model, sample, V):
    #define a function to caculate perplexity . Parameter 'model' means the given model that trained by ourselves. Parameter 'sample' means and 'V' means the vocabulary size.
    #firstly, derive length of sample
    n = len(sample)
    prob = 1
    for i in range(2,n):
    #use a loop for automatically traversing text with index between i-2 and 1-n
        for j in range(0,V):
            if model[V*V*j][0][0]==sample[i-2]:
            #compare the first character of sequences in given model with the sample's characters so that we can match the probabilities of sequences from sample and trigram sequences from model
                for k in range(0,V):
                    if model[V*V*j+V*k][0][1]==sample[i-1]:
	                #find the proper trigram probability which corresponds to the sample's sequence
                        for l in range(0,V):
                            if model[V*V*j+V*k+l][0][2]==sample[i]:
                                prob *= np.power(model[V*V*j+V*k+l][1],-1.0/n)
	                            #implement equation of (P(W1.....Wn).^(-1/n)), which aims to figure out the perplexity
                                break
                        break
                break

    return prob


# ====================================Test=====================================#
start = time.clock()
Q1_model = read_model('Q1model.txt', SpecialCase=False)
#Use read_model function to read a given model and transform data inside to more efficient structure.
test = [('#'), ('#'), ('a'), ('b'), ('a'), ('a'), ('b'), ('#')]
PP_test = cal_perplexity(Q1_model, test, 3)
#Use cal_perplexity to
print ('Q1_Perplexity: ', PP_test)

My_model = Trigram_training('training.en', 'EN_model')
Given_model = read_model('model-br.en')
#Use read_model function to read a given model and transform data inside to more efficient structure.
My_result = generate_sample(My_model, 30, 300)
#Generate 300 characters sample base on our trained model
print ('My model result: ' + My_result)
Given_result = generate_sample(My_model, 30, 300)
#Generate 300 characters sample base on given model
print ('Given model result: ' + Given_result)

sample = process_line('test.txt')
#Preprocess given text
PP_EN = cal_perplexity(My_model, sample, 30)
#caculate perplexity base on our own model and given sample
print ('Sample Perplexity under my English model: ', PP_EN)
PP_EN = cal_perplexity(Given_model, sample, 30)
#caculate perplexity base on trained English model and given sample
print ('Sample Perplexity under given English model: ', PP_EN)
My_model = Trigram_training('training.de', 'DE_model')
#train trigram language model base on given German text
PP_DE = cal_perplexity(My_model, sample, 30)
#caculate perplexity base on trained German model and given sample
print ('Sample Perplexity under my Germany model: ', PP_DE)
My_model = Trigram_training('training.es', 'ES_model')
#train trigram language model base on given English text
PP_ES = cal_perplexity(My_model, sample, 30)
print ('Sample Perplexity under my Spanish model: ', PP_ES)
#caculate perplexity base on trained spanish model and given sample
end = time.clock()
print ('running time: ',end-start)

# ====================================Interpolation Smoothing=====================================#
def generate_Bigrams_list():
    vacabulary = np.array([' ', '#', '.', '0', 'a', 'b', 'c', 'd', 'e', 'f',
                           'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    Bigrams_list = {}
    for a in vacabulary:
        for b in vacabulary:
            Bigrams_list[a + b] = 0
    return Bigrams_list


def get_Bigrams(input, Bigrams_list):
    input = process_line(input)
    for i in range(len(input) - 1):
        ngramTemp = "".join(input[i:i + 2])
        Bigrams_list[ngramTemp] += 1
    return Bigrams_list


def generate_Unigrams_list():
    vacabulary = np.array([' ', '#', '.', '0', 'a', 'b', 'c', 'd', 'e', 'f',
                           'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                           'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
    Unigrams_list = {}
    for a in vacabulary:
        Unigrams_list[a] = 0
    return Unigrams_list


def get_Unigrams(input, Unigrams_list):
    input = process_line(input)
    for i in range(len(input)):
        ngramTemp = input[i]
        Unigrams_list[ngramTemp] += 1
    return Unigrams_list


Trigrams_list = {}
for i in My_model:
    Trigrams_list[i[0]]=i[1]

Bigrams_list = generate_Bigrams_list()
Bigrams_list = get_Bigrams('training.en', Bigrams_list)

Unigrams_list = generate_Unigrams_list()
Unigrams_list = get_Unigrams('training.en', Unigrams_list)

counts = 0.0
for i in Unigrams_list:
    counts += Unigrams_list[i]

PP_MIN = 50.0
i_min = 0.0
j_min = 0.0
s = 1000       #bisection step
a = c = 0      #bisection lower limit
b = d = 10000  #bisection upper limit
for m in range(0,3): #bisection loop
    print('Wait...')
    for i in range(a,b,s):
        for j in range(c,d,s):
            New_Trigrams_list = {}
            for k in Trigrams_list:
                New_Trigrams_list[k] = ((i/10000.0) * Trigrams_list[k]) + ( (j/10000.0) *float(Bigrams_list[k[1] + k[2]])/Unigrams_list[k[1]]) + (((10000.0-i-j)/10000.0)* float(Unigrams_list[k[2]]) / counts) #computation of Interpolation Smoothing model
            New_Trigrams_list = sorted(New_Trigrams_list.items(), key=operator.itemgetter(0))
            PP_IN = cal_perplexity(New_Trigrams_list, sample, 30)
            if PP_IN<PP_MIN:
                PP_MIN = PP_IN
                i_min = i
                j_min = j
    s = s/10   #step down
    print s
    a = i_min-s*5   #narrow limits
    if a<0:
        a=0
    b = i_min+s*5
    if b>10000:
        b=10000
    c = j_min-s*5
    if c<0:
        c=0
    d = j_min+s*5
    if d>10000:
        d=10000
Interprolation_Smoothing_model = {}
for k in Trigrams_list:
    Interprolation_Smoothing_model[k] = ((i_min / 10000.0) * Trigrams_list[k]) + ((j_min / 10000.0) * float(Bigrams_list[k[1] + k[2]]) / Unigrams_list[k[1]]) + (((10000.0 - i - j) / 10000.0) * float(Unigrams_list[k[2]]) / counts)
Interprolation_Smoothing_model = sorted(Interprolation_Smoothing_model.items(), key=operator.itemgetter(0))
SUM = 0.0
for i in range(9000,9030):
    SUM+=Interprolation_Smoothing_model[i][1]
print ('Sum of a set of conditional probabilities: ',SUM)
print ( 'Lambda1= ',i_min/10000.0)
print ( 'Lambda2= ',j_min/10000.0)
print ( 'Lambda3= ',round(1-i_min/10000.0-j_min/10000.0,3))
print ('Minimum Sample Perplexity under Interprolation Smoothing English model: ', PP_MIN)
print ('FINISH!')