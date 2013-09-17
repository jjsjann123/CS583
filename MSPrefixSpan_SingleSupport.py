#!/usr/bin/env python
# encoding: utf-8
"""
MSPrefixSpan.py

Created by Yuzong Liu on 2011-03-14.
Copyright (c) 2011 . All rights reserved.
"""

import sys, os
import re
import string
import util
import copy
from dataSequence import *


def gen_l1patterns(SequenceDataset,M,min_sup):
    '''returns a list of length-1 patterns:
        each element of the list is a tuple in the form of
        (item, count, projected-Database)'''
    L1Patterns=[]
    F = []
    for item in M:
        count = 0
        for sequence in SequenceDataset:
            flag, [pos,idx] = util.isItemInElement(item,sequence)
            count += int(flag)
        if count >= min_sup:
            F.append(item)
    # print F        
    for item in F:
        count = 0
        projDB=[]
        for sequence in SequenceDataset:
            flag, [pos,idx] = util.isItemInElement(item,sequence)
            count += int(flag)
            if flag:
                "locate the position in the sequence"
                seq = sequence[pos:]
                "locate the index of the position"
                seq[0] = seq[0][idx:]
                if len(seq[0]) == 1:
                    seq = seq[1:]                    
                else:
                    seq[0][0] = '_'
                if seq != []:
                    i = 0
                    j = 0
                    while i < len(seq):
                        while j < len(seq[i]):
                            if F.count(seq[i][j]) == 0 and seq[i][j] != '_':
                                del seq[i][j]
                            j += 1
                        i += 1        
                    projDB.append(seq)
        if count < min_sup:
            continue     
        L1Patterns.append(([item],count,projDB))        
    return L1Patterns    
        
	    
def prefixSpan(pattern,l,projDB,F,min_sup):
    # output_Patterns = {} 
    nextSeqPattern = []
    l += 1
    output_Patterns = []
    for item in F:
        # print item
        count = 0
        newProjDB = []
        "find all patterns of the form <{30}{x}>"
        for sequence in projDB:
            # print sequence
            if sequence[0][0] == '_':
                continue
            flag, [pos,idx] = util.isItemInElement(item,sequence)
            # print flag, [pos, idx]
            count += int(flag)
            if flag:
                seq = sequence[pos:]
                seq[0] = seq[0][idx:]
                if len(seq[0]) == 1:
                    seq = seq[1:]
                else:
                    seq[0][0] = '_'
                if seq != []:
                    i = 0
                    j = 0
                    while i < len(seq):
                        while j < len(seq[i]):
                            if F.count(seq[i][j]) == 0 and seq[i][j] != '_':
                                del seq[i][j]
                            j += 1
                        i += 1        
                    newProjDB.append(seq)                   
        if count >= min_sup:
            output_Patterns.append(([pattern,[item]],count,newProjDB))  
                      

        count = 0
        newProjDB = []            
        "find all patterns of the form <{30,x}>"
        for sequence in projDB:
            # print sequence
            flag, [pos,idx] = util.isItemInElement(item,sequence)
            # print flag, [pos, idx]
            if flag:
                if sequence[0][0] == '_' and pos == 0:
                    count += int(flag)
                    seq = sequence[pos:]
                    seq[0] = seq[0][idx:]
                    if len(seq[0]) == 1:
                        seq = seq[1:]
                    else:
                        seq[0][0] = '_'
                    if seq != []:
                        newProjDB.append(seq)
                # elif pattern < sequence[pos]:
                #     count += int(flag)
                #     print sequence
                #     seq = sequence[pos:]
                #     seq[0] = seq[0][idx:]
                #     if len(seq[0]) == 1:
                #         seq = seq[1:]
                #     else:
                #         seq[0][0] = '_'
                #     if seq != []:
                #         newProjDB.append(seq)             
        if count >= min_sup:
            pattern.append([item])
            output_Patterns.append((pattern,count,newProjDB))   
            # # output_Patterns[l].append(([pattern,[item]],count,newProjDB))    
            # print output_Patterns[l]        
        # prefixSpan()
        
    return output_Patterns           
	    



def main():
    MIS = {}    # MIS Value
    SDC = 0.0    # Support DifferenceConstraint
    SequenceDataset = []    # Sequence Dataset
    SplitLine =  "***************************"


    " Data Initilization "
    MIS, SDC = util.readMISFile("paraTest.txt", MIS, SDC)
    print "MIS = " + str(MIS)
    print "SDC = " + str(SDC)
    SequenceDataset = util.readDataFile('dataTest.txt',SequenceDataset)
    print "SequenceDataset = " + str(SequenceDataset)
    M = util.sort(MIS)
    print "M = " + str(M)
    n = len(SequenceDataset)
    
    "Length-1 seqential patterns"
    L1Patterns = gen_l1patterns(SequenceDataset,M,2)
    FreqItems = []
    F = []
    for item in L1Patterns:
        (a,b,c) = item
        FreqItems.append(a)
        F.append(a[0])
        
    
    # outputSeqPatterns=[]
    # for (item,count) in L1Patterns:
    #     outputSeqPatterns.append(prefixSpan(item,1,projDB,M,min_sup))
    # L1Patterns = prefixSpan([],0,SequenceDataset,M,2)
    print "Length-1 Sequential Patterns: \n" +str(L1Patterns)
    print F
    print SplitLine
    
    output_Patterns = []
    for (pattern,count,projDB) in L1Patterns:
        print pattern,count,projDB
        output_Patterns.append(prefixSpan(pattern,1,projDB,F,2))
    print output_Patterns
    output_Patterns.append(prefixSpan([[30], [40]],1,[[['_', 70]], [['_', 70, 80], [90]]],F,2))
    print output_Patterns

if __name__ == "__main__":
    main()	    
	