#!/usr/bin/env python
# ECE 2524 Homework 3 Problem 2
# Thomas Elliott

import argparse
import sys
import fileinput
import csv
import ast
from operator import itemgetter

parser = argparse.ArgumentParser(description='Multiply some integers.')
parser.add_argument("-f, --data-file", action='store',  dest=  'dataFile',   help="path to the data file to read at startup")
args = parser.parse_args()
dictList = []

def add_funct(arg):
    dictList.append(ast.literal_eval(arg))
    print "The item was added successfully"
    
def del_funct(arg):
    deleteCheck = False
    (field, equal,  value) = arg.partition("=")
    for item in dictList:
        print item[field]
        if item[field] == value:
            deleteCheck = True
            print "got inside if loop"
            del dictList[dictList.index(item)]
            print "The item with value: {} in field: {} was deleted".format(value,  field)
    if deleteCheck == False:
        print "The item with value: {} in field: {} was not found, so nothing was deleted".format(value, field)
        
def set_funct(arg):
    (change,  sep,  identifier) = arg.partition(" for ")
    (fieldChange,  equal, changeValue) = change.partition("=")
    (fieldSet,  equal2,  setValue) = identifier.partition("=")
    try:
        dictList[0][fieldChange]
        dictList[0][fieldSet]
        for item in dictList:
            if item[fieldSet] == setValue:
                dictList[dictList.index(item)][fieldChange] = changeValue
                print "The item has been updated"
    except KeyError as e:
        sys.stderr.write("{} or {} is not a valid field name\n".format(fieldChange,  fieldSet))
    
def list_funct(arg):
    writer = csv.DictWriter(sys.stdout,  fieldnames = dictList[0].keys(),  delimiter='|')
    if arg == "all":
        writer.writeheader()
        writer.writerows(dictList)
    else:
        try:
            if arg.find("with") > 0:
                (beginning,  middle,  identifier) = arg.partition(" with ")
                (field,  equal,  value) = identifier.partition("=")
                dictList[0][field]
                writer.writeheader()
                for item in dictList:
                    if item[field] == value:
                        writer.writerow(item)
            if arg.find("sort") > 0:
                (beginning,  sort,  field)  = arg.partition(" sort by ")
                if field == "Quantity":
                    sortedList = sorted(dictList,  key =  itemgetter(field)
                else:
                    sortedList = sorted(dictList,  key = itemgetter(field)
                writer.writeheader()
                writer.writerows(sortedList)
        except KeyError as e:
            sys.stderr.write("{} is not a valid field name\n".format(field))

#Read in file and store in list of Dictionaries
try:
    with open(args.dataFile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile,  delimiter='|')
        for row in reader:
            dictList.append(row)
except IOError as e:
    sys.stderr.write("The file at the path: {} was not found".format(args.dataFile))
    sys.exit(1)

#process commands entered on standard in
for data in iter(sys.stdin.readline,  ''):
    caseDict = {'add': add_funct,  'remove': del_funct,  'set':set_funct,  'list': list_funct}
    (action,  space,  modifier) = data.partition(" ")
    modifier = modifier.rstrip("\n")
    
    try:
        caseDict[action](modifier)
    except KeyError as e:
        sys.stderr.write("The command {} was not recognized\n".format(action))
    
#Write list of dictionaries back to file
with open(args.dataFile,  'wb') as outFile:
    writer = csv.DictWriter(outFile,  fieldnames = dictList[0].keys(),  delimiter='|')
    writer.writeheader()
    writer.writerows(dictList)
