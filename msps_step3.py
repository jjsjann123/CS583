from MSPS_PROJ1 import *

#################################################################
#
#	Merge the postFix sequence list to the prefix item i.
#
#	Note: postFix could be starting with '_a' or 'a'
#
#################################################################
def merge_item_to_sequence( i, seq):
	if ( seq == [] ):
		seq.append([i])
	elif ( seq[0][0][0] == '_' ):
		seq[0][0] = seq[0][0][1:]
		seq[0].insert(0, i)
	else:
		seq.insert(0,[i])
	return seq
	
def merge_item_to_sequence_list( i, seq_list):
	ret = []
	if (seq_list == [] ):
		ret.append([[i]])
	else:
		for seq in seq_list:
			ret.append(merge_item_to_sequence( i, seq))
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
	totalLenth = len(Sk)
	output = []
	for ik in freqItemDic:
		if (ik == '1'):
			#	remove all item that has exceeds the support difference coverage
			newSk = filteredDBBySDC( Sk, sup, ik, sdc, totalLenth )
			#	remove all sequence that does not contain ik
			#newSk = exclude(newSk, ik)
			print ik , " Sk:"
			print newSk
			ret = PrefixSpan( None, newSk, mis[ik]*totalLenth)
			
			#Kick out frequent sequence without ik
			ret = exclude(ret, ik)
			output.append(ret)
			
			#Shrink Sequence Database
			#Sk = shrink( Sk, ik )
			Sk = removeItemFromDB(Sk, ik)
			
	return output
#################################################################
#
#	PrefixSpan. 
#
#################################################################	
def PrefixSpan( item, Sk, sup ):
	ret = []
	if ( len(Sk) >= sup):
		freItemList = modifiedFindAllPatterns(Sk, sup)
		print "for ", item,  ":"
		print freItemList
		print Sk
		if ( len(freItemList) != 0):
			for next in freItemList:
				SubSk = single_prefix_projection( Sk, next )
				postSeq = PrefixSpan( next, SubSk, sup )
				if ( item != None ):
					#print "add: ", postSeq, " after: " , next
					ret = ret + merge_item_to_sequence_list( next, postSeq ) 
					#print "res: ", ret
				else:
					ret = postSeq
		else:
			ret = [[[item]]]
	else:
		ret = [[[item]]]
	return ret
	
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

		

dataDir="./testbuild/"
datafile = dataDir+'data.txt'
paramfile = dataDir+'para.txt'

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

