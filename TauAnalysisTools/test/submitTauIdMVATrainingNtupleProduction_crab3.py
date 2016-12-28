#!/usr/bin/env python

#import TauAnalysis.Configuration.tools.eos as eos

import os
import shlex
import string
import subprocess
import time

samples = {
    'ZplusJets_mcatnlo' : {
        'datasetpath'                        : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    },
    'TT_powheg': {
        'datasetpath'                        : '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'PPmuXptGt20Mu15' : {
        'datasetpath'                        : '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt30to50' : {
        'datasetpath'                        : '/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt50to80' : {
        'datasetpath'                        : '/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt80to120' : {
        'datasetpath'                        : '/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt120to170' : {
        'datasetpath'                        : '/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },    
    'QCDmuEnrichedPt170to300' : {
        'datasetpath'                        : '/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt300to470' : {
        'datasetpath'                        : '/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt470to600' : {
        'datasetpath'                        : '/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt600to800' : {
        'datasetpath'                        : '/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPt800to1000' : {
        'datasetpath'                        : '/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDmuEnrichedPtGt1000' : {
        'datasetpath'                        : '/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'WplusJets_mcatnlo' : {
        'datasetpath'                        : '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsFlatPt15to7000' : {
        'datasetpath'                        : '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt30to50' : {
        'datasetpath'                        : '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt50to80' : {
        'datasetpath'                        : '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt80to120' : {
        'datasetpath'                        : '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt120to170' : {
        'datasetpath'                        : '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },        
    'QCDjetsPt170to300' : {
        'datasetpath'                        : '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt300to470' : {
        'datasetpath'                        : '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt470to600' : {
        'datasetpath'                        : '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt600to800' : {
        'datasetpath'                        : '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt800to1000' : {
        'datasetpath'                        : '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt1000to1400' : {
        'datasetpath'                        : '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt1400to1800' : {
        'datasetpath'                        : '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt1800to2400' : {
        'datasetpath'                        : '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,  
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt2400to3200' : {
        'datasetpath'                        : '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPtGt3200' : {
        'datasetpath'                        : '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDEmEnrichedPt20to30' : {
        'datasetpath'                        : '/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDEmEnrichedPt30to50' : {
        'datasetpath'                        : '/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    #'QCDEmEnrichedPt50to80' : {
    #    'datasetpath'                        : '/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',
    #    'files_per_job'                      : 1,
    #    'total_files'                        : -1,
    #    'type'                               : 'BackgroundMC'
    #},
    #'QCDEmEnrichedPt80to120' : {
    #    'datasetpath'                        : '/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/AODSIM',
    #    'files_per_job'                      : 1,
    #    'total_files'                        : -1,
    #    'type'                               : 'BackgroundMC'
    #},
    #'QCDEmEnrichedPt120to170' : {
    #    'datasetpath'                        : '/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM',
    #    'files_per_job'                      : 1,
    #    'total_files'                        : -1,
    #    'type'                               : 'BackgroundMC'
    #},
    'QCDEmEnrichedPt170to300' : {
        'datasetpath'                        : '/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDEmEnrichedPtGt300' : {
        'datasetpath'                        : '/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },


}
smHiggsMassPoints = [ 120, 125, 130 ]
for massPoint in smHiggsMassPoints:
    #ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    #samples[ggSampleName] = {
    #    'datasetpath'                        : '/GluGluHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
    #    'files_per_job'                      : 1,
    #    'total_files'                        : -1,
    #    'type'                               : 'SignalMC'
    #}
    #vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    #samples[vbfSampleName] = {
    #    'datasetpath'                        : '/VBFHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
    #    'files_per_job'                      : 1,
    #    'total_files'                        : -1,
    #    'type'                               : 'SignalMC'
    #}
    #tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
    #samples[tthSampleName] = {
    #    'datasetpath'                        : '/ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
    #    'files_per_job'                      : 1,
    #    'total_files'                        : -1,
    #    'type'                               : 'SignalMC'
    #}
    wPlusHSampleName = "WplusHHiggs%1.0ftoTauTau" % massPoint
    samples[wPlusHSampleName] = {
        'datasetpath'                        : '/WplusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }
    wMinusHSampleName = "WminusHHiggs%1.0ftoTauTau" % massPoint
    samples[wMinusHSampleName] = {
        'datasetpath'                        : '/WminusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }
    zHSampleName = "ZHHiggs%1.0ftoTauTau" % massPoint
    samples[zHSampleName] = {
        'datasetpath'                        : '/ZHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }
smHiggsMassPoints5 = [ 120, 130 ]
for massPoint in smHiggsMassPoints5:
    tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
    samples[tthSampleName] = {
        'datasetpath'                        : '/ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }
ggSampleName = "ggHiggs125toTauTau"
samples[ggSampleName] = {
    'datasetpath'                        : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
    'files_per_job'                      : 1,
    'total_files'                        : -1,
    'type'                               : 'SignalMC'
}
# currently 15 mass points available
mssmHiggsMassPoints1 = [ 90, 120, 130, 250, 300, 450, 500, 600, 1000, 1500, 2000, 2300, 2600, 2900, 3200 ]
for massPoint in mssmHiggsMassPoints1:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1, 
        'type'                               : 'SignalMC'
    }

# currently 23 mass points available
mssmHiggsMassPoints2 = [ 90, 100, 120, 140, 160, 200, 250, 350, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500, 2000, 2300, 2600, 2900, 3200 ]
for massPoint in mssmHiggsMassPoints2:
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    samples[bbSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1, 
        'type'                               : 'SignalMC'
    }

# currently 6 mass points available
ZprimeMassPoints = [ 750, 1250, 1500, 2000, 3000, 3500 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/ZprimeToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }

# currently 24 mass points available
WprimeMassPoints = [ 400, 600, 1000, 1200, 1400, 1600, 1800, 2000, 2400, 2600, 2800, 3000, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5600, 5800 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauNu" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : '/WprimeToTauNu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }

version = "tauId_v1"

submitJobFraction = 1.00

crab_template_mc = string.Template('''
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '$ui_working_dir'
config.General.workArea = 'TauIDMVATraining_v1'

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
config.Data.outLFNDirBase = '/store/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V1/'
config.Data.publication = False

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
config.Data.outLFNDirBase = '/store/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V1/'
config.Data.publication = False                                                                                                                                                  

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
''')

configFile = "produceTauIdMVATrainingNtupleMiniAOD_cfg.py"

currentDirectory    = os.getcwd()
#submissionDirectory = os.path.join(currentDirectory, "crab")
submissionDirectory = ""

executable_crab = 'crab'
#executable_crab = 'crab -GRID.dont_check_proxy 1' # NOTE: requires to execute 'voms-proxy-init -voms cms -valid 72:0' prior to running submitAntiMuonDiscrMVATrainingNtupleProduction_grid.py

def getStringRep_bool(flag):
    retVal = None
    if flag:
        retVal = "True"
    else:
        retVal = "False"
    return retVal

def runCommand(commandLine):
    print(commandLine)
    subprocess.call(commandLine, shell = True)

#def createFilePath(filePath):
#    try:
#        eos.lsl(filePath)
#    except IOError:
#        print "filePath = %s does not yet exist, creating it." % filePath
#        eos.mkdir(filePath)
#        time.sleep(3)
#    eos.chmod(filePath, 777)

crabCommands_create_and_submit = []
crabCommands_publish           = []

for sampleName, sampleOption in samples.items():
    
    # create config file for cmsRun
    cfgFileName_original = configFile
    cfgFile_original = open(cfgFileName_original, "r")
    cfg_original = cfgFile_original.read()
    cfgFile_original.close()

    cfg_modified = cfg_original.replace("#__", "")
    cfg_modified = cfg_modified.replace("#type#", "'%s'" % sampleOption['type'])

    cfgFileName_modified = os.path.join(submissionDirectory, cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (sampleName, version)))
    cfgFile_modified = open(cfgFileName_modified, "w")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()

    #output_files = [ "tauIdMVATrainingNtuple.root" ]
        
    # create crab config file
    crabOptions = None
    crab_template = None    
    if sampleOption['type'] == "SignalMC" or sampleOption['type'] == "BackgroundMC":
        total_files = None
        if submitJobFraction < 1.0 and sampleOption['total_files'] != -1:
            print "submitting fraction = %1.2f of event statistics for sample = %s" % (submitJobFraction, sampleName)
            total_files = int(submitJobFraction*sampleOption['total_files'])
        else:
            total_files = sampleOption['total_files']
        crabOptions = {
            'datasetpath'            : sampleOption['datasetpath'],
            'total_files'            : total_files,
            'files_per_job'          : sampleOption['files_per_job'],
            'pset'                   : cfgFileName_modified,
            'ui_working_dir'         : os.path.join(submissionDirectory, "crabdir_%s_%s" % (sampleName, version))
        }
        crab_template = crab_template_mc
    elif sampleOption['type'] == "Data":
        crabOptions = {
            'datasetpath'            : sampleOption['datasetpath'],
            'lumis_per_job'          : sampleOption['lumis_per_job'],
            'pset'                   : cfgFileName_modified,
            'ui_working_dir'         : os.path.join(submissionDirectory, "crabdir_%s_%s" % (sampleName, version))
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
    #createFilePath("/store/user/veelken/CMSSW_5_3_x/Ntuples/tauIdMVATraining/%s" % version)
    #createFilePath("/store/user/veelken/CMSSW_5_3_x/Ntuples/tauIdMVATraining/%s/%s" % (version, sampleName))

    # keep track of commands necessary to create, submit and publish crab jobs
    crabCommands_create_and_submit.append('%s submit %s' % (executable_crab, crabFileName_full)) #not needed any more

    
shellFileName_create_and_submit = "tauIdMVATrainingNtupleProduction_crab_create_and_submit.sh"
shellFile_create_and_submit = open(shellFileName_create_and_submit, "w")
for crabCommand in crabCommands_create_and_submit:
    shellFile_create_and_submit.write("%s\n" % crabCommand)
shellFile_create_and_submit.close()

print("Finished building config files. Now execute 'source %s' to create & submit crab jobs." % shellFileName_create_and_submit)

