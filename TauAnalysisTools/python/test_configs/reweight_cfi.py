import FWCore.ParameterSet.Config as cms

import os

process = cms.PSet()

process.fwliteInput = cms.PSet(
    fileNames=cms.vstring(),
    maxEvents=cms.int32(-1),
    outputEvery=cms.uint32(100000)
)

process.fwliteInput.fileNames = cms.vstring(
    'preselectTreeTauIdMVA_signal.root',
    'preselectTreeTauIdMVA_background.root'
)

process.reweightTreeTauIdMVA = cms.PSet(

    inputTreeName=cms.string('preselectedTauIdMVATrainingNtuple'),
    outputTreeName=cms.string('reweightedTauIdMVATrainingNtuple'),

    signalSamples=cms.vstring('signal'),
    backgroundSamples=cms.vstring('background'),

    applyPtReweighting=cms.bool(True),
    branchNamePt=cms.string('recTauPt'),
    applyEtaReweighting=cms.bool(True),
    branchNameEta=cms.string('recTauEta'),
    reweight=cms.string("flat"),

    branchNameEvtWeight=cms.string('evtWeight'),

    keepAllBranches=cms.bool(False),
    checkBranchesForNaNs=cms.bool(True),

    inputVariables=cms.vstring(
        ##'TMath::Log(TMath::Max(1., recTauPt))/F',
        'TMath::Abs(recTauEta)/F',
        'TMath::Log(TMath::Max(1.e-2, tauIsoDeltaR05PtThresholdsLoose3HitsChargedIsoPtSum))/F',
        'TMath::Log(TMath::Max(1.e-2, tauIsoDeltaR05PtThresholdsLoose3HitsNeutralIsoPtSum))/F',
        'TMath::Log(TMath::Max(1.e-2, tauIsoDeltaR08PtThresholdsLoose3HitsPUcorrPtSum))/F',
        'recTauDecayMode/I'
    ),
    spectatorVariables=cms.vstring(
        'recTauPt/F',
        ##'recTauDecayMode/I',
        'leadPFChargedHadrCandPt/F',
        'numOfflinePrimaryVertices/I'
    ),

    outputFileName=cms.string('reweightTreeTauIdMVA.root'),
    save=cms.string('signal')
)

# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/reweightTreeTauIdMVA TauAnalysisTools/TauAnalysisTools/python/test_configs/reweight_cfi.py

key = '2018_background'
key = '2018_signal'
out_dir = '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/'
year, typ = key.split('_')
process.fwliteInput.fileNames = cms.vstring()
d = {
    '2018': {
        'signal': {
            'path': '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/presel_2018_sg.root',
            # 'tree': 'tauIdMVATrainingNtupleMiniAOD',
        },
        'background': {
            'path': '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/presel_2018_bg.root',
            # 'tree': 'tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD',
        }
    }
}
process.fwliteInput.fileNames = cms.vstring()
# process.fwliteInput.fileNames.append(d[year]['signal']['path'])
process.fwliteInput.fileNames.append('/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauIdv2/tauId_dR05_new_v2/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_background.root')
process.fwliteInput.fileNames.append(d[year]['background']['path'])

process.reweightTreeTauIdMVA.inputTreeNamesg = cms.string('reweightedTauIdMVATrainingNtuple')
process.reweightTreeTauIdMVA.inputTreeNamebg = cms.string('preselectedTauIdMVATrainingNtuple')
process.reweightTreeTauIdMVA.signalSamples = cms.vstring('reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_background')  # signal
process.reweightTreeTauIdMVA.backgroundSamples = cms.vstring('bg')  # background
process.reweightTreeTauIdMVA.applyPtReweighting = cms.bool(True)
process.reweightTreeTauIdMVA.applyEtaReweighting = cms.bool(True)
process.reweightTreeTauIdMVA.reweight = cms.string('background')  # ('min:KILL')
process.reweightTreeTauIdMVA.inputVariables = cms.vstring(['TMath::Log(TMath::Max(1., recTauPt))/F', 'TMath::Abs(recTauEta)/F', 'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))/F', 'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))/F', 'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))/F', 'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))/F', 'recTauDecayMode/I', 'TMath::Min(30., recTauNphoton_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)/F', 'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)/F', 'TMath::Min(1., recTauEratio)/F', 'TMath::Sign(+1., recImpactParam)/F', 'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))/F', 'TMath::Min(10., TMath::Abs(recImpactParamSign))/F', 'TMath::Sign(+1., recImpactParam3D)/F', 'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))/F', 'TMath::Min(10., TMath::Abs(recImpactParamSign3D))/F', 'hasRecDecayVertex/I', 'TMath::Sqrt(recDecayDistMag)/F', 'TMath::Min(10., recDecayDistSign)/F', 'TMath::Max(-1.,recTauGJangleDiff)/F'])
process.reweightTreeTauIdMVA.spectatorVariables = cms.vstring(['2018_raw_new/F', 'recTauPt/F', 'leadPFChargedHadrCandPt/F', 'numOfflinePrimaryVertices/I', 'genVisTauPt/F', 'genTauPt/F', 'byCombinedIsolationDeltaBetaCorrRaw3Hits', 'byLooseCombinedIsolationDeltaBetaCorr3Hits', 'byMediumCombinedIsolationDeltaBetaCorr3Hits', 'byTightCombinedIsolationDeltaBetaCorr3Hits', 'byIsolationMVArun2v1DBnewDMwLTraw', 'byIsolationMVArun2v1DBnewDMwLTraw2016', 'byIsolationMVArun2017v2DBnewDMwLTraw2017', 'byIsolationMVArun2v1DBnewDMwLTraw', 'byIsolationMVArun2v1DBnewDMwLTraw2016', 'recTauNphoton', 'recTauNphoton_ptGt1.0', 'photonPtSumOutsideSignalCone_ptGt1.0', 'photonPtSumOutsideSignalConedRgt0p1_ptGt1.0', 'neutralIsoPtSum_ptGt1.0', 'recTauPtWeightedDetaStrip_ptGt1.0', 'recTauPtWeightedDphiStrip_ptGt1.0', 'recTauPtWeightedDrSignal_ptGt1.0', 'recTauPtWeightedDrIsolation_ptGt1.0', 'chargedIsoPtSumdR03', 'neutralIsoPtSumdR03', 'neutralIsoPtSum_IsoConeR0p3_ptGt1.0', 'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0'])
process.reweightTreeTauIdMVA.outputFileName = cms.string(os.path.join(out_dir, 'reweighted_' + year + '_' + typ + '_bg_to_MVA2018v2REW' + '.root'))
process.reweightTreeTauIdMVA.save = cms.string(typ)
# nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/reweightTreeTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauIdv2/tauId_dR05_new_v2/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_signal_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauIdv2/tauId_dR05_new_v2/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_signal.log

process.reweightTreeTauIdMVA.xmltraining = cms.string('')
# process.reweightTreeTauIdMVA.xmltraining_name = cms.string('background')
process.reweightTreeTauIdMVA.xmlinputVariables = cms.vstring([
    # "TMath::Log(TMath::Max(1., recTauPt))/F",
    # "TMath::Abs(recTauEta)/F",
    # "TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))/F",
    # "TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))/F",
    # "TMath::Log(TMath::Max(1.e-2, puCorrPtSum))/F",
    # "TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))/F",
    # "recTauDecayMode/I",
    # "TMath::Min(30., recTauNphoton_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)/F",
    # "TMath::Min(1., recTauEratio)/F",
    # "TMath::Sign(+1., recImpactParam)/F",
    # "TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))/F",
    # "TMath::Min(10., TMath::Abs(recImpactParamSign))/F",
    # "TMath::Sign(+1., recImpactParam3D)/F",
    # "TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))/F",
    # "TMath::Min(10., TMath::Abs(recImpactParamSign3D))/F",
    # "hasRecDecayVertex/I",
    # "TMath::Sqrt(recDecayDistMag)/F",
    # "TMath::Min(10., recDecayDistSign)/F",
    # "TMath::Max(-1.,recTauGJangleDiff)/F",
])
process.reweightTreeTauIdMVA.xmlspectatorVariables = cms.vstring([
    # "recTauPt",
    # "leadPFChargedHadrCandPt",
    # "numOfflinePrimaryVertices",
    # "genVisTauPt",
    # "genTauPt",
    # "byIsolationMVArun2v1DBdR03oldDMwLTraw",
    # "byIsolationMVArun2v1DBoldDMwLTraw",
    # "byIsolationMVArun2v1DBoldDMwLTraw2016",
    # "byIsolationMVArun2017v1DBoldDMwLTraw2017",
    # "byIsolationMVArun2v1DBnewDMwLTraw",
    # "byIsolationMVArun2v1DBnewDMwLTraw2016",
    # "byCombinedIsolationDeltaBetaCorrRaw3Hits",
    # "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    # "byMediumCombinedIsolationDeltaBetaCorr3Hits",
    # "byTightCombinedIsolationDeltaBetaCorr3Hits",
    # "byIsolationMVArun2v1DBoldDMwLTraw",
    # "byIsolationMVArun2v1DBoldDMwLTraw2016",
    # "byIsolationMVArun2017v1DBoldDMwLTraw2017",
    # "recTauNphoton",
    # "recTauNphoton_ptGt1.0",
    # "recTauNphoton_ptGt1.5",
    # "photonPtSumOutsideSignalCone_ptGt1.0",
    # "photonPtSumOutsideSignalCone_ptGt1.5",
    # "photonPtSumOutsideSignalConedRgt0p1_ptGt1.0",
    # "photonPtSumOutsideSignalConedRgt0p1_ptGt1.5",
    # "neutralIsoPtSum_ptGt1.0",
    # "neutralIsoPtSum_ptGt1.5",
    # "recTauPtWeightedDetaStrip_ptGt1.0",
    # "recTauPtWeightedDetaStrip_ptGt1.5",
    # "recTauPtWeightedDphiStrip_ptGt1.0",
    # "recTauPtWeightedDphiStrip_ptGt1.5",
    # "recTauPtWeightedDrSignal_ptGt1.0",
    # "recTauPtWeightedDrSignal_ptGt1.5",
    # "recTauPtWeightedDrIsolation_ptGt1.0",
    # "recTauPtWeightedDrIsolation_ptGt1.5",
    #     "chargedIsoPtSumdR03",
    # "neutralIsoPtSumdR03",
    # "neutralIsoPtSum_IsoConeR0p3_ptGt1.0",
    # "neutralIsoPtSum_IsoConeR0p3_ptGt1.5",
    # "photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0",
    # "photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.5",
])
process.reweightTreeTauIdMVA.gbrForestName = cms.string('')  # "BDT::BDTG"
process.reweightTreeTauIdMVA.createClassId = cms.bool(False)  # "BDT::BDTG"
process.reweightTreeTauIdMVA.classId = cms.int32(1)  # "BDT::BDTG"
