#####################################################################################################
#	Graph generator entry point 
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import inc.generators as gens
import inc.gnc as gnc
import inc.baxter as baxter

algos = [
    {"name": "GNC", "method": gnc.generateGNC, "nodes":True, "edges":False},
    {"name": "GD-GNC", "method": gnc.generateGeneralizedDoubleGNC, "floatProb": ["p", "q"], "nodes":True, "edges":False},
    {"name": "Baxter & Frean", "method": baxter.generateBaxterFreanModel, "floatProb": ["gamma"], "nodes":False, "edges":True},
    {"name": "Vazquez", "method": gens.generateVazquez, "floatProb": ["p"], "nodes":True, "edges":False},
    {"name": "Dorogovtsev", "method": gens.generateDorogovtsev, "consts": ["m", "A"], "nodes":True, "edges":False},
    {"name": "Grindrod", "method": gens.generateGrindrod, "floatProb": ["alpha", "lambda"], "nodes":True, "edges":False},
    {"name": "Kumar Linear", "method": gens.generateKumarLinear, "floatProb": ["copyfactor"], "consts": ["d"], "nodes":True, "edges":False},
    {"name": "Erdos Renyi", "method": gens.generateNxErdosRenyi, "floatProb": ["p"], "nodes":True, "edges":False},
    {"name": "R-MAT", "method": gens.generateRMat, "floatProb": ["a", "b", "c", "d"], "nodes":True, "edges":True},
    {"name": "Bollobas", "method": gens.generateBollobas, "consts": ["deltain", "deltaout"], "floatProb": ["alpha", "beta", "gamma"], "nodes":False, "edges":True},
    {"name": "Goh", "method": gens.generateGoh, "floatProb": ["alpha_in", "alpha_out"], "nodes":True, "edges":True}
];  

def help():
    print("\n   Synopsis: %s <Nr> [nodes=x] [edges=x] [...]\n"%os.path.basename(__file__))
    print("Look up in the following table to find Nr and various parameters required by the algorithm")
    print("_" * 92)
    print("| %3s | %20s | %5s | %5s | %20s | %20s |"%("Nr", "Name", "Nodes", "Edges", "Floats parameters", "Constants parameters"))
    print("_" * 92)
    
    for i in range(len(algos)):
        ai = algos[i]
        
        floats = ""
        if "floatProb" in ai:
            for t in ai["floatProb"]:
                floats = "%s%s, "%(floats,t)
            floats = floats[0:-2]
        else:
            floats = "-" * 20
        
        ints = ""
        if "consts" in ai:
            for t in ai["consts"]:
                ints = "%s%s, "%(ints,t)
            ints = ints[0:-2]
        else:
            ints = "-" * 20
        
        print("| %3d | %20s | %5s | %5s | %20s | %20s |"%(i, ai["name"], ai["nodes"], ai["edges"], floats, ints))
    
    print("_" * 92)
    
if __name__ == "__main__":
    if(len(sys.argv) == 1):
        help()
        sys.exit(0)
        
    inParameters = sys.argv[2:]
    
    params = {}
    nbs = {}
    
    if len(inParameters) > 0:
        for elem in inParameters:
            k = elem.partition("=")[0]
            v = elem.partition("=")[2]
            
            if k == "nodes":
                nbs["nb_nodes"] = int(v)
            elif k == "edges":
                nbs["nb_edges"] = int(v)
            else:
                params[k] = v
    
    print(nbs)
    print(params)
    
    algoId = int(sys.argv[1])
    algoEntry = algos[algoId]
    
    fail = False
    
    if(algoEntry["nodes"] and not("nb_nodes" in nbs)):
        fail = True
    
    if(not(fail) and algoEntry["edges"] and not("nb_edges" in nbs)):
        fail = True
    
    if(not(fail) and "floatProb" in algoEntry):
        for par in algoEntry["floatProb"]:
            if par in params:
                params[par] = float(params[par])
            else:
                fail = True
            
    if(not(fail) and "consts" in algoEntry):
        for par in algoEntry["consts"]:
            if par in params:
                params[par] = int(params[par])
            else:
                fail = True
            
    if(not(fail)):
        print("Algo: %s"%algoEntry["name"])
        if(algoId == 0):
            G = algoEntry["method"](nbs=nbs);
        else:
            G = algoEntry["method"](nbs=nbs, proba = params);
        for edge in G.edges():
            print("%d;%d"%edge)
    else:
        print("Bad parameters.")
        help()
