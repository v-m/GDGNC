#####################################################################################################
#	Digraph generator according to Baxter & Frean
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import networkx as nx
import random as rand

def updateDegreeTable(degreeTable, node, graph):
	degreeTable[node - 1][0] = graph.in_degree(node)
	degreeTable[node - 1][1] = graph.out_degree(node)

def updateNodesProp(nodesprop, degreeTable, t):
	for node in range(len(degreeTable)):
		#node = node - 1
		nodesprop[node][0] = degreeTable[node][0]/(t*1.0)
		nodesprop[node][1] = degreeTable[node][1]/(t*1.0)

def newNodeInserted(nodesprop, degreeTable):
	nodesprop.append([-1, -1])
	degreeTable.append([-1, -1])

def pickRandomNode(nodesprop, propToIn = True):
	i = -1
	test = rand.random()
	cumul = 0.0

	while i == -1 or cumul < test:
		i = i + 1
		cell = nodesprop[i]
		cumul = cumul + (cell[0] if propToIn else cell[1])
		#print "cumul is %f for treshold %f"%(cumul, test)

	return i + 1

def sanityCheck(nodesprop, degreeTable, graph, t):
	totin = totout = 0
	psin = psout = 0.0
	# Checking 1
	for node in graph.nodes():
		nin = graph.in_degree(node)
		nout = graph.out_degree(node)

		totin = totin + nin
		totout = totout + nout

		# Checking degree integrity
		if degreeTable[node -1][0] != nin:
			print('node %d has in degree %d but stored is %d'%(node, nin, degreeTable[node -1][0]))
			return False
		if degreeTable[node -1][1] != nout:
			print('node %d has out degree %d but stored is %d'%(node, nout, degreeTable[node -1][1]))
			return False

		# Checking probability intrgrity
		if abs(nodesprop[node -1][0]-nin/(t*1.0)) > 0.01:
			print('node %d has in probability %f but stored is %f (abs = %f)'%(node, nin/(t*1.0), nodesprop[node -1][0], abs(nodesprop[node -1][0]-nin/(t*1.0))))
			return False
		psin = psin + nodesprop[node -1][0]
		if abs(nodesprop[node -1][1]-nout/(t*1.0)) > 0.01:
			print('node %d has out probability %f but stored is %f (abs = %f)'%(node, nout/(t*1.0), nodesprop[node -1][1], abs(nodesprop[node -1][1]-nout/(t*1.0))))
			return False
		psout = psout + nodesprop[node -1][1]
	if totin != totout != t:
		print("totals doesn't match: %d %d %d"%(totin, totout, t))
		return False

	if psin < 0.99 or psin > 1.01 or psout < 0.99 or psout > 1.01:
		print("Sum of probability don't equals 1. IN = %f / OUT = %f"%(psin, psout))
		return False

	return True
	
def generateBaxterFreanModel(nbs, proba):
	# Pre executon test
	if not "gamma" in proba or proba["gamma"] < 0.01:
		return None
	
	nb_edges = nbs["nb_edges"]
	nodesprop = []
	degreeTable = []
	t = 1
	graph = nx.DiGraph()

	graph.add_node(1)
	newNodeInserted(nodesprop, degreeTable)
	graph.add_edge(1,1)
	updateDegreeTable(degreeTable, 1, graph)
	updateNodesProp(nodesprop, degreeTable, t)
	t_final = nb_edges

	while t < t_final:
			
		# ===== Algorithm code start =====
		# select parent node m with probability vm/t
		m = pickRandomNode(nodesprop, False)

		test = rand.random()
		# With probability (1 - proba["gamma"]) simply add an edge:
		if test <= 1-proba["gamma"]:
			# the parent node m is the out node
			# select in node n with probability wn/t
			n = pickRandomNode(nodesprop, True)

			if m == n or graph.has_edge(m,n):
				t = t - 1
			else:
				# vm -> vm + 1 and wn -> wn + 1
				graph.add_edge(m,n)
				updateDegreeTable(degreeTable, m, graph)
				updateDegreeTable(degreeTable, n, graph)
		# Otherwise, with probability proba["gamma"], split the parent node:
		else:
			k = graph.number_of_nodes() + 1
			graph.add_node(k)
			newNodeInserted(nodesprop, degreeTable)

			outiter = graph.out_edges_iter(m)
			initer = graph.in_edges_iter(m)

			r = rand.randint(1, graph.out_degree(m))
			s = rand.randint(0, graph.in_degree(m) - 1 if graph.in_degree(m) > 0 else 0)
			
			removeedges = []
			addedges = []

			# Transfering r out degrees from parent
			i = 0
			while i < r:
				transf = outiter.next()
				removeedges.append((transf[0], transf[1]))
				addedges.append((k, transf[1]))
				i = i + 1
							
			# Transfering s in degrees from parent
			i = 0			
			while i < s:
				transf = initer.next()
				removeedges.append((transf[0], transf[1]))
				addedges.append((transf[0], k))
				i = i + 1
			
			# Doing connections changes
			for change in removeedges:
				graph.remove_edge(change[0], change[1])
				if change[0] != k and change[0] != m:
					updateDegreeTable(degreeTable, change[0], graph)
				if change[1] != k and change[1] != m:
					updateDegreeTable(degreeTable, change[1], graph)

			for change in addedges:
				graph.add_edge(change[0], change[1])
				if change[0] != k and change[0] != m:
					updateDegreeTable(degreeTable, change[0], graph)
				if change[1] != k and change[1] != m:
					updateDegreeTable(degreeTable, change[1], graph)

			# Connecting parent to new node
			graph.add_edge(m, k)
			updateDegreeTable(degreeTable, k, graph)
			updateDegreeTable(degreeTable, m, graph)
			nodesprop.append([k, -1, -1])

		# Increment the counter t -> t + 1
		t = t + 1
		updateNodesProp(nodesprop, degreeTable, t)

	# ===== Algorithm code end =====
	if not sanityCheck(nodesprop, degreeTable, graph, t_final):
		print('Sanity check failed ! Please review source code !')
		return None
	return graph

