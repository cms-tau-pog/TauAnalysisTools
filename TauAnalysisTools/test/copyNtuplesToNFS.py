#!/usr/bin/env python

import os
import subprocess
import shlex
import shutil

# generic path to dCache where ntuples are stored
inputPath = "/pnfs/desy.de/cms/tier2/store/user/ohlushch/TauIDMVATraining2016/Summer17_25ns_V1_allPhotonsCut"

# generic path to NFS where we want to copy ntuples to
outputPath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_V1_allPhotonsCut/ntuples/"

# more or less a copy of the samples in submitTauIdMVATrainingNtupleProduction_crab3.py
# with reduced information

samples = {
    'ZplusJets_madgraph' : {
        'datasetpath'                        : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',#same /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    },
    'TT_powheg': {
        'datasetpath'                        : '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'TTJets': {
        'datasetpath'                        : '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
   # 'PPmuXptGt20Mu15' : {
   #     'datasetpath'                        : '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-FlatPU0to70_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
   #     'files_per_job'                      : 1,
   #     'total_files'                        : -1,
   #     'type'                               : 'BackgroundMC'
   # },
   'QCDmuEnrichedPt15to20' : {
       'datasetpath'                        : '/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt20to30' : {
       'datasetpath'                        : '/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt30to50' : {
       'datasetpath'                        : '/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt50to80' : {
       'datasetpath'                        : '/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt80to120' : {
       'datasetpath'                        : '/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt120to170' : {
       'datasetpath'                        : '/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt170to300' : {
       'datasetpath'                        : '/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt300to470' : {
       'datasetpath'                        : '/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt470to600' : {
       'datasetpath'                        : '/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt600to800' : {
       'datasetpath'                        : '/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDmuEnrichedPt800to1000' : {
       'datasetpath'                        : '/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   #? 'QCDmuEnrichedPtGt1000' : {
   #     'datasetpath'                        : '/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM',
   #     'files_per_job'                      : 1,
   #     'total_files'                        : -1,
   #     'type'                               : 'BackgroundMC'
   # },

    'WplusJets_madgraph' : {
        'datasetpath'                        : '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'# /WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_SUS01_92X_upgrade2017_realistic_v10-v1/MINIAODSIM
    },
    #?    'QCDjetsFlatPt15to7000' : {
    #        'datasetpath'                        : '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
    #        'files_per_job'                      : 1,
    #        'total_files'                        : -1,
    #        'type'                               : 'BackgroundMC'
    #/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer17MiniAOD-FlatPU0to70_magnetOn_92X_upgrade2017_realistic_v10-v1/MINIAODSIM
    #/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIISummer17MiniAOD-NoPU_magnetOn_92X_upgrade2017_realistic_v10-v1/MINIAODSIM

    #    },
    'QCDjetsPt30to50' : {
        'datasetpath'                        : '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    # 'QCDjetsPt50to80' : {
    #     'datasetpath'                        : '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM',
    #     'files_per_job'                      : 1,
    #     'total_files'                        : -1,
    #     'type'                               : 'BackgroundMC'
    # },
    'QCDjetsPt80to120' : {
        'datasetpath'                        : '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt120to170' : {
        'datasetpath'                        : '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt170to300' : {
        'datasetpath'                        : '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt300to470' : {
        'datasetpath'                        : '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt470to600' : {
        'datasetpath'                        : '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt600to800' : {
        'datasetpath'                        : '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt800to1000' : {
        'datasetpath'                        : '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt1000to1400' : {
        'datasetpath'                        : '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPt1400to1800' : {
        'datasetpath'                        : '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
   'QCDjetsPt1800to2400' : {
       'datasetpath'                        : '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
    'QCDjetsPt2400to3200' : {
        'datasetpath'                        : '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
    'QCDjetsPtGt3200' : {
        'datasetpath'                        : '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8',
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'BackgroundMC'
    },
   'QCDEmEnrichedPt15to20' : {
       'datasetpath'                        : '/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPt20to30' : {
       'datasetpath'                        : '/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPt30to50' : {
       'datasetpath'                        : '/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPt50to80' : {
       'datasetpath'                        : '/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPt80to120' : {
       'datasetpath'                        : '/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPt120to170' : {
       'datasetpath'                        : '/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPt170to300' : {
       'datasetpath'                        : '/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   },
   'QCDEmEnrichedPtGt300' : {
       'datasetpath'                        : '/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8',
       'files_per_job'                      : 1,
       'total_files'                        : -1,
       'type'                               : 'BackgroundMC'
   }
}

#smHiggsMassPoints = [ 120, 125, 130 ]
#for massPoint in smHiggsMassPoints:
#    #ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
#    #samples[ggSampleName] = {
#    #    'datasetpath'                        : '/GluGluHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
#    #    'files_per_job'                      : 1,
#    #    'total_files'                        : -1,
#    #    'type'                               : 'SignalMC'
#    #}
#    #vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
#    #samples[vbfSampleName] = {
#    #    'datasetpath'                        : '/VBFHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
#    #    'files_per_job'                      : 1,
#    #    'total_files'                        : -1,
#    #    'type'                               : 'SignalMC'
#    #}
#    wPlusHSampleName = "WplusHHiggs%1.0ftoTauTau" % massPoint
#    samples[wPlusHSampleName] = {
#        'datasetpath'                        : '/WplusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
#        'files_per_job'                      : 1,
#        'total_files'                        : -1,
#        'type'                               : 'SignalMC'
#    }
#    wMinusHSampleName = "WminusHHiggs%1.0ftoTauTau" % massPoint
#    samples[wMinusHSampleName] = {
#        'datasetpath'                        : '/WminusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
#        'files_per_job'                      : 1,
#        'total_files'                        : -1,
#        'type'                               : 'SignalMC'
#    }
#    zHSampleName = "ZHHiggs%1.0ftoTauTau" % massPoint
#    samples[zHSampleName] = {
#        'datasetpath'                        : '/ZHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
#        'files_per_job'                      : 1,
#        'total_files'                        : -1,
#        'type'                               : 'SignalMC'
#    }
#smHiggsMassPoints2 = [ 120, 130 ]
#for massPoint in smHiggsMassPoints2:
#   tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
#   samples[tthSampleName] = {
#       'datasetpath'                            : '/ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
#       'files_per_job'                          : 1,
#       'total_files'                            : -1,
#       'type'                                   : 'SignalMC'
#   }
#tthSampleName = "tthHiggs125toTauTau"
#samples[tthSampleName] = {
#    'datasetpath'                            : '/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext4-v1/MINIAODSIM',
#    'files_per_job'                          : 1,
#    'total_files'                            : -1,
#    'type'                                   : 'SignalMC'
#}
#ggSampleName = "ggHiggs130toTauTau"
#samples[ggSampleName] = {
#    'datasetpath'                        : '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
#    'files_per_job'                      : 1,
#    'total_files'                        : -1,
#    'type'                               : 'SignalMC'
#}

ggSampleName = "ggHiggs125toTauTau"
samples[ggSampleName] = {
   'datasetpath'                        : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8',
   'files_per_job'                      : 1,
   'total_files'                        : -1,
   'type'                               : 'SignalMC'
}

vbfSampleName = "vbfHiggs125toTauTau"
samples[vbfSampleName] = {
   'datasetpath'                        : '/VBFHToTauTau_M125_13TeV_powheg_pythia8',
   'files_per_job'                      : 1,
   'total_files'                        : -1,
   'type'                               : 'SignalMC'
}

# currently 23 mass points available
mssmHiggsMassPoints1 = [ 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
for massPoint in mssmHiggsMassPoints1:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }

# currently 23 mass points available
mssmHiggsMassPoints3 = [ 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
for massPoint in mssmHiggsMassPoints3:
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    samples[bbSampleName] = {
        'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8' % massPoint,
        'files_per_job'                      : 1,
        'total_files'                        : -1,
        'type'                               : 'SignalMC'
    }

# currently 9 mass points available
#epsent ZprimeMassPoints = [ 750, 1000, 1250, 1750, 2000, 2500, 3000, 3500, 4000 ]
# for massPoint in ZprimeMassPoints:
#     sampleName = "Zprime%1.0ftoTauTau" % massPoint
#     samples[sampleName] = {
#         'datasetpath'                        : '/ZprimeToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
#         'files_per_job'                      : 1,
#         'total_files'                        : -1,
#         'type'                               : 'SignalMC'
#     }

## currently 27 mass points available
#WprimeMassPoints = [ 400, 600, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800 ]
#for massPoint in WprimeMassPoints:
#    sampleName = "Wprime%1.0ftoTauNu" % massPoint
#    samples[sampleName] = {
#        'datasetpath'                        : '/WprimeToTauNu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
#        'files_per_job'                      : 1,
#        'total_files'                        : -1,
#        'type'                               : 'SignalMC'
#    }

# loop through dictionary, create directories according to sampleName
# and copy corresponding ntuples to the directory
print "Starting folder creation and copying of files. \n=====>Be mindfull and better remove old folders manualy before calling this script."

rewriteall = None
for sampleName, sampleOption in samples.items():
    folderToBeCreated = outputPath + sampleName
    print folderToBeCreated

    if os.path.isdir(folderToBeCreated):
        if rewriteall != True:

            tocontinue = False

            if rewriteall == None:
                reply = None
                while not any(x == reply for x in ["y", "Y", "n", "N"]):
                    reply = raw_input('rewrite the ' + folderToBeCreated + "folder? [y/n]. Type [Y/N] to apply this to all files.")
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

    filesToCopy = inputPath + sampleOption['datasetpath'] + "/*/*/*/*.root"
    copyCommand = "cp " + filesToCopy + " " + folderToBeCreated + "/"
    args = shlex.split(copyCommand)
    args[0] = sampleName
    #subprocess.call(copyCommand, shell = True)
    subprocess.Popen(copyCommand, shell = True)

print "done"
