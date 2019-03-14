# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 22:38:06 2019

@author: dipie
"""

import time
from operator import itemgetter
from itertools import groupby, takewhile

#Ready, set, go!
start = time.time()

#This file has the raw data
def cleanData(filepath):
    with open(filepath, "r", encoding="unicode_escape") as file:
        #Create an array with partially clean data
        parsedresults = []
        for line in file:
            if "=" in line: parsedresults.append(line)
    data = [x.replace("DNF","99").replace("DNS","98") for x in parsedresults]
    return data

def getNumbers(data):
    numbers = [[a for a in line if a.isdigit()] for line in data]
    numbers = [(x[0]+x[1],x[2]+x[3],x[4]+x[5]) for x in numbers]
    numbers = [[int(x) for x in l] for l in numbers]
    numbers = [(x+[round((sum(x)/3),2)]) for x in numbers]
    numbers = [[str(n) for n in x] for x in numbers]
    numbers = [[s.replace("99","DNF").replace("98","DNS") for s in x] for x in numbers]
    for each in numbers:
        if "DNF" in each or "DNS" in each:
            each[3] = "DNF"
    return numbers

def getNames(data):
    data = [[''.join(list(takewhile((lambda x: not x.isdigit()),l))[0:-1])] for l in data]
    return data

def genDataArray(rawdata):
    names = getNames(rawdata)
    numbers = getNumbers(rawdata)
    arr = [names[i]+numbers[i] for i in range(len(names))]
    arr = list(sorted(arr, key=itemgetter(3,4)))
    arr = [[str(i+1)] + l for i,(k,g) in enumerate(groupby(arr,key=itemgetter(3,4))) for l in g]
    return arr

test = genDataArray(cleanData("FMCranks.txt"))

#Finished!
print(str(time.time() - start) + " seconds elapsed.\nEnjoy ;D")