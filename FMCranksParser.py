# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 11:49:13 2019

@author: dipie
"""

import xlsxwriter, operator, time

start = time.time()

workbook = xlsxwriter.Workbook('FMCranks.xlsx')
worksheet = workbook.add_worksheet()

weeklyresults = []

file = open("FMCranks.txt", "r")
targetfile = open("parsedFMCranks.txt", 'r+')

for line in file:
    if "=" in line:
        targetfile.write(line)

targetfile.seek(0)
for line in targetfile:
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

row = 1
col = 0

podiums = [[],[],[]]
for i in range(1,4):
    podiums[i-1] = list(sorted(set([x[i] for x in weeklyresults])))[0:3]

first_format = workbook.add_format({'bg_color': '#FFCC00'})
second_format = workbook.add_format({'bg_color': '#808080'})
third_format = workbook.add_format({'bg_color': '#B33C00'})
formats = [first_format, second_format, third_format,None]
DNFormat = workbook.add_format({'font_color': '#E62E00'})
DNSormat = workbook.add_format({'font_color': '#0099FF'})
                                
weeklyresults = list(sorted(weeklyresults, key=operator.itemgetter(4,5)))

worksheet.write(0,0,"")

for item, a0,a1,a2,mean,_ in (weeklyresults):
    if a0 == 99:
        a0 = "DNF"
        mean = "DNF"
    if a1 == 99:
        a1 = "DNF"
        mean = "DNF"
    if a2 == 99:
        a2 = "DNF"
        mean = "DNF"
    if a0 == 98:
        a0 = "DNS"
        mean = "DNF"
    if a1 == 98:
        a1 = "DNS"
        mean = "DNF"
    if a2 == 98:
        a2 = "DNS"
        mean = "DNF"
    formato0 = formats[podiums[0].index(a0)] if a0 in podiums[0] else None
    formato1 = formats[podiums[1].index(a1)] if a1 in podiums[1] else None
    formato2 = formats[podiums[2].index(a2)] if a2 in podiums[2] else None
    if a0 == "DNF":
        formato0 = DNFormat
    if a1 == "DNF":
        formato1 = DNFormat
    if a2 == "DNF":
        formato2 = DNFormat
    if mean == "DNF":
        formato3 = DNFormat
    if a0 == "DNS":
        formato0 = DNSormat
    if a1 == "DNS":
        formato1 = DNSormat
    if a2 == "DNS":
        formato2 = DNSormat
    if mean == "DNS":
        formato3 = DNSormat
    elif mean != "DNS" and mean != "DNF":
        formato3 = None
    worksheet.write(row, col,     item)
    worksheet.write(row, col + 1, a0, formato0)
    worksheet.write(row, col + 2, a1, formato1)
    worksheet.write(row, col + 3, a2, formato2)
    worksheet.write(row, col + 4, mean, formato3)
    #worksheet.write(row, col + 5, "=MIN(B{}:D{})".format(row+1,row+1))
    #best solve not needed because the sorting is handled in Python directly
    row += 1

workbook.close()
file.close()
targetfile.close()
print("\n"+str(time.time() - start) + " seconds elapsed.\nEnjoy your XLSX file ;D")
input()
