# -*- coding: utf-8 -*-
import re



def process_line(input):  #function to perfixing and sufixing the notation of "#" to every sentence. In order to identify the begin and end of a sentence.
    b='#'
    f=open('test1.txt','w')    # open or create a new file txt
    g = open(input)
    for line in g:          #just do it
        line = b + b + line[:-1] + b
        f.write(line)
    f.close()
    gg5 = open("test1.txt").read()
    gg5 = cleanInput(gg5)

    return gg5


def cleanText(input):

    input = re.sub('[^a-zA-Z0-9^#^ ]', '', input) #delete characters except for English letter, #, space, period and digits
    input = input.lower()   #lowercase all the characters
    input = re.sub('\d', '0', input)    #replace all digits with '0'
    input = bytes(input)   #character all of them

    return input #return input

def cleanInput(input): #ready to process the lines
    input = cleanText(input) #firstly do clean text
    cleanInput = []     #create a list call cleanInput

    for item in input:   #collect the text letter by letter
        if len(item) == 1:
            cleanInput.append(item)
    return cleanInput

test_process_line = process_line("training.de") #try
print test_process_line

