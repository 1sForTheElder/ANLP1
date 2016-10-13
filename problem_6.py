# -*- coding: utf-8 -*-

# Problem6:
# Extend your program to read in a test document and compute (and output)
# its perplexity under the estimated language models.

import re
import numpy as np
import operator
from numpy.random import random_sample
import math
import problem_2 as p2
import problem_4 as p4
import problem_5 as p5

def caculate_perplexity(test): #caculate perplexity function by using distribution.values
    distribution = p5.compute_distribution(test)
    value = np.array(distribution.values())
    b = 0

    for a in value:
        b += -math.log(a,2)

    b = b / len(value) # formation (1/n)log2(p(n))
    return b


#####################  test  ####################

b = caculate_perplexity('test.txt')
print b

