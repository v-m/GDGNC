#####################################################################################################
#	MW p-value between two generations or a generation and the software
#       Check if values belong to a same population
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import inc.statistics as stats
import inc.scores as score
import inc.utils as utils
import os

def help():
    print("\n   Synopsis: %s <program> <generations1> [generations2] \n"%os.path.basename(__file__))
    
if __name__ == "__main__":
    if(len(sys.argv) < 3):
        help()
        sys.exit(1)

    generations = []
    otherData = []
    
    for oneFile in os.listdir(sys.argv[2]):
            fullPathFile = "%s/%s"%(sys.argv[2], oneFile)
            
            if os.path.isfile(fullPathFile) and fullPathFile[-4:] == ".csv":
                generations.append(fullPathFile)
    
    if(len(sys.argv) == 3):
        targetDirectory = sys.argv[1][0:sys.argv[1].rfind("/")]
        for oneFile in os.listdir(targetDirectory):
            fullPathFile = "%s/%s"%(targetDirectory, oneFile)
            
            if os.path.isfile(fullPathFile) and fullPathFile != sys.argv[1] and fullPathFile[-4:] == ".csv":
                otherData.append(fullPathFile)    
    else:
        # Generated test...
        for oneFile in os.listdir(sys.argv[3]):
            fullPathFile = "%s/%s"%(sys.argv[3], oneFile)
            
            if os.path.isfile(fullPathFile) and fullPathFile[-4:] == ".csv":
                otherData.append(fullPathFile)
    
    mannwithn = stats.computeCloseness(sys.argv[1], generations, otherData, useMethod=score.computeScore)
    
    print("Mann-whitney p-value = %f"%mannwithn["max"][1])    