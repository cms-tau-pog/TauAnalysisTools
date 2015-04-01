import FWCore.ParameterSet.Config as cms

import os

process = cms.PSet()

process.fwliteInput = cms.PSet(
    fileNames = cms.vstring(),
    
    ##maxEvents = cms.int32(100000),
    maxEvents = cms.int32(-1),
    
    outputEvery = cms.uint32(100000)
)

#----------------------------------------------------------------------------------------------------
inputFilePath  = "/<path-to-be-overwritten>/"
#inputFilePath  = "/pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/tauPOG/CMSSW_7_2_X/antiElectronDiscrMVATraining/ntuples/2015-03-30/"

signalSamples = [
    "ZplusJets_madgraph_signal",
    "WplusJets_madgraph_signal",
    "TTplusJets_madgraph_signal"
]
smHiggsMassPoints = [ 125 ]
for massPoint in smHiggsMassPoints:
    ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(ggSampleName)
    vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(vbfSampleName)
mssmHiggsMassPoints = [  ]
for massPoint in mssmHiggsMassPoints:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    signalSamples.append(ggSampleName)
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    signalSamples.append(bbSampleName)
ZprimeMassPoints = [  ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    signalSamples.append(sampleName)
WprimeMassPoints = [  ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauNu" % massPoint  
    signalSamples.append(sampleName)

backgroundSamples = [
    "ZplusJets_madgraph_background",
    "WplusJets_madgraph_background",
    "TTplusJets_madgraph_background"
]
ZprimeMassPoints = [  ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoElecElec" % massPoint
    backgroundSamples.append(sampleName)
WprimeMassPoints = [  ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoElecNu" % massPoint
    backgroundSamples.append(sampleName)
DrellYanMassPoints = [ 50 ]
for massPoint in DrellYanMassPoints:
    sampleName = "DY%1.0ftoElecElec" % massPoint
    ##sampleName = "DY%1.0ftoMuElecElec" % massPoint
    backgroundSamples.append(sampleName)
    
allSamples = []
allSamples.extend(signalSamples)
allSamples.extend(backgroundSamples)

inputFileNames = []
for sample in allSamples:
    try:
        inputFileNames.extend([ os.path.join(inputFilePath, sample, file) for file in os.listdir(os.path.join(inputFilePath, sample)) ])
    except OSError:
        print "inputFilePath = %s does not exist --> skipping !!" % os.path.join(inputFilePath, sample)
        continue
print "inputFileNames = %s" % inputFileNames
process.fwliteInput.fileNames = cms.vstring(inputFileNames)
#----------------------------------------------------------------------------------------------------

process.extendTreeAntiElectronDiscrMVA = cms.PSet(

    inputTreeName = cms.string('antiElectronDiscrMVATrainingNtupleProducer/tree'),
    outputTreeName = cms.string('extendedTree'),

    categories = cms.PSet(),

    samples = cms.vstring(allSamples),

    outputFileName = cms.string('extendTreeAntiElectronDiscrMVA.root')
)
