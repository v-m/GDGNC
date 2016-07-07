#####################################################################################################
#	Return a CSV file for histogram plotting of nodes/edges number for a list of projects
#   Synopsis: graphstats.py <nodes|edges> <csvfile1> ... <csvfilen>
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import inc.utils as utils
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy

font = {#'family': "",
        #'weight': "normal",
        'size': 16}

plt.rc('font', **font)


isedge = False

N = []
E = []

NLIM = 220 #1050
ELIM = 560 #4200

for project in sys.argv[1:]:
    G = utils.readGraphCsv(project)
    G_e = G.number_of_edges()
    G_n = G.number_of_nodes()
    conc = (G_e*1.0) /(G_n * (G_n - 1))

    N.append(G_n)
    E.append(G_e)

    print("%50s || %5d | %5d | %.5f"%(project, G_n, G_e, conc))

drop = []
for i in N:
    if i > NLIM:
        drop.append(i)

print("Dropped (>%d) %d nodes"%(NLIM, len(drop)))
print(sorted(drop))

pp = PdfPages("graphstats.pdf")

plt.hist(N, 2000)
#plt.title("Nodes")
plt.xlabel("#nodes")
plt.ylabel("Frequency")
plt.xlim(50, NLIM)
plt.ylim(0, 5)
#plt.show()
pp.savefig()
plt.close()

drop = []
for i in E:
    if i > ELIM:
        drop.append(i)

print("Dropped (>%d) %d edges"%(ELIM, len(drop)))
print(sorted(drop))

plt.hist(E, 2000, color="green")
#plt.title("Edges")
plt.xlabel("#edges")
plt.ylabel("Frequency")
plt.xlim(100, ELIM)
plt.ylim(0, 5)
#plt.show()
pp.savefig()
pp.close()
plt.close()

print("Stats")

print("Nodes: min=%d, max=%d, median=%f"%(min(N), max(N), numpy.median(N)))
print("Edges: min=%d, max=%d, median=%f"%(min(E), max(E), numpy.median(E)))