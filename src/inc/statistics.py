#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import inc.utils as utils
import inc.scores as score
import scipy.stats as stats
import numpy

def computeScores(program, otherData, useMethod = score.computeScore):
	scores = {"in": [], "out": []}

	# merged contains metric which are computed according to in and out simultaneously
	# fscore combines both in/out in fscore
	# max chooses the max values in in/out
	mergedscores = {"fscore": [], "max": []}
	prog = utils.readGraphCsv(program)

	for oneGeneration in otherData:
		graph = utils.readGraphCsv(oneGeneration)

		if graph is None:
			return None

		score.computeAndAppendScore(graph, prog, scores, useMethod)
		score.computeAndAppendScoreMerged(graph, prog, mergedscores, useMethod)

	return {"scores": scores, "mergedscores": mergedscores}

def computeScoresSummary(computed):
	mergeddic = {}
	mergeddic["fscore"] = {}
	mergeddic["fscore"]["min"] = score.resultScoreUnique(computed["mergedscores"]["fscore"], "min")  # min(mergedscores["fscore"]),
	mergeddic["fscore"]["med"] = score.resultScoreUnique(computed["mergedscores"]["fscore"])
	mergeddic["fscore"]["max"] = score.resultScoreUnique(computed["mergedscores"]["fscore"], "max")  # max(mergedscores["fscore"])
	mergeddic["fscore"]["avg"] = score.resultScoreUnique(computed["mergedscores"]["fscore"], "avg")

	mergeddic["max"] = {}
	mergeddic["max"]["min"] = score.resultScoreUnique(computed["mergedscores"]["max"], "min")  # min(mergedscores["max"]),
	mergeddic["max"]["med"] = score.resultScoreUnique(computed["mergedscores"]["max"])
	mergeddic["max"]["max"] = score.resultScoreUnique(computed["mergedscores"]["max"], "max")  # max(mergedscores["max"])
	mergeddic["max"]["avg"] = score.resultScoreUnique(computed["mergedscores"]["max"], "avg")

	return {"inout": score.resultScore(computed["scores"], "median"), "merged": mergeddic}

def computeScoresAndSummary(program, otherData, useMethod = score.computeScore):
	computed = computeScores(program, otherData, useMethod)
	return computeScoresSummary(computed)
    
def computeCloseness(program, data1, data2, useMethod = score.computeScore):
	set1in = []
	set1out = []
	set1max = []
	set2in = []
	set2out = []
	set2max = []
	
	prog = utils.readGraphCsv(program)
	
	for oneGraph in data1:
		graph = utils.readGraphCsv(oneGraph)
		
		r1 = useMethod(graph, prog)
		
		set1in.append(r1["in"])
		set1out.append(r1["out"])
		set1max.append(max(r1["in"],r1["out"]))
		
	for oneGraph in data2:
		graph = utils.readGraphCsv(oneGraph)
		
		r2 = useMethod(graph, prog)
		
		set2in.append(r1["in"])
		set2out.append(r1["out"])
		set2max.append(max(r1["in"],r1["out"]))
		
	return {"in": stats.mannwhitneyu(set1in, set2in), "out": stats.mannwhitneyu(set1out, set2out), "max": stats.mannwhitneyu(set1max, set2max)}	



def calculateScoresForProgramOneAgainstOther(prog, allprogs, useMethod = score.computeScore):
	scores = {"in":[], "out":[]}
	mergedscores = {"fscore":[], "max":[]}

	for prog2 in allprogs:
		if prog2==prog:
			continue;

		score.computeAndAppendScore(prog, prog2, scores, useMethod)
		score.computeAndAppendScoreMerged(prog, prog2, mergedscores, useMethod)

	fscore = score.resultScoreUnique(mergedscores["fscore"])
	cmax = score.resultScoreUnique(mergedscores["max"])

	mergeddic = {"fscore": {"min": min(mergedscores["fscore"]), "med": fscore, "max": max(mergedscores["fscore"])}, "max": {"min": min(mergedscores["max"]), "med": cmax, "max": max(mergedscores["max"])}}
	return {"inout": score.resultScore(scores, "median"), "merged": mergeddic}


# prog is the target program
# graphs is a list of defined graphs
# programs is a list of all programs
def computeClosenessBetweenGenerationsAndEmpirical(prog, graphs, programs, useMethod = score.computeScore):
	set1in = []
	set1out = []
	set1max = []
	set2in = []
	set2out = []
	set2max = []

	for graph1 in graphs:
		r1 = useMethod(graph1, prog)

		set1in.append(r1["in"])
		set1out.append(r1["out"])

		set1max.append(max(r1["in"],r1["out"]))

	for prog2 in programs:
		if prog == prog2:
			continue

		r2 = useMethod(prog2, prog)
		set2in.append(r2["in"])
		set2out.append(r2["out"])
		set2max.append(max(r2["in"],r2["out"]))

	return {"in": stats.mannwhitneyu(set1in, set2in), "out": stats.mannwhitneyu(set1out, set2out), "max": stats.mannwhitneyu(set1max, set2max)}

# prog is the target program
# graphs is a list of defined graphs
# programs is a list of all programs
def computeClosenessBetweenGenerationsOptimized(generated1, generated2, prog, useMethod = score.computeScore):
	set1in = []
	set1out = []
	set1max = []
	set2in = []
	set2out = []
	set2max = []

	for i in range(len(generated1)):
		graph1 = generated1[i]
		graph2 = generated2[i]

		g1load = utils.readGraphCsv(graph1)
		g2load = utils.readGraphCsv(graph2)

		r1 = useMethod(g1load, prog)
		r2 = useMethod(g2load, prog)

		set1in.append(r1["in"])
		set1out.append(r1["out"])
		set2in.append(r2["in"])
		set2out.append(r2["out"])

		set1max.append(max(r1["in"],r1["out"]))
		set2max.append(max(r2["in"],r2["out"]))

	return {"in": stats.mannwhitneyu(set1in, set2in), "out": stats.mannwhitneyu(set1out, set2out), "max": stats.mannwhitneyu(set1max, set2max)}

# Compute the Cohen d effect size
def cohen_d(x, y):
	return (numpy.mean(x) - numpy.mean(y)) / numpy.sqrt((numpy.std(x, ddof=1) ** 2 + numpy.std(y, ddof=1) ** 2) / 2.0)
