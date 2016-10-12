import FWCore.ParameterSet.Config as cms

process = cms.Process("produceTauIdMVATrainingNtupleMiniAOD")

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
#process.load('Configuration.StandardSequences.Geometry_cff')
#process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = cms.string('auto:run2_mc')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

#process.add_(cms.Service("PrintLoadingPlugins"))

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:/data1/veelken/CMSSW_5_3_x/skims/96E96DDB-61D3-E111-BEFB-001E67397D05.root'
        #'file:/nfs/dust/cms/user/anayak/CMS/Ntuple_Phys14TauId/AOD_VBFHTauTau_fromYuta.root'
        #'root://xrootd.ba.infn.it//store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/00CC714A-F86B-E411-B99A-0025904B5FB8.root'
        #'file:/afs/cern.ch/work/f/fromeo/public/TauRunII/GluGluToHToTauTau_M125_D08.root'
        #'root://xrootd.ba.infn.it//store/cmst3/user/ytakahas/CMG/QCD_Pt-15to3000_Tune4C_Flat_13TeV_pythia8/Phys14DR-PU20bx25_trkalmb_PHYS14_25_V1-v1/AODSIM/Dynamic95_20150520/aod_1.root'
        'file:/disk1/MVAonMiniAOD/8020_file1_official.root'
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
    cut = cms.string("isValid & ndof >= 4 & chi2 > 0 & tracksSize > 0 & abs(z) < 24 & abs(position.Rho) < 2."),
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
    srcRecTaus = cms.InputTag('slimmedTaus'),
    srcGenParticles = cms.InputTag('packedGenParticles'),        
    minGenVisPt = cms.double(10.),                                          
    dRmatch = cms.double(0.3),
    tauIdDiscriminators = cms.PSet(
        decayModeFindingNewDMs = cms.string('decayModeFindingNewDMs'),
        decayModeFindingOldDMs = cms.string('decayModeFinding'),
        #byLooseCombinedIsolationDeltaBetaCorr8Hits = cms.string('tausForTauIdMVATrainingDiscriminationByLooseCombinedIsolationDBSumPtCorr'),
        #byMediumCombinedIsolationDeltaBetaCorr8Hits = cms.string('tausForTauIdMVATrainingDiscriminationByMediumCombinedIsolationDBSumPtCorr'),
        #byTightCombinedIsolationDeltaBetaCorr8Hits = cms.string('tausForTauIdMVATrainingDiscriminationByTightCombinedIsolationDBSumPtCorr'),
        byLooseCombinedIsolationDeltaBetaCorr3Hits = cms.string('byLooseCombinedIsolationDeltaBetaCorr3Hits'),
        byMediumCombinedIsolationDeltaBetaCorr3Hits = cms.string('byMediumCombinedIsolationDeltaBetaCorr3Hits'),
        byTightCombinedIsolationDeltaBetaCorr3Hits = cms.string('byTightCombinedIsolationDeltaBetaCorr3Hits'),
        #byLoosePileupWeightedIsolation3Hits = cms.string('tausForTauIdMVATrainingDiscriminationByLoosePileupWeightedIsolation3Hits'),
        #byMediumPileupWeightedIsolation3Hits = cms.string('tausForTauIdMVATrainingDiscriminationByMediumPileupWeightedIsolation3Hits'),
        #byTightPileupWeightedIsolation3Hits = cms.string('tausForTauIdMVATrainingDiscriminationByTightPileupWeightedIsolation3Hits'),
        chargedIsoPtSum = cms.string('chargedIsoPtSum'),
        neutralIsoPtSum = cms.string('neutralIsoPtSum'),
        puCorrPtSum = cms.string('puCorrPtSum'),
        neutralIsoPtSumWeight = cms.string('neutralIsoPtSumWeight'),
        footprintCorrection = cms.string('footprintCorrection'),
        photonPtSumOutsideSignalCone = cms.string('photonPtSumOutsideSignalCone'),
        #byIsolationMVAraw = cms.string('tausForTauIdMVATrainingDiscriminationByIsolationMVAraw'),
        #byIsolationMVA2raw = cms.string('tausForTauIdMVATrainingDiscriminationByIsolationMVA2raw'),
        #byIsolationMVA3oldDMwoLTraw = cms.string('tausForTauIdMVATrainingDiscriminationByIsolationMVA3oldDMwoLTraw'),
        #byVLooseIsolationMVA3oldDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByVLooseIsolationMVA3oldDMwoLT'),
        #byLooseIsolationMVA3oldDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByLooseIsolationMVA3oldDMwoLT'),
        #byMediumIsolationMVA3oldDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByMediumIsolationMVA3oldDMwoLT'),
        #byTightIsolationMVA3oldDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByTightIsolationMVA3oldDMwoLT'),
        #byVTightIsolationMVA3oldDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByVTightIsolationMVA3oldDMwoLT'),
        #byVVTightIsolationMVA3oldDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByVVTightIsolationMVA3oldDMwoLT'),                 
        #byIsolationMVA3oldDMwLTraw = cms.string('tausForTauIdMVATrainingDiscriminationByIsolationMVA3oldDMwLTraw'),
        #byVLooseIsolationMVA3oldDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByVLooseIsolationMVA3oldDMwLT'),
        #byLooseIsolationMVA3oldDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByLooseIsolationMVA3oldDMwLT'),
        #byMediumIsolationMVA3oldDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByMediumIsolationMVA3oldDMwLT'),
        #byTightIsolationMVA3oldDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByTightIsolationMVA3oldDMwLT'),
        #byVTightIsolationMVA3oldDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByVTightIsolationMVA3oldDMwLT'),
        #byVVTightIsolationMVA3oldDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByVVTightIsolationMVA3oldDMwLT'),                
        #byIsolationMVA3newDMwoLTraw = cms.string('tausForTauIdMVATrainingDiscriminationByIsolationMVA3newDMwoLTraw'),
        #byVLooseIsolationMVA3newDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByVLooseIsolationMVA3newDMwoLT'),
        #byLooseIsolationMVA3newDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByLooseIsolationMVA3newDMwoLT'),
        #byMediumIsolationMVA3newDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByMediumIsolationMVA3newDMwoLT'),
        #byTightIsolationMVA3newDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByTightIsolationMVA3newDMwoLT'),
        #byVTightIsolationMVA3newDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByVTightIsolationMVA3newDMwoLT'),
        #byVVTightIsolationMVA3newDMwoLT = cms.string('tausForTauIdMVATrainingDiscriminationByVVTightIsolationMVA3newDMwoLT'),                                   
        #byIsolationMVA3newDMwLTraw = cms.string('tausForTauIdMVATrainingDiscriminationByIsolationMVA3newDMwLTraw'),
        #byVLooseIsolationMVA3newDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByVLooseIsolationMVA3newDMwLT'),
        #byLooseIsolationMVA3newDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByLooseIsolationMVA3newDMwLT'),
        #byMediumIsolationMVA3newDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByMediumIsolationMVA3newDMwLT'),
        #byTightIsolationMVA3newDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByTightIsolationMVA3newDMwLT'),
        #byVTightIsolationMVA3newDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByVTightIsolationMVA3newDMwLT'),
        #byVVTightIsolationMVA3newDMwLT = cms.string('tausForTauIdMVATrainingDiscriminationByVVTightIsolationMVA3newDMwLT'),                                  
        #againstElectronLooseMVA3 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA3LooseElectronRejection'),
        #againstElectronMediumMVA3 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA3MediumElectronRejection'),
        #againstElectronTightMVA3 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA3TightElectronRejection'),
        #againstElectronVTightMVA3 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA3VTightElectronRejection'),
        #againstElectronLoose = cms.string('tausForTauIdMVATrainingDiscriminationByLooseElectronRejection'),
        #againstElectronMedium = cms.string('tausForTauIdMVATrainingDiscriminationByMediumElectronRejection'),
        #againstElectronTight = cms.string('tausForTauIdMVATrainingDiscriminationByTightElectronRejection'),
        #againstElectronLooseMVA5 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA5LooseElectronRejection'),
        #againstElectronMediumMVA5 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA5MediumElectronRejection'),
        #againstElectronTightMVA5 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA5TightElectronRejection'),
        #againstElectronVLooseMVA5 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA5VLooseElectronRejection'),
        #againstElectronVTightMVA5 = cms.string('tausForTauIdMVATrainingDiscriminationByMVA5VTightElectronRejection'),
        #againstElectronDeadECAL = cms.string('tausForTauIdMVATrainingDiscriminationByDeadECALElectronRejection'),
        #againstMuonLoose = cms.string('tausForTauIdMVATrainingDiscriminationByLooseMuonRejection'),
        #againstMuonMedium = cms.string('tausForTauIdMVATrainingDiscriminationByMediumMuonRejection'),
        #againstMuonTight = cms.string('tausForTauIdMVATrainingDiscriminationByTightMuonRejection'),
        #againstMuonLoose2 = cms.string('tausForTauIdMVATrainingDiscriminationByLooseMuonRejection2'),
        #againstMuonMedium2 = cms.string('tausForTauIdMVATrainingDiscriminationByMediumMuonRejection2'),
        #againstMuonTight2 = cms.string('tausForTauIdMVATrainingDiscriminationByTightMuonRejection2'),
        againstMuonLoose3 = cms.string('againstMuonLoose3'),
        againstMuonTight3 = cms.string('againstMuonTight3')
        #againstMuonMVAraw = cms.string('tausForTauIdMVATrainingDiscriminationByMVArawMuonRejection'),                                                            
        #againstMuonLooseMVA = cms.string('tausForTauIdMVATrainingDiscriminationByMVALooseMuonRejection'),
        #againstMuonMediumMVA = cms.string('tausForTauIdMVATrainingDiscriminationByMVAMediumMuonRejection'),
        #againstMuonTightMVA = cms.string('tausForTauIdMVATrainingDiscriminationByMVATightMuonRejection')                                         
    ),
    isolationPtSums = cms.PSet(
        chargedIsoPtSum = cms.string("chargedIsoPtSum"),
        neutralIsoPtSum = cms.string("neutralIsoPtSum"),
        puCorrPtSum = cms.string("puCorrPtSum"), 
        neutralIsoPtSumWeight = cms.string("neutralIsoPtSumWeight"),
        footprintCorrection = cms.string("footprintCorrection"),
        photonPtSumOutsideSignalCone = cms.string("photonPtSumOutsideSignalCone")
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
    #--------------------------------------------------------                                                                       
    srcWeights = cms.VInputTag(srcWeights),
    verbosity = cms.int32(0)
)

dRisoCone = 0.4

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

process.p = cms.Path(process.produceTauIdMVATrainingNtupleMiniAODSequence)
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




