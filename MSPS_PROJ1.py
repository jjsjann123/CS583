import re

datafile = "F:\\Course\\CS583\\PROJ1\\testbuild\\data.txt"
paramfile = "F:\\Course\\CS583\\PROJ1\\testbuild\\para.txt"
db = []
mis = []
sdc = 0.0
sup = {}
frequentItemSet = {}

def main():
    val = []
    checkSequence(datafile,db)
    #print db
    #for seq in db:
    #    print seq
    #print len(db)
    checkParams(paramfile,mis,val)
    #for miss in mis:
    #    print miss
    #print val[0]
    sdc = val[0]
    #print sdc
    #print mis[10]
    pickFrequentItem(db,sup)
    #for item in sup.values():
    #    print item
    
    
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
            mm = map(float,m)
            mis.append(mm[0])
        elif SDC_flag==False and re.findall(r'^SDC',sline):
            SDC_flag=True
            #print m
            mm =  map(float,m)
            sdc.append( mm[0] )

#error check: range should be modified for new test cases
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
    for index in sup:
        print sup[index]/float(len(sup)), ' ',  mis[index-1]
        if sup[index]/float(len(sup)) >= mis[index-1]:
            frequentItemSet.setdefault(index,sup[index])
    
    print frequentItemSet
        



            
if __name__ == "__main__":
    main()

    

