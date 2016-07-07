# How to use: 
# python2 keeponly.py 50 ../SF100/ $(ls ../SF100/*.csv)

import sys
import csv
import networkx as nx

nbcases = int(sys.argv[1])
path = sys.argv[2]

cases = {}

for case in sys.argv[3:]:
    with open("%s/%s"%(path, case), 'r') as csvfile:
        mygraph = nx.DiGraph()
        graphreader = csv.reader(csvfile, delimiter=';', quotechar='|')

        for graphedge in graphreader:
            mygraph.add_edge(graphedge[0], graphedge[1])

        if not(mygraph.number_of_nodes() in cases):
            cases[mygraph.number_of_nodes()] = []

        cases[mygraph.number_of_nodes()].append(case)

cpt = 0
for k in reversed(sorted(cases.keys())):
    for case in cases[k]:
        print("ln -s %s"%(case))
        cpt = cpt + 1

        if cpt >= nbcases:
            break;

    if cpt >= nbcases:
        break;
