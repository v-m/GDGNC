#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import os
import networkx as nx
import csv

def buildFolderTree(path):
	parts = path.split("/")
	apath = ""
	for i in range(len(parts)):
		apath = "%s%s%s"%(apath, "/" if len(apath) > 0 else "", parts[i])
		if not os.path.isdir(apath):
			os.mkdir(apath)
			
def checkFileExistance(fname):
	try:
		with open(fname):
			return True
	except IOError:
	   return False
       
def readGraph(filepath):
	if os.path.isfile(filepath):
		gdata = nx.readwrite.edgelist.read_edgelist(filepath, delimiter=';', create_using=nx.DiGraph())
		return gdata
	else:
		return None
            
def readGraphCsv(filepath):
        with open(filepath, 'r') as csvfile:
                mygraph = nx.DiGraph()
                graphreader = csv.reader(csvfile, delimiter=';', quotechar='|')
			
                for graphedge in graphreader:
                        mygraph.add_edge(graphedge[0], graphedge[1])
                    
        return mygraph

def writeGraphCsv(G, filepath):
	with open(filepath, 'w') as csvfile:
		for e in G.edges_iter():
			csvfile.write("%s;%s\n"%(e[0], e[1]))

# http://arxiv.org/abs/1308.4067
def s_score(G):
	score = 0

	for e in G.edges_iter():
		deg1 = G.degree(e[0])
		deg2 = G.degree(e[1])

		score = score + (deg1 * deg2)

	return score