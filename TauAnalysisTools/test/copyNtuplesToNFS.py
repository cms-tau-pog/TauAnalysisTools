#!/usr/bin/env python

import os
import subprocess
import shlex
import shutil
from samplesHandles import SamplesHandles
import pprint
pp = pprint.PrettyPrinter(indent=4)

# generic path to dCache where ntuples are stored
inputPath = "/pnfs/desy.de/cms/tier2/store/user/ohlushch/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial"
version = "tauId_v1"
subfolder = "" # for regular runs use empty string
sh = SamplesHandles("2017MCv2")
samples = sh.samples
# samples = sh.getSamplesPU17(subfolder)

# generic path to NFS where we want to copy ntuples to
outputPath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/ntuples/" + subfolder + (len(subfolder) > 0 )*"/"

# loop through dictionary, create directories according to sampleName
# and copy corresponding ntuples to the directory
print "Starting folder creation and copying of files. \n=====>Be mindfull and better remove old folders manualy before calling this script."

rewriteall = None
for sampleName, sampleOption in samples.items():
    #pp.pprint("sampleName, sampleOption:", sampleName, sampleOption)

    folderToBeCreated = outputPath + sampleName
    print "folderToBeCreated:", folderToBeCreated

    if os.path.isdir(folderToBeCreated):
        if rewriteall != True:

            tocontinue = False

            if rewriteall == None:
                reply = None
                while not any(x == reply for x in ["y", "Y", "n", "N"]):
                    reply = raw_input('rewrite the ' + folderToBeCreated + " folder? [y/n]. Type [Y/N] to apply this to all files.")
                    if reply == "Y": rewriteall = True
                    elif reply == "n":
                        print "Ignorig rewriting", folderToBeCreated
                        tocontinue = True
                        break
                    elif reply == "N":
                        rewriteall = False
                        tocontinue = True
                        break
                    elif reply != "y":
                        print ("Sorry, invalid input, try again.")

            if rewriteall == False or tocontinue:
                print "Ignoring", folderToBeCreated
                continue

        print "Overwriting ", folderToBeCreated
        shutil.rmtree(folderToBeCreated)

    os.makedirs(folderToBeCreated)
    subfolder = sampleName + "_" + version
    filesToCopy = inputPath + "/" + sampleOption['datasetpath'].split('/')[1] + "/*" + subfolder + (len(subfolder) > 0 )*"*" + "/*/*/*.root"
    copyCommand = "cp " + filesToCopy + " " + folderToBeCreated + "/"
    args = shlex.split(copyCommand)
    args[0] = sampleName
    print copyCommand, "\n"
    subprocess.Popen(copyCommand, shell = True)#subprocess.call(copyCommand, shell = True)

print "submission done"
