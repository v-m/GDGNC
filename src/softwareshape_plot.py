#####################################################################################################
#	Plot the cumulative degree distributions of software
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import sys
import os
import inc.utils as utils
import inc.degrees as dl
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

graphfonttitles = 10
graphfontaxis = 1
graphfontlegend = 10

distintscolors = ("#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
        "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
        "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
        "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
        "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
        "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
        "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
        "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
        "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
        "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
        "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
        "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
        "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
        "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
        "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
        "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58")

def help():
    print("\n   Synopsis: %s <graphplotfile> <softwarefolder ...>\n"%os.path.basename(__file__))
    
    
if __name__ == "__main__":
    if(len(sys.argv) < 3):
        help()
        sys.exit(0)
        
    programsToProcess = sys.argv[2:]

    print("plot ",programsToProcess)
    targetFile = sys.argv[1]

    i = 0
    
    for program in programsToProcess:
        progname = program[program.rindex("/")+1:-4]
        
	prog = utils.readGraphCsv(program)
	vprog = dl.inOutTotalDegreeDistrib(prog)
	vprog.transformToCumulative(True)
	vprog.normalizeAxis(False, True)
	ax = plt.subplot(1,1,1)
	plt.figure(1)
	vprog.plotOnGraph(iin = True, iout = False, thickness=.5, color=distintscolors[i], label=progname, linestyle="-", marker="")
	plt.figure(2)
	vprog.plotOnGraph(iin = False, iout = True, thickness=.5, color=distintscolors[i], label=progname, linestyle="-", marker="")
	i = i + 1

    for fig in range(2):
	plt.figure(fig+1)
	ax = plt.subplot(1,1,1)
	#handles, labels = ax.get_legend_handles_labels()
	#ax.legend(handles, labels)

	#plt.xlim([1,50])
	plt.ylim([0.001,1.0])
	ax.set_xscale('log')
	ax.set_yscale('log')
	plt.xlabel("%s-degrees"%("In" if fig == 0 else "Out"))
	plt.ylabel("Cumulative frequency")
	plt.gcf().set_size_inches(10,6)
	plt.savefig('%s%s.pdf'%(targetFile, "In" if fig == 0 else "Out"))
	#pp.savefig()
	
    #pp.close()