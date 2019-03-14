# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:11:20 2019

@author: dipie
"""

from src.list_to_image import list_2_image
from src.FMCranksParserV3 import cleanData, getNames, getNumbers

def main():
    scores = getNumbers(cleanData("FMCranks.txt"))
    print(scores)
    names = getNames(cleanData("FMCranks.txt"))
    print(names)
    #scores = random_scores()
    #names = random_names()
    
    img = list_2_image(names, scores)
    img.save('image.png')    

main()