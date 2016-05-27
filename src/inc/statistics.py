#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import inc.utils as utils
import inc.scores as score
import scipy.stats as stats

def computeScores(program, otherData, useMethod = score.computeScore):
	scores = {"in":[], "out":[]}
	mergedscores = {"fscore":[], "max":[]}
	prog = utils.readGraphCsv(program)
        
	for oneGeneration in otherData:
		graph = utils.readGraphCsv(oneGeneration)
		
		if graph is None:
			return None
		
		score.computeAndAppendScore(graph, prog, scores, useMethod)
		score.computeAndAppendScoreMerged(graph, prog, mergedscores, useMethod)
	
	fscore = score.resultScoreUnique(mergedscores["fscore"])
	cmax = score.resultScoreUnique(mergedscores["max"])

	mergeddic = {}
	mergeddic["fscore"] = {"min": min(mergedscores["fscore"]), "med": fscore, "max": max(mergedscores["fscore"])}
	mergeddic["max"] = {"min": min(mergedscores["max"]), "med": cmax, "max": max(mergedscores["max"])}
	return {"inout": score.resultScore(scores, "median"), "merged": mergeddic}
    
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
	