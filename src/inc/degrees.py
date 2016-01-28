#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import matplotlib.pyplot as plt
import numpy as np
import pylab
import math
import sys

class inOutTotalDegreeDistrib:
	def __init__(self, agraph = None):
		self.degs = degreeDistrib()
		self.indegs = degreeDistrib()
		self.outdegs = degreeDistrib()
		self.jointdegrees = jointDistrib()

		self.isXNormalized = False
		self.isYNormalized = False

		if agraph is not None:
			self.readDegreeFromGraph(agraph)

	def readDegreeFromGraph(self, agraph):
		mygraph = agraph

		for anode in mygraph.nodes_iter(): 
			self.degs.addX(mygraph.degree(anode))
			self.indegs.addX(mygraph.in_degree(anode))
			self.outdegs.addX(mygraph.out_degree(anode))
			self.jointdegrees.addPoint(mygraph.in_degree(anode), mygraph.out_degree(anode))

	def normalizeAxis(self, x=True, y=True):
		self.degs.normalize(x,y)
		self.indegs.normalize(x,y)
		self.outdegs.normalize(x,y)

		self.isXNormalized = True if x else self.isXNormalized
		self.isYNormalized = True if y else self.isYNormalized

	def transformToCumulative(self, reverse=False):
		self.degs.transformToCumulative(reverse)
		self.indegs.transformToCumulative(reverse)
		self.outdegs.transformToCumulative(reverse)

	def selectDistribution(self, iin = True, iout= True):
		if not iin and not iout:
			return None
		else:
			if iin and iout:
				return self.degs
			elif iin:
				return self.indegs
			else:
				return self.outdegs
	
	def plotOnGraph(self, iin = True, iout= True, color="Black", label="", thickness=1, linestyle="-", alpha=1, marker=None, markersize=10, markevery=1):
		distSel = self.selectDistribution(iin, iout)
		retv, = plt.plot(distSel.getXAxis(), distSel.getYAxis(), c=color, label=label, linewidth=thickness, linestyle=linestyle, alpha=alpha, marker=marker, markersize=markersize, markevery=markevery)
		return retv,

	def jointPlotOnGraph(self):
		plt.matshow(self.jointdegrees.items, cmap=plt.cm.gray)

	def addZeroZeroPoints(self):
		self.degs.addZeroZeroPoint()
		self.indegs.addZeroZeroPoint()
		self.outdegs.addZeroZeroPoint()

	def exportPoints(self, f, forIn = True, separator = "\t", normalized = False):
		dist = self.indegs if forIn else self.outdegs
		cumul = 0.0
		
		for i in range(len(dist.items)):
			cumul = cumul + dist.items[i][1]
			
		print cumul
		
		for i in range(len(dist.items)):
			if normalized:
				st = "%f%s%.100f\n"%(i, separator, dist.items[i][1]/cumul)
			else:
				st = "%f%s%.100f\n"%(i, separator, dist.items[i][1])
			f.write(st)

class degreeDistrib:
	def __init__(self):
		self.items = []
		self.maxX = -99999
		self.cptX = 0
		self.maxY = -99999

	def addX(self, xval, incy = 1):

		# Check if item interval exists
		if xval + 1 > len(self.items):
			addnb = xval + 1 - len(self.items)
			actCpt = len(self.items)
			for i in range(addnb):
				self.items.append([actCpt + i , 0])

		for i in range(len(self.items)):
			item = self.items[i]

			if item[0] == xval:
				item[1] = item[1] + incy
				if item[1] > self.maxY:
					self.maxY = item[1]
				break

		if xval > self.maxX:
			self.maxX = xval

		self.cptX = self.cptX + incy

	def normalize(self, x=True, y=True):
		if not x and not y:
			return

		for item in self.items:
			if x:
				item[0] = item[0] / (self.cptX * 1.0)

			if y:
				item[1] = item[1] / (self.maxY * 1.0)


	def getXAxis(self):
		retv = []
		for item in self.items:
			retv.append(item[0])

		return retv

	def getYAxis(self):
		retv = []
		for item in self.items:
			retv.append(item[1])

		return retv

	def transformToCumulative(self, reverse=False):
		cumul = 0
		src = self.items if not reverse else reversed(self.items)
		for item in src:
			cumul = cumul + item[1]
			item[1] = cumul
			self.maxY = cumul

	def addZeroZeroPoint(self):
		tmp = [[0,0]] + self.items
		self.items = tmp

class jointDistrib:
	def __init__(self):
		self.items = [[]]

	@staticmethod
	def generateARow(nbcols):
		if not isinstance(nbcols,int):
			nbcols = len(nbcols)

		myrow = []
		i = 0
		while i < nbcols:
			myrow.append(0)
			i = i + 1

		return myrow

	def addPoint(self, indeg, outdeg):
		# Add lines
		if outdeg + 1 >= len(self.items):
			
			for i in range(outdeg):
				self.items.append(jointDistrib.generateARow(self.items[0]))
		
		if indeg + 1 >= len(self.items[0]):
			for anout in self.items:
				for j in range(indeg - len(anout) + 1):
					anout.append(0)

		self.items[outdeg][indeg] = self.items[outdeg][indeg] + 1

	def getData(self):
		return self.items

	def getRootsData(self):
		return self.items[0:100][0:100]

	def getCompactedData(self, xpc = .5, ypc = .5):
		# Reduce to global inc
		ypc = xpc

		xinc = math.floor(len(self.items)*xpc)
		yinc = math.floor(len(self.items[0])*ypc)

		# Reduce to global inc
		if xinc > yinc:
			xinc = yinc
		else:
			yinc = xinc

		nbx = int(math.ceil(len(self.items)/xinc))
		nby = int(math.ceil(len(self.items[0])/yinc))

		xinc = int(xinc)
		yinc = int(yinc)

		ret = []
		for x in range(nbx):
			tp = []
			for y in range(nby):
				tp.append(jointDistrib.calcCluster(y,x,self.items,xinc, yinc))
			ret.append(tp)
		return ret

	@staticmethod
	def calcCluster(x,y,tab,xinc,yinc):
		rv = 0

		for i in range(xinc):
			for j in range(yinc):
				cx = (x*xinc)+i
				cy = (y*yinc)+j

				if cx >= len(tab[0]) or cy >= len(tab):
					continue

				rv = rv + tab[cy][cx]
		
		return rv
