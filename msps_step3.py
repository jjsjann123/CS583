import MSPS_PROJ1

#################################################################
#
#	Merge the postFix sequence list to the prefix item i.
#
#	Note: postFix could be starting with '_a' or 'a'
#
#################################################################
def merge_item_to_sequence( i, seq):
	if ( seq == [] ):
		set.append([i])
	elif ( seq[0][0][0] == '_' ):
		seq[0][0] = seq[0][0][1]
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
def r_PrefixSpan( Sk, sup):
	freqItemDic = pickFrequentItem(Sk, sup)
	output = []
	for ik in freqItemDic:
		ret = PrefixSpan( None, Sk, freqItemDic[i][1])
		
		#Kick out frequent sequence without ik
		ret = exclude( ret, ik )
		output.append(ret)
		
		#Shrink Sequence Database
		Sk = shrink( Sk, ik )
		
	return output
#################################################################
#
#	PrefixSpan. 
#
#################################################################	
def PrefixSpan( i, Sk, sup ):
	ret = []
	if ( len(Sk) >= sup):
		freItemList = findAllPatterns(Sk, sup)
		if ( len(freItemList) != 0):
			for next in freItemList:
				SubSk = single_prefix_projection( Sk, next )
				postSeq = PrefixSpan( next, SubSk, sup )
				if ( i != None ):
					ret.append( merge_item_to_sequence_list( i, postSeq ) )
				else:
					ret = postSeq			
	return ret
	
a = [['a'], ['b', 'c', 'f', 'e'], ['a', 'b', 'f', 'd'],['d', 'g', 'q', 'z']]
b = [['b', 'f'], ['a']]
c = [a,b]
