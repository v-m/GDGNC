#####################################################################################################
#	Return a CSV file for histogram plotting of nodes/edges number for a list of projects
#   Synopsis: graphstats.py <nodes|edges> <csvfile1> ... <csvfilen>
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import inc.utils as utils
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

isedge = False

N = []
E = []

for project in sys.argv[1:]:
    G = utils.readGraphCsv(project)
    G_e = G.number_of_edges()
    G_n = G.number_of_nodes()
    conc = (G_e*1.0) /(G_n * (G_n - 1))

    N.append(G_n)
    E.append(G_e)

    print("%50s || %5d | %5d | %.5f"%(project, G_n, G_e, conc))

pp = PdfPages("graphstats.pdf")

plt.hist(N, 100)
plt.title("#Nodes")
plt.xlabel("#noeds")
plt.ylabel("occurences")
#plt.show()
pp.savefig()


plt.hist(E, 100)
plt.title("#Edges")
plt.xlabel("#edges")
plt.ylabel("occurences")
#plt.show()
pp.savefig()

pp.close()
#plt.show()