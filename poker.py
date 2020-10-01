from scores import combi,hand_values, df, should_call, combinations, score_hand, expected_value

from functools import lru_cache as cache
import pandas as pd
from IPython import get_ipython;   
import itertools
from statistics import mean
from numba import jit, vectorize
import timeit
import numpy as np
from itertools import permutations
from numpy import vectorize
import random

@jit(nopython=True)
def numba_4():
    results = []
    len1 = c4.shape[0]
    len2 = combi.shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c4[i],combi[j]) == 4:
                results.append(combi[j])
    return results

@jit(nopython=True)
def numba_3():
    results = []
    len1 = c3.shape[0]
    len2 = combi.shape[0]
    for i in range(len1):
        for j in range(len2):
            if common(c3[i],combi[j]) == 4:
                results.append(combi[j])
    return results

@cache(maxsize=None)
def opti_3():
    values= numba_3()
    return [score_hand(i) for i in values]

@cache(maxsize=None)
def opti_4():
    values= numba_4()
    return [score_hand(i) for i in values]

def expected_value(hand,combi):
    if len(hand) == 5:
        maxi = score_hand(hand)
        mean= mean(opti_3() + opti_4())
    elif len(mano) == 6:
        maxi = max([score_hand(i) for i in combinations(mano,5)])
        media = mean(opti_4())
    elif len(mano) == 7:
        maxi = max([score_hand(i) for i in combinations(mano,5)])
        mean= maxi    
    values = [maxi,mean]
    return values
  
def should_call(players,percentile,pot,price):
    pwin = (percentile/100)**players
    ev = pwin*pot
    if ev <= 0:
        print('you should fold')
    if ev > 0:
        print('You should bet as long as it is less than %s $' % ev)
    print('The expected value betting %s is %s $' % (price,ev-price))
    return pwin*100
