#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import os
import inc.kstest as kstest
import inc.utils as utils
import inc.degrees as dl
import inc.scores as score
from scipy.stats import ks_2samp

def help():
    print("\n   Synopsis: %s <softwaregraph1> ... <softwaregraphn>\n"%os.path.basename(__file__))

    
if __name__ == "__main__":
    if(len(sys.argv) == 1):
        help()
        sys.exit(0)
        
    programsToProcess = []

    programsToProcess = sys.argv[1:]
    #while targetFolder[-1] == "/":
    #    targetFolder = targetFolder[0:-1]
    
    #for oneFile in os.listdir(targetFolder):
    #for oneFile in os.listdir(targetFolder):
    #    fullPathFile = "%s/%s"%(targetFolder, oneFile)
    #
    #    if os.path.isfile(fullPathFile) and fullPathFile[-4:] == ".csv":
    #        programsToProcess.append(fullPathFile)
            
    stats = [ [0, 0, 0, 0], [0, 0, 0, 0]]

    print("%78s%s"%("", 35*"*"))
    print("%77s |              p-value            |"%"")
    print("*"*113)
    print("%30s | %30s | %3s | %8s | %8s > %3s | %8s > %3s | %8s > %3s |"%("Prog 1", "Prog 2", "Dir", "Ks Stat", "Crit val", "Rej", "python", "Rej", "vince", "Rej"))
    print("*"*113)

    gran = kstest.ALPHA001
    for forIn in [True, False]:
        for program1 in programsToProcess:
            for program2 in programsToProcess:
                if program1 == program2 or program1 > program2:
                    continue
                #prog1name = program1[program1.rindex("/")+1:-4]
                #prog2name = program2[program2.rindex("/")+1:-4]
                
                prog1 = utils.readGraphCsv(program1)
                prog2 = utils.readGraphCsv(program2)
                vprog1 = dl.inOutTotalDegreeDistrib(prog1)
                vprog2 = dl.inOutTotalDegreeDistrib(prog2)
                            
                fsrc1 = score.unshield(vprog1, forIn)
                fsrc2 = score.unshield(vprog2, forIn)
                            
                ret = ks_2samp(fsrc1, fsrc2)
                ret2 = kstest.ks(fsrc1, fsrc2, Int=True)
                criticalVal = kstest.calculateCriticalValue(fsrc1, fsrc2, gran[1])
                            
                rejectCrtVal = ret2[0]>criticalVal
                rejectPython = ret[1]<gran[0] 
                rejectVince = ret2[1]<gran[0]
                            
                print("%30s | %30s | %3s | %f | %f > %3s | %f > %3s | %f > %3s |"%(program1[-40:-10], program2[-40:-10], "IN" if forIn else "OUT", ret2[0], criticalVal, ("YES" if rejectCrtVal else "NO"), ret[1], ("YES" if rejectPython else "NO"), ret2[1], ("YES" if rejectVince else "NO")))
                            
                if rejectCrtVal:
                    stats[forIn][0] = stats[forIn][0] + 1
                            
                if rejectPython:
                    stats[forIn][1] = stats[forIn][1] + 1
                            
                if rejectVince:
                    stats[forIn][2] = stats[forIn][2] + 1
                                    
                stats[forIn][3] = stats[forIn][3] + 1
        print("*"*113)
            
    print("Results")
    print("*******")

    print("IN")
    print("Rejecting with critical value: %d/%d"%(stats[1][0], stats[1][3]))
    print("Rejecting with Python stat: %d/%d"%(stats[1][1], stats[1][3]))
    print("Rejecting with Vince stat: %d/%d"%(stats[1][2], stats[1][3]))
    print("")

    print("OUT")
    print("Rejecting with critical value: %d/%d"%(stats[0][0], stats[0][3]))
    print("Rejecting with Python stat: %d/%d"%(stats[0][1], stats[0][3]))
    print("Rejecting with Vince stat: %d/%d"%(stats[0][2], stats[0][3]))