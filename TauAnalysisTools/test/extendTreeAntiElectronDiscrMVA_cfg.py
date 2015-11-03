import FWCore.ParameterSet.Config as cms

import os
import glob

process = cms.PSet()

process.fwliteInput = cms.PSet(
    fileNames = cms.vstring(),
    
    ##maxEvents = cms.int32(100000),
    maxEvents = cms.int32(-1),
    
    outputEvery = cms.uint32(100000)
)

#----------------------------------------------------------------------------------------------------
inputFilePath  = "/<path-to-be-overwritten>/"
# path for test
#inputFilePath  = "/pnfs/desy.de/cms/tier2/store/user/fcolombo/higgs-kit/tauPOG/CMSSW_7_4_X/antiElectronDiscrMVATraining/ntuples/2015-10-15_test/"

signalSamples = [
    "ZplusJets_madgraph_signal",
    "WplusJets_madgraph_signal",
    "TTplusJets_madgraph_signal"
]
smHiggsMassPoints = [ 120,125,130 ]
for massPoint in smHiggsMassPoints:
    ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(ggSampleName)
    vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(vbfSampleName)
    wplushSampleName = "wplusHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(wplushSampleName)
    wminushSampleName = "wminusHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(wminushSampleName)

mssmHiggsMassPoints = [ 80,90,100,110,120,130,140,160,180,200,250,300,350,400,450,500,600,700,800,900,1000,1200,1400,1500,1600,1800,2000,2300,2600,2900,3200 ]
for massPoint in mssmHiggsMassPoints:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    signalSamples.append(ggSampleName)
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    signalSamples.append(bbSampleName)

ZprimeMassPoints = [ 500,1000,1500,2000,2500,3000,3500,4000,4500,5000 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    signalSamples.append(sampleName)

WprimeMassPoints = [ 1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200,5400,5600,5800 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauNu" % massPoint  
    signalSamples.append(sampleName)

backgroundSamples = [
    "ZplusJets_madgraph_background",
    "WplusJets_madgraph_background",
    "TTplusJets_madgraph_background",
    #"QCDflat_pythia8"
]

ZprimeMassPoints = [ 5000 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoElecElec" % massPoint
    backgroundSamples.append(sampleName)

WprimeMassPoints = [ 1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200,3400,3600,3800,4000,4200,4400,4600,4800,5000,5200,5400,5600,5800 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoElecNu" % massPoint
    backgroundSamples.append(sampleName)

sampleName = "DYtoElecElec"
backgroundSamples.append(sampleName)

#QCDMassPoints = [ '5to10','10to15','15to30','30to50','50to80','80to120','120to170','170to300','300to470','470to600','600to800','800to1000','1000to1400','1400to1800','1800to2400','2400to3200','3200toInf' ]
QCDMassPoints = [  ]
for massPoint in QCDMassPoints:
    sampleName = "QCD_Pt%s" % massPoint
    #backgroundSamples.append(sampleName)

#QCDEMenrichMassPoints = [ '15to20','20to30','30to50','50to80','80to120','120to170','170to300','300toInf' ]
QCDEMenrichMassPoints = [  ]
for massPoint in QCDMassPoints:
    sampleName = "QCD_EMEnriched_Pt%s" % massPoint
    #backgroundSamples.append(sampleName)

#QCDMuenrichMassPoints = [ '15to20','20to30','30to50','50to80','80to120','120to170','170to300','300to470','470to600','600to800','800to1000','1000toInf' ]
QCDMuenrichMassPoints = [  ]
for massPoint in QCDMassPoints:
    sampleName = "QCD_MuEnriched_Pt%s" % massPoint
    #backgroundSamples.append(sampleName)


allSamples = []
allSamples.extend(signalSamples)
allSamples.extend(backgroundSamples)

inputFileNames = []
for sample in allSamples:
    try:
        inputFileNames.extend(glob.glob(os.path.join(inputFilePath, '*/crab_'+sample, '*/*/*.root')))
    except OSError:
        print "inputFilePath = %s does not exist --> skipping !!" % os.path.join(inputFilePath, sample)
        continue
print len(inputFileNames)
process.fwliteInput.fileNames = cms.vstring(inputFileNames)

#----------------------------------------------------------------------------------------------------

process.extendTreeAntiElectronDiscrMVA = cms.PSet(

    inputTreeName = cms.string('antiElectronDiscrMVATrainingNtupleProducer/tree'),
    outputTreeName = cms.string('extendedTree'),

    categories = cms.PSet(),
    mva = cms.PSet( 
        mvaWeightPath = cms.string('') 
    ),

    samples = cms.vstring(allSamples),

    outputFileName = cms.string('extendTreeAntiElectronDiscrMVA.root')
)
