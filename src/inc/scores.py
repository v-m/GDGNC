#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################


import inc.degrees as dl
from scipy.stats import ks_2samp
import inc.kstest as ks

def unshield(data, forIn):
	src1 = data.indegs if forIn else data.outdegs
			
	fsrc1 = []
			
	for item in src1.items:
		fsrc1.append(item[1])
	
	return fsrc1

def calculateScore(d1, d2):
	fsrc1 = unshield(dl.inOutTotalDegreeDistrib(d1), True)
	fsrc2 = unshield(dl.inOutTotalDegreeDistrib(d2), True)
	inDist = ks.ksStat(fsrc1, fsrc2, Int=True)[0]
	
	fsrc1 = unshield(dl.inOutTotalDegreeDistrib(d1), False)
	fsrc2 = unshield(dl.inOutTotalDegreeDistrib(d2), False)
	outDist = ks.ksStat(fsrc1, fsrc2, Int=True)[0]
	
	return {"in":inDist, "out":outDist}

def calculateKsPython(pvalue, d1, d2):
	vprog1 = dl.inOutTotalDegreeDistrib(d1)
	vprog2 = dl.inOutTotalDegreeDistrib(d2)

	fsrc1 = unshield(vprog1, True)
	fsrc2 = unshield(vprog2, True)

	inDist = ks_2samp(fsrc1, fsrc2)[0 if not pvalue else 1]
	
	fsrc1 = unshield(vprog1, False)
	fsrc2 = unshield(vprog2, False)
	
	outDist = ks_2samp(fsrc1, fsrc2)[0 if not pvalue else 1]
	
	return {"in":inDist, "out":outDist}

def calculateScorePython(d1, d2):
	return calculateKsPython(False, d1, d2)


def calculateAndAppendScore(d1, d2, scorearr, useMethod = calculateScore):
	outScore = useMethod(d1, d2)
	
	scorearr["in"].append(outScore["in"])
	scorearr["out"].append(outScore["out"])
	
def calculateAndAppendScoreMerged(d1, d2, scorearr, useMethod = calculateScore):
	outScore = useMethod(d1, d2)
	
	rin = outScore["in"]
	rout = outScore["out"]
	
	cmax = max(rin, rout)
	tmpx = 1 - rin
	tmpy = 1 - rout
	fscore = 2 * ((tmpx * tmpy) / (tmpx + tmpy)) if (tmpx + tmpy) > 0 else 0.0
	
	scorearr["max"].append(cmax)
	scorearr["fscore"].append(fscore)

def resultScoreUnique(data, t = "median"):
	datas = sorted(data)
	
	if t == "median":
		lenins = int(len(datas) / 2)
		if not len(datas) % 2:
			datam = (datas[lenins] + datas[lenins]) / 2.0
		else:		
			datam = datas[lenins]
	elif t == "avg":
		for i in range(len(datas)):
			datam = datas[i]
		datam = datam / len(datas)
	elif t == "max":
		datam = -1
		for i in range(len(ins)):
			datam = datas[i] if datas[i] > datam else datam
			
	dataid = 0
	for i in data:
		if i != datam:
			dataid = dataid + 1
		else:
			break
		
	return {"value": datam, "id": dataid}

def resultScore(data, t = "median"):
	allin = resultScoreUnique(data["in"], t)
	allout = resultScoreUnique(data["out"], t)
	
	inid = allin["id"]
	outid = allout["id"]
	
	invalues = {"in":data["in"][inid], "out":data["out"][inid]}
	outvalues = {"in":data["in"][outid], "out":data["out"][outid]}
	
	# All returns are for median except for "min" and "max" prepended key
	return {"in":allin["value"], "idin": allin["id"], "invalues": invalues, "minin": min(data["in"]), "maxin": max(data["in"]), "out":allout["value"], "idout": allout["id"],  "outvalues": outvalues, "minout": min(data["out"]), "maxout": max(data["out"])}