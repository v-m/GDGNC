#####################################################################################################
#	Author: Vincenzo Musco (http://www.vmusco.com)
# This file is intended to generate dependencies files from JAR files
#####################################################################################################


import sys
import subprocess
import os
import tempfile
import utils

debug = False

os.environ['JAVA_HOME'] = "/usr"
skip_if_already_generated = False

def cleanStar(nitem):
	if(len(nitem) > 0 and nitem[len(nitem)-1] == "*"):
		nitem = nitem[0:len(nitem)-1]
	return nitem.strip()

def determinePkg(item):
	pkg = cleanStar(item.replace('\n', "").strip())
	if pkg.strip() == "":
		pkg = "!defaultpackage!"

	return pkg

def determineClass(item):
	return cleanStar(item[4:].replace('\n', "").strip())

def contentASplit(aStr,splits):
	for split in splits:
		if split in aStr:
			return True

	return False

def writeAppropriateOption(subItem,fo, nodeParent, splits, mode="internal", minPoints=2):
	nitem = cleanStar(subItem[4:].replace('\n', "").strip()).replace(", ", "+")

	if len(nitem.split("(")[0].split(".")) < minPoints + 1:
		nitem = "%s.%s"%("!defaultpackage!", nitem)

	if mode == "internal":
		keepIt = contentASplit(nitem,splits) and contentASplit(nodeParent,splits)
	elif mode == "external":
		keepIt = (contentASplit(nitem,splits) and not contentASplit(nodeParent,splits)) or (not contentASplit(nitem,splits) and contentASplit(nodeParent,splits))
	else:		# Otherwise it's both !
		keepIt = contentASplit(nitem,splits) or contentASplit(nodeParent,splits)

	if not keepIt:
		return False

	if(subItem[0:3] == "<--"):
		# If is <--
		writeThis = "%s;%s\n" % (nitem.replace(' ', '_'),nodeParent.replace(' ', '_'))
		fo.write(writeThis)
	else:
		# If is -->
		writeThis = "%s;%s\n" % (nodeParent.replace(' ', '_'),nitem.replace(' ', '_'))
		fo.write(writeThis)

	return True

def getAllJarFilesInForlderAsParameter(folder):
	cmd = "find %s -name \"*.jar\""%folder
	if debug:
		print(cmd)
	cpt = 0

	process = subprocess.Popen(cmd, shell=True,
		                   stdout=subprocess.PIPE,
		                   stderr=subprocess.PIPE)

	# wait for the process to terminate
	out, err = process.communicate()

	out = out.decode()
	outp = ""

	for apath in out.split("\n"):
		cpt = cpt + 1
		if len(outp) > 0:
			outp = "%s %s"%(outp, apath)
		else:
			outp = "%s"%(apath)

	return outp


def extractDependenciesAsXmlFile(xmlFile, dependencyFinderPath, projectFolder):
        jars = getAllJarFilesInForlderAsParameter(projectFolder)
        cmd = "%s/DependencyExtractor %s -xml -out %s"%(dependencyFinderPath,jars,xmlFile)

        subprocess.call(cmd, shell=True)
        print "Invoking: %s"%cmd
        return jars

def proceedFeatures(dependencyFinderPath, xmlFile, dstFile, splits, mode="internal"):
	cmd = "%s/DependencyReporter -show-outbounds %s -out .temp"%(dependencyFinderPath,xmlFile)
	if debug:
		print(cmd)

	if skip_if_already_generated and utils.checkFileExistance(dstFile):
		return -1,-1
	else:
		subprocess.call(cmd, shell=True)

		f = open(".temp")
		fo = open(dstFile, 'w')

		lines = f.readlines()
		f.close()

		currentPackage = ""
		currentClass = "";
		currentMethod = "";

		dropped = 0
		kept = 0

		for item in lines:
			if(item[0:12] == "            "):
				#Determine direction <-- or -->
				subItem = item[12:]
				nodeParent = currentPackage+"."+currentClass+"."+currentMethod
				if writeAppropriateOption(subItem,fo, nodeParent, splits, mode, 2):
					kept = kept + 1
				else:
					dropped = dropped + 1
			elif(item[0:8] == "        "):
				#Defines a method
				currentMethod = cleanStar(item[8:].replace('\n', "").strip()).replace(", ", "+")
			elif(item[0:4] == "    "):
				#Defines a class
				currentClass = determineClass(item)
			else:
				#Defines a package
				currentPackage = determinePkg(item)

		if kept > 0 or dropped > 0:
			ratiokept = float(kept)/(kept+dropped) * 100

		fo.close()
		subprocess.call(["rm", ".temp"])

		return kept,dropped

# Processing classes
######################
def proceedClasses(dependencyFinderPath, xmlFile, dstFile, splits, mode="internal"):
	cmd = "%s/DependencyReporter -show-outbounds -class-filter -class-scope %s -out .temp"%(dependencyFinderPath,xmlFile)
	if debug:
		print(cmd)

	if skip_if_already_generated and utils.checkFileExistance(dstFile):
		return -1,-1
	else:
		subprocess.call(cmd, shell=True)
		#subprocess.call(["%s/DependencyReporter" % dependencyFinderPath, "-show-outbounds", "-class-filter", "-class-scope", xmlFile, "-out .temp"])
		#print "    Reporting classes..."

		f = open(".temp")
		fo = open(dstFile, 'w')

		#print "\tProcessing classes..."

		lines = f.readlines()
		f.close()

		currentPackage = ""
		currentClass = "";
		dropped = 0
		kept = 0

		for item in lines:
			if(item[0:8] == "        "):
				subItem = item[8:]
				nodeParent = currentPackage+"."+currentClass
				if writeAppropriateOption(subItem,fo, nodeParent, splits, mode, 1):
					kept = kept + 1
				else:
					dropped = dropped + 1
			elif(item[0:4] == "    "):
				currentClass = determineClass(item)
			else:
				currentPackage = determinePkg(item)
		if kept > 0 or dropped > 0:
			ratiokept = float(kept)/(kept+dropped) * 100
		fo.close()
		subprocess.call(["rm", ".temp"])

		return kept,dropped

# Processing packages
######################
def proceedPackages(dependencyFinderPath, xmlFile, dstFile, splits, mode="internal"):
	cmd = "%s/DependencyReporter -show-outbounds -package-filter -package-scope %s -out .temp"%(dependencyFinderPath,xmlFile)
	if debug:
		print(cmd)

	if skip_if_already_generated and utils.checkFileExistance(dstFile):
		return -1,-1
	else:
		subprocess.call(cmd, shell=True)
		#subprocess.call(["%s/DependencyReporter" % dependencyFinderPath, "-show-outbounds", "-package-filter", "-package-scope", xmlFile, "-out .temp"])
		#print "    Reporting packages..."

		f = open(".temp")
		fo = open(dstFile, 'w')

		#print "\tProcessing packages..."

		lines = f.readlines()
		f.close()

		currentPackage = ""
		dropped = 0
		kept = 0

		for item in lines:
			if(item[0:4] == "    "):
				subItem = item[4:]
				nodeParent = currentPackage

				if subItem.strip() == "":
					subItem = "!defaultpackage!"
				if writeAppropriateOption(subItem,fo, nodeParent, splits,mode, 0):
					kept = kept + 1
				else:
					dropped = dropped + 1
			else:
				currentPackage = determinePkg(item)
		if kept > 0 or dropped > 0:
			ratiokept = float(kept)/(kept+dropped) * 100
		fo.close()
		subprocess.call(["rm", ".temp"])

		return kept,dropped
