import FWCore.ParameterSet.Config as cms

process = cms.Process("produceTauIdMVATrainingNtupleMiniAOD")

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
#process.load('Configuration.StandardSequences.Geometry_cff')
#process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '81X_upgrade2017_realistic_v26', '')

#process.add_(cms.Service("PrintLoadingPlugins"))

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:/data1/veelken/CMSSW_5_3_x/skims/96E96DDB-61D3-E111-BEFB-001E67397D05.root'
        #'file:/nfs/dust/cms/user/anayak/CMS/Ntuple_Phys14TauId/AOD_VBFHTauTau_fromYuta.root'
        #'root://xrootd.ba.infn.it//store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/00CC714A-F86B-E411-B99A-0025904B5FB8.root'
        #'file:/afs/cern.ch/work/f/fromeo/public/TauRunII/GluGluToHToTauTau_M125_D08.root'
        #'root://xrootd.ba.infn.it//store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Dynamic95_20150520/aod_1.root'
        #'file:/disk1/MVAonMiniAOD/RelValZTT_8_0_20_PU25ns_MINIAODSIM_1.root',
        #'file:/disk1/MVAonMiniAOD/RelValZTT_8_0_20_PU25ns_MINIAODSIM_2.root'
        '/store/mc/RunIISummer17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/92X_upgrade2017_realistic_v10_ext1-v2/10000/00F9D855-E293-E711-B625-02163E014200.root'
        # 'root://cms-xrd-global.cern.ch//store/mc/PhaseIFall16MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26_ext1-v1/70000/02A37775-A0E9-E611-8E01-0025907B4F2E.root'
        #'file:/disk1/MVAonMiniAOD/DYJetsToLLM50_AMCATNLO_MORIOND17_MINIAODSIM_1.root'
        #'/store/mc/RunIISummer16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/00312D7A-FEBD-E611-A713-002590DB923E.root'
    ),
    ##eventsToProcess = cms.untracked.VEventRange(
    ##    '1:917:1719279',
    ##    '1:1022:1915188'
    ##),
    ##skipEvents = cms.untracked.uint32(539)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

#--------------------------------------------------------------------------------
# define configuration parameter default values

type = 'SignalMC'
#type = 'BackgroundMC'
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# define "hooks" for replacing configuration parameters
# in case running jobs on the CERN batch system/grid
#
#__type = #type#
#
isMC = None
if type == 'SignalMC' or type == 'BackgroundMC':
    isMC = True
else:
    isMC = False

# information for cleaning against leptons
isSignal = None
dRClean = 0.5
if type == 'SignalMC':
    isSignal = True
    dRClean = 0.3
else:
    isSignal = False
#--------------------------------------------------------------------------------
from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *

process.rerunDiscriminationByIsolationOldDMMVArun2v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
	PATTauProducer = cms.InputTag('slimmedTaus'),
	Prediscriminants = noPrediscriminants,
	loadMVAfromDB = cms.bool(True),
	mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1"),
	mvaOpt = cms.string("DBoldDMwLT"),
	requireDecayMode = cms.bool(True),
	verbosity = cms.int32(0)
)

process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
	PATTauProducer = cms.InputTag('slimmedTaus'),    
	Prediscriminants = noPrediscriminants,
	toMultiplex = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1raw'),
	key = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1raw:category'),
	loadMVAfromDB = cms.bool(True),
	mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_mvaOutput_normalization"),
	mapping = cms.VPSet(
		cms.PSet(
			category = cms.uint32(0),
			cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff90"),
			variable = cms.string("pt"),
		)
	)
)

process.rerunDiscriminationByIsolationOldDMMVArun2v1Loose = process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationOldDMMVArun2v1Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff80")
process.rerunDiscriminationByIsolationOldDMMVArun2v1Medium = process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationOldDMMVArun2v1Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff70")
process.rerunDiscriminationByIsolationOldDMMVArun2v1Tight = process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationOldDMMVArun2v1Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff60")
process.rerunDiscriminationByIsolationOldDMMVArun2v1VTight = process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationOldDMMVArun2v1VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff50")
process.rerunDiscriminationByIsolationOldDMMVArun2v1VVTight = process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationOldDMMVArun2v1VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff40")

process.rerunDiscriminationByIsolationNewDMMVArun2v1raw = process.rerunDiscriminationByIsolationOldDMMVArun2v1raw.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1raw.mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1")
process.rerunDiscriminationByIsolationNewDMMVArun2v1raw.mvaOpt = cms.string("DBnewDMwLT")

process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose = process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.toMultiplex = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1raw')
process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.key = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1raw:category')
process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_mvaOutput_normalization")
process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff90")

process.rerunDiscriminationByIsolationNewDMMVArun2v1Loose = process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff80")
process.rerunDiscriminationByIsolationNewDMMVArun2v1Medium = process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff70")
process.rerunDiscriminationByIsolationNewDMMVArun2v1Tight = process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff60")
process.rerunDiscriminationByIsolationNewDMMVArun2v1VTight = process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff50")
process.rerunDiscriminationByIsolationNewDMMVArun2v1VVTight = process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
process.rerunDiscriminationByIsolationNewDMMVArun2v1VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff40")

process.rerunMvaIsolationSequence = cms.Sequence(
	process.rerunDiscriminationByIsolationOldDMMVArun2v1raw
	*process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose
	*process.rerunDiscriminationByIsolationOldDMMVArun2v1Loose
	*process.rerunDiscriminationByIsolationOldDMMVArun2v1Medium
	*process.rerunDiscriminationByIsolationOldDMMVArun2v1Tight
	*process.rerunDiscriminationByIsolationOldDMMVArun2v1VTight
	*process.rerunDiscriminationByIsolationOldDMMVArun2v1VVTight
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1raw
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1Loose
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1Medium
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1Tight
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1VTight
	*process.rerunDiscriminationByIsolationNewDMMVArun2v1VVTight
)

embedID = cms.EDProducer("PATTauIDEmbedder",
	src = cms.InputTag('slimmedTaus'),
	tauIDSources = cms.PSet(
		byIsolationMVArun2v1DBoldDMwLTraw2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1raw'),
		byVLooseIsolationMVArun2v1DBoldDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1VLoose'),
		byLooseIsolationMVArun2v1DBoldDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1Loose'),
		byMediumIsolationMVArun2v1DBoldDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1Medium'),
		byTightIsolationMVArun2v1DBoldDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1Tight'),
		byVTightIsolationMVArun2v1DBoldDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1VTight'),
		byVVTightIsolationMVArun2v1DBoldDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1VVTight'),
		byIsolationMVArun2v1DBnewDMwLTraw2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1raw'),
		byVLooseIsolationMVArun2v1DBnewDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1VLoose'),
		byLooseIsolationMVArun2v1DBnewDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1Loose'),
		byMediumIsolationMVArun2v1DBnewDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1Medium'),
		byTightIsolationMVArun2v1DBnewDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1Tight'),
		byVTightIsolationMVArun2v1DBnewDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1VTight'),
		byVVTightIsolationMVArun2v1DBnewDMwLT2016 = cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1VVTight')
	),
)
setattr(process, "NewTauIDsEmbedded", embedID)

#--------------------------------------------------------------------------------
   
process.produceTauIdMVATrainingNtupleMiniAODSequence = cms.Sequence()

#--------------------------------------------------------------------------------
# select "good" reconstructed vertices
#
# CV: cut on ndof >= 4 if using 'offlinePrimaryVertices',
#                 >= 7 if using 'offlinePrimaryVerticesWithBS' as input
#
process.selectedOfflinePrimaryVertices = cms.EDFilter("VertexSelector",
    src = cms.InputTag('offlineSlimmedPrimaryVertices'),
    #cut = cms.string("isValid & ndof >= 4 & chi2 > 0 & tracksSize > 0 & abs(z) < 24 & abs(position.Rho) < 2."),
    cut = cms.string("isValid & ndof >= 4 & chi2 > 0 & abs(z) < 24 & abs(position.Rho) < 2."), # tracksSize & nTracks are set to 0 in MiniAOD
    filter = cms.bool(False)                                          
)
process.produceTauIdMVATrainingNtupleMiniAODSequence += process.selectedOfflinePrimaryVertices
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# compute event weights for pile-up reweighting
# (Summer'12 MC to 2012 run ABCD data)

srcWeights = []
#inputFileNameLumiCalc = None
#if isMC:
#    from TauAnalysis.RecoTools.vertexMultiplicityReweight_cfi import vertexMultiplicityReweight
#    process.vertexMultiplicityReweight3d2012RunABCD = vertexMultiplicityReweight.clone(
#        inputFileName = cms.FileInPath("TauAnalysis/RecoTools/data/expPUpoissonMean_runs190456to208686_Mu17_Mu8.root"),
#        type = cms.string("gen3d"),
#        mcPeriod = cms.string("Summer12_S10")
#    )
#    process.produceTauIdMVATrainingNtupleSequence += process.vertexMultiplicityReweight3d2012RunABCD
#    srcWeights.extend([ 'vertexMultiplicityReweight3d2012RunABCD' ])
#    inputFileNameLumiCalc = 'TauAnalysis/RecoTools/data/dummy.txt'
#else:
#    inputFileNameLumiCalc = 'TauAnalysis/RecoTools/data_nocrab/lumiCalc_2012RunABCD_byLS.out'
#--------------------------------------------------------------------------------

process.tauIdMVATrainingNtupleProducerMiniAOD = cms.EDProducer("TauIdMVATrainingNtupleProducerMiniAOD",
<<<<<<< HEAD
    srcRecTaus = cms.InputTag('NewTauIDsEmbedded'),
    srcPrunedGenParticles = cms.InputTag('prunedGenParticles'),
    srcPackedGenParticles = cms.InputTag('packedGenParticles'),
    srcRecJets = cms.InputTag('slimmedJets'),
    minGenVisPt = cms.double(10.),
    dRmatch = cms.double(0.3),
    tauIdDiscriminators = cms.PSet(
        decayModeFindingNewDMs = cms.string('decayModeFindingNewDMs'),
        decayModeFindingOldDMs = cms.string('decayModeFinding'),
        byCombinedIsolationDeltaBetaCorrRaw3Hits = cms.string('byCombinedIsolationDeltaBetaCorrRaw3Hits'),
        byLooseCombinedIsolationDeltaBetaCorr3Hits = cms.string('byLooseCombinedIsolationDeltaBetaCorr3Hits'),
        byMediumCombinedIsolationDeltaBetaCorr3Hits = cms.string('byMediumCombinedIsolationDeltaBetaCorr3Hits'),
        byTightCombinedIsolationDeltaBetaCorr3Hits = cms.string('byTightCombinedIsolationDeltaBetaCorr3Hits'),
        byIsolationMVArun2v1DBoldDMwLTraw = cms.string("byIsolationMVArun2v1DBoldDMwLTraw"),
        byVLooseIsolationMVArun2v1DBoldDMwLT = cms.string("byVLooseIsolationMVArun2v1DBoldDMwLT"),
        byLooseIsolationMVArun2v1DBoldDMwLT = cms.string("byLooseIsolationMVArun2v1DBoldDMwLT"),
        byMediumIsolationMVArun2v1DBoldDMwLT = cms.string("byMediumIsolationMVArun2v1DBoldDMwLT"),
        byTightIsolationMVArun2v1DBoldDMwLT = cms.string("byTightIsolationMVArun2v1DBoldDMwLT"),
        byVTightIsolationMVArun2v1DBoldDMwLT = cms.string("byVTightIsolationMVArun2v1DBoldDMwLT"),
        byVVTightIsolationMVArun2v1DBoldDMwLT = cms.string("byVVTightIsolationMVArun2v1DBoldDMwLT"),
        byIsolationMVArun2v1DBnewDMwLTraw = cms.string("byIsolationMVArun2v1DBnewDMwLTraw"),
        byVLooseIsolationMVArun2v1DBnewDMwLT = cms.string("byVLooseIsolationMVArun2v1DBnewDMwLT"),
        byLooseIsolationMVArun2v1DBnewDMwLT = cms.string("byLooseIsolationMVArun2v1DBnewDMwLT"),
        byMediumIsolationMVArun2v1DBnewDMwLT = cms.string("byMediumIsolationMVArun2v1DBnewDMwLT"),
        byTightIsolationMVArun2v1DBnewDMwLT = cms.string("byTightIsolationMVArun2v1DBnewDMwLT"),
        byVTightIsolationMVArun2v1DBnewDMwLT = cms.string("byVTightIsolationMVArun2v1DBnewDMwLT"),
        byVVTightIsolationMVArun2v1DBnewDMwLT = cms.string("byVVTightIsolationMVArun2v1DBnewDMwLT"),
        byIsolationMVArun2v1DBdR03oldDMwLTraw = cms.string("byIsolationMVArun2v1DBdR03oldDMwLTraw"),
        byVLooseIsolationMVArun2v1DBdR03oldDMwLT = cms.string("byVLooseIsolationMVArun2v1DBdR03oldDMwLT"),
        byLooseIsolationMVArun2v1DBdR03oldDMwLT = cms.string("byLooseIsolationMVArun2v1DBdR03oldDMwLT"),
        byMediumIsolationMVArun2v1DBdR03oldDMwLT = cms.string("byMediumIsolationMVArun2v1DBdR03oldDMwLT"),
        byTightIsolationMVArun2v1DBdR03oldDMwLT = cms.string("byTightIsolationMVArun2v1DBdR03oldDMwLT"),
        byVTightIsolationMVArun2v1DBdR03oldDMwLT = cms.string("byVTightIsolationMVArun2v1DBdR03oldDMwLT"),
        byVVTightIsolationMVArun2v1DBdR03oldDMwLT = cms.string("byVVTightIsolationMVArun2v1DBdR03oldDMwLT"),
        byIsolationMVArun2v1DBoldDMwLTraw2016 = cms.string("byIsolationMVArun2v1DBoldDMwLTraw2016"),
        byVLooseIsolationMVArun2v1DBoldDMwLT2016 = cms.string("byVLooseIsolationMVArun2v1DBoldDMwLT2016"),
        byLooseIsolationMVArun2v1DBoldDMwLT2016 = cms.string("byLooseIsolationMVArun2v1DBoldDMwLT2016"),
        byMediumIsolationMVArun2v1DBoldDMwLT2016 = cms.string("byMediumIsolationMVArun2v1DBoldDMwLT2016"),
        byTightIsolationMVArun2v1DBoldDMwLT2016 = cms.string("byTightIsolationMVArun2v1DBoldDMwLT2016"),
        byVTightIsolationMVArun2v1DBoldDMwLT2016 = cms.string("byVTightIsolationMVArun2v1DBoldDMwLT2016"),
        byVVTightIsolationMVArun2v1DBoldDMwLT2016 = cms.string("byVVTightIsolationMVArun2v1DBoldDMwLT2016"),
        byIsolationMVArun2v1DBnewDMwLTraw2016 = cms.string("byIsolationMVArun2v1DBnewDMwLTraw2016"),
        byVLooseIsolationMVArun2v1DBnewDMwLT2016 = cms.string("byVLooseIsolationMVArun2v1DBnewDMwLT2016"),
        byLooseIsolationMVArun2v1DBnewDMwLT2016 = cms.string("byLooseIsolationMVArun2v1DBnewDMwLT2016"),
        byMediumIsolationMVArun2v1DBnewDMwLT2016 = cms.string("byMediumIsolationMVArun2v1DBnewDMwLT2016"),
        byTightIsolationMVArun2v1DBnewDMwLT2016 = cms.string("byTightIsolationMVArun2v1DBnewDMwLT2016"),
        byVTightIsolationMVArun2v1DBnewDMwLT2016 = cms.string("byVTightIsolationMVArun2v1DBnewDMwLT2016"),
        byVVTightIsolationMVArun2v1DBnewDMwLT2016 = cms.string("byVVTightIsolationMVArun2v1DBnewDMwLT2016"),
        againstMuonLoose3 = cms.string('againstMuonLoose3'),
        againstMuonTight3 = cms.string('againstMuonTight3')
    ),
    isolationPtSums = cms.PSet(
        chargedIsoPtSum = cms.string("chargedIsoPtSum"),
        neutralIsoPtSum = cms.string("neutralIsoPtSum"),
        puCorrPtSum = cms.string("puCorrPtSum"), 
        neutralIsoPtSumWeight = cms.string("neutralIsoPtSumWeight"),
        footprintCorrection = cms.string("footprintCorrection"),
        photonPtSumOutsideSignalCone = cms.string("photonPtSumOutsideSignalCone"),
        chargedIsoPtSumdR03 = cms.string('chargedIsoPtSumdR03'),
        neutralIsoPtSumdR03 = cms.string('neutralIsoPtSumdR03'),
        neutralIsoPtSumWeightdR03 = cms.string('neutralIsoPtSumWeightdR03'),
        footprintCorrectiondR03 = cms.string('footprintCorrectiondR03'),
        photonPtSumOutsideSignalConedR03 = cms.string('photonPtSumOutsideSignalConedR03')
    ),
    vertexCollections = cms.PSet(
        offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
        selectedOfflinePrimaryVertices = cms.InputTag('selectedOfflinePrimaryVertices')
    ),
    #--------------------------------------------------------
    # CV: pile-up information for Monte Carlo and data                                                               
    srcGenPileUpSummary = cms.InputTag('slimmedAddPileupInfo'),
    #inputFileNameLumiCalc = cms.FileInPath(inputFileNameLumiCalc),
    isMC = cms.bool(isMC),
    isSignal = cms.bool(isSignal),
    dRClean = cms.double(dRClean),
    ptCleanMin = cms.double(10.),
    matchGenTauVis = cms.bool(True),
    #--------------------------------------------------------                                                                       
    srcWeights = cms.VInputTag(srcWeights),
    ptMin_allPhotonsVariables = cms.vstring("0.5","1.0","1.5"),
    ptMin_nPhotons = cms.vstring("0.5","0.75","1.0","1.25","1.5"),
    ptMin_photonPtSumOutsideSignalCone = cms.vstring("0.5","1.0","1.5"),
    ptMin_photonPtSumOutsideSignalConedRgt0p1 = cms.vstring("0.5","1.0","1.5"),
    verbosity = cms.int32(0)
)

#dRisoCone = 0.4

#pset = cms.PSet(
#    chargedIsoPtSum = cms.string("chargedIsoPtSum"),
#    neutralIsoPtSum = cms.string("neutralIsoPtSum"),
#    puCorrPtSum = cms.string("puCorrPtSum"), 
#    neutralIsoPtSumWeight = cms.string("neutralIsoPtSumWeight"),
#    footprintCorrection = cms.string("footprintCorrection"),
#    photonPtSumOutsideSignalCone = cms.string("photonPtSumOutsideSignalCone")
#)
#psetName = "tauIsoDeltaR%02.0f" % (dRisoCone*10.)    
#setattr(process.tauIdMVATrainingNtupleProducerMiniAOD.isolationPtSums, psetName, pset)
process.produceTauIdMVATrainingNtupleMiniAODSequence += process.tauIdMVATrainingNtupleProducerMiniAOD

process.p = cms.Path(process.rerunMvaIsolationSequence*getattr(process, "NewTauIDsEmbedded")*process.produceTauIdMVATrainingNtupleMiniAODSequence)
#process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")
#process.printFirstEventContentPath = cms.Path(process.printEventContent)
#process.Schedule = cms.Schedule(process.p, process.printFirstEventContentPath)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("tauIdMVATrainingNtupleMiniAOD.root")
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(False)
)

#processDumpFile = open('produceTauIdMVATrainingNtupleMiniAOD.dump', 'w')
#print >> processDumpFile, process.dumpPython()




