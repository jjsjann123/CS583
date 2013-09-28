import re
import operator
from types import *

dir_home = "F:\\Course\\CS583\\PROJ1\\testbuild\\"
dir_dt = "C:\\RAYMON\\CS583\\project1\\testbuild\\"
datafile = dir_home+"data.txt"
paramfile = dir_home+"para.txt"
db = []
dbSize = 0
numItems = 0
mis = {}
sdc = 0.0
sup = {}
frequentItemSet = {}        #ordered by index - format- "index:sup"
ascendFrequentItemSet = {}  # {(index, (MIS, sup))...}, ascend by MIS

def main():
    val = []
    checkSequence(datafile,db)
    dbSize = len(db)
    #print db
    for seq in db:
        print seq
    print  'db size: ' ,len(db)
    checkParams(paramfile,mis,val)
    print 'MIS: ',mis
    #for miss,misss in mis.items():
    #    print miss, '\t',misss
    #print val[0]
    sdc = val[0]
    numItems = len(mis)
    print 'number of items: ',numItems
    print 'SDC: ',sdc
    #print mis[10]
    
    ascendFrequentItemSet = pickFrequentItem(db,sup,numItems)
    print 'Sup: '
    print sup
    print 'ascendFrequentItemSet: '
    print ascendFrequentItemSet
    
    #print sup[48]
    #for item in sup.items():
    #    print item

    #print dbSize
    #print numItems

    


    #ascendFrequentItemSet = sorted(frequentItemSet.iteritems(), key=operator.itemgetter(0))
    #ascendMIS = sorted(mis.iteritems(), key=operator.itemgetter(1))
    #print ascendFrequentItemSet
    #print ascendMIS

    a = [['49'], ['_26', '37', '34', '44'], ['22', '_26', '37', '45'],['42', '32', '_26', '37']]
    b = [['22','34']]

    c= [a,b]
    #print a
    #print b
    #print c

    #print isNumber('_')
    #print eval('3')
    #print findAllPatterns(c)
    #print modifiedFindAllPatterns(c,0.05)
    
    output = []
    #print projection(a,b)
    #print checkSubList([9],[49,9])
    #print '\n\n\n\n\n\n'
    #print modifiedCheckPrefix(a,b,output)
    #print output
    #print projection(a,b)

    #a=[1,2,3,4,5,6,7,8]
    #b=[4,5,6,8]
    #print checkSubList(a,b)
    
    #print 'a= ',a
    #print filteredSeqBySDC(db,sup,'37',sdc,dbSize)
    #print filteredDBBySDC(db,sup,'1',sdc,dbSize)
    #print removeItemFromSequence(a,'_26')
    #print diffItemsInSequence(a)
    for item in removeItemFromDB(db,'48'):
        print item
    #print diffItemsInDB(db)
    
#error check TBD
#...
def checkSequence(filename, db):
    metadata = file(filename)
    lines = metadata.readlines()
    for sline in lines:
        itemset = []
        sline = sline.replace('\n','')
        sline = sline.replace(' ', '')
        #print sline
        m = re.findall(r'{(.*?)}',sline) #find all the itemsets in "{}" as string
        for mm in m:
            mm = re.findall(r'(\d+),*',mm) #find all the item strings of numbers in one itemset
            itemset.append(map(str,mm)) #store the numbers
        db.append(itemset)

#error check TBD:
#1. if #sdc>1
#2. if elements & mis's sizes cannot match
#3. invalid number for mis & sdc
#...
def checkParams(filename, mis, sdc):
    SDC_flag = False
    metadata = file(filename)
    lines = metadata.readlines()
    for sline in lines:
        
        sline = sline.replace('\n','')
        sline = sline.replace(' ', '')
        #print sline
        m = re.findall(r'\d*.\d*$',sline)
        #if m.isdigit():
        #    print m
        if re.findall(r'^MIS',sline):
            i = re.findall(r'^MIS\((\d*)\)',sline)
            ii = map(str,i)
            mm = map(float,m)
            #mis.append(mm[0])
            mis.setdefault(ii[0],mm[0])
        elif SDC_flag==False and re.findall(r'^SDC',sline):
            SDC_flag=True
            #print m
            mm =  map(float,m)
            sdc.append( mm[0] )

#error check TBD:
#range should be modified for new test cases
#2. mis might need to be a dict, in case the element is not consecutive ones
def pickFrequentItem(db,sup, ni, mis):
    #print ni
    #print mis
    for index in range(1,ni+1):
        for seq in db:
            for itemset in seq:
                if itemset.count(str(index))>0:
                    if sup.has_key(str(index)):
                        sup[str(index)]=sup[str(index)]+1
                    else:
                        sup.setdefault(str(index),1)
                    break

    for index in sup:
        #print sup[index]/float(len(sup)), ' ',  mis[index]
        if sup[index]/float(len(sup)) >= mis[index]:
            frequentItemSet.setdefault(index,sup[index])
    
    ascendMIS = sorted(mis.iteritems(), key=operator.itemgetter(1))
    ret = []
    for item in ascendMIS:
        #print 'in ascendMIS ',item
        if frequentItemSet.has_key(item[0]):
            #print item[0]
            #ret.setdefault( item[0], ( item[1],sup[item[0]] ) )
            ret.append(item[0])
    return ret

# remove the all single item = value in sequence
##def removeItemFromSequence(seq,val):
##    ret = []
##    for itemset in seq:
##        output = []
##        for item in itemset:
##            if item != val:
##                output.append(item)
##        if len(output)>0:
##            ret.append(output)
##    return ret

# remove the all single item = value in sequence
# the null sequence won't be added.
def removeItemFromDB(db,val):
    ret = []
    for seq in db:
        outputs = []
        for itemset in seq:
            output = []
            for item in itemset:
                if item != val:
                    output.append(item)
            if len(output)>0:
                outputs.append(output)
        if len(outputs)>0:
            ret.append(outputs)
    return ret

# seq: [[,,],[,,]]
##def diffItemsInSequence(seq):   
##    ret = []
##    for itemset in seq:
##        for item in itemset:
##            if ret.count(item) == 0:
##                ret.append(item)
##    return ret

def diffItemsInDB(db):   
    ret = []
    for seq in db:
        for itemset in seq:
            for item in itemset:
                if ret.count(item) == 0:
                    ret.append(item)
    return ret

#items-output of diffItemsInSequence(..)
##def filteredSeqBySDC(seq,sup,val,v_sdc,v_dbsize): #Sk
##    ret = seq
##    items = diffItemsInSequence(seq)
##    print 'diff items: ',items
##    if items.count(val)<=0:
##        print 'error in filteredSeqBySDC! - val is not contained in the seq'
##    for item in items:
##        if item != val:
##            print 'item: ',item,' val: ',val,' abs: ',abs(sup[item]-sup[val])
##            if abs(sup[item]-sup[val])>v_sdc*float(v_dbsize):
##                ret = removeItemFromSequence(ret,item)
##    return ret

def filteredDBBySDC(db,sup,val,v_sdc,v_dbsize): #Sk
    #print 'filterDBBySDC- THRESHOLD: ',v_sdc*float(v_dbsize)
    ret = db
    items = diffItemsInDB(db)
    #print 'diff items: ',items
    if items.count(val)<=0:
        print 'error in filteredSeqBySDC! - val is not contained in the seq'
    for item in items:
        
        if item != val:
            #print 'item: ',item,' val: ',val,' abs: ','item Sup: ',sup[item], ' with ',sup[val], 'margin: ',abs(sup[item]-sup[val])
            if abs(sup[item]-sup[val])>v_sdc*float(v_dbsize):
                ret = removeItemFromDB(ret,item)
    return ret

#def checkPrefix(seq,prefix):
#    if cmp(seq[:len(prefix)-1],prefix[:len(prefix)-1])==0:
#        if cmp(prefix[-1], seq[len(prefix)-1][:len(prefix[-1])])==0:
#            for item in prefix[-1]:
#                for i in seq[len(prefix)-1][len(prefix[-1]):]:
#                    if item>i:
#                        return False
#            return True
#    return False

# according to the weird description from MS-PS algorithm paper
# the elements of prefix can be dispersed in each element of the sequence
# edit: find a subsequence in the sequence that has the prefix of alpha, since it s already
# lexicographically sorted, the suffix should fine w/o the em-em' check
# store a list [seq index, item index] in output for the last prefix element index
# index starts from 0
##def modifiedCheckPrefix(seq, p,output):
##    curElem = 0
##    for itemset in p:
##        #print 'search for new itemset: ',itemset
##        for i in range(curElem,len(seq)):
##            #print 'seq[',i,']:',seq[i],'itemset: ',itemset, 'result: ', checkSubList(seq[i],itemset)
##            checkResult = checkSubList(seq[i],itemset)
##            if checkResult>=0:
##                if cmp(itemset,p[-1])==0:
##                    output.append(i)
##                    output.append(checkResult)
##                    #print 'reach the last prefix element, return true'
##                    return True
##                else:
##                    #print 'match found, continue the match for the next prefix element'
##                    curElem = i+1
##                    break
##            elif len(itemset)!=0 and i==len(seq)-1:
##                return False
##            #print 'search in current sequence element failed, try next sequence element'
##    return False

# l: list,  itemset: pattern to be found.
# neither contains sublists
# return the index start from 0
#def checkSubList(l, itemset):
#    if(len(itemset)==0 or len(itemset)>len(l)):
#        return -1
#    for i in range(0,len(l)):
#        if l[i]==itemset[0]:
#            if(len(itemset)==1):
#                return i
#            for j in range(1,len(itemset)):
#                if l[i+j]!=itemset[j]:
#                    return -1
#                elif j==len(itemset)-1:
#                    return i+j
#    return -1

# p only has two formats '#' or '_#'
##def checkSinglePrefix(seq,p,output):
##    if isNumber(p):
##        return True
##    else:
##        return False
    

##def projection(seq, prefix):
##    index = []
##    if modifiedCheckPrefix(seq,prefix,index) == True:
##        if cmp(prefix[-1], seq[index[0]])==0:
##            return seq[index[0]+1:]
##        else:
##            ret = seq[index[0]+1:]
##            addItemset = seq[index[0]][index[1]+1:]
##            addItemset.insert(0,'_')
##            ret.insert(0,addItemset)
##            return ret
##    else:
##        #exception might be needed
##        print 'Abort - ', prefix, ' is not a prefix of the sub-sequence', seq
##        #to be tested
##        return []

#find all 1-length patterns in projected database[ [[]..], [[]..], [[]..] ]
#OUT OF DATE!!! DON'T USE THIS ONE!!
##def findAllPatterns(pdb, minsup=0.0):
##    ap = []
##    #threshold = minsup*len(pdb)
##    threshold = minsup*len(db)
##    #print pdb
##    #print len(pdb)
##    #print threshold
##    counterDict = {} # list : sup
##    for s in pdb: #sequence
##        for l in s: #list
##            for i in l: #item
##                if isNumber(i):
##                    p1 = str(i)
##                    if l.index(i)>0 and l[l.index(i)-1]=='_':
##                        p1 = '_'+p1 #complex pattern  "_a"
##
##                    if counterDict.has_key(str(p1)):
##                        counterDict[p1] = counterDict[p1]+1
##                    else:
##                        counterDict.setdefault(p1,1)
##    for string,n in counterDict.iteritems():
##        #print string,' ',n
##        if n>=threshold:
##            ap.append(string)
##			                
##    return ap

#find all 1-length patterns in projected database[ [[]..], [[]..], [[]..] ]
def modifiedFindAllPatterns(pdb, minsup=0.0):
    ap = []
    #threshold = minsup*len(pdb)
    threshold = minsup*len(db)
    #print pdb
    #print len(pdb)
    #print threshold
    counterDict = {} # list : sup
    for s in pdb: #sequence
        for l in s: #list
            for i in l: #item
                if counterDict.has_key(i):
                        counterDict[i] = counterDict[i]+1
                else:
                     counterDict.setdefault(i,1)
    for string,n in counterDict.iteritems():
       # print string,' ',n
        if n>=threshold:
            ap.append(string)
			                
    return ap

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    main()

    

