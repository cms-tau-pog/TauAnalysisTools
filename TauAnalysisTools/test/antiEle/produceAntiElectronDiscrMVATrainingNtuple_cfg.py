import FWCore.ParameterSet.Config as cms

process = cms.Process("produceAntiElectronDiscrMVATrainingNtuple")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
print "Use GeometryRecoDB and condDBv2"
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")

globalTag = "MCRUN2_74_V9"
process.GlobalTag.globaltag = cms.string(globalTag)
print "GlobalTag:", process.GlobalTag.globaltag

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://xrootd.unl.edu//store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/002F7FDD-BA13-E511-AA63-0026189437F5.root'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
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

process.load("RecoTauTag/Configuration/RecoPFTauTag_cff")
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.PFTau

##process.load("TauAnalysis/RecoTools/recoVertexSelection_cff")
##process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.selectPrimaryVertex

##process.dumpPFTaus = cms.EDAnalyzer("DumpPFTaus",
##    src = cms.InputTag('hpsPFTauProducer'),
##    srcTauRef = cms.InputTag('hpsPFTauProducer'),
##    srcTauRefDiscriminators = cms.VInputTag('hpsPFTauDiscriminationByDecayModeFinding'),
##    srcVertex = cms.InputTag('selectedPrimaryVertexHighestPtTrackSum')
##)
##process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.dumpPFTaus

process.tausForAntiElectronDiscrMVATraining = cms.EDFilter("PFTauSelector",
    src = cms.InputTag('hpsPFTauProducer'),
    discriminators = cms.VPSet(
        cms.PSet(
            discriminator = cms.InputTag('hpsPFTauDiscriminationByDecayModeFindingNewDMs'),
            selectionCut = cms.double(0.5)
        )
    ),
    cut = cms.string("pt > 18. & abs(eta) < 2.4")
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.tausForAntiElectronDiscrMVATraining

process.tausForAntiElectronDiscrMVATrainingDiscriminationByDecayModeFinding = process.hpsPFTauDiscriminationByDecayModeFindingNewDMs.clone(
    PFTauProducer = cms.InputTag('tausForAntiElectronDiscrMVATraining')
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.tausForAntiElectronDiscrMVATrainingDiscriminationByDecayModeFinding

process.tausForAntiElectronDiscrMVATrainingPrimaryVertexProducer = process.hpsPFTauPrimaryVertexProducer.clone(
    PFTauTag = cms.InputTag("tausForAntiElectronDiscrMVATraining"),
    discriminators = cms.VPSet(),
    cut = cms.string('')
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.tausForAntiElectronDiscrMVATrainingPrimaryVertexProducer
process.tausForAntiElectronDiscrMVATrainingSecondaryVertexProducer = process.hpsPFTauSecondaryVertexProducer.clone(
    PFTauTag = cms.InputTag("tausForAntiElectronDiscrMVATraining")
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.tausForAntiElectronDiscrMVATrainingSecondaryVertexProducer
process.tausForAntiElectronDiscrMVATrainingTransverseImpactParameters = process.hpsPFTauTransverseImpactParameters.clone(
    PFTauTag =  cms.InputTag("tausForAntiElectronDiscrMVATraining"),
    PFTauPVATag = cms.InputTag("tausForAntiElectronDiscrMVATrainingPrimaryVertexProducer"),
    PFTauSVATag = cms.InputTag("tausForAntiElectronDiscrMVATrainingSecondaryVertexProducer")
)    
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.tausForAntiElectronDiscrMVATrainingTransverseImpactParameters

tauIdDiscriminatorsToReRun = [
    "hpsPFTauDiscriminationByDecayModeFindingNewDMs",
    "hpsPFTauDiscriminationByDecayModeFindingOldDMs",
    "hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr",
    "hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr",
    "hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr",
    "hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits",
    "hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits",
    "hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits",
    "hpsPFTauDiscriminationByLooseElectronRejection",
    "hpsPFTauDiscriminationByMediumElectronRejection",
    "hpsPFTauDiscriminationByTightElectronRejection",
    "hpsPFTauDiscriminationByMVA5rawElectronRejection",
    "hpsPFTauDiscriminationByMVA5LooseElectronRejection",
    "hpsPFTauDiscriminationByMVA5MediumElectronRejection",
    "hpsPFTauDiscriminationByMVA5TightElectronRejection",
    "hpsPFTauDiscriminationByMVA5VTightElectronRejection",
]
for tauIdDiscriminator in tauIdDiscriminatorsToReRun:
    moduleToClone = getattr(process, tauIdDiscriminator)
    module = moduleToClone.clone(
        PFTauProducer = cms.InputTag('tausForAntiElectronDiscrMVATraining')
    )
    if hasattr(module, "Prediscriminants") and hasattr(module.Prediscriminants, "decayMode"):
        module.Prediscriminants.decayMode.Producer = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByDecayModeFinding')
    # CV: handle MVA working-point discriminators that are based on cutting on the raw MVA output stored in another discriminator
    if hasattr(module, "key"):
        module.key = cms.InputTag(module.key.getModuleLabel().replace("hpsPFTau", "tausForAntiElectronDiscrMVATraining"),  module.key.getProductInstanceLabel())
    if hasattr(module, "toMultiplex"):
        module.toMultiplex = cms.InputTag(module.toMultiplex.getModuleLabel().replace("hpsPFTau", "tausForAntiElectronDiscrMVATraining"), module.toMultiplex.getProductInstanceLabel())
    if hasattr(module, "srcTauTransverseImpactParameters"):
        module.srcTauTransverseImpactParameters = cms.InputTag('tausForAntiElectronDiscrMVATrainingTransverseImpactParameters')
    for srcIsolation in [ "srcChargedIsoPtSum", "srcNeutralIsoPtSum", "srcPUcorrPtSum" ]:
        if hasattr(module, srcIsolation):
            moduleAttr = getattr(module, srcIsolation)
            moduleAttr = cms.InputTag(moduleAttr.getModuleLabel().replace("hpsPFTau", "tausForAntiElectronDiscrMVATraining"), moduleAttr.getProductInstanceLabel())
            setattr(module, srcIsolation, moduleAttr)    
    moduleName = tauIdDiscriminator.replace("hpsPFTau", "tausForAntiElectronDiscrMVATraining")
    setattr(process, moduleName, module)
    process.produceAntiElectronDiscrMVATrainingNtupleSequence += module
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# select "good" reconstructed vertices
#
# CV: cut on ndof >= 4 if using 'offlinePrimaryVertices',
#                 >= 7 if using 'offlinePrimaryVerticesWithBS' as input
#
process.selectedOfflinePrimaryVertices = cms.EDFilter("VertexSelector",
    src = cms.InputTag('offlinePrimaryVertices'),
    cut = cms.string("isValid & ndof >= 4 & chi2 > 0 & tracksSize > 0 & abs(z) < 24 & abs(position.Rho) < 2."),
    filter = cms.bool(False)                                          
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.selectedOfflinePrimaryVertices

process.selectedOfflinePrimaryVerticesWithBS = process.selectedOfflinePrimaryVertices.clone(
    src = cms.InputTag('offlinePrimaryVerticesWithBS'),
    cut = cms.string("isValid & ndof >= 7 & chi2 > 0 & tracksSize > 0 & abs(z) < 24 & abs(position.Rho) < 2.")
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.selectedOfflinePrimaryVerticesWithBS
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# select generator level hadronic tau decays,
# veto jets overlapping with electrons or muons

process.prePFTauSequence = cms.Sequence()

if type == 'SignalMC' or type == 'BackgroundMC':
    process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
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
        src = cms.InputTag("genParticles"),
        cut = cms.string('abs(pdgId) = 11 & pt > 10.'),
        stableOnly = cms.bool(True),
        filter = cms.bool(False)
    )
    process.prePFTauSequence += process.genElectrons

    jetCollection = None
    if type == 'SignalMC':
        process.tauGenJetsSelectorAllHadrons.filter = cms.bool(True)

        process.genTauMatchedPFJets = cms.EDFilter("PFJetAntiOverlapSelector",
            src = cms.InputTag('ak4PFJets'),
            srcNotToBeFiltered = cms.VInputTag(
                'tauGenJetsSelectorAllHadrons'
            ),
            dRmin = cms.double(0.3),
            invert = cms.bool(True),
            filter = cms.bool(False)                                                          
        )
        process.prePFTauSequence += process.genTauMatchedPFJets
        jetCollection = "genTauMatchedPFJets"
    elif type == 'BackgroundMC':
        process.genElectrons.filter = cms.bool(True)
        
        process.genElectronMatchedPFJets = cms.EDFilter("PFJetAntiOverlapSelector",
            src = cms.InputTag('ak4PFJets'),
            srcNotToBeFiltered = cms.VInputTag(
                'genElectrons'
            ),
            dRmin = cms.double(0.3),
            invert = cms.bool(True),
            filter = cms.bool(False)                                                          
        )
        process.prePFTauSequence += process.genElectronMatchedPFJets
        jetCollection = "genElectronMatchedPFJets"
    if not jetCollection:
        raise ValueError("Invalid Parameter 'jetCollection' = None !!")    
    process.ak4PFJetTracksAssociatorAtVertex.jets = cms.InputTag(jetCollection)
    process.ak4PFJetsLegacyHPSPiZeros.jetSrc = cms.InputTag(jetCollection)
    process.recoTauAK4PFJets08Region.src = cms.InputTag(jetCollection)
    process.ak4PFJetsRecoTauChargedHadrons.jetSrc = cms.InputTag(jetCollection)
    process.combinatoricRecoTaus.jetSrc = cms.InputTag(jetCollection)

process.produceAntiElectronDiscrMVATrainingNtupleSequence.replace(process.PFTau, process.prePFTauSequence + process.PFTau)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# compute event weights for pile-up reweighting
# (Summer'12 MC to 2012 run ABCD data)

srcWeights = []
#if isMC:
    #from TauAnalysis.RecoTools.vertexMultiplicityReweight_cfi import vertexMultiplicityReweight
    #process.vertexMultiplicityReweight3d2012RunABCD = vertexMultiplicityReweight.clone(
        #inputFileName = cms.FileInPath("TauAnalysis/RecoTools/data/expPUpoissonMean_runs190456to208686_Mu17_Mu8.root"),
        #type = cms.string("gen3d"),
        #mcPeriod = cms.string("Summer12_S10")
    #)
    #process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.vertexMultiplicityReweight3d2012RunABCD
    #srcWeights.extend([ 'vertexMultiplicityReweight3d2012RunABCD' ])
#--------------------------------------------------------------------------------

process.antiElectronDiscrMVATrainingNtupleProducer = cms.EDAnalyzer("AntiElectronDiscrMVATrainingNtupleProducer",
    srcPFTaus = cms.InputTag('tausForAntiElectronDiscrMVATraining'),
    tauIdDiscriminators = cms.PSet(
        DecayModeFindingNewDMs = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByDecayModeFindingNewDMs'),
        DecayModeFindingOldDMs = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByDecayModeFindingOldDMs'),
        LooseCombIso = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByLooseCombinedIsolationDBSumPtCorr'),
        MediumCombIso = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMediumCombinedIsolationDBSumPtCorr'),
        TightCombIso = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByTightCombinedIsolationDBSumPtCorr'),
        LooseComb3HitsIso = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits'),
        MediumComb3HitsIso = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits'),
        TightComb3HitsIso = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits'),
        AntiELoose = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByLooseElectronRejection'),
        AntiEMedium = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMediumElectronRejection'),
        AntiETight = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByTightElectronRejection'),
        AntiEMVA5raw = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMVA5rawElectronRejection'),
        AntiEMVA5category = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMVA5rawElectronRejection:category'),
        AntiELooseMVA5 = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMVA5LooseElectronRejection'),
        AntiEMediumMVA5 = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMVA5MediumElectronRejection'),
        AntiETightMVA5 = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMVA5TightElectronRejection'),
        AntiEVTightMVA5 = cms.InputTag('tausForAntiElectronDiscrMVATrainingDiscriminationByMVA5VTightElectronRejection'),                                                               
    ),
    srcGsfElectrons = cms.InputTag('gedGsfElectrons'),
    srcPrimaryVertex = cms.InputTag('selectedOfflinePrimaryVertices'),
    srcGenElectrons = cms.InputTag('genElectrons'),
    srcGenTaus = cms.InputTag('tauGenJetsSelectorAllHadrons'),
    srcGenJets = cms.InputTag("genJetsAntiOverlapWithLeptonsVeto"),
    srcWeights = cms.VInputTag(srcWeights),
    verbosity = cms.int32(0)
)
process.produceAntiElectronDiscrMVATrainingNtupleSequence += process.antiElectronDiscrMVATrainingNtupleProducer

process.p = cms.Path(process.produceAntiElectronDiscrMVATrainingNtupleSequence)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("antiElectronDiscrMVATrainingNtuple.root")
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

processDumpFile = open('produceAntiElectronDiscrMVATrainingNtuple.dump', 'w')
print >> processDumpFile, process.dumpPython()
