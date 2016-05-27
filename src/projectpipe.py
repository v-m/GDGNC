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
import inc.gnc as gnc
import inc.baxter as baxter
import inc.utils as utils
import inc.dependencies as dl
import inc.statistics as stats
import inc.scores as score

#Change this according to the bin folder where you installed depfinder
depfind = "/home/vince/depfinder/bin"

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
        4:["org.apache"],
        5: ["org.apache"],
        81: ["org.character"],
        95: ["java.net"],
        96: ["com.ora.jsp"],
        #2: [],          #OK
        #3: [],          #??
        #51: [],         #OK?
        #57: [],         #OK
        #58: [],         #??
        #70: [],         # ??
        #71: [],         # OK?
        #78: [],         # OK?
        #7: [],         # OK?
        #27: [],        # CLEARLY OK
        #62: [],        # OK?
        #96: [],        # OK?
    }

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
            produced = dl.extractDependenciesAsXmlFile(projxml, depfind, projdir)

        # To use old generation process, remove False from condition to enable!
        if (False or not (os.path.isfile(projcdp)) or os.path.getsize(projcdp) == 0):
            # Extract class dependencies
            filt = ["!defaultpackage!", projnme]
            if(projnum in filterfor):
                for anewfilteritem in filterfor[projnum]:
                    filt.append(anewfilteritem)
            dl.proceedClasses(depfind, projxml, projcdp, filt, "internal")

            if(os.path.getsize(projcdp) == 0):
                print("Nothing generated for %s (%d)"%(projnme, projnum))

        if (not (os.path.isfile(projcdpjar)) or os.path.getsize(projcdpjar) == 0):
            inarchive = getClassesAndJarInJar(projjar, True)
            if(len(inarchive[0]) > 0):
                print(inarchive[0])

            filt = list(inarchive[1])
            filt.append("!defaultpackage!")

            if (projnum in excludefor):
                dl.proceedClasses(depfind, projxml, projcdpjar, filt, "internal", excludefor[projnum])
            else:
                dl.proceedClasses(depfind, projxml, projcdpjar, filt, "internal")


            if(os.path.getsize(projcdpjar) == 0):
                print("Nothing generated as dependency for %s (%d) using jar"%(projnme, projnum))

        G = utils.readGraphCsv(projcdpjar)
        G_n = G.number_of_nodes()
        G_e = G.number_of_edges()

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
                    #print("(%.1f%c) Skipped   %s" % ((curtogen / maxtogen) * 100, '%', genfile))
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
                        #print("(%.1f%c) Skipped   %s" % ((curtogen / maxtogen) * 100, '%', genfile))
                        pass


                q = q + 0.1
            q = 0.0
            p = p + 0.1

    print("Generations over -- starting computations")
    for fulldir in sys.argv[1:]:
        if fulldir[-1] == "/":
            fulldir = fulldir[0:-1]

        dir = fulldir[fulldir.rfind("/") + 1:]
        projnum = int(dir[0:dir.find("_")])
        projnme = dir[dir.find("_") + 1:]

        projdfn = "%s/depfind" % (fulldir)
        realproj = "%s/classes.jar.csv"%(projdfn)

        # Processing Baxter
        gendir = "%s/generations" % (projdfn)
        gendirtype = "%s/BaxterFreanModel" % (gendir)

        gamma = 0.1

        resultsbaxter = {}

        while gamma < 1.01:
            genkey = "gamma%.1f"%gamma
            gendirincr = "%s/%s"%(gendirtype, genkey)

            generations = os.listdir(gendirincr)
            for i in range(0, len(generations)):
                generations[i] = "%s/%s"%(gendirincr, generations[i])

            result = stats.computeScores(realproj, generations, useMethod=score.computeScore)
            result = result["merged"]["max"]

            resultsbaxter[genkey] = result["med"]
            #print(result["med"])

            gamma = gamma + 0.1

            #print("Delta (min)    : %.5f" % result["min"])
            #print("Delta (median) : %.5f" % result["med"]["value"])
            #print("Delta (max)    : %.5f" % result["max"])

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
                genkey = "p%.1fq%.1f" % (p,q)
                #print(genkey)
                gendirincr = "%s/%s" % (gendirtype, genkey)

                generations = os.listdir(gendirincr)
                for i in range(0, len(generations)):
                    generations[i] = "%s/%s" % (gendirincr, generations[i])

                result = stats.computeScores(realproj, generations, useMethod=score.computeScore)
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

        print("%25s | %3d || %10s | %.5f | %3d || %10s | %.5f | %3d"%(projnme, projnum, minfoundbaxter, resultsbaxter[minfoundbaxter]["value"], resultsbaxter[minfoundbaxter]["id"],minfoundgdgnc, resultsgdgnc[minfoundgdgnc]["value"], resultsgdgnc[minfoundgdgnc]["id"]))