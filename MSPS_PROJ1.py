import re
import operator

datafile = "F:\\Course\\CS583\\PROJ1\\testbuild\\data.txt"
paramfile = "F:\\Course\\CS583\\PROJ1\\testbuild\\para.txt"
db = []
dbSize = 0
numItems = 0
mis = {}
sdc = 0.0
sup = {}
frequentItemSet = {}
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
    #for item in sup.values():
    #    print item
    numItems = len(sup)
    #print dbSize
    #print numItems

    #ascendFrequentItemSet = sorted(frequentItemSet.iteritems(), key=operator.itemgetter(0))
    #ascendMIS = sorted(mis.iteritems(), key=operator.itemgetter(1))
    print ascendFrequentItemSet
    #print ascendMIS
    
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
        



            
if __name__ == "__main__":
    main()

    

