#####################################################################################################
#	Uses Dependency Finder to obtain software dependencies in XML form
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import inc.dependencies as dl
import os

def help():
    print("\n   Synopsis: %s <soft> <outfile> <depfinder_root>\n"%os.path.basename(__file__))
    print("Extract the Dependency Finder XML dependency graph file for the program pointed by <soft>.")
    print("The output is produced in [outfile] if specified or to ./dep.xml")
    print("<depfinder_root>  specify the absolute path to the dependency finder bin folder.")

if __name__ == "__main__":
    if(len(sys.argv) < 4):
        help()
        sys.exit(0)

    proceedFiles = sys.argv[1]
    outfile = sys.argv[2]
    depfind = sys.argv[3]

    produced = dl.extractDependenciesAsXmlFile(outfile,depfind,proceedFiles)

    print("Input project folder is %s"%proceedFiles)
    print("XML file has been generated in %s"%outfile)
    print("It includes following JARS:")

    for jar in produced.split(" "):
        if(jar.strip()==""):
            continue

        print("\t- %s"%jar[len(proceedFiles):])
