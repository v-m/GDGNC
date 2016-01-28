#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

# This script is intended to check the baxter frean model
# it tries to reproduce the figure 6 of the paper

import matplotlib
import matplotlib.pyplot as plt
import inc.degrees as deg
import inc.baxter as baxter

print('Generating graph')
g = baxter.generateBaxterFreanModel({"nb_edges": 5000}, {"gamma": 0.3})

print('Plotting')
vprog = deg.inOutTotalDegreeDistrib(g)

plt.subplot(2,1,1)
plt.yscale('log')
plt.xlim([1,50])

vprog.transformToCumulative(True)
vprog.normalizeAxis(x=False)

vprog.plotOnGraph(iin = False, linestyle="-", thickness=2)
vprog.plotOnGraph(iout = False, linestyle="--", thickness=2)

plt.subplot(2,1,2)
plt.xscale('log')
plt.yscale('log')
plt.xlim([1,50])
vprog.plotOnGraph(iin = False, linestyle="-", thickness=2)
vprog.plotOnGraph(iout = False, linestyle="--", thickness=2)

plt.show()
