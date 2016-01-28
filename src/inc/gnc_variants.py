#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import gnc

# This method is the GNC atomic variant operation as defined by Valverde & Sole variant
def ao_GNCWithProb(G, node, alpha, beta):
	randn = rand.randint(0, node - 1)
	
	if rand.random() < beta:
		G.add_edge(node, randn)
		
	for edge in G.out_edges(randn):
		if rand.random() < alpha:
			G.add_edge(node, edge[1])


# Magic version
def generateMagic(nbs, proba = {"doubleiterationchances" : 0.5, "ratiotoGNC" : 0.6}, consts={}, Gstart = None, returnDebuggingInformations=False):
	nb_nodes = nbs["nb_nodes"]
	G, cpt = gnc.initGraph(Gstart)	

	counts = {"doubleiterationchances" : 0, "ratiotoGNC" : 0, "total": 0}

	while cpt < nb_nodes:
		G.add_node(cpt)

		for i in range(2 if cpt+1 < nb_nodes and rand.random() > proba["doubleiterationchances"] else 1):
			counts["total"] = counts["total"] + 1
			if i == 1:
				counts["doubleiterationchances"] = counts["doubleiterationchances"] + 1

			if rand.random() <= proba["ratiotoGNC"]:
				gnc.ao_GNC(G, cpt)
				counts["ratiotoGNC"] = counts["ratiotoGNC"] + 1
			else:
				gnc.ao_attachment(G, cpt)
		
		cpt = cpt + 1

	if returnDebuggingInformations:
		return G, counts
	else:
		return G

# More generic version
def generateCristal(nbs, proba = {"p" : 0.5, "q" : 0.6}, consts={}, Gstart = None, returnDebuggingInformations=False):
	nb_nodes = nbs["nb_nodes"]
	G, cpt = gnc.initGraph(Gstart)	
		
	counts = {"p" : 0, "q" : 0, "total": 0}
	
	while cpt < nb_nodes:
		counts["total"] = counts["total"] + 1
		G.add_node(cpt)
		
		gnc.ao_attachment(G, cpt)

		if rand.random() <= proba["p"]:
			counts["p"] = counts["p"] + 1
			gnc.ao_GNC(G, cpt)
			if rand.random() <= proba["q"]:
				counts["q"] = counts["q"] + 1
				gnc.ao_GNC(G, cpt)
		cpt = cpt + 1


	if returnDebuggingInformations:
		return G, counts
	else:
		return G
            
def generateGNCVariantAsValverdeSole(nbs, proba = {"a" : 0.5, "b" : 0.6}, consts={}, Gstart = None):
	if proba["b"] <= 0:
		return None
	
	nb_nodes = nbs["nb_nodes"]
	G, cpt = gnc.initGraph(Gstart)	
	
	while cpt < nb_nodes:
		G.add_node(cpt)
		gnc.ao_GNCWithProb(G, cpt, proba["a"], proba["b"])
		cpt = cpt + 1
		
	return G


def generateTripleGNC(nbs, proba = {"p" : 0.5}, consts={}, Gstart = None, returnDebuggingInformations=False):
	nb_nodes = nbs["nb_nodes"]
	G, cpt = gnc.initGraph(Gstart)	
		
	counts = {"p" : 0, "total": 0}
	
	while cpt < nb_nodes:
		counts["total"] = counts["total"] + 1
		G.add_node(cpt)
		
		gnc.ao_attachment(G, cpt)

		if rand.random() <= proba["p"]:
			counts["p"] = counts["p"] + 1
			gnc.ao_GNC(G, cpt)
			gnc.ao_GNC(G, cpt)
			gnc.ao_GNC(G, cpt)
		else:
			gnc.ao_attachment(G, cpt)

		cpt = cpt + 1


	if returnDebuggingInformations:
		return G, counts
	else:
		return G


def generateProbaCaseWithAttachmentFull(nbs, proba = {"p2gnc" : .1, "p2ref" : .3, "p1gnc1ref" : .1, "p1gnc" : .1, "p1ref" : .4}, consts={}, Gstart = None, returnDebuggingInformations=False):
	nb_nodes = nbs["nb_nodes"]
	p = [proba["p2gnc"],proba["p2ref"],proba["p1gnc1ref"],proba["p1gnc"],proba["p1ref"]]
	k = ["p2gnc","p2ref","p1gnc1ref","p1gnc","p1ref"]

	if sum(p) < 0.99 or sum(p) > 1.01:
		return None

	G, cpt = gnc.initGraph(Gstart)

	counts = {"p2gnc" : 0, "p2ref" : 0, "p1gnc1ref" : 0, "p1gnc" : 0, "p1ref" : 0, "total": 0}

	while cpt < nb_nodes:
		counts["total"] = counts["total"] + 1
		G.add_node(cpt)

		ppick = rand.random()
		case = 0
		ptot = p[case]

		while ppick > ptot:
			case = case + 1
			ptot = ptot + p[case]
			counts[k[case]] = counts[k[case]] + 1

		for operation in casesForProbaCase[case]:
			operation(G, cpt)

		cpt = cpt + 1

	if returnDebuggingInformations:
		return G, counts
	else:
		return G

def generateProbaCaseWithAttachmentLight(nbs, proba = {"p2gnc" : .1, "p1gnc1ref" : .1, "p1ref" : .4}, consts={}, Gstart = None, returnDebuggingInformations=False):
	return generateProbaCaseWithAttachmentFull(nbs, proba = {"p2gnc" : proba["p2gnc"], "p2ref" : 0, "p1gnc1ref" : proba["p1gnc1ref"], "p1gnc" : 0, "p1ref" : proba["p1ref"]}, consts=consts, Gstart = Gstart, returnDebuggingInformations=returnDebuggingInformations)

def generateProbaCaseWithoutAttachment(nbs, proba = {"p2gnc" : .1, "p1gnc" : .1, "p1ref" : .4}, consts={}, Gstart = None, returnDebuggingInformations=False):
	return generateProbaCaseWithAttachmentFull(nbs, proba = {"p2gnc" : proba["p2gnc"], "p2ref" : 0, "p1gnc1ref" : 0, "p1gnc" : proba["p1gnc"], "p1ref" : proba["p1ref"]}, consts=consts, Gstart = Gstart, returnDebuggingInformations=returnDebuggingInformations)
    