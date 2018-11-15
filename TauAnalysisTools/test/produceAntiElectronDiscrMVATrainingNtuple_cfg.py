import FWCore.ParameterSet.Config as cms

#from RecoEgamma.ElectronIdentification.data import *

from Configuration.StandardSequences.Eras import eras
process = cms.Process("produceAntiElectronDiscrMVATrainingNtuple",eras.Run2_2017,eras.run2_nanoAOD_94XMiniAODv2)

process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")

globalTag = "94X_mc2017_realistic_v14"
process.GlobalTag.globaltag = cms.string(globalTag)
print "GlobalTag:", process.GlobalTag.globaltag

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://xrootd.unl.edu///store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/70000/F2283B5C-6044-E811-B61D-0025905B859A.root'
     )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
    #input = cms.untracked.int32(-1)
)

#--------------------------------------------------------------------------------
# define configuration parameter default values

##type = 'SignalMC'
type = 'BackgroundMC'
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
#--------------------------------------------------------------------------------
   
process.produceAntiElectronDiscrMVATrainingNtupleSequence = cms.Sequence()

#--------------------------------------------------------------------------------
# rerun tau reconstruction with latest tags
# MB: removed, if needed it should be done when MiniAOD samples are prepared

process.selectedOfflinePrimaryVertices = cms.EDFilter("VertexSelector",
    src = cms.InputTag('offlineSlimmedPrimaryVertices'),
    cut = cms.string("isValid & ndof >= 4 & chi2 > 0 & tracksSize > 0 & abs(z) < 24 & abs(position.Rho) < 2."),
    filter = cms.bool(False)					      
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.selectedOfflinePrimaryVertices

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# select generator level hadronic tau decays,
# and prompt electrons

process.prePFTauSequence = cms.Sequence()

if type == 'SignalMC' or type == 'BackgroundMC':
    process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
    process.tauGenJets.GenParticles = cms.InputTag('prunedGenParticles')
    process.prePFTauSequence += process.tauGenJets
    process.load("PhysicsTools.JetMCAlgos.TauGenJetsDecayModeSelectorAllHadrons_cfi")
    process.tauGenJetsSelectorAllHadrons.select = cms.vstring(
        'oneProng0Pi0', 
        'oneProng1Pi0', 
        'oneProng2Pi0', 
        'oneProngOther',
        'threeProng0Pi0', 
        'threeProng1Pi0', 
        'threeProngOther', 
        'rare'
    )
    process.prePFTauSequence += process.tauGenJetsSelectorAllHadrons

    process.genElectrons = cms.EDFilter("GenParticleSelector",
        src = cms.InputTag("prunedGenParticles"),
        cut = cms.string('abs(pdgId) = 11 & pt > 10.& (statusFlags().isPrompt() || statusFlags().isDirectPromptTauDecayProduct())'),
        stableOnly = cms.bool(True),
        filter = cms.bool(False)
    )
    process.prePFTauSequence += process.genElectrons

# Run MVAIso (use sequences from NanoAOD)
process.load('PhysicsTools.NanoAOD.taus_updatedMVAIds_cff')
#MB: use correct era in process definition
process.prePFTauSequence += process.patTauMVAIDsSeq

process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.prePFTauSequence

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

# Load tools and function definitions
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

process.load("RecoEgamma.ElectronIdentification.ElectronMVAValueMapProducer_cfi")
#process.load("RecoEgamma.ElectronIdentification.ElectronRegressionValueMapProducer_cfi")

#**********************
dataFormat = DataFormat.MiniAOD
switchOnVIDElectronIdProducer(process, dataFormat)
#**********************

process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
# overwrite a default parameter: for miniAOD, the collection name is a slimmed one
process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag('slimmedElectrons')

from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)

# Define which IDs we want to produce
my_id_modules = [
    'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns
    #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
    #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',   #Spring16
    #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff',   #Spring16 HZZ
    'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff'

] 
#Add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
egmMod = 'egmGsfElectronIDs'
mvaMod = 'electronMVAValueMapProducer'
regMod = 'electronRegressionValueMapProducer'
setattr(process,egmMod,process.egmGsfElectronIDs.clone())
setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
setattr(process,regMod,process.electronRegressionValueMapProducer.clone())
process.electrons = cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod))
    
    
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.electrons

process.antiElectronDiscrMVATrainingNtupleProducer = cms.EDAnalyzer("AntiElectronDiscrMVATrainingNtupleProducer",
    srcPFTaus = cms.InputTag('slimmedTausUpdated'),
    tauIdDiscriminators = cms.vstring(
        #DM finding
        "decayModeFindingNewDMs",
        "decayModeFinding",
        #Cut-based iso
        "photonPtSumOutsideSignalCone",
        "byCombinedIsolationDeltaBetaCorrRaw3Hits",
        "byLooseCombinedIsolationDeltaBetaCorr3Hits",
        "byMediumCombinedIsolationDeltaBetaCorr3Hits",
        "byTightCombinedIsolationDeltaBetaCorr3Hits",
        #MVAIso 2015
        "byIsolationMVArun2v1DBnewDMwLTraw",
        "byVLooseIsolationMVArun2v1DBnewDMwLT",
        "byLooseIsolationMVArun2v1DBnewDMwLT",
        "byMediumIsolationMVArun2v1DBnewDMwLT",
        "byTightIsolationMVArun2v1DBnewDMwLT",
        "byVTightIsolationMVArun2v1DBnewDMwLT",
        #MVAIso 2017v2
        "byIsolationMVArun2v1DBnewDMwLTraw2017v2", 
        "byVLooseIsolationMVArun2v1DBnewDMwLT2017v2",
        "byLooseIsolationMVArun2v1DBnewDMwLT2017v2",
        "byMediumIsolationMVArun2v1DBnewDMwLT2017v2",
        "byTightIsolationMVArun2v1DBnewDMwLT2017v2",
        "byVTightIsolationMVArun2v1DBnewDMwLT2017v2",
        #Anti-e MVA6 (2015 training)
        "againstElectronMVA6Raw",
        "againstElectronMVA6category",
        "againstElectronVLooseMVA6",
        "againstElectronLooseMVA6",
        "againstElectronMediumMVA6",
        "againstElectronTightMVA6",
        "againstElectronVTightMVA6",
        #Anti-mu cut based
        "againstMuonLoose3",
        "againstMuonTight3",
    ),
    srcGsfElectrons = cms.InputTag('slimmedElectrons'),
    conversionsMiniAOD = cms.InputTag('reducedEgamma:reducedConversions'),
    srcPrimaryVertex = cms.InputTag('offlineSlimmedPrimaryVertices'),
    srcGenElectrons = cms.InputTag('genElectrons'),
    srcGenTaus = cms.InputTag('tauGenJetsSelectorAllHadrons'),
    srcGenJets = cms.InputTag("genJetsAntiOverlapWithLeptonsVeto"),
    verbosity = cms.int32(0),
    #effAreasConfigFile = cms.FileInPath("RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt"),
    #MB: Use "Spring15 25ns cut-based "Veto" ID" as in 2nd ele veto the HTT analysis https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2017#Baseline%20$e\tau_{h}$ even if new tunes exist...     
    electronIdVeto = cms.string("cutBasedElectronID-Spring15-25ns-V1-standalone-veto"), #MB: This ID is used if set correctly and present in patElectrons, otherwise use custom one from eleTightIdMap
    eleTightIdMap = cms.InputTag("egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto"), #MB: To be used in case custom/new ID not in pat. To activate it one should set a dummy value to electronIdVeto argument
    #MB: ... one can also considered tighter selection for 3rd lepton veto i.e. "MVA ID 90% efficiency WP" (egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90)
    #electronIdVeto = cms.string("mvaEleID-Fall17-noIso-V1-wp90"),
    #eleTightIdMap = cms.InputTag("egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90"),
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.antiElectronDiscrMVATrainingNtupleProducer

process.p = cms.Path(process.produceAntiElectronDiscrMVATrainingNtupleSequence)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("antiElectronDiscrMVATrainingNtupleFromMiniAOD.root")
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)#,
    #SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.load('FWCore.MessageLogger.MessageLogger_cfi')
if process.maxEvents.input.value()>10:
     process.MessageLogger.cerr.FwkReport.reportEvery = process.maxEvents.input.value()//10
if process.maxEvents.input.value()>10000 or process.maxEvents.input.value()<0:
     process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')

#Uncomment to dump plain configuration for debugging
#processDumpFile = open('produceAntiElectronDiscrMVATrainingNtupleFromMiniAOD.dump', 'w')
#print >> processDumpFile, process.dumpPython()

