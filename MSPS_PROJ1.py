import re

datafile = "F:\\Course\\CS583\\PROJ1\\testbuild\\data.txt"
paramfile = "F:\\Course\\CS583\\PROJ1\\testbuild\\para.txt"
db = []
mis = []
sdc = []

def main():
    checkSequence(datafile,db)
    #print db
    #for seq in db:
    #    print seq
    #print len(db)
    checkParams(paramfile,mis,sdc)
    print mis
    print sdc[0]
    
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
            
if __name__ == "__main__":
    main()

    

