from MSPS_PROJ1 import *

#################################################################
#
#	Testing code
#
#################################################################	
def pp( q ):
	for t in q:
		print t
a = [['a'], ['b', 'c', 'f', 'e'], ['a', 'b', 'f', 'd'],['d', 'g', 'q', 'z']]
b = [['b', 'f'], ['a']]
c = [a,b]

def recursive(q):
	if ( q < 10 ):
		q+=1
		recursive(q)
		print q

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

def pickFrequentItem(db,sup, ni, mis):
    #print ni
    #print mis
	countREM = {}
	frequentItemSet = {}
	for i in mis:
		sup.update( {i: 0})
		countREM.update( {i: False} )
			
	for seq in db:
		print seq
		for itemset in seq:
			for item in itemset:
				countREM[item] = True
		print "flagAdded ", countREM
		for i in countREM:
			if countREM[i] == True:
				countREM[i] = False
				sup[i] += 1
		print sup
		print "flagCleared ", countREM

	for index in sup:
		if sup[index]/float(len(db)) >= mis[index]:
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



#################################################################
#
#	Merge the postFix sequence list to the prefix item i.
#
#	Note: postFix could be starting with '_a' or 'a'
#
#################################################################
def merge_item_to_sequence_front( i, seq):
	if ( seq == [] ):
		seq.append([i])
	elif ( seq[0][0][0] == '_' ):
		seq[0][0] = seq[0][0][1:]
		seq[0].insert(0, i)
	else:
		seq.insert(0,[i])
	return seq
	
def merge_item_to_sequence_front_list( i, seq_list):
	ret = []
	if (seq_list == [] ):
		ret.append([[i]])
	else:
		for seq in seq_list:
			ret.append(merge_item_to_sequence( i, seq))
	return ret

def merge_item_to_sequence_end( i, seq):
	if ( seq == None ):
		q= [[i]]
	elif ( i[0] == '_' ):
		i = i[1:]
		q = []
		#q = seq[:]
		#Note: Fucking python treat everything as reference!
		for itemset in seq:
			q.append(itemset[:])
		q[len(q)-1].append(i)
	else:
		q = []
		for itemset in seq:
			q.append(itemset[:])
		q.append([i])
	return q
	
def merge_item_to_sequence_end_list( i, seq_list):
	ret = []
	if (seq_list == [] ):
		ret.append([[i]])
	else:
		for seq in seq_list:
			ret.append(merge_item_to_sequence_end( i, seq))
	return ret

#################################################################
#
#	Removes all item i in sequence Database
#
#################################################################
def shrink( db, i ):
	q = []
	for sequence in db:
		q.append(removeItemFromSequence( sequence, i ))
	return q

#################################################################
#
#	Removes all sequence in sequence list that does not contain:
#
#					ik
#
#################################################################
def findItemInSeq(seq, i):
	if ( seq == [] ):
		return False
	else:
		for itemset in seq:
			for item in itemset:
				if (item == i):
					return True
	return False

def exclude(db, ik):
	ret = []
	for seq in db:
		if (findItemInSeq(seq, ik)):
			ret.append(seq)
	return ret
#################################################################
#
#	Projection
#
#################################################################
def single_prefix_projection(db, prefix):
	ret = []
	for sequence in db:
		foundFlag = 0
		projectedSequence = []
		for itemset in sequence:
			if(foundFlag != 0):
				projectedSequence.append(itemset)
				continue
			for item in itemset:
				if (foundFlag == 2):
					firstItemSet.append(item)	
				if (foundFlag == 1):
					foundFlag = 2
					firstItemSet = [ '_' + item ]
				if (item == prefix):
					foundFlag = 1
			if (foundFlag == 2):
				projectedSequence.append(firstItemSet)

		if (projectedSequence != [] ):
			ret.append(projectedSequence)

	return ret
#################################################################
#
#	restricted PrefixSpan, This is the Function that should be called.
#
#	returns all the frequent item sets without sort.
#
#################################################################
def r_PrefixSpan( Sk, mis, sdc, numItems):
	sup = {}
	freqItemDic = pickFrequentItem(Sk, sup, numItems, mis)
	print "dic", freqItemDic
	totalLenth = len(Sk)
	output = []
	for ik in freqItemDic:
		if (True):
			#	remove all item that has exceeds the support difference coverage
			newSk = filteredDBBySDC( Sk, sup, ik, sdc, totalLenth)
			#	remove all sequence that does not contain ik
			newSk = exclude(newSk, ik)
			print ik , " Sk:"
			pp( newSk )
			ret = PrefixSpan( None, newSk, mis[ik]*totalLenth, 0)
			
			print ik, "*******"
			print ret
			#Kick out frequent sequence without ik
			ret = exclude(ret, ik)
			output += ret
			
			#Shrink Sequence Database
			#Sk = shrink( Sk, ik )
			Sk = removeItemFromDB(Sk, ik)
		
	return output
#################################################################
#
#	PrefixSpan. 
#
#################################################################	
def PrefixSpan( item, Sk, sup, iter):
	ret = []
	iter += 1
	testFlag = False
	#print "for ", item,  ":"
	if ( len(Sk) >= sup):
		freItemList = modifiedFindAllPatterns(Sk, sup)
		#print freItemList
		pp(Sk)
		if ( len(freItemList) != 0):
			for next in freItemList:
				newPrefix = merge_item_to_sequence_end( next, item )
				print "!!!!!!!" , id(newPrefix)
				print "??????", id(item), item
				print "now prefix: " , newPrefix, " at: " , iter
				ret.append( newPrefix )
				if ( newPrefix == [['2']] ):
					print "###############***********"
					print "return " , ret
				#print "return ", ret
				SubSk = single_prefix_projection( Sk, next )
				if ( newPrefix == [['2']] ):
					print "####################*****"
					print "return " , ret
				newSeq = []
				if ( newPrefix == [['2']] ):
					print "####**********####****"
					print "return " , ret
					testFlag = True
				newSeq = PrefixSpan( newPrefix, SubSk, sup, iter)
				if ( testFlag ):
					print "####**************"
					print " prefix: ", newPrefix
					print "return " , ret
				#ret = ret + merge_item_to_sequence_list( next, postSeq ) 
				ret = ret + newSeq
				if ( testFlag ):
					print "#########################"
					print "return " , ret
				testFlag = False
					# # print "add: ", postSeq, " after: " , next
					# ret = ret + merge_item_to_sequence_list( next, postSeq ) 
					# # print "res: ", ret
				# else:
					# print "return ", ret
					# print "return value: ", postSeq
					# ret = postSeq
		else:
			print "return itself cause no freqItemfound"
			#ret = [[[item]]]
	else:
		print "return itself cause length < sup"
		#ret = [[[item]]]
	return ret
	
#################################################################
#
#	Testing code
#
#################################################################	
		

dataDir="./testbuild/"
datafile = dataDir+'data2.txt'
paramfile = dataDir+'para2.txt'

db = []
dbSize = 0
numItems = 0
mis = {}
sdc = 0.0
sup = {}
val = []
frequentItemSet = {}        #ordered by index - format- "index:sup"
ascendFrequentItemSet = {}  # {(index, (MIS, sup))...}, ascend by MIS

checkSequence(datafile,db)
dbSize = len(db)
checkParams(paramfile,mis,val)
sdc = val[0]
numItems = len(mis)

#output = r_PrefixSpan( db, mis, sdc, numItems)

