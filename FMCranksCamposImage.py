# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:11:20 2019

@author: dipie
"""

from src.list_to_image import list_2_image
from src.FMCranksParser import cleanData, getNames, getNumbers

def main():
    scores = getNumbers(cleanData("FMCranks.txt"))
    names = getNames(cleanData("FMCranks.txt"))
    
    img = list_2_image(names, scores)
    img.save('image.png')    

main()
