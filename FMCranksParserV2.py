# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 19:34:45 2019

@author: dipie
"""

import xlsxwriter, time, excel2img
from operator import itemgetter
from itertools import groupby

#Ready, set, go!
start = time.time()

#This file has the raw data
file = open("FMCranks.txt", "r")

#Create an array with partially clean data
parsedresults = []
for line in file:
    if "=" in line:
        parsedresults.append(line)
file.close()

#Generates the weeklyresult array (processed results)
#Each item is [name, a0, a1, a2, mean, best]
weeklyresults = []
for line in parsedresults:
    #Changing DNF and DNS to have only numbers
    #Will be changed back later
    line = line.replace("DNF","99")
    line = line.replace("DNS","98")
    numbers = ''.join([x for x in line if x.isdigit()])
    numbers = numbers[0:6]
    numbers = [int(numbers[i:i+2]) for i in range(0, len(numbers), 2)]
    numbers = numbers + [round(sum(numbers)/3,2)]
    name = line.split()[0:3]
    name = [x for x in name if not any(char.isdigit() for char in x) and "DNF" not in x]
    name = " ".join(name)
    print(name,numbers)
    result = [name] + numbers + [min(numbers)]
    weeklyresults.append(result)

#Gens podiums (top3 results for each scramble)
podiums = [[],[],[]]
for i in range(1,4):
    podiums[i-1] = list(sorted(set([x[i] for x in weeklyresults])))[0:3]                             

#Sorts weeklyresults and enumerates the results
weeklyresults = list(sorted(weeklyresults, key=itemgetter(4,5)))
weeklyresults = [[str(i+1)] + l for i,(k,g) in enumerate(groupby(weeklyresults,key=itemgetter(4,5))) for l in g]

#Generates woaj and appends to weeklyresults
woajindiv = [min(x) for x in podiums]
woajrank = str(int(weeklyresults[-1][0])+1)
woaj = [woajrank] + ["woaj"] + woajindiv + [round(sum(woajindiv)/3,2)] + [min(woajindiv)]
weeklyresults = weeklyresults + [woaj]

#Init XLSX workbook
workbook = xlsxwriter.Workbook('FMCranks.xlsx')
worksheet = workbook.add_worksheet()

#Leave first row empty if you want to use the XLSX file
#otherwise it takes the first row as the headings
worksheet.write(0,0,"")

#Replacing 99 with DNF and 98 with DNS again...
for i in range(len(weeklyresults)):
    if 99 in weeklyresults[i] or 98 in weeklyresults[i]:
        weeklyresults[i][5] = "DNF"
        if 99 in weeklyresults[i]:
            weeklyresults[i][weeklyresults[i].index(99)] = "DNF"
        if 98 in weeklyresults[i]:
            weeklyresults[i][weeklyresults[i].index(98)] = "DNS"
            
#Formats
first_format = workbook.add_format({'bg_color': '#FFCC00', 'align': 'center'})
second_format = workbook.add_format({'bg_color': '#808080', 'align': 'center'})
third_format = workbook.add_format({'bg_color': '#B33C00', 'align': 'center'})
formato_verde = workbook.add_format({'bg_color': '#39B55A', 'align': 'center'})
formato_center_alig = workbook.add_format({'align': 'center'})
formats = [first_format, second_format, third_format,None]
DNFormat = workbook.add_format({'font_color': '#E62E00', 'align': 'center'})
DNSormat = workbook.add_format({'font_color': '#0099FF', 'align': 'center'})
badResultFormat = {"DNF": DNFormat, "DNS": DNSormat}   

#Writing to XLSX file
row = 1
col = 0
for ranking,item,a0,a1,a2,mean,_ in (weeklyresults):
    finalformats = ['','','','']
    variables = [a0,a1,a2,mean]
    
    #Formatting cells
    for i in range(0,4):
        if type(variables[i]) is str:
            finalformats[i] = badResultFormat[variables[i]]
        else:
            if i < 3:
                finalformats[i] = formats[podiums[i].index(variables[i])] if variables[i] in podiums[i] else formato_center_alig
            else:
                finalformats[3] = formato_center_alig
                
    if(item == "woaj"):
        worksheet.write(row, col, "", first_format)
        worksheet.write(row, col + 1, item, first_format)
        worksheet.write(row, col + 2, a0, first_format)
        worksheet.write(row, col + 3, a1, first_format)
        worksheet.write(row, col + 4, a2, first_format)
        worksheet.write(row, col + 5, mean, first_format)
    else:
        worksheet.write(row, col, int(ranking), formato_verde)
        worksheet.write(row, col + 1, item)
        worksheet.write(row, col + 2, a0, finalformats[0])
        worksheet.write(row, col + 3, a1, finalformats[1])
        worksheet.write(row, col + 4, a2, finalformats[2])
        worksheet.write(row, col + 5, mean, finalformats[3])
    row += 1
    
#Change column's widths
worksheet.set_column(0, 0, 2)
worksheet.set_column(1, 1, 20)
worksheet.set_column(2, 4, 4)
worksheet.set_column(5, 5, 5)

#Done with this file!
workbook.close()

#Say cheese! Taking screenshot of XLSX range
excel2img.export_img("FMCranks.xlsx", "FMCranks.png", "", "Sheet1!A2:F{}".format(row))

#Finished!
print(str(time.time() - start) + " seconds elapsed.\nEnjoy ;D")
