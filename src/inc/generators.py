#####################################################################################################
#	Various digraph generator implementations
#	Author: Vincenzo Musco (http://www.vmusco.com)
#	Date  : 2014-02-27
#####################################################################################################

import networkx as nx
import math
import random as rand
import numpy as np
import itertools
import random

# This code is taken from networkx repository and adapted
def generateErdosRenyi(nbs, proba = {"p" : 0.5}):
	n = nbs["nb_nodes"]
	p = proba["p"]
	
	G=nx.DiGraph()

	G.add_nodes_from(range(n))

	if p<=0.01 or p >= 0.99:
		return None

	edges=itertools.permutations(range(n),2)
    
	for e in edges:
		if random.random() < p:
			G.add_edge(*e)
	
	return G

def generateNxErdosRenyi(nbs, proba = {"p" : 0.5}):
	n = nbs["nb_nodes"]
	p = proba["p"]
	
	G=nx.generators.random_graphs.fast_gnp_random_graph(n, p, seed=None, directed=True)
	
	return G

def selectNodeUsingProbabilityList(problist):
	spl = sum(problist)
	
	if spl < 0.99 or spl > 1.01:
		print("Error, probabilites do not sum to 1.0 (%f) !!!"%spl)
		
	
	cnode = 0
	selproba = rand.random()
	probacalc = problist[0]
	
	while probacalc < selproba:
		cnode = cnode + 1
		probacalc = probacalc + problist[cnode]
		
	return cnode

# alphas must belong to range [0,1)
# nb_nodes is the number of created nodes
# nbedges allows to calculate the number of edges such as nbnomdes*nbedges
def generateGoh(nbs, proba = {"alpha_in" : 0.5, "alpha_out" : 0.6}):
	if "nb_edges" not in nbs or "nb_nodes" not in nbs or "alpha_in" not in proba or "alpha_out" not in proba or proba["alpha_in"] > 1.01 or proba["alpha_in"] < -0.01 or proba["alpha_out"] > 1.01 or proba["alpha_out"] < -0.01:
		return None
	nb_nodes = nbs["nb_nodes"]
	nb_edges = nbs["nb_edges"]
	
	pi_weights = []
	qi_weights = []
	totsum = 0
	
	# Insert nodes on graph
	G = nx.DiGraph()
	
	for i in range(nb_nodes + 1):
		curi = i + 1
		G.add_node(curi)
		pi_weights.append(pow(curi, -1*proba["alpha_out"]))
		qi_weights.append(pow(curi, -1*proba["alpha_in"]))
		totsum = totsum + curi
		
	pis = map(lambda x: x/sum(pi_weights), pi_weights)
	qis = map(lambda x: x/sum(qi_weights), qi_weights)
	
	nbit = nb_nodes * nb_edges
	
	for i in range(nbit):
		# select i
		inode = selectNodeUsingProbabilityList(pis)
		jnode = selectNodeUsingProbabilityList(qis)
		#print "selected pair: %d %d"%(inode+1,jnode+1)
		
		if not G.has_edge(inode, jnode):
			G.add_edge(inode, jnode)
			
	return G


def generateVazquez(nbs, proba = {"p" : 0.5}):
	if not "p" in proba:
		return None
	
	nb_nodes = nbs["nb_nodes"]
	G = nx.DiGraph()
	G.add_node(0)
	
	for i in range(nb_nodes):
		realnode = i + 1
		randnode = rand.randint(0, realnode - 1)

		G.add_node(realnode)
		G.add_edge(realnode, randnode)
		
		# Walking step
		visited = []
		tovisit = [randnode]
		
		while len(tovisit) > 0:
			visitingnode = tovisit.pop(0)
			visited.append(visitingnode)

			if not G.has_edge(realnode, visitingnode) and rand.random() < proba["p"]:
				G.add_edge(realnode, visitingnode)
				
			newtovisit = G.out_edges(visitingnode)
			newtovisit = map(lambda x: x[1], newtovisit)
			
			newtovisit = [aa for aa in newtovisit if aa not in set(visited)]	# Difference of lists
			newtovisit = [aa for aa in newtovisit if aa not in set(tovisit)]	# Difference of lists
			
			if len(newtovisit) > 0:
				tovisit = tovisit + newtovisit
				
	return G

# Generate a Drogovtsev DiGraph with nb_nodes nodes, at each node insertion, add m edges on the graph.
# A is the default attractiveness for a nodes (>= 0)
# Note that we use the special case where each source node is self !
def generateDorogovtsev(nbs, proba = {"m" : 3, "A": 5}):
	if not "nb_nodes" in nbs or "A" not in proba or "m" not in proba or proba["A"] <= 0  or proba["m"] <= 0:
		return None
	
	nb_nodes = nbs["nb_nodes"]
	G = nx.DiGraph()
	A = proba["A"] * 1.0
	
	for i in range(nb_nodes):
		G.add_node(i)
		
		# Add m edges
		for j in range(proba["m"]):
			if G.number_of_nodes() > 1:
				fromnode = i
				problist = range(i)
				problist = map(lambda x: (A + G.in_degree(x)), problist)
				sumpl = sum(problist)
				problist = map(lambda x: (x / sumpl), problist)
				
				tonode = selectNodeUsingProbabilityList(problist)
				if not G.has_edge(fromnode, tonode):
					G.add_edge(fromnode, tonode)
					
	return G

				
# For compatibility purposes, this algorithm takes an nb_nodes parameter but it is not used !!!
# alpha + beta + gamma = 1
# deltain & deltaout >= 0
def generateBollobas(nbs, proba = {"alpha": 0.3, "beta": 0.3, "gamma": 0.4, "deltain": 2, "deltaout": 3}):
	if not "nb_edges" in nbs or not "alpha" in proba or not "beta" in proba or not "gamma" in proba or not "deltain" in proba or not "deltaout" in proba:
		return None

	if proba["alpha"] + proba["beta"] + proba["gamma"] > 1.01 or proba["alpha"] + proba["beta"] + proba["gamma"] < 0.99:
		return None
	
	if proba["deltain"] < 0.01 or proba["deltaout"] < 0.01:
		return None

	nb_edges = nbs["nb_edges"]
	G = nx.DiGraph()
	G.add_node(0)	
	
	for i in range(nb_edges):
		rval = rand.random()
		
		nbnode = G.number_of_nodes()
		nbedges = G.number_of_edges()
		probin = range(nbnode)
		probin = map(lambda x: (1.0 * G.in_degree(x) + proba["deltain"]) / (1.0 * nbedges + (1.0 * proba["deltain"] * nbnode)), probin)
		probout = range(nbnode)
		probout = map(lambda x: (1.0 * G.out_degree(x) + proba["deltaout"]) / (1.0 * nbedges + (1.0 * proba["deltaout"] * nbnode)), probout)
		
		if rval < proba["alpha"]:
			G.add_node(nbnode)
			fromnode = nbnode
			tonode = selectNodeUsingProbabilityList(probin)
		elif rval < proba["alpha"]+proba["beta"]:
			if G.number_of_nodes() < 2:
				continue
			
			fromnode = selectNodeUsingProbabilityList(probout)
			tonode = selectNodeUsingProbabilityList(probin)
		else:
			G.add_node(nbnode)
			fromnode = selectNodeUsingProbabilityList(probout)
			tonode = nbnode
			
		if not G.has_edge(fromnode, tonode):
			G.add_edge(fromnode, tonode)
		
	return G

# alpha & labda in (0, 1]
# range is centered around 0, if impair number of nodes is asked, the largest numbe of node is on postive interval
def generateGrindrod(nbs, proba = {"alpha": 0.4, "lambda": 0.6}):
	nb_nodes = nbs["nb_nodes"]
	G = nx.DiGraph()

	G.add_node(0)
	
	for i in range(int((nb_nodes)/2)):
		effi = i + 1 
		G.add_node(effi)
		if G.number_of_nodes() < nb_nodes:
			G.add_node(-1 * effi)

	for i in G.nodes():
		for j in G.nodes():
			if i == j:
				continue
			
			prob = pow(proba["alpha"] * proba["lambda"], abs(j-i) - 1)
			if rand.random() < prob:
				G.add_edge(i,j)
	
	return G

def generateKumarLinear(nbs, proba = {"copyfactor": 0.5, "d": 5}):
	nb_nodes = nbs["nb_nodes"]
	G = nx.DiGraph()
	
	for i in range(nb_nodes):
		G.add_node(i)
		
		if G.number_of_nodes() < 2:
			continue
	
		# Pick up prototype node p
		p = rand.randint(0, i - 1)
		
		for j in range(proba["d"]):
			if rand.random() < proba["copyfactor"]:
				dst = rand.randint(0, i - 1)
			else:
				protoutdeg = map(lambda x: x[1], G.out_edges(p))
				
				if(len(protoutdeg) <= j):
					continue
					
				dst = protoutdeg[j]
			
			if not G.has_edge(i, dst):
				G.add_edge(i, dst)
			
	return G

def generateRMat(nbs, proba = {"a": 0.3, "b": 0.2, "c": 0.3, "d": 0.2}):
	nb_nodes = nbs["nb_nodes"]
	nb_edges = nbs["nb_edges"]
	a = proba["a"]
	b = proba["b"]
	c = proba["c"]
	d = proba["d"]
	
	sm = a + b + c + d
	if sm < .99 or sm > 1.01:
		return None
	
	adjmat = []
	
	for i in range(nb_nodes):
		lineadjmat = [[0] * nb_nodes]
		adjmat = adjmat + lineadjmat
		
	#adjmat = np.matrix(adjmat)
	
	for i in range(nb_edges):
		area = {"x": [0, len(adjmat) - 1], "y": [0, len(adjmat) - 1]}
		
		while area["x"][0] != area["x"][1] and area["y"][0] != area["y"][1]:
			prob = rand.random()
			
			xpart1 = [area["x"][0], area["x"][0] + ((area["x"][1] - area["x"][0]) / 2)]
			decrv = ((area["x"][1] - area["x"][0]) / 2)
			if (area["x"][1] - area["x"][0]) % 2 == 0:
				decrv = decrv - 1
			xpart2 = [area["x"][1] - decrv, area["x"][1]]
			
			ypart1 = [area["y"][0], area["y"][0] + ((area["y"][1] - area["y"][0]) / 2)]
			decrv = ((area["y"][1] - area["y"][0]) / 2)
			if (area["y"][1] - area["y"][0]) % 2 == 0:
				decrv = decrv - 1
			ypart2 = [area["y"][1] - decrv, area["y"][1]]
			
			if prob < a:
				area["x"] = xpart1
				area["y"] = ypart1
			elif prob < a + b:
				area["x"] = xpart2
				area["y"] = ypart1
			elif prob < a + b + c:
				area["x"] = xpart1
				area["y"] = ypart2
			else:
				area["x"] = xpart2
				area["y"] = ypart2
		
			# Renormalize
			a = a + rand.random()
			b = b + rand.random()
			c = c + rand.random()
			d = d + rand.random()
			
			msum = a + b + c + d
			a = a / msum
			b = b / msum
			c = c / msum
			d = d / msum
			
		# to avoid self loops
		if area["y"][0] != area["x"][0]:
			adjmat[int(area["y"][0])][int(area["x"][0])] = 1
		
	matrx = np.matrix(adjmat)
	G = nx.from_numpy_matrix(matrx, nx.DiGraph())
	return G