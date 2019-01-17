#!/usr/bin/env python

import TauAnalysisTools.TauAnalysisTools.tools.eos as eos

import os
import shlex
import string
import subprocess
from datetime import date

samples = {
    'ZplusJets_madgraph_signal' : {
        'datasetpath'                        : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',
        'type'                               : 'SignalMC'
    },
    'ZplusJets_madgraph_background' : {
        'datasetpath'                        : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',
        'type'                               : 'BackgroundMC'
    },
    'WplusJets_madgraph_signal' : {
        'datasetpath'                        : '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',
        'type'                               : 'SignalMC'
    },
    'WplusJets_madgraph_background' : {
        'datasetpath'                        : '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',
        'type'                               : 'BackgroundMC'
    },
    'TTplusJets_madgraph_signal' : {
        'datasetpath'                        : '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',
        'type'                               : 'SignalMC'
    },
    'TTplusJets_madgraph_background' : {
        'datasetpath'                        : '/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM',
        'type'                               : 'BackgroundMC'
    },
#    'QCDflat_pythia8' : {
#        'datasetpath'                        : '/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISpring15DR74-Asympt25nsRaw_MCRUN2_74_V9-v3/AODSIM',
#        'type'                               : 'BackgroundMC'
#    }
}

smHiggsMassPoints = [ 120,125,130 ]
for massPoint in smHiggsMassPoints:
    ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : '/GluGluHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
        'type'                               : 'SignalMC'
    }
    vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    samples[vbfSampleName] = {
        'datasetpath'                        : '/VBFHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
        'type'                               : 'SignalMC'
    }
    wplushSampleName = "wplusHiggs%1.0ftoTauTau" % massPoint
    samples[wplushSampleName] = {
        'datasetpath'                        : '/WplusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
        'type'                               : 'SignalMC'
    }
    wminushSampleName = "wminusHiggs%1.0ftoTauTau" % massPoint
    samples[wminushSampleName] = {
        'datasetpath'                        : '/WminusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v3" if massPoint == 120 else "v1"),
        'type'                               : 'SignalMC'
    }

mssmHiggsMassPoints = [ 80,90,100,110,120,130,140,160,180,200,250,300,350,400,450,500,600,700,800,900,1000,1200,1400,1500,1600,1800,2000,2300,2600,2900,3200 ]
for massPoint in mssmHiggsMassPoints:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint in [90,600,700,1400] else "v1"),
        'type'                               : 'SignalMC'
    }
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    samples[bbSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint in [100,110,160,600,1600,2000] else "v1"),
        'type'                               : 'SignalMC'
    }

ZprimeMassPoints = [ 500,1000,1500,2000,2500,3000,3500,4000,4500,5000 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/ZprimeToTauTau_M_%1.0f_TuneCUETP8M1_tauola_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint == 3000 else "v1"),
        'type'                               : 'SignalMC'
    }

WprimeMassPoints = [ 1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200,5400,5600,5800 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauNu" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/WprimeToTauNu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint in [2600,5600] else "v1"),
        'type'                               : 'SignalMC'
    }

ZprimeMassPoints = [ 5000 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoElecElec" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/ZprimeToEE_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
        'type'                               : 'BackgroundMC'
    }

WprimeMassPoints = [ 1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200,5400,5600,5800 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoElecNu" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/WprimeToENu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint in [1000,3200] else "v1"),
        'type'                               : 'BackgroundMC'
    }

sampleName = "DYtoElecElec"
samples[sampleName] = {
    'datasetpath'                    : '/DYToEE_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',
    'type'                           : 'BackgroundMC'
    }

#QCDMassPoints = [ '5to10','10to15','15to30','30to50','50to80','80to120','120to170','170to300','300to470','470to600','600to800','800to1000','1000to1400','1400to1800','1800to2400','2400to3200','3200toInf' ]
QCDMassPoints = [  ]
for massPoint in QCDMassPoints:
    sampleName = "QCD_Pt%s" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/QCD_Pt_%s_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v1" if massPoint in ['80to120','120to170','300to470','1000to1400','1400to1800','1800to2400','2400to3200','3200toInf'] else "v3" if massPoint in ['600to800'] else "v2"),
        'type'                               : 'BackgroundMC'
    }

#QCDEMenrichMassPoints = [ '15to20','20to30','30to50','50to80','80to120','120to170','170to300','300toInf' ]
QCDEMenrichMassPoints = [  ]
for massPoint in QCDEMenrichMassPoints:
    sampleName = "QCD_EMEnriched_Pt%s" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/QCD_Pt-%s_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint in ['300toInf'] else "v3" if massPoint in ['80to120'] else "v1"),
        'type'                               : 'BackgroundMC'
    }

#QCDMuenrichMassPoints = [ '15to20','20to30','30to50','50to80','80to120','120to170','170to300','300to470','470to600','600to800','800to1000','1000toInf' ]
QCDMuenrichMassPoints = [  ]
for massPoint in QCDMuenrichMassPoints:
    sampleName = "QCD_MuEnriched_Pt%s" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/QCD_Pt-%s_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-%s/AODSIM' % (massPoint, "v2" if massPoint in ['20to30','120to170','170to300','300to470','470to600','600to800','800to1000','1000toInf'] else "v1"),
        'type'                               : 'BackgroundMC'
    }

version = "antiElectronDiscr74X"

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
;sites = -samtests -group_admin -monitor -lcgadmin -cmsprod -cmsprodhi

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


from CRABClient.UserUtilities import config
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
from multiprocessing import Process

def createFilePath(filePath):
    try:
        eos.lsl(filePath)
    except IOError:
        print "filePath = %s does not yet exist, creating it." % filePath
        eos.mkdir(filePath)

def submitWithCrab(config):
    try:
        crabCommand('submit', config = config)
    except HTTPException as hte:
        print "Failed submitting task: %s" % (hte.headers)
    except ClientException as cle:
        print "Failed submitting task: %s" % (cle)

gcOptions = {
	"se_path" : "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/tauPOG/CMSSW_7_4_X/antiElectronDiscrMVATraining/ntuples/%s" % date.today()
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
        
    # create config file for Crab
    crabConfig = config()
    crabConfig.General.workArea = os.path.join(submissionDirectoryCrab, "crabdir_%s_%s" % (sampleName, version))
    #check_path(crabConfig.General.workArea)
    crabConfig.General.transferOutputs = True
    crabConfig.General.transferLogs = True
    crabConfig.General.requestName = sampleName
    crabConfig.User.voGroup = 'dcms'

    crabConfig.JobType.pluginName = 'Analysis'
    crabConfig.JobType.psetName = cfgFileName_modified
    crabConfig.JobType.allowUndistributedCMSSW = True
    crabConfig.JobType.outputFiles = [ "antiElectronDiscrMVATrainingNtuple.root" ]

    crabConfig.Data.inputDBS = 'global'
    crabConfig.Data.inputDataset = sampleOption['datasetpath']
    crabConfig.Data.splitting = 'FileBased'
    crabConfig.Data.unitsPerJob = 1
    crabConfig.Data.outLFNDirBase = '/store/user/fcolombo/higgs-kit/tauPOG/CMSSW_7_4_X/antiElectronDiscrMVATraining/ntuples/%s_test' % date.today()
    crabConfig.Data.publication = False

    crabConfig.Site.storageSite = "T2_DE_DESY"
    p = Process(target=submitWithCrab, args=(crabConfig,))
    p.start()
    p.join()


    # fill gc config options
    gcCfgFileName_modified = os.path.join(submissionDirectoryGc, os.path.basename(cfgFileName_modified))
    gcOptions["dataset"] = (gcOptions.get("dataset", "") + "\n\t" + sampleName + " : " + sampleOption['datasetpath'])
    gcOptions["nickname_config"] = (gcOptions.get("nickname_config", "") + "\n\t" + sampleName + " => " + os.path.basename(gcCfgFileName_modified))
    if not os.path.exists(os.path.dirname(gcCfgFileName_modified)): os.makedirs(os.path.dirname(gcCfgFileName_modified))
    os.system("cp " + cfgFileName_modified + " " + gcCfgFileName_modified)

gcFileName = "gc_tauIdMVATrainingNtupleProduction_%s_%s.cfg" % (version, date.today())
gcFileName_full = os.path.join(submissionDirectoryGc, gcFileName)
gcFile = open(gcFileName_full, 'w')
gcConfig = gc_template.substitute(gcOptions)
gcFile.write(gcConfig)
gcFile.close()

print("Finished building config files.")
print("Execute '~/<your-grid-control-dir>/go.py -Gc -m 10 %s' to submit grid-control jobs." % os.path.relpath(gcFileName, "."))
