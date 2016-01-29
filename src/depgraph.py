#####################################################################################################
#	Software graph extractor entry point
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import inc.dependencies as dl
import os 

def help():
    print("\n   Synopsis: %s <xmlfile> <outfile> <mode> <granluarity> <depfinder_root> <signaturefilter ...>\n"%os.path.basename(__file__))
    print("Extract the Dependendencies using a dependency finder XML file.")
    print("<mode> indicated if only endo dependencies should be considered. To do so, use 'internal'. The opposite is obtained using 'external'. Use 'all' to consider all.")
    print("<granluarity> indicated the granularity of extracted items, can be: package, class or feature.")
    print("The result is saved in <outfile>.")
    print("<depfinder_root>  specify the absolute path to the dependency finder bin folder.")
    print("<signaturefilter ...> specify string which validate an item (according to its signature). Use '!' for default package.")

if __name__ == "__main__":
    if(len(sys.argv) < 7):
        help()
        sys.exit(0)

    xmlfile = sys.argv[1]
    outfile = sys.argv[2]
    mode = sys.argv[3]
    gran = sys.argv[4]
    depfind = sys.argv[5]
    splits = sys.argv[6:]

    for i in range(len(splits)):
        if splits[i] == "!":
            splits[i] = "!defaultpackage!"

    if not(mode == "internal" or mode == "external" or mode == "both"):
        print("Unknown mode.")
        help()
        sys.exit(1)


    if gran == "package":
        dl.proceedPackages(depfind, xmlfile, outfile, splits, mode)
    elif gran == "class":
        dl.proceedClasses(depfind, xmlfile, outfile, splits, mode)
    elif gran == "feature":
        dl.proceedFeatures(depfind, xmlfile, outfile, splits, mode)
    else:
        print("Unknown granularity !")
        help()
