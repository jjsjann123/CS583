import re

datafile = "C:\\RAYMON\\data.txt"
db = []

def main():
    checkSequence(datafile,db)
    for seq in db:
        print seq
    print len(db)

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

if __name__ == "__main__":
    main()

    

