#####################################################################################################
#	Digraph generator according to GNC
#          + implementation of GDGNC and variants
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import random as rand
import networkx as nx

# This method determine the initial graph to use and the initial counter value
def initGraph(Gstart):
	if Gstart == None:
		G = nx.DiGraph()
		G.add_node(0)
		cpt = 1
	else:
		G = Gstart.copy();
		cpt = G.number_of_nodes()

	return G, cpt

# This method is the GNC atomic operation
def ao_GNC(G, node):
	randn = rand.randint(0, node - 1)
	G.add_edge(node, randn)		
	for edge in G.out_edges(randn):
		G.add_edge(node, edge[1])


# This method is the "refactor" atomic operation
def ao_attachment(G, node):
	randn = rand.randint(0, node - 1)
	G.add_edge(randn, node)


casesForProbaCase = [
	[ao_GNC, ao_GNC],
	[ao_attachment, ao_attachment],						# Removed
	[ao_GNC, ao_attachment],						# Attachment
	[ao_GNC],								# Removed
	[ao_attachment]								# Refactor
]



#####################################################################################################
#####################################################################################################
##												   ##
#						ALGORITHMS					    #
##												   ##
#####################################################################################################
#####################################################################################################


# Classic GNC case
def generateGNC(nbs, Gstart = None, returnDebuggingInformations = False):
	if not "nb_nodes" in nbs:
		return None
	
	nb_nodes = nbs["nb_nodes"]

	G, nodescount = initGraph(Gstart)

	while nodescount < nb_nodes:
		attachTo = rand.randint(0, nodescount-1)
		G.add_node(nodescount)

		for edge in G.out_edges(attachTo):
			G.add_edge(nodescount, edge[1])

		G.add_edge(nodescount, attachTo)
		
		nodescount = nodescount + 1


	if returnDebuggingInformations:
		return G, None
	else:
		return G

# Explanation: evolution occurs everywhere on the software graph, sometimes it has more impact, sometimes less...
def generateGeneralizedDoubleGNC(nbs, proba = {"p" : 0.5, "q" : 0.6}, consts={}, Gstart = None, returnDebuggingInformations=False):
	nb_nodes = nbs["nb_nodes"]
	G, cpt = initGraph(Gstart)	
	
	counts = {"p" : 0, "q" : 0, "total": 0}
	
	while cpt < nb_nodes:
		counts["total"] = counts["total"] + 1
		G.add_node(cpt)
		
		if rand.random() <= proba["p"]:
			counts["p"] = counts["p"] + 1
			ao_GNC(G, cpt)
			if rand.random() <= proba["q"]:
				counts["q"] = counts["q"] + 1
				ao_GNC(G, cpt)
		else: 
			ao_attachment(G, cpt)
		cpt = cpt + 1

	if returnDebuggingInformations:
		return G, counts
	else:
		return G
