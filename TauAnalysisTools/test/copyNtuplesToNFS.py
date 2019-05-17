#!/usr/bin/env python

import os
import subprocess
import shlex
import shutil
from samplesHandles import SamplesHandles
import pprint
pp = pprint.PrettyPrinter(indent=4)
# from python_wrappers.subprocessHandler import SubprocessHandler

import yaml
config = yaml.load(open(os.path.join(os.environ['CMSSW_BASE'], "src/TauAnalysisTools/TauAnalysisTools/test/config.yaml"), 'r'))

# renice -n 19 -u `whoami`

# generic path to dCache where ntuples are stored
inputPath = os.path.join(config['pnfs_base'], config['store_base'], config['workarea_base'] + config['version'])  # '/pnfs/desy.de/cms/tier2/store/user/ohlushch/TauIDMVATraining2018/Autum2018tauId_v1'  # "/pnfs/desy.de/cms/tier2/store/user/ohlushch/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial_withraw15"
version = config['version']  # "tauId_v1"
subfolder = ""  # for regular runs use empty string
sh = SamplesHandles("2018")
samples = sh.samples
# samples = sh.getSamplesPU17(subfolder)

# generic path to NFS where we want to copy ntuples to
outputPath = os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], 'ntuples', subfolder)  # "/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/ntuples/", subfolder)

# loop through dictionary, create directories according to sampleName
# and copy corresponding ntuples to the directory
print "Starting folder creation and copying of files. \n=====>Be mindfull and better remove old folders manualy before calling this script."

rewriteall = None
commands = []
count = 0
for sampleName, sampleOption in samples.items():
    # pp.pprint("sampleName, sampleOption:", sampleName, sampleOption)

    folderToBeCreated = outputPath + sampleName
    print "folderToBeCreated:", folderToBeCreated

    # if os.path.isdir(folderToBeCreated) and len(os.listdir(folderToBeCreated)) != 0:
    #     if rewriteall is not True:

    #         tocontinue = False

    #         if rewriteall is None:
    #             reply = None
    #             while not any(x == reply for x in ["y", "Y", "n", "N"]):
    #                 reply = raw_input('rewrite the ' + folderToBeCreated + " folder? [y/n]. Type [Y/N] to apply this to all files.")
    #                 if reply == "Y":
    #                     rewriteall = True
    #                 elif reply == "n":
    #                     print "Ignorig rewriting", folderToBeCreated
    #                     tocontinue = True
    #                     break
    #                 elif reply == "N":
    #                     rewriteall = False
    #                     tocontinue = True
    #                     break
    #                 elif reply != "y":
    #                     print ("Sorry, invalid input, try again.")

    #         if rewriteall is False or tocontinue:
    #             print "Ignoring", folderToBeCreated
    #             continue

    #     print "Overwriting ", folderToBeCreated
    #     shutil.rmtree(folderToBeCreated)

    if not os.path.isdir(folderToBeCreated):
        os.makedirs(folderToBeCreated)

    # subfolder = sampleName  #+ "_" + version
    filesToCopy = os.path.join(inputPath, sampleOption['datasetpath'].split('/')[1], '*' + sampleName + '*', "*/*/*.root")

    copyCommand = "cp -n " + filesToCopy + " " + folderToBeCreated + "/"
    args = shlex.split(copyCommand)
    args[0] = sampleName
    print copyCommand, "\n"
    # exit(1)
    subprocess.Popen(copyCommand, shell=True)  # subprocess.call(copyCommand, shell = True)
    # commands.append(copyCommand)
    # count += 1
    # if count == 3:
    #     break

# dry = False
# debug = True
# n_threads = 20
# yes_on_command = True
# silent = False
# subprocessHandler = SubprocessHandler(
#     commands=commands,
#     dry=dry,
#     debug=debug,
#     n_threads=n_threads,
#     yes_on_command=yes_on_command,
#     silent=silent,
# )
# subprocessHandler.run()

print "copy done"
