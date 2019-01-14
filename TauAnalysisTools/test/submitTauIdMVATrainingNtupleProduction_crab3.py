#!/usr/bin/env python


import inspect
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

#  import time
from samplesHandles import SamplesHandles
from crab_templates import crab_template_mc, crab_template_data
# from submitHelpers import *

# ---------- Settings to touch ----------------
sh = SamplesHandles("2018")
samples = sh.samples
# samples = {"ggA180toTauTau": samples["ggA180toTauTau"],
# "QCDjetsPt2400to3200v1 ": samples["QCDjetsPt2400to3200v1"]}

version = "tauId_v1"  # tauId_v1 appears in jobs only
# suffix = "_"  # "_full_v2"  # appears in crab workdir name in the end
workarea = "Autum2018" + version  # + suffix  # "Summer17_25ns_2017MCv2_maxlikelihood_3"  # "Summer17_25ns_2017MCv2_partial_withraw15"
submitJobFraction = 1.00
cfgFile_original_name = "produceTauIdMVATrainingNtupleMiniAOD_cfg.py"
store_output_path = '/store/user/ohlushch/TauIDMVATraining2018/' + workarea + '/'
# ---------- end Settings to touch ----------------

# Construct relevant names and pathes
currentDirectory = os.getcwd()
configFile_dir = os.path.dirname(os.path.abspath(os.path.abspath((inspect.stack()[0])[1])))
configFile = os.path.join(configFile_dir, cfgFile_original_name)
submissionDirectory = os.path.join(currentDirectory, workarea)
try:
    os.makedirs(submissionDirectory)
except:
    print "the submition directory is existing. remove manually!:", submissionDirectory
    exit(1)

# Read base cmsRun config script
cfgFile_original = open(configFile, "r+")  # open(submissionDirectory + "/" + cfgFile_original_name, "r+") configFile
cfg_original = cfgFile_original.read()
cfgFile_original.close()

# Submittion script
shellFileName_create_and_submit = os.path.join(submissionDirectory, "submit_tauId_ntuplizer_crab" + ".sh")  # suffix
shellFile_create_and_submit = open(shellFileName_create_and_submit, "w")

# Print info
print 'configFile', configFile
print "submissionDirectory:", submissionDirectory

executable_crab = 'crab'
# executable_crab = 'crab -GRID.dont_check_proxy 1'
# NOTE: requires to execute:
# 'voms-proxy-init -voms cms -valid 72:0'
# prior to running submitAntiMuonDiscrMVATrainingNtupleProduction_grid.py

for sampleName, sampleOption in samples.items():

    # create config file for cmsRun
    cfg_modified = cfg_original.replace("#__", "")
    cfg_modified = cfg_modified.replace("#type#", "'%s'" % sampleOption['type'])
    cfg_modified = cfg_modified.replace("#gttype#", "'%s'" % sh.global_tag)

    #__globaltag_name = #gttype#

    new_conf_name = cfgFile_original_name.replace("_cfg.py", "_%s_%s_cfg.py" % (sampleName, workarea))
    cfgFile_modified_name = os.path.join(submissionDirectory, new_conf_name)
    cfgFile_modified = open(cfgFile_modified_name, "w+")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()

    # create crab config
    # crab_template = None
    crabOptions = {
        'datasetpath': sampleOption['datasetpath'],
        'pset': new_conf_name,
        'ui_working_dir': os.path.join("crabdir_%s_%s" % (sampleName, workarea)),
        'workarea': workarea,
        'store_output_path': store_output_path,
    }
    if sampleOption['type'] == "SignalMC" or sampleOption['type'] == "BackgroundMC":
        crab_template = crab_template_mc
        if submitJobFraction < 1.0 and sampleOption['total_files'] != -1:
            total_files = int(submitJobFraction * sampleOption['total_files'])
            print "submitting fraction = %1.2f of event statistics for sample %s = %d" % (submitJobFraction, sampleName, total_files)
        else:
            # total_files = sampleOption['total_files']
            try:
                total_files = sampleOption['total_files']
            except:
                print 'total_files not specified, taking all events '
                total_files = -1
        crabOptions.update({
            'total_files': total_files,
            'files_per_job': sampleOption['files_per_job'],
        })
    elif sampleOption['type'] == "Data":
        crab_template = crab_template_data
        crabOptions.update({'lumis_per_job': sampleOption['lumis_per_job']})
    else:
        raise ValueError("Invalid sample type = %s !!" % sampleOption['type'])

    # save crab config file
    crabFileName = "crab_tauId_ntuplizer_%s_%s_cfg.py" % (sampleName, workarea)
    crabFileName_full = os.path.join(submissionDirectory, crabFileName)
    crabFile = open(crabFileName_full, 'w')
    crabConfig = crab_template.substitute(crabOptions)
    crabFile.write(crabConfig)
    crabFile.close()

    # keep track of commands necessary to create, submit and publish crab jobs
    shellFile_create_and_submit.write("%s\n" % '%s submit %s' % (executable_crab, crabFileName_full))

shellFile_create_and_submit.close()

print("Finished building config files. Now execute ' cd %s; source %s' to create & submit crab jobs. "
      % (submissionDirectory, shellFileName_create_and_submit))
