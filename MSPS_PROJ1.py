import re
import operator

dir_home = "F:\\Course\\CS583\\PROJ1\\testbuild\\"
dir_dt = "C:\\RAYMON\\CS583\\project1\\testbuild\\"
datafile = dir_dt+"data.txt"
paramfile = dir_dt+"para.txt"
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
    #for seq in db:
    #    print seq
    #print len(db)
    checkParams(paramfile,mis,val)
    #for miss,misss in mis.items():
    #    print miss, '\t',misss
    #print val[0]
    sdc = val[0]
    #print sdc
    #print mis[10]
    pickFrequentItem(db,sup)
    #print sup[48]
    #for item in sup.items():
    #    print item

    #numItems = len(sup)
    #print dbSize
    #print numItems

    #ascendFrequentItemSet = sorted(frequentItemSet.iteritems(), key=operator.itemgetter(0))
    #ascendMIS = sorted(mis.iteritems(), key=operator.itemgetter(1))
    #print ascendFrequentItemSet
    #print ascendMIS

    a = [[33, 37], [49], [17, 22, 34, 44], [22, 31, 37, 45]]
    b = [[33],[22,34]]
    print a
    print b
    output = []
    #print projection(a,b)
    #print checkSubList([9],[49,9])
    #print '\n\n\n\n\n\n'
    print modifiedCheckPrefix(a,b,output)
    print output
    print projection(a,b)

    #a=[1,2,3,4,5,6,7,8]
    #b=[4,5,6,8]
    #print checkSubList(a,b)
    
    #print 'a= ',a
    #print filteredSeqBySDC(a,sup,37,sdc,len(db))
    #print removeItemFromSequence(a,38)
    #print diffItemsInSequence(a)
    
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
            mmm = map(int,mm) #convert the strings into integers
            itemset.append(mmm) #store the numbers
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
            ii = map(int,i)
            #print ii[0]
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
def pickFrequentItem(db,sup):
    for index in range(1,49+1):
        for seq in db:
            for itemset in seq:
                if itemset.count(index)>0:
                    if sup.has_key(index):
                        sup[index]=sup[index]+1
                    else:
                        sup.setdefault(index,1)
                    break
    #numItems = len(sup)   #this won't work for the external variables(immutable) outside def.
    #print 'in pfi: ', numItems
    for index in sup:
        #print sup[index]/float(len(sup)), ' ',  mis[index-1]
        if sup[index]/float(len(sup)) >= mis[index]:
            frequentItemSet.setdefault(index,sup[index])
    
    ascendMIS = sorted(mis.iteritems(), key=operator.itemgetter(1))
    #print ascendMIS
    for item in ascendMIS:
        if frequentItemSet.has_key(item[0]):
            ascendFrequentItemSet.setdefault(item[0], (ascendMIS[item[0]-1][1],sup[item[0]]))
            
    #for index,val in frequentItemSet.items():
    #    print index, ' ', val
        
def removeItemFromSequence(seq,val):
    ret = []
    for itemset in seq:
        output = []
        for item in itemset:
            if item != val:
                output.append(item)
        if len(output)>0:
            ret.append(output)
    return ret

def diffItemsInSequence(seq):   
    ret = []
    for itemset in seq:
        for item in itemset:
            if ret.count(item) == 0:
                ret.append(item)
    return ret

#items-output of diffItemsInSequence(..)
def filteredSeqBySDC(seq,sup,val,v_sdc,v_dbsize): #Sk
    ret = seq
    items = diffItemsInSequence(seq)
    #print 'diff items: ',items
    if items.count(val)<=0:
        print 'error in filteredSeqBySDC! - val is not contained in the seq'
    for item in items:
        if item != val:
            #print 'item: ',item,' val: ',val,' abs: ',abs(sup[item]-sup[val])
            if abs(sup[item]-sup[val])>v_sdc*float(v_dbsize):
                ret = removeItemFromSequence(ret,item)
    return ret

def checkPrefix(seq,prefix):
    if cmp(seq[:len(prefix)-1],prefix[:len(prefix)-1])==0:
        if cmp(prefix[-1], seq[len(prefix)-1][:len(prefix[-1])])==0:
            for item in prefix[-1]:
                for i in seq[len(prefix)-1][len(prefix[-1]):]:
                    if item>i:
                        return False
            return True
    return False

# according to the weird description from MS-PS algorithm paper
# the elements of prefix can be dispersed in each element of the sequence
# store a list [seq index, item index] in output for the last prefix element index
# index starts from 0
def modifiedCheckPrefix(seq, p,output):
    curElem = 0
    for itemset in p:
        #print 'search for new itemset: ',itemset
        for i in range(curElem,len(seq)):
            #print 'seq[',i,']:',seq[i],'itemset: ',itemset, 'result: ', checkSubList(seq[i],itemset)
            checkResult = checkSubList(seq[i],itemset)
            if checkResult>=0:
                if cmp(itemset,p[-1])==0:
                    output.append(i)
                    output.append(checkResult)
                    #print 'reach the last prefix element, return true'
                    return True
                else:
                    #print 'match found, continue the match for the next prefix element'
                    curElem = i+1
                    break
            elif len(itemset)!=0 and i==len(seq)-1:
                return False
            #print 'search in current sequence element failed, try next sequence element'
    return False

# l: list,  itemset: pattern to be found.
# neither contains sublists
# return the index start from 0
def checkSubList(l, itemset):
    if(len(itemset)==0 or len(itemset)>len(l)):
        return -1
    for i in range(0,len(l)):
        if l[i]==itemset[0]:
            if(len(itemset)==1):
                return i
            for j in range(1,len(itemset)):
                if l[i+j]!=itemset[j]:
                    return -1
                elif j==len(itemset)-1:
                    return i+j
    return -1

def projection(seq, prefix):
    index = []
    if modifiedCheckPrefix(seq,prefix,index) == True:
        if cmp(prefix[-1], seq[index[0]])==0:
            return seq[index[0]+1:]
        else:
            ret = seq[index[0]+1:]
            addItemset = seq[index[0]][index[1]+1:]
            addItemset.insert(0,'_')
            ret.insert(0,addItemset)
            return ret
    else:
        print 'Abort - ', prefix, ' is not a prefix of ', seq


            
if __name__ == "__main__":
    main()

    

