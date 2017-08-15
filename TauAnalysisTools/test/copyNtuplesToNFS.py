#!/usr/bin/env python

import os
import subprocess

# generic path to dCache where ntuples are stored
inputPath = "/pnfs/desy.de/cms/tier2/store/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V2/"

# generic path to NFS where we want to copy ntuples to
outputPath = "/nfs/dust/cms/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V2/ntuples/"

# more or less a copy of the samples in submitTauIdMVATrainingNtupleProduction_crab3.py
# with reduced information

samples = {
    'ZplusJets_mcatnlo' : {
        'datasetpath'                        : 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'
    },
    'TT_powheg': {
        'datasetpath'                        : 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'
    },
    'PPmuXptGt20Mu15' : {
        'datasetpath'                        : 'QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt30to50' : {
        'datasetpath'                        : 'QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt50to80' : {
        'datasetpath'                        : 'QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt80to120' : {
        'datasetpath'                        : 'QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt120to170' : {
        'datasetpath'                        : 'QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },    
    'QCDmuEnrichedPt170to300' : {
        'datasetpath'                        : 'QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt300to470' : {
        'datasetpath'                        : 'QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt470to600' : {
        'datasetpath'                        : 'QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt600to800' : {
        'datasetpath'                        : 'QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPt800to1000' : {
        'datasetpath'                        : 'QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDmuEnrichedPtGt1000' : {
        'datasetpath'                        : 'QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8'
    },
    'WplusJets_mcatnlo' : {
        'datasetpath'                        : 'WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8'
    },
    'QCDjetsFlatPt15to7000' : {
        'datasetpath'                        : 'QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8'
    },
    'QCDjetsPt30to50' : {
        'datasetpath'                        : 'QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt50to80' : {
        'datasetpath'                        : 'QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt80to120' : {
        'datasetpath'                        : 'QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt120to170' : {
        'datasetpath'                        : 'QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8'
    },        
    'QCDjetsPt170to300' : {
        'datasetpath'                        : 'QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt300to470' : {
        'datasetpath'                        : 'QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt470to600' : {
        'datasetpath'                        : 'QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt600to800' : {
        'datasetpath'                        : 'QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt800to1000' : {
        'datasetpath'                        : 'QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt1000to1400' : {
        'datasetpath'                        : 'QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt1400to1800' : {
        'datasetpath'                        : 'QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt1800to2400' : {
        'datasetpath'                        : 'QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPt2400to3200' : {
        'datasetpath'                        : 'QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDjetsPtGt3200' : {
        'datasetpath'                        : 'QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDEmEnrichedPt20to30' : {
        'datasetpath'                        : 'QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDEmEnrichedPt30to50' : {
        'datasetpath'                        : 'QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDEmEnrichedPt50to80' : {
        'datasetpath'                        : 'QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDEmEnrichedPt80to120' : {
        'datasetpath'                        : 'QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    },
    #'QCDEmEnrichedPt120to170' : {
    #    'datasetpath'                        : 'QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    #},
    'QCDEmEnrichedPt170to300' : {
        'datasetpath'                        : 'QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    },
    'QCDEmEnrichedPtGt300' : {
        'datasetpath'                        : 'QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8'
    },


}
smHiggsMassPoints = [ 120, 125, 130 ]
for massPoint in smHiggsMassPoints:
    #ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    #samples[ggSampleName] = {
    #    'datasetpath'                        : 'GluGluHToTauTau_M%1.0f_13TeV_powheg_pythia8' % massPoint
    #}
    #vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    #samples[vbfSampleName] = {
    #    'datasetpath'                        : 'VBFHToTauTau_M%1.0f_13TeV_powheg_pythia8' % massPoint
    #}
    #tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
    #samples[tthSampleName] = {
    #    'datasetpath'                        : 'ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8' % massPoint
    #}
    wPlusHSampleName = "WplusHHiggs%1.0ftoTauTau" % massPoint
    samples[wPlusHSampleName] = {
        'datasetpath'                        : 'WplusHToTauTau_M%1.0f_13TeV_powheg_pythia8' % massPoint
    }
    wMinusHSampleName = "WminusHHiggs%1.0ftoTauTau" % massPoint
    samples[wMinusHSampleName] = {
        'datasetpath'                        : 'WminusHToTauTau_M%1.0f_13TeV_powheg_pythia8' % massPoint
    }
    zHSampleName = "ZHHiggs%1.0ftoTauTau" % massPoint
    samples[zHSampleName] = {
        'datasetpath'                        : 'ZHToTauTau_M%1.0f_13TeV_powheg_pythia8' % massPoint
    }
smHiggsMassPoints5 = [ 120, 130 ]
for massPoint in smHiggsMassPoints5:
    tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
    samples[tthSampleName] = {
        'datasetpath'                        : 'ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8' % massPoint
    }
ggSampleName = "ggHiggs125toTauTau"
samples[ggSampleName] = {
    'datasetpath'                        : 'GluGluHToTauTau_M125_13TeV_powheg_pythia8'
}
vbfSampleName = "vbfHiggs125toTauTau"
samples[vbfSampleName] = {
    'datasetpath'                        : 'VBFHToTauTau_M125_13TeV_powheg_pythia8'
}
# currently 29 mass points available
mssmHiggsMassPoints1 = [ 80, 90, 100, 110, 120, 130, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
for massPoint in mssmHiggsMassPoints1:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    samples[ggSampleName] = {
        'datasetpath'                        : 'SUSYGluGluToHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8' % massPoint
    }

# currently 31 mass points available
mssmHiggsMassPoints2 = [ 80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
for massPoint in mssmHiggsMassPoints2:
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    samples[bbSampleName] = {
        'datasetpath'                        : 'SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8' % massPoint
    }

# currently 11 mass points available
ZprimeMassPoints = [ 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : 'ZprimeToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola' % massPoint
    }

# currently 27 mass points available
WprimeMassPoints = [ 400, 600, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauNu" % massPoint
    samples[sampleName] = {
        'datasetpath'                        : 'WprimeToTauNu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola' % massPoint
    }

# loop through dictionary, create directories according to sampleName
# and copy corresponding ntuples to the directory
print "starting folder creation and copying of files"

for sampleName, sampleOption in samples.items():
    
    folderToBeCreated = outputPath + sampleName
    os.makedirs(folderToBeCreated)
    
    filesToCopy = inputPath + sampleOption['datasetpath'] + "/*/*/*/*.root"
    copyCommand = "cp " + filesToCopy + " " + folderToBeCreated + "/"
    print "copying " + filesToCopy
    subprocess.call(copyCommand, shell = True)

print "done"
