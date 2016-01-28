#####################################################################################################
#	Computes ks distances between generations or software
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import inc.statistics as stats
import inc.scores as score
import inc.utils as utils
import os

def help():
    print("\n   Synopsis: %s <program> [generations]\n"%os.path.basename(__file__))
    
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        help()
        sys.exit(1)

    testWith = []
    

    if(len(sys.argv) == 2):
        targetDirectory = sys.argv[1][0:sys.argv[1].rfind("/")]
        # Empirical test...
        for oneFile in os.listdir(targetDirectory):
            fullPathFile = "%s/%s"%(targetDirectory, oneFile)
            
            if os.path.isfile(fullPathFile) and fullPathFile != sys.argv[1] and fullPathFile[-4:] == ".csv":
                testWith.append(fullPathFile)
    else:
        # Generated test...
        for oneFile in os.listdir(sys.argv[2]):
            fullPathFile = "%s/%s"%(sys.argv[2], oneFile)
            
            if os.path.isfile(fullPathFile) and fullPathFile[-4:] == ".csv":
                testWith.append(fullPathFile)
    
    result = stats.calculateScores(sys.argv[1], testWith, useMethod=score.calculateScore)["merged"]["max"]
    
    print("Delta (min)    : %.5f"%result["min"])
    print("Delta (median) : %.5f"%result["med"]["value"])
    print("Delta (max)    : %.5f"%result["max"])
        
    