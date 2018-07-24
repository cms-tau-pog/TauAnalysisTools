#!/usr/bin/env python


# import TauAnalysis.Configuration.tools.eos as eos
import inspect
import os
# import shlex
import pprint
import string
import subprocess

#  import time
from samplesHandles import SamplesHandles


def runcommand(commandline):
    """Run and print a specific command."""
    print(commandline)
    subprocess.call(commandline, shell=True)


# def createFilePath(filePath):
#    try:
#        eos.lsl(filePath)
#    except IOError:
#        print "filePath = %s does not yet exist, creating it." % filePath
#        eos.mkdir(filePath)
#        time.sleep(3)
#    eos.chmod(filePath, 777)


pp = pprint.PrettyPrinter(indent=4)

# ---------- Settings to touch ----------------
sh = SamplesHandles("2017MCv2")
samples = sh.samples
version = "tauId_v2_maxlikelihood_3"  # appears in jobs only
# samples = {"ggA180toTauTau": samples["ggA180toTauTau"],
# "QCDjetsPt2400to3200v1 ": samples["QCDjetsPt2400to3200v1"]}
suffix = "_maxlikelihood_3"  # "_full_v2"  # appears in crab workdir name in the end
workarea = "Summer17_25ns_2017MCv2_maxlikelihood_3"  # "Summer17_25ns_2017MCv2_partial_withraw15"
submitJobFraction = 1.00
# ----------------------------------------------

crab_template_mc = string.Template('''
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '$ui_working_dir'
config.General.workArea = '$workarea'
config.General.transferLogs = True

config.section_("User")
config.User.voGroup = 'dcms'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '$pset'

config.section_("Data")
config.Data.inputDataset = '$datasetpath'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = $files_per_job
config.Data.totalUnits = $total_files
config.Data.outLFNDirBase = '/store/user/ohlushch/TauIDMVATraining2017/$workarea/'
config.Data.publication = False
config.Data.allowNonValidInputDataset = True

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
''')

crab_template_data = string.Template('''
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '$ui_working_dir'
config.General.workArea = 'TauIDMVATraining_v1'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '$pset'

config.section_("Data")
config.Data.inputDataset = '$datasetpath'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = $lumis_per_job
config.Data.totalUnits = $total_lumis
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.outLFNDirBase = '/store/user/ohlushch/TauIDMVATraining2017/$workarea/'
config.Data.publication = False

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
''')

currentDirectory = os.getcwd()
# submissionDirectory = os.path.join(currentDirectory, "Summer17_25ns_withCutbased")
# submissionDirectory = ""
# filename = inspect.getframeinfo(inspect.currentframe()).filename
submissionDirectory = os.path.abspath((inspect.stack()[0])[1])
# if "/" in submissionDirectory:
#     submissionDirectory = "/" + submissionDirectory
print "submissionDirectory:", submissionDirectory

# print "os.path.abspath(filename)", os.path.abspath(filename)
submissionDirectory = os.path.dirname(os.path.abspath(submissionDirectory))
# submissionDirectory = submissionDirectory[1:]
print "submissionDirectory:", submissionDirectory


if len(submissionDirectory) > 0:
    submissionDirectory += "/"
configFile = submissionDirectory + "produceTauIdMVATrainingNtupleMiniAOD_cfg.py"
print "configFile:", configFile
submissionDirectory += workarea
print "submissionDirectory:", submissionDirectory
if not os.path.exists(submissionDirectory):
    os.makedirs(submissionDirectory)

executable_crab = 'crab'
# executable_crab = 'crab -GRID.dont_check_proxy 1'
# NOTE: requires to execute:
# 'voms-proxy-init -voms cms -valid 72:0'
# prior to running submitAntiMuonDiscrMVATrainingNtupleProduction_grid.py

crabCommands_create_and_submit = []
crabCommands_publish = []

for sampleName, sampleOption in samples.items():

    # create config file for cmsRun
    cfgFileName_original = "produceTauIdMVATrainingNtupleMiniAOD_cfg.py"
    print "configFile", configFile
    cfgFile_original = open(configFile, "r+")  # open(submissionDirectory + "/" + cfgFileName_original, "r+") configFile
    cfg_original = cfgFile_original.read()
    cfgFile_original.close()

    cfg_modified = cfg_original.replace("#__", "")
    cfg_modified = cfg_modified.replace("#type#", "'%s'" % sampleOption['type'])

    print "submissionDirectory:", submissionDirectory
    new_conf_name = cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (sampleName, version))
    print "cfgFileName_original", new_conf_name
    cfgFileName_modified = os.path.join(submissionDirectory + "/", new_conf_name)
    # if cfgFileName_modified[0] == "/":
    #     cfgFileName_modified = cfgFileName_modified[1:]
    print "cfgFileName_modified", cfgFileName_modified
    cfgFile_modified = open(cfgFileName_modified, "w+")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()

    # output_files = [ "tauIdMVATrainingNtuple.root" ]

    # create crab config file
    crabOptions = None
    crab_template = None
    if sampleOption['type'] == "SignalMC" or sampleOption['type'] == "BackgroundMC":
        total_files = None
        if submitJobFraction < 1.0 and sampleOption['total_files'] != -1:
            print "submitting fraction = %1.2f of event statistics for sample = %s" % (submitJobFraction, sampleName)
            total_files = int(submitJobFraction * sampleOption['total_files'])
        else:
            total_files = sampleOption['total_files']
        crabOptions = {
            'datasetpath': sampleOption['datasetpath'],
            'total_files': total_files,
            'files_per_job': sampleOption['files_per_job'],
            'pset': new_conf_name,
            'ui_working_dir': os.path.join("crabdir_%s_%s" % (sampleName, version)),
            'workarea': workarea
        }
        crab_template = crab_template_mc
    elif sampleOption['type'] == "Data":
        crabOptions = {
            'datasetpath': sampleOption['datasetpath'],
            'lumis_per_job': sampleOption['lumis_per_job'],
            'pset': new_conf_name,
            'ui_working_dir': os.path.join("crabdir_%s_%s" % (sampleName, version)),
            'workarea': workarea
        }
        crab_template = crab_template_data
    else:
        raise ValueError("Invalid sample type = %s !!" % sampleOption['type'])
    crabFileName = "crab_tauIdMVATrainingNtupleProduction_%s_%s_cfg.py" % (sampleName, version)
    crabFileName_full = os.path.join(submissionDirectory, crabFileName)
    crabFile = open(crabFileName_full, 'w')
    crabConfig = crab_template.substitute(crabOptions)
    crabFile.write(crabConfig)
    crabFile.close()

    # create output directory
    # createFilePath("/store/user/veelken/CMSSW_5_3_x/Ntuples/tauIdMVATraining/%s" % version)
    # createFilePath("/store/user/veelken/CMSSW_5_3_x/Ntuples/tauIdMVATraining/%s/%s" % (version, sampleName))

    # keep track of commands necessary to create, submit and publish crab jobs
    # not needed any more
    crabCommands_create_and_submit.append('%s submit %s' % (executable_crab, crabFileName_full))

print "submissionDirectory:", submissionDirectory
shellFileName_create_and_submit = submissionDirectory + "/" + \
    "tauIdMVATrainingNtupleProduction_crab_create_and_submit" + suffix + ".sh"
shellFile_create_and_submit = open(shellFileName_create_and_submit, "w")

for crabCommand in crabCommands_create_and_submit:
    shellFile_create_and_submit.write("%s\n" % crabCommand)
shellFile_create_and_submit.close()

print("Finished building config files. Now execute ' cd %s; source %s' to create & submit crab jobs. "
      % (submissionDirectory, shellFileName_create_and_submit))
