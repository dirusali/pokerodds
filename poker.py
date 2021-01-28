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

numbers=list(range(2,15))
palos=['C','P','T','R']
baraja = []
for i in numbers:
    for p in palos:
        c = p+str(i)
        baraja.append(c)



def check_poker(hand,letras,numeros,rnum,rletras):
    for i in numeros:
            if numeros.count(i) == 4:
                poker = i
            elif numeros.count(i) == 1:
                carta = i
    score = 105 + poker + carta/100
    return score

def check_full(hand,letras,numeros,rnum,rletras):
    for i in numeros:
        if numeros.count(i) == 3:
            full = i
        elif numeros.count(i) == 2:
            p = i
    score = 90 + full + p/100  
    return score

def check_trio(hand,letras,numeros,rnum,rletras):
    cartas = []
    tipo = 'trio'
    for i in numeros:
        if numeros.count(i) == 3:
            trio = i
        else: 
            cartas.append(i)
    score = 45 + trio + max(cartas) + min(cartas)/1000
    return score

def check_doble_pareja(hand,letras,numeros,rnum,rletras):
    parejas = []
    cartas = []
    for i in numeros:
        if numeros.count(i) == 2:
            parejas.append(i)
        elif numeros.count(i) == 1:
            cartas.append(i)
            cartas = sorted(cartas,reverse=True)
    score = 30 + max(parejas) + min(parejas)/100 + cartas[0]/1000
    return score

def check_pareja(hand,letras,numeros,rnum,rletras):    
    pareja = []
    cartas  = []
    for i in numeros:
        if numeros.count(i) == 2:
            pareja.append(i)
        elif numeros.count(i) == 1:    
            cartas.append(i)
            cartas = sorted(cartas,reverse=True)
    score = 15 + pareja[0] + cartas[0]/100 + cartas[1]/1000 + cartas[2]/10000
    return score

def score_hand(hand):
    letras = [hand[i][:1] for i in range(5)]
    numeros = [int(hand[i][1:]) for i in range(5)]
    rnum = [numeros.count(i) for i in numeros]
    rletras = [letras.count(i) for i in letras]
    dif = max(numeros) - min(numeros)
    tipo= ''
    score = 0
    if 5 in rletras:
        if numeros ==[14,13,12,11,10]:
            tipo = 'escalerareal'
            score = 135
        elif dif == 4 and max(rnum) == 1:
            tipo = 'escaleracolor'
            score = 120 + max(numeros)
        elif 4 in rnum:
            tipo == 'poker'
            score = check_poker(hand,letras,numeros,rnum,rletras)
        elif sorted(rnum) == [2,2,3,3,3]:
            tipo == 'full'
            score = check_full(hand,letras,numeros,rnum,rletras)
        elif 3 in rnum:
            tipo = 'trio'
            score = check_trio(hand,letras,numeros,rnum,rletras)
        elif rnum.count(2) == 4:
            tipo = 'doble_pareja'
            score = check_doble_pareja(hand,letras,numeros,rnum,rletras)
        elif rnum.count(2) == 2:
            tipo = 'pareja'
            score = check_pareja(hand,letras,numeros,rnum,rletras)
        else:
            tipo = 'color'
            score = 75 + max(numeros)/100
    elif 4 in rnum:
        tipo = 'poker'
        score = check_poker(hand,letras,numeros,rnum,rletras)
    elif sorted(rnum) == [2,2,3,3,3]:
        tipo = 'full'
        score = check_full(hand,letras,numeros,rnum,rletras)
    elif 3 in rnum:
        tipo = 'trio'
        score = check_trio(hand,letras,numeros,rnum,rletras)
    elif rnum.count(2) == 4:
        tipo = 'doblepareja'
        score = check_doble_pareja(hand,letras,numeros,rnum,rletras)
    elif rnum.count(2) == 2:
        tipo = 'pareja'
        score = check_pareja(hand,letras,numeros,rnum,rletras)
    elif dif == 4:
        tipo = 'escalera'
        score = 65 + max(numeros)
    else:
        tipo= 'cartalta'
        numero = sorted(numeros,reverse=True)
        score = numeros[0] + numeros[1]/100 + numeros[2]/1000 + numeros[3]/10000 + numeros[4]/100000
    return score
    

def combs(a, r):
    a = np.asarray(a)
    dt = np.dtype([('', a.dtype)]*r)
    b = np.fromiter(itertools.combinations(a, r), dt)
    return b.view(a.dtype).reshape(-1, r)



def handvalues(combi):
    scores =[{"mano": i, "valor": score_hand(i)} for i in combi]
    scores = sorted(scores, key = lambda k: k['valor'])
    return scores
 

def getcards(cards):
    return ''.join(cards)

def blind():
    cards = []
    cards.append(random.choice(baraja))
    cards.append(random.choice(baraja))
    return cards

def should_call(players,percentile,pot,price):
    pwin = (percentile/100)**players
    ev = pwin*pot
    if ev - price <= 0:
        print('you should fold')
    if ev - price > 0:
        print('You should bet')
    print('The expected value betting %s is %s $' % (price,ev-price))
    return pwin*100


def flop():
    flop = []
    flop.append(random.choice(baraja))
    flop.append(random.choice(baraja))
    flop.append(random.choice(baraja))
    return flop

def riverturn():
    river = []
    river.append(random.choice(baraja))
    return river

def bluffsize(freq):
    return freq/(1-2*freq)

def bluff_freq():
    freq = np.linspace(0.2,0.43,10)
    n = random.randint(0,9)
    bluffing = freq[n]*100
    lista = []
    for i in range(0,100):
        if i < bluffing:
            lista.append('bluffing')
        elif i >= bluffing:
            lista.append('value betting')
            
    r = random.randint(0,100)
    if lista[r] == 'bluffing':
        print('bluffing con size of bet de %s pot' % bluffsize(freq[n]))
    else:
        return lista[r]
    
            
    
def call_bluffs(potrate):
    return 1/(1 + potrate)

@cache(maxsize=2)
def combiopti(combi,c4):
    for i in c4:
        values = [j for j in combi if all(elem in j for elem in i) == True]
    return [score_hand(i) for i in values]

def evalua(mano,combi):
    c5= tuple([tuple(sorted(i)) for i in combs(mano,5)])
    c4= tuple([tuple(sorted(i)) for i in combs(mano,4)])
    c3= tuple([tuple(sorted(i)) for i in combs(mano,3)])
    tuples = tuple(tuple(sorted(i)) for i in combi)
    if len(mano) > 5:
        combiflop = combs(mano,5)
    values = []
    if len(mano) == 5:
        maximo = score_hand(mano)
        s3 = combiopti(tuples,c3)
        s4 = combiopti(tuples,c4)
        media = mean(s3 + s4)
    elif len(mano) == 6:
        maximo = max([score_hand(i) for i in combiflop])
        media = mean(combiopti(tuples,c4))
    elif len(mano) == 7:
        maximo = max([score_hand(i) for i in combiflop])
        media = maximo    
    values = [maximo,media]
    return values

combi = combs(baraja,5)
hand_values= handvalues(combi)
x = [i.get("mano","") for i in hand_values]
z = [i.get("valor","") for i in hand_values]

data = {'manos':x, 'valor':z}
df = pd.DataFrame(data)


#bluff_freq()

#preflop = []
#for i in range(0,2):
#    preflop.append(str(input('enter card: ')))
#print('the preflop cards are %s' % preflop)
#base = mean(basevalue(preflop))
#print('the score is %s' % base)

#a = df.loc[df['score'] >= base, ['percentil']]
#percen = df.iloc[a.index[0]].percentil
#print('my preflop value is %s' % percen)

#players = float(input('enter number of players: '))
#pot = float(input('enter pot value: '))
#price = float(input('enter value of your bet: '))
#should_call(players,percen,pot,price)

flop = []

for i in range(0,5):
    flop.append(str(input('enter card: ')))
flopscore = evalua(flop,combi)
actual = (df.loc[df['valor'] >= flopscore[0], ['valor']].index[0]/2598960)*100
futuro = (df.loc[df['valor'] >= flopscore[1], ['valor']].index[0]/2598960)*100
print('tengo ahora un valor de %s y la media futura es %s' % (actual,futuro))
players = float(input('enter number of players: '))
pot = float(input('enter pot value: '))
price = float(input('enter value of your bet: '))
if actual > futuro:
    should_call(players,actual,pot,price)
else:
    should_call(players,futuro,pot,price)

    
turn = []

turn.append(str(input('enter card: '))) 
flop.append(turn[0]) 

combiturn = evalua(flop,combi)
actual = (df.loc[df['valor'] >= combiturn[0], ['valor']].index[0]/2598960)*100
futuro = (df.loc[df['valor'] >= combiturn[0], ['valor']].index[0]/2598960)*100
print('tengo ahora un valor de %s y la media futura es %s' % (actual,futuro))

players = float(input('enter number of players: ')) 
pot = float(input('enter pot value: ')) 
price = float(input('enter value of your bet: ')) 
if  actual > futuro:
    should_call(players,actual,pot,price)
else: 
    should_call(players,futuro,pot,price)

    
    
river = []
river.append(str(input('enter card: ')))
flop.append(river[0])
combiriver = evalua(flop,combi)
r = df.loc[df['valor'] >= combiriver, ['valor']]
actual = (df.loc[df['valor'] >= combiriver[0], ['valor']].index[0]/2598960)*100
print('Mi valor final máximo es %s' % actual)
players = float(input('enter number of players: '))
pot = float(input('enter pot value: '))
price = float(input('enter value of your bet: '))
should_call(players,actual,pot,price)
