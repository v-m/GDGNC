#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
# K-S Statistics reimplementation
# Date: 2014-05-14
#####################################################################################################


from scipy.stats import ks_2samp
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
import math

ALPHA010 = [0.1, 1.22]
ALPHA005 = [0.05, 1.36]
ALPHA0025 = [0.025, 1.48]
ALPHA001 = [0.01, 1.63]
ALPHA0005 = [0.005, 1.73]
ALPHA0001 = [0.001, 1.95]

def ks(x, y, Int = False):
	nb = 1000
	
	if len(y) < len(x):
		return (ksStat(x, y, Int)[0], ksPvalue(x, y, nb, Int))
	else:
		return (ksStat(y, x, Int)[0], ksPvalue(y, x, nb, Int))


def calculateCriticalValue(sample1, sample2, alpha):
	n1 = 1.0 * len(sample1)
	n2 = 1.0 * len(sample2)
	
	return alpha * math.sqrt((n1 + n2) / (n1*n2))

# Deprecated --- not used anymore
def extractNPointsOn(data, n):
	retList = []
	
	if(n > len(data)):
		return None
	
	random.seed()
	while(len(retList) < n):
		nxt = random.randint(0, len(data) - 1)
	
		if nxt not in retList:
			retList.append(nxt)
		
	retList.sort()
	
	for i in range(len(retList)):
		retList[i] = data[retList[i]]
		
	return retList

'''
def generatePointsAccordingTo(data, nb ,startat, step):
	generated = []
	
	for i in range(nb):
		rndval = random.random()
		i = 0
		
		while rndval >= data[i]:
			i = i + 1
		
		#val = startat + step * (i * 1.0)
		if len(generated) < i + 1:
			while len(generated) < i:
				generated.append(0)
			generated.append(1)
		else:
			generated[i] = generated[i] + 1
		
	return generated
'''

# This function simulate the p-value process.
def ksPvalue(x, y, N = 1000, Int = False):
	pos = 0
	neg = 0
	
	ksstat = ksStat(x, y, Int)
	startat = ksstat[1]
	step = ksstat[2]
	ksstat = ksstat[0]
	xcumul = toDistribCumulativeForKs(x, startat, step)
	
	
	for i in range(N):
		
		#echsize = int(1 * len(x))
		#echsize = len(x)
		echsize = sum(x)
				
		#xbis = generatePointsAccordingTo(xcumul, echsize, startat, step)
		xbis = generateAccordingTo(x, echsize)
		
		ksstatbis = ksStat(x, xbis, Int)[0]
		
		if ksstatbis >= ksstat:
			pos = pos + 1
		else:
			neg = neg + 1
	
	#print "pos/neg # = %d/%d"%(pos, neg)
	return  pos/(N * 1.0)

# This function calculate the k-s statistic value between two empirical distributions
def ksStat(x, y, Int = False):
	# This function search the maximum value of all distances for all points
	#maxval = -1
	
	ctndistrib = []
	
	# We search the minimum x-axis value for searching
	startat = min(x) if min(x) < min(y) else min(y)
	if Int:
		step = 1
	else:
		step = 1.0 / len(x) if 1.0 / len(x) < 1.0 / len(y) else 1.0 / len(y)
	
	# Then we generate the Empirical distribution function for both distributions
	xdta = toDistribCumulativeForKs(x, startat, step)
	ydta = toDistribCumulativeForKs(y, startat, step)
	
	# Once we have two EDF we search for the shortest item in which we'll search
	# this step is needed to avoid an index out of bound in lists
	left = ydta if len(xdta) > len(ydta) else xdta
	right = ydta if left == xdta else xdta
	
	# We then iterate through all items on each list determining the distance for each
	# At each iteration, we keep the value only if this value is the greatest
	for i in range(len(left)):
		tmpval = abs(xdta[i] - ydta[i])
		ctndistrib.append(tmpval)
		
		#if tmpval > maxval:
		#	maxval = tmpval
		
	return (max(ctndistrib), startat, step, ctndistrib)

def toDistribForKs(data, startat = None, step = None):
	distribs = []
	
	# We set n to the number of items in the dataset
	n = len(data)
	# We set the step for ranging to 1/n
	if step is None:
		inc = 1.0 / n
	else:
		inc = step * 1.0
	
	if startat is None:
		curcpt = min(data)
	else:
		curcpt = startat
	
	# We copy the list in order to sort it and explore it efficiently
	rdata = list(copy.deepcopy(data))
	rdata.sort()
	
	# We initialize a counter to count how many items has been discovered.
	cpt = 0
	# We'll loop until we find all items
	while cpt != n:
		# For each jump step, we count how many items in the dataset is <= to this new jump value
		while len(rdata) > 0 and rdata[0] <= curcpt:
			cpt = cpt + 1
			rdata.pop(0)
				
		# We do not forget to divide the count value by n
		distribs.append(cpt)
		# Jump to next step :-)
		curcpt = curcpt + inc
	
	return distribs

# This function build an Empirical distribution function for a dataset
# As this EDF is inteded to be compared against an other one, the starting point should be determined here.
# If ignored, the smallest value of this distribution will be taken
def toDistribCumulativeForKs(data, startat = None, step = None):
	n = len(data) * 1.0
	
	distribs =  toDistribForKs(data, startat, step)
	
	for i in range(len(distribs)):
		distribs[i] = distribs[i] / n
		
	return distribs


def normalizeY(data):
	ndata = []
	mx = sum(data)
	for i in range(len(data)):
		ndata.append(data[i] / (mx * 1.0))
	
	return ndata

def toCumulative(data):
	cptr = 0.0
	ndata = []
	
	for i in range(len(data)):
		cptr = cptr + data[i]
		ndata.append(cptr)
	
	return ndata

def generateAccordingTo(data, nb, untreatedData = True):
	if untreatedData:
		fdata = toCumulative(normalizeY(data))
	else:
		fdata = data
	
	ret = []
	cpt = 0
	
	while cpt < nb:
		val = random.random()
		nextpos = 0
		
		while val > fdata[nextpos]:
			nextpos = nextpos + 1
			
		if len(ret) <= nextpos:
			while len(ret) < nextpos - 1:
				ret.append(0)
			ret.append(1)
		else:
			ret[nextpos] = ret[nextpos] + 1
		
		cpt = cpt + 1
	
	return ret
