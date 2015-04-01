#!/usr/bin/env python

import TauAnalysisTools.TauAnalysisTools.tools.eos as eos

import os
import shlex
import string
import subprocess
from datetime import date

samples = {
    'ZplusJets_madgraph_signal' : {
        'datasetpath'                        : '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 2829164,
        'type'                               : 'SignalMC'
    },
    'ZplusJets_madgraph_background' : {
        'datasetpath'                        : '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 2829164,
        'type'                               : 'BackgroundMC'
    },
    'WplusJets_madgraph_signal' : {
        'datasetpath'                        : '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 10017930,
        'type'                               : 'SignalMC'
    },
    'WplusJets_madgraph_background' : {
        'datasetpath'                        : '/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 10017930,
        'type'                               : 'BackgroundMC'
    },
    'TTplusJets_madgraph_signal' : {
        'datasetpath'                        : '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 25446993,
        'type'                               : 'SignalMC'
    },
    'TTplusJets_madgraph_background' : {
        'datasetpath'                        : '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM',
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 25446993,
        'type'                               : 'BackgroundMC'
    }
}
smHiggsMassPoints = [ 125 ]
for massPoint in smHiggsMassPoints:
    ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : '/GluGluToHToTauTau_M-%1.0f_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 456682,
        'type'                               : 'SignalMC'
    }
    vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    samples[vbfSampleName] = {
        'datasetpath'                        : '/VBF_HToTauTau_M-%1.0f_13TeV-powheg-pythia6/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v2/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 466354,
        'type'                               : 'SignalMC'
    }
mssmHiggsMassPoints = [  ]
for massPoint in mssmHiggsMassPoints:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 200000,
        'type'                               : 'SignalMC'
    }
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    samples[bbSampleName] = {
        'datasetpath'                        : '/SUSYBBHToTauTau_M-%1.0f_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 200000,
        'type'                               : 'SignalMC'
    }
ZprimeMassPoints = [  ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/ZprimeSSMToTauTau_M-%1.0f_TuneZ2star_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : -1,
        'type'                               : 'SignalMC'
    }
WprimeMassPoints = [  ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauNu" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/WprimeToTauNu_M-%1.0f_TuneZ2star_8TeV-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : -1,
        'type'                               : 'SignalMC'
    }
# CV: add Z' -> ee and W'-> enu background samples
ZprimeMassPoints = [  ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoElecElec" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/ZprimePSIToEE_M-%1.0f_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : -1,
        'type'                               : 'BackgroundMC'
    }
WprimeMassPoints = [  ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoElecNu" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/WprimeToENu_M-%1.0f_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : -1,
        'type'                               : 'BackgroundMC'
    }
DrellYanMassPoints = [ 50 ]
for massPoint in DrellYanMassPoints:
    sampleName = "DY%1.0ftoElecElec" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/DYToEE_M-%1.0f_Tune4C_13TeV-pythia8/Phys14DR-PU20bx25_tsg_castor_PHYS14_25_V1-v1/AODSIM' % massPoint,
        'dbs_url'                            : 'http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet',
        'events_per_job'                     : 50000,
        'total_number_of_events'             : 3070559,
        'type'                               : 'BackgroundMC'
    }

version = "antiElectronDiscr_v1_2"

submitJobFraction = 1.00

crab_template_mc = string.Template('''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein
use_server = 0

[CMSSW]
datasetpath = $datasetpath
dbs_url = $dbs_url
pset = $pset
output_file = antiElectronDiscrMVATrainingNtuple.root
total_number_of_events = $total_number_of_events
events_per_job = $events_per_job

[USER]
ui_working_dir = $ui_working_dir
return_data = 0
copy_data = 1
publish_data = 0
storage_element = T2_CH_CERN
user_remote_dir = $user_remote_dir
debug_wrapper = 1

[GRID]
##SE_white_list = T2_DE_DESY
SE_black_list = T2_US_Nebraska,T2_KR_KNU,T2_IT_Legnaro,T2_RU_JINR
''')

crab_template_data = string.Template('''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein
use_server = 0
 
[CMSSW]
datasetpath = $datasetpath
dbs_url = $dbs_url
pset = $pset
output_file = $output_file
lumi_mask = /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt
total_number_of_lumis = -1
lumis_per_job = $lumis_per_job
#runselection = 190450-190790

[USER]
ui_working_dir = $ui_working_dir
return_data = 0
copy_data = 1
publish_data = 0
storage_element = T2_CH_CERN
user_remote_dir = $user_remote_dir
debug_wrapper = 1

[GRID]
##SE_white_list = T2_DE_DESY
SE_black_list = T2_US_Nebraska,T2_KR_KNU,T2_IT_Legnaro,T2_RU_JINR
''')

gc_template = string.Template('''
[global]
module = CMSSW_Advanced

[jobs]
wall time = 24:00
in flight       = -1
in queue        = -1
shuffle = True
monitor = dashboard
queue timeout = 10:00:00

[storage]
se path = $se_path
se output files = antiElectronDiscrMVATrainingNtuple.root
se output pattern = @NICK@/@NICK@_@MY_JOBID@.root

[grid]
sites = -samtests -group_admin -monitor -lcgadmin -cern -ucsd -cmsprod -cmsprodhi -brunel

[CMSSW_Advanced]
project area = ../../../../../
events per job = 100000
se runtime      = True
software requirements = False
prepare config = True
area files += .git/COMMIT_EDITMSG .git/FETCH_HEAD .git/HEAD .git/ORIG_HEAD .git/branches .git/config .git/description .git/gitk.cache .git/hooks .git/index .git/info .git/logs .git/packed-refs .git/refs

dataset = $dataset
nickname config = $nickname_config

dataset provider= DBS3Provider
dataprovider    = DBS3Provider
''')

configFile = "produceAntiElectronDiscrMVATrainingNtuple_cfg.py"

currentDirectory    = os.getcwd()
submissionDirectoryCrab = os.path.join(currentDirectory, "crab")
submissionDirectoryGc = os.path.join(currentDirectory, "gc")

executable_crab = 'crab'
#executable_crab = 'crab -GRID.dont_check_proxy 1' # NOTE: requires to execute 'voms-proxy-init -voms cms -valid 72:0' prior to running submitAntiElectronDiscrMVATrainingNtupleProduction_grid.py

def createFilePath(filePath):
    try:
        eos.lsl(filePath)
    except IOError:
        print "filePath = %s does not yet exist, creating it." % filePath
        eos.mkdir(filePath)

crabCommands_create_and_submit = []
crabCommands_publish           = []

gcOptions = {
	"se_path" : "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/tauPOG/CMSSW_7_2_X/antiElectronDiscrMVATraining/ntuples/%s" % date.today()
}

for sampleName, sampleOption in samples.items():

    # create config file for cmsRun
    cfgFileName_original = configFile
    cfgFile_original = open(cfgFileName_original, "r")
    cfg_original = cfgFile_original.read()
    cfgFile_original.close()

    cfg_modified = cfg_original.replace("#__", "")
    cfg_modified = cfg_modified.replace("#type#", "'%s'" % sampleOption['type'])

    cfgFileName_modified = os.path.join(submissionDirectoryCrab, cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (sampleName, version)))
    if not os.path.exists(os.path.dirname(cfgFileName_modified)): os.makedirs(os.path.dirname(cfgFileName_modified))
    cfgFile_modified = open(cfgFileName_modified, "w")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()

    output_files = [ "antiElectronDiscrMVATrainingNtuple.root" ]
        
    # create crab config file
    crabOptions = None
    crab_template = None
    if sampleOption['type'] == "SignalMC" or sampleOption['type'] == "BackgroundMC":
        total_number_of_events = None
        if submitJobFraction < 1.0 and sampleOption['total_number_of_events'] != -1:
            print "submitting fraction = %1.2f of event statistics for sample = %s" % (submitJobFraction, sampleName)
            total_number_of_events = int(submitJobFraction*sampleOption['total_number_of_events'])
        else:
            total_number_of_events = sampleOption['total_number_of_events']
        crabOptions = {
            'datasetpath'            : sampleOption['datasetpath'],
            'dbs_url'                : sampleOption['dbs_url'],
            'total_number_of_events' : total_number_of_events,
            'events_per_job'         : sampleOption['events_per_job'],
            'pset'                   : cfgFileName_modified,
            'output_file'            : ",".join(output_files),
            'ui_working_dir'         : os.path.join(submissionDirectoryCrab, "crabdir_%s_%s" % (sampleName, version)),
            'user_remote_dir'        : "CMSSW_5_3_x/Ntuples/antiElectronDiscrMVATraining/%s/%s" % (version, sampleName)
        }
        crab_template = crab_template_mc
    elif sampleOption['type'] == "Data":
        crabOptions = {
            'datasetpath'            : sampleOption['datasetpath'],
            'dbs_url'                : sampleOption['dbs_url'],
            'lumis_per_job'          : sampleOption['lumis_per_job'],
            'pset'                   : cfgFileName_modified,
            'output_file'            : ",".join(output_files),
            'ui_working_dir'         : os.path.join(submissionDirectoryCrab, "crabdir_%s_%s" % (sampleName, version)),
            'user_remote_dir'        : "CMSSW_5_3_x/Ntuples/antiElectronDiscrMVATraining/%s/%s" % (version, sampleName)
        }
        crab_template = crab_template_data
    else:
        raise ValueError("Invalid sample type = %s !!" % sampleOption['type'])
    crabFileName = "crab_antiElectronDiscrMVATrainingNtupleProduction_%s_%s.cfg" % (sampleName, version)
    crabFileName_full = os.path.join(submissionDirectoryCrab, crabFileName)
    crabFile = open(crabFileName_full, 'w')
    crabConfig = crab_template.substitute(crabOptions)
    crabFile.write(crabConfig)
    crabFile.close()

    # fill gc config options
    gcCfgFileName_modified = os.path.join(submissionDirectoryGc, os.path.basename(cfgFileName_modified))
    gcOptions["dataset"] = (gcOptions.get("dataset", "") + "\n\t" + sampleName + " : " + sampleOption['datasetpath'])
    gcOptions["nickname_config"] = (gcOptions.get("nickname_config", "") + "\n\t" + sampleName + " => " + os.path.basename(gcCfgFileName_modified))
    if not os.path.exists(os.path.dirname(gcCfgFileName_modified)): os.makedirs(os.path.dirname(gcCfgFileName_modified))
    os.system("cp " + cfgFileName_modified + " " + gcCfgFileName_modified)

    # create output directory uncommenting the lines below (does not work on the NAF)
    # (in principle crab will do this, but sometimes fails with 'Permission denied' error, causing all jobs to fail with error code 60307)
    #createFilePath("/store/user/<user-name>/<path>/%s" % version)
    #createFilePath("/store/user/<user-name>/<path>/%s/%s" % (version, sampleName))

    # keep track of commands necessary to create, submit and publish crab jobs
    crabCommands_create_and_submit.append('%s -create -cfg %s' % (executable_crab, crabFileName_full))
    if 'events_per_job' in sampleOption.keys(): # MC
        events_total = None
        if sampleOption['total_number_of_events'] == -1:
            events_total = 10000000
        else:
            events_total = sampleOption['total_number_of_events']
        if (events_total / sampleOption['events_per_job']) < 450: # CV: add 10% safety margin to avoid jobs not getting submitted at all in case crab decides to create more than 500 jobs
            crabCommands_create_and_submit.append('%s -submit -c %s' % (executable_crab, crabOptions['ui_working_dir']))
        else:
            numJobs = (events_total / sampleOption['events_per_job'])
            if (events_total % sampleOption['events_per_job']) != 0:
                numJobs = numJobs + 1
            numJobs_per_submitCall = 500
            numSubmitCalls = (numJobs / numJobs_per_submitCall)
            if (numJobs % numJobs_per_submitCall) != 0:
                numSubmitCalls = numSubmitCalls + 1
            for submitIdx in range(numSubmitCalls):
                jobId_first = submitIdx*500 + 1
                jobId_last  = (submitIdx + 1)*500
                if jobId_last > numJobs:
                    jobId_last = numJobs
                crabCommands_create_and_submit.append('echo "pausing for 10 seconds before submitting next batch of jobs..."')
                crabCommands_create_and_submit.append('sleep 10')
                crabCommands_create_and_submit.append('%s -submit %i-%i -c %s' % (executable_crab, jobId_first, jobId_last, crabOptions['ui_working_dir']))
    else: # Data
        crabCommands_create_and_submit.append('%s -submit -c %s' % (executable_crab, crabOptions['ui_working_dir']))

gcFileName = "gc_tauIdMVATrainingNtupleProduction_%s_%s.cfg" % (version, date.today())
gcFileName_full = os.path.join(submissionDirectoryGc, gcFileName)
gcFile = open(gcFileName_full, 'w')
gcConfig = gc_template.substitute(gcOptions)
gcFile.write(gcConfig)
gcFile.close()
   
shellFileName_create_and_submit = "antiElectronDiscrMVATrainingNtupleProduction_crab_create_and_submit.sh"
shellFile_create_and_submit = open(shellFileName_create_and_submit, "w")
for crabCommand in crabCommands_create_and_submit:
    shellFile_create_and_submit.write("%s\n" % crabCommand)
shellFile_create_and_submit.close()

print("Finished building config files.")
print("Execute 'source %s' to create & submit crab jobs." % shellFileName_create_and_submit)
print("Execute '~/<your-grid-control-dir>/go.py -Gc -m 10 %s' to submit grid-control jobs." % os.path.relpath(gcFileName_full, "."))
