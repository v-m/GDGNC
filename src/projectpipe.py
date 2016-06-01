#####################################################################################################
#	Processing projects passed as arguments
#   Working with the SF100 dataset (http://www.evosuite.org/experimental-data/sf100/)
#	Author: Vincenzo Musco (http://www.vmusco.com)
#####################################################################################################

import os
import zipfile
import shutil
import time
import sys
import csv
import inc.gnc as gnc
import inc.baxter as baxter
import inc.utils as utils
import inc.dependencies as dl
import inc.statistics as stats
import inc.scores as score

# Script Configuration

#Change this according to the bin folder where you installed depfinder
DEPFIND = "/home/vince/depfinder/bin"

READJAR_PROCESS1 = False
READJAR_PROCESS2 = False

OPTIM_GENERATION = False
COMPR_GENERATION = "/home/vince/Experiments/SF100/allresults.csv"   #Put None to disable this part

COMPUTEOPERATION = "optimize" # Set to "compare", "optimize" or None

filterfor = {
    72: ["bcry"],
    10: ["simulator"],
    89: ["jigl"],
    22: ["yui"],
    87: ["jaw"],
    17: ["allenstudio"],
    69: ["macaw"],
    80: ["wheel"],
    77: ["ioproject"],
    19: ["JMCA"],
    14: ["objectmentors"],
    11: ["momed"],
    39: ["beiri22"],
    84: ["ifxfv3"],
    25: ["jniinchi"],
    79: ["fortbattleplayer"],
    90: ["parseargs"],
    34: ["sbml2"],
    78: ["lts"],
    38: ["framework"],
    88: ["progra.charting"],
    86: ["atrobots"],
    8: ["unice.gfarce"],
    1: ["ib.client"],
    63: ["de.paragon.explorer"],
    16: ["com.rakegroup"],
    98: ["Joshua"],
    30: ["ch.bluepenguin"],
    68: ["bible"],
    56: ["handball"],
    76: ["dash"],
    91: ["com.jstevh"],
    73: ["osa.ora"],
    29: ["jahuwaldt.plot", "apbs_mem_gui"],
    66: ["exolab.jms"],
    64: ["pingtimeout.jtail"],
    54: ["com.gbshape.dbe"],
    49: ["bierse"],
    21: ["oasis", "google"],
    70: ["edu.uiuc.ndiipp.hubandspoke"],
    99: ["Newzgrabber"],
    67: ["gaeappmanager"],
    27: ["map", "module", "state", "util"],
    92: ["jcvi"],
    7: ["com.hf.sfm"],
    33: ["com.pmdesigns.jvc"],
    61: ["fi.vtt.probeframework"],
    65: ["com.gotoservers", "com.isnetworks", "mindbright"],
    97: ["src"],
    57: ["client", "common", "db", "logging", "messages", "server", "sound"],
    44: ["statsbiblioteket"]
}
excludefor = {
    100: ["java.awt"],
    27: ["java.util"],
    47: ["javax.swing", "org.netbeans"],
    4: ["org.apache"],
    5: ["org.apache"],
    81: ["org.character"],
    95: ["java.net"],
    96: ["com.ora.jsp"],
    # 2: [],          #OK
    # 3: [],          #??
    # 51: [],         #OK?
    # 57: [],         #OK
    # 58: [],         #??
    # 70: [],         # ??
    # 71: [],         # OK?
    # 78: [],         # OK?
    # 7: [],         # OK?
    # 27: [],        # CLEARLY OK
    # 62: [],        # OK?
    # 96: [],        # OK?
}

def getClassesAndJarInJar(jar, reccursive=True):
    print("Treating %s"%jar)
    classes = []
    jars = []

    zf = zipfile.ZipFile(jar, 'r')
    try:
        lst = zf.infolist()
        for zi in lst:
            fn = zi.filename
            if fn.endswith('.class'):
                clazz = fn.replace("/", ".")[0:-6]
                classes.append(clazz)
            elif fn.endswith('.jar'):
                if(reccursive):
                    workingfolder = "/tmp/.gdgnctemp_%d"%int(round(time.time() * 1000))
                    zf.extract(fn, workingfolder)
                    subinarchive = getClassesAndJarInJar("%s/%s"%(workingfolder,fn), False)
                    shutil.rmtree(workingfolder)
                    classes.extend(subinarchive[1])
                    jars.extend(subinarchive[0])
                jars.append(fn)
    finally:
        zf.close()

    return [set(jars), set(classes)]

if __name__ == "__main__":

    if COMPUTEOPERATION is None or len(COMPUTEOPERATION) <= 0:
        pass
    elif COMPUTEOPERATION[0] == "o" or COMPUTEOPERATION[0] == "O":
        print("num;projet;nodes;edges;density;baxter_param;baxter_score;baxter_id;gdgnc_param;gdgnc_score;gdgnc_id")
    elif COMPUTEOPERATION[0] == "c" or COMPUTEOPERATION[0] == "C":
        # projet   nodes edges avg_delta_baxter avg_delta_gd_gnc p_value Cohen_effect_size
        print("num;projet;nodes;edges;density;avg_delta_baxter;avg_delta_gd_gnc;p_value;Cohen_effect_size")

    for fulldir in sys.argv[1:]:
        if fulldir[-1] == "/":
            fulldir = fulldir[0:-1]

        dir = fulldir[fulldir.rfind("/")+1:]
        projnum = int(dir[0:dir.find("_")])
        projnme = dir[dir.find("_") + 1:]

        projjar = "%s/%s.jar"%(fulldir, projnme)

        if(not(os.path.isfile(projjar))):
            for f in os.listdir(fulldir):
                if ".jar" in f:
                    projjar = "%s/%s"%(fulldir, f)

        projdfn = "%s/depfind" % (fulldir)
        if(not(os.path.isdir(projdfn))):
            os.mkdir(projdfn)
        projxml = "%s/dep.xml"%(projdfn)
        projcdp = "%s/classes.csv"%(projdfn)
        projcdpjar = "%s/classes.jar.csv"%(projdfn)


        #print("=== %s (%d) ==="%(projnme, projnum))

        if(not(os.path.isfile(projxml))):
            # Extract the xml file
            produced = dl.extractDependenciesAsXmlFile(projxml, DEPFIND, projdir)

        # To use old generation process, remove False from condition to enable!
        if (READJAR_PROCESS1 or not (os.path.isfile(projcdp)) or os.path.getsize(projcdp) == 0):
            # Extract class dependencies
            filt = ["!defaultpackage!", projnme]
            if(projnum in filterfor):
                for anewfilteritem in filterfor[projnum]:
                    filt.append(anewfilteritem)
            dl.proceedClasses(DEPFIND, projxml, projcdp, filt, "internal")

            if(os.path.getsize(projcdp) == 0):
                print("Nothing generated for %s (%d)"%(projnme, projnum))

        if (READJAR_PROCESS2 or not (os.path.isfile(projcdpjar)) or os.path.getsize(projcdpjar) == 0):
            inarchive = getClassesAndJarInJar(projjar, True)
            if(len(inarchive[0]) > 0):
                print(inarchive[0])

            filt = list(inarchive[1])
            filt.append("!defaultpackage!")

            if (projnum in excludefor):
                dl.proceedClasses(DEPFIND, projxml, projcdpjar, filt, "internal", excludefor[projnum])
            else:
                dl.proceedClasses(DEPFIND, projxml, projcdpjar, filt, "internal")


            if(os.path.getsize(projcdpjar) == 0):
                print("Nothing generated as dependency for %s (%d) using jar"%(projnme, projnum))

        G = utils.readGraphCsv(projcdpjar)
        G_n = G.number_of_nodes()
        G_e = G.number_of_edges()
        G_d = float(G_e) / (G_n * (G_n - 1))

        if OPTIM_GENERATION:
            # Generate 30 graphs with similar features
            ## For Baxter
            gamma = 0.1

            gendir = "%s/generations"%(projdfn)
            if(not(os.path.isdir(gendir))):
                os.mkdir(gendir)

            gendirtype = "%s/BaxterFreanModel"%(gendir)
            if (not (os.path.isdir(gendirtype))):
                os.mkdir(gendirtype)

            while gamma < 1.01:
                gendirincr = "%s/gamma%.1f"%(gendirtype, gamma)
                if (not (os.path.isdir(gendirincr))):
                    os.mkdir(gendirincr)

                for cpt in range(0, 30, 1):
                    genfile = "%s/%d.csv"%(gendirincr, cpt)

                    if not(os.path.isfile(genfile)):
                        B = baxter.generateBaxterFreanModel(nbs={"nb_edges": G_e}, proba={"gamma": gamma})
                        utils.writeGraphCsv(B, genfile)
                        print("Saved   %s" % (genfile))
                    else:
                        #print("Skipped   %s" % (genfile))
                        pass


                gamma = gamma + 0.1

            ## For GDGNC
            p = 0.0
            q = 0.0

            gendirtype = "%s/GeneralizedDoubleGNC"%(gendir)
            if (not (os.path.isdir(gendirtype))):
                os.mkdir(gendirtype)

            while p < 1.01:
                while q < 1.01:
                    gendirincr = "%s/p%.1fq%.1f" % (gendirtype, p, q)
                    if (not (os.path.isdir(gendirincr))):
                        os.mkdir(gendirincr)

                    for cpt in range(0, 30, 1):
                        genfile = "%s/%d.csv" % (gendirincr, cpt)

                        if not (os.path.isfile(genfile)):
                            G2 = gnc.generateGeneralizedDoubleGNC(nbs={"nb_nodes": G_n}, proba={"p": p, "q": q})
                            utils.writeGraphCsv(G2, genfile)
                            print("Saved   %s" % (genfile))
                        else:
                            #print("Skipped   %s" % (genfile))
                            pass


                    q = q + 0.1
                q = 0.0
                p = p + 0.1

        if not COMPR_GENERATION is None:
            with open(COMPR_GENERATION, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')

                concerned = None
                for row in csvreader:
                    if len(row) < 10:
                        continue

                    if int(row[0]) == projnum and row[1] == projnme:
                        concerned = row
                        break

                #print(concerned)
                if not concerned is None:
                    baxterfolder = "%s/tests/BaxterFreanModel" % (projdfn)
                    gdgncfolder = "%s/tests/GeneralizedDoubleGNC" % (projdfn)

                    gamma = float(concerned[5][-3:])
                    pparam = float(concerned[8][1:4])
                    qparam = float(concerned[8][5:8])

                    if not (os.path.isdir(baxterfolder)):
                        os.mkdir(baxterfolder)

                    if not (os.path.isdir(gdgncfolder)):
                        os.mkdir(gdgncfolder)

                    # Generate Baxter 30 graphs
                    for cpt in range(0, 30, 1):
                        genfile = "%s/%d.csv" % (baxterfolder, cpt)

                        if not (os.path.isfile(genfile)):
                            B = baxter.generateBaxterFreanModel(nbs={"nb_edges": G_e}, proba={"gamma": gamma})
                            utils.writeGraphCsv(B, genfile)
                            print("Saved   %s" % (genfile))
                        else:
                            #print("Skipped   %s" % (genfile))
                            pass

                    for cpt in range(0, 30, 1):
                        genfile = "%s/%d.csv" % (gdgncfolder, cpt)

                        if not (os.path.isfile(genfile)):
                            G2 = gnc.generateGeneralizedDoubleGNC(nbs={"nb_nodes": G_n}, proba={"p": pparam, "q": qparam})
                            utils.writeGraphCsv(G2, genfile)
                            print("Saved   %s" % (genfile))
                        else:
                            #print("Skipped   %s" % (genfile))
                            pass

        if COMPUTEOPERATION is None or len(COMPUTEOPERATION) <= 0:
            pass
        elif COMPUTEOPERATION[0] == "o" or COMPUTEOPERATION[0] == "O":
            # Processing Baxter
            gendir = "%s/generations" % (projdfn)
            gendirtype = "%s/BaxterFreanModel" % (gendir)

            gamma = 0.1

            resultsbaxter = {}

            while gamma < 1.01:
                genkey = "gamma%.1f" % gamma
                gendirincr = "%s/%s" % (gendirtype, genkey)

                generations = os.listdir(gendirincr)
                for i in range(0, len(generations)):
                    generations[i] = "%s/%s" % (gendirincr, generations[i])

                result = stats.computeScoresAndSummary(projcdpjar, generations, useMethod=score.computeScore)
                result = result["merged"]["max"]

                resultsbaxter[genkey] = result["med"]
                # print(result["med"])

                gamma = gamma + 0.1

                # print("Delta (min)    : %.5f" % result["min"])
                # print("Delta (median) : %.5f" % result["med"]["value"])
                # print("Delta (max)    : %.5f" % result["max"])

            minfoundbaxter = None

            for e in resultsbaxter:
                if minfoundbaxter is None or resultsbaxter[e]["value"] < resultsbaxter[minfoundbaxter]["value"]:
                    minfoundbaxter = e

            p = 0.0
            q = 0.0

            resultsgdgnc = {}

            gendirtype = "%s/GeneralizedDoubleGNC" % (gendir)

            while p < 1.01:
                while q < 1.01:
                    genkey = "p%.1fq%.1f" % (p, q)
                    # print(genkey)
                    gendirincr = "%s/%s" % (gendirtype, genkey)

                    generations = os.listdir(gendirincr)
                    for i in range(0, len(generations)):
                        generations[i] = "%s/%s" % (gendirincr, generations[i])

                    result = stats.computeScoresAndSummary(projcdpjar, generations, useMethod=score.computeScore)
                    result = result["merged"]["max"]

                    resultsgdgnc[genkey] = result["med"]
                    # print(result["med"])

                    q = q + 0.1
                q = 0.0
                p = p + 0.1

                # print("Delta (min)    : %.5f" % result["min"])
                # print("Delta (median) : %.5f" % result["med"]["value"])
                # print("Delta (max)    : %.5f" % result["max"])

            minfoundgdgnc = None

            for e in resultsgdgnc:
                if minfoundgdgnc is None or resultsgdgnc[e]["value"] < resultsgdgnc[minfoundgdgnc]["value"]:
                    minfoundgdgnc = e

            print("%d;%s;%d;%d;%f;%s;%f;%d;%s;%f;%d" % (projnum,projnme,G_n,G_e,G_d,minfoundbaxter,resultsbaxter[minfoundbaxter]["value"],resultsbaxter[minfoundbaxter]["id"],minfoundgdgnc,resultsgdgnc[minfoundgdgnc]["value"],resultsgdgnc[minfoundgdgnc]["id"]))
        elif COMPUTEOPERATION[0] == "c" or COMPUTEOPERATION[0] == "C":
            baxterfolder = "%s/tests/BaxterFreanModel" % (projdfn)
            gdgncfolder = "%s/tests/GeneralizedDoubleGNC" % (projdfn)

            BG = []
            GG = []

            Bgenerations = os.listdir(baxterfolder)
            for i in range(0, len(Bgenerations)):
                Bgenerations[i] = "%s/%s" % (baxterfolder, Bgenerations[i])

            bscores = stats.computeScores(projcdpjar, Bgenerations, useMethod=score.computeScore)
            bresult = stats.computeScoresSummary(bscores)
            bresult = bresult["merged"]["max"]

            Ggenerations = os.listdir(gdgncfolder)
            for i in range(0, len(Ggenerations)):
                Ggenerations[i] = "%s/%s" % (gdgncfolder, Ggenerations[i])

            gscores = stats.computeScores(projcdpjar, Ggenerations, useMethod=score.computeScore)
            gresult = stats.computeScoresSummary(gscores)
            gresult = gresult["merged"]["max"]

            mw2 = stats.computeClosenessBetweenGenerationsOptimized(Bgenerations, Ggenerations, G)
            cohend = stats.cohen_d(bscores["mergedscores"]["max"], gscores["mergedscores"]["max"])

            #projet   nodes edges avg_delta_baxter avg_delta_gd_gnc p_value Cohen_effect_size
            params = (projnum,projnme,G_n,G_e,G_d,bresult["avg"]["value"],gresult["avg"]["value"],mw2["max"].pvalue,cohend)
            print("%d;%s;%d;%d;%f;%f;%f;%f;%f"%params)