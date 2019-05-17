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
inputFilePath  = "/data2/veelken/CMSSW_5_3_x/Ntuples/tauIdMVATraining/v1_2/"
inputFilePath += "user/veelken/CMSSW_5_3_x/Ntuples/tauIdMVATraining/v1_2/"

signalSamples = [
    "ZplusJets_madgraph"
]
smHiggsMassPoints = [ 80, 90, 100, 110, 120, 130, 140 ]
for massPoint in smHiggsMassPoints:
    ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(ggSampleName)
    vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
    signalSamples.append(vbfSampleName)
mssmHiggsMassPoints = [ 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000 ]
for massPoint in mssmHiggsMassPoints:
    ggSampleName = "ggA%1.0ftoTauTau" % massPoint
    signalSamples.append(ggSampleName)
    bbSampleName = "bbA%1.0ftoTauTau" % massPoint
    signalSamples.append(bbSampleName)
ZprimeMassPoints = [ 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500 ]
for massPoint in ZprimeMassPoints:
    sampleName = "Zprime%1.0ftoTauTau" % massPoint
    signalSamples.append(sampleName)
WprimeMassPoints = [ 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3200, 3500, 4000 ]
for massPoint in WprimeMassPoints:
    sampleName = "Wprime%1.0ftoTauTau" % massPoint
    signalSamples.append(sampleName)

backgroundSamples = [
    "PPmuXptGt20Mu15",
    "QCDmuEnrichedPt50to80",
    "QCDmuEnrichedPt80to120",
    "QCDmuEnrichedPt120to170",
    "QCDmuEnrichedPt170to300",
    "QCDmuEnrichedPt300to470",
    "QCDmuEnrichedPt470to600",
    "QCDmuEnrichedPt600to800",
    "QCDmuEnrichedPt800to1000",
    "QCDmuEnrichedPtGt1000",
    "WplusJets_madgraph",
    "QCDjetsFlatPt15to3000",
    "QCDjetsPt50to80",
    "QCDjetsPt80to120",
    "QCDjetsPt120to170",
    "QCDjetsPt170to300",
    "QCDjetsPt300to470",
    "QCDjetsPt470to600",
    "QCDjetsPt600to800",
    "QCDjetsPt800to1000",
    "QCDjetsPt1000to1400",
    "QCDjetsPt1400to1800",
    "QCDmuEnrichedPtGt1800"
]

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

process.preselectTreeTauIdMVA = cms.PSet(

    inputTreeName = cms.string('tauIdMVATrainingNtupleProducer/tauIdMVATrainingNtuple'),
    outputTreeName = cms.string('preselectedTauIdMVATrainingNtuple'),

    preselection = cms.string('recTauDecayMode == 0 || recTauDecayMode == 1 || recTauDecayMode == 2 || recTauDecayMode == 10'),

    samples = cms.vstring(signalSamples),
    ##samples = cms.vstring(backgroundSamples),

    branchNamePt = cms.string('recTauPt'),
    branchNameEta = cms.string('recTauEta'),

    branchNameEvtWeight = cms.string('evtWeight'),

    applyEventPruning = cms.int32(1),
    applyPtDependentPruning = cms.bool(False),

    keepAllBranches = cms.bool(False),
    checkBranchesForNaNs = cms.bool(True),

    inputVariables = cms.vstring(
        ##'TMath::Log(TMath::Max(1., recTauPt))/F',
        'TMath::Abs(recTauEta)/F',
        'TMath::Log(TMath::Max(1.e-2, tauIsoDeltaR05PtThresholdsLoose3HitsChargedIsoPtSum))/F',
        'TMath::Log(TMath::Max(1.e-2, tauIsoDeltaR05PtThresholdsLoose3HitsNeutralIsoPtSum))/F',
        'TMath::Log(TMath::Max(1.e-2, tauIsoDeltaR08PtThresholdsLoose3HitsPUcorrPtSum))/F',
        'recTauDecayMode/I'
    ),
    spectatorVariables = cms.vstring(
        'recTauPt/F',
        ##'recTauDecayMode/I',
        'leadPFChargedHadrCandPt/F',
        'numOfflinePrimaryVertices/I'
    ),
    otherVariables = cms.vstring(
    ),

    outputFileName = cms.string('preselectTreeTauIdMVA.root')
)
key = '2018_bg'
out_dir = '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/'
year, typ = key.split('_')
process.fwliteInput.fileNames = cms.vstring()
d = {
    '2018': {
        'sg': {
            'path': '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_2018_raw_newv1/ntuples/ZplusJets_madgraph/ZplusJets_madgraph_7.31165184839fr_1000000ev.root',
            'tree': 'tauIdMVATrainingNtupleMiniAOD',
        },
        'bg': {
            'path': '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/tauIdMVATrainingNtupleMiniAOD_2018_QCD15to7000_2018_raw_new.root',
            'tree': 'tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD',
        }
    }
}
process.fwliteInput.fileNames.append(d[year][typ]['path'])

process.preselectTreeTauIdMVA.samples = cms.vstring(d[year][typ]['path'])
process.preselectTreeTauIdMVA.inputTreeName = cms.string(d[year][typ]['tree'])
process.preselectTreeTauIdMVA.preselection = cms.string('decayModeFindingNewDMs > 0.5 && numSelectedOfflinePrimaryVertices >= 1 && TMath::Abs(recTauVtxZ - selectedOfflinePrimaryVertexZ) < 0.4 && recJetLooseId > 0.5 && leadPFChargedHadrCandPt > 1. && chargedIsoPtSum < 10.')
process.preselectTreeTauIdMVA.applyEventPruning = cms.int32(0)
process.preselectTreeTauIdMVA.applyPtDependentPruning = cms.bool(True)
process.preselectTreeTauIdMVA.inputVariables = cms.vstring(['TMath::Log(TMath::Max(1., recTauPt))/F', 'TMath::Abs(recTauEta)/F', 'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))/F', 'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))/F', 'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))/F', 'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))/F', 'recTauDecayMode/I', 'TMath::Min(30., recTauNphoton_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)/F', 'TMath::Min(1., recTauEratio)/F', 'TMath::Sign(+1., recImpactParam)/F', 'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))/F', 'TMath::Min(10., TMath::Abs(recImpactParamSign))/F', 'TMath::Sign(+1., recImpactParam3D)/F', 'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))/F', 'TMath::Min(10., TMath::Abs(recImpactParamSign3D))/F', 'hasRecDecayVertex/I', 'TMath::Sqrt(recDecayDistMag)/F', 'TMath::Min(10., recDecayDistSign)/F', 'TMath::Max(-1.,recTauGJangleDiff)/F'])
process.preselectTreeTauIdMVA.spectatorVariables = cms.vstring(['2018_raw_new/F', 'recTauPt/F', 'leadPFChargedHadrCandPt/F', 'numOfflinePrimaryVertices/I', 'genVisTauPt/F', 'genTauPt/F', 'byCombinedIsolationDeltaBetaCorrRaw3Hits', 'byLooseCombinedIsolationDeltaBetaCorr3Hits', 'byMediumCombinedIsolationDeltaBetaCorr3Hits', 'byTightCombinedIsolationDeltaBetaCorr3Hits', 'byIsolationMVArun2v1DBnewDMwLTraw', 'byIsolationMVArun2v1DBnewDMwLTraw2016', 'byIsolationMVArun2017v2DBnewDMwLTraw2017', 'byIsolationMVArun2v1DBnewDMwLTraw', 'byIsolationMVArun2v1DBnewDMwLTraw2016', 'recTauNphoton', 'recTauNphoton_ptGt1.0', 'photonPtSumOutsideSignalCone_ptGt1.0', 'photonPtSumOutsideSignalConedRgt0p1_ptGt1.0', 'neutralIsoPtSum_ptGt1.0', 'recTauPtWeightedDetaStrip_ptGt1.0', 'recTauPtWeightedDphiStrip_ptGt1.0', 'recTauPtWeightedDrSignal_ptGt1.0', 'recTauPtWeightedDrIsolation_ptGt1.0', 'chargedIsoPtSumdR03', 'neutralIsoPtSumdR03', 'neutralIsoPtSum_IsoConeR0p3_ptGt1.0', 'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0'])
process.preselectTreeTauIdMVA.otherVariables = cms.vstring([])
process.preselectTreeTauIdMVA.outputFileName = cms.string(os.path.join(out_dir, 'presel_' + year + '_' + typ + '.root'))
# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/preselectTreeTauIdMVA TauAnalysisTools/TauAnalysisTools/python/test_configs/presel_cfi.py
