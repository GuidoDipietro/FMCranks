# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 22:38:06 2019

@author: dipie
"""

from operator import itemgetter
from itertools import groupby, takewhile

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
    numbers = [[x[0]+x[1],x[2]+x[3],x[4]+x[5]] for x in numbers]
    numbers = [[s.replace("99","DNF").replace("98","DNS") for s in x] for x in numbers]
    numbers = [[int(x) if x.isdigit() else x for x in l] for l in numbers]
    return numbers

def getNames(data):
    data = [''.join(list(takewhile((lambda x: not x.isdigit()),l))[0:-1]) for l in data]
    return data