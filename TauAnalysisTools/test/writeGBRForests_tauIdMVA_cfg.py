import FWCore.ParameterSet.Config as cms

process = cms.Process("writeGBRForests")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1) # CV: needs to be set to 1 so that GBRForestWriter::analyze method gets called exactly once         
)

process.source = cms.Source("EmptySource")

process.gbrForestWriter = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        cms.PSet(
            categories = cms.VPSet(
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V2/tauId_v3_0/trainfilesfinal_v1_oldDMs/weights/mvaIsolation3HitsDeltaR05opt1aLTDB_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
			            'TMath::Log(TMath::Max(1., recTauPt))',
			            'TMath::Abs(recTauEta)',
			            'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
			            'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum))',
			            'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
			            'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone))',
			            'recTauDecayMode',
			            'TMath::Min(30., recTauNphoton)',
			            'TMath::Min(0.5, recTauPtWeightedDetaStrip)',
			            'TMath::Min(0.5, recTauPtWeightedDphiStrip)',
			            'TMath::Min(0.5, recTauPtWeightedDrSignal)',
			            'TMath::Min(0.5, recTauPtWeightedDrIsolation)',
			            'TMath::Min(100., recTauLeadingTrackChi2)',
			            'TMath::Min(1., recTauEratio)',
			            'TMath::Sign(+1., recImpactParam)',
			            'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
			            'TMath::Min(10., TMath::Abs(recImpactParamSign))',
			            'TMath::Sign(+1., recImpactParam3D)',
			            'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
			            'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
			            'hasRecDecayVertex',
			            'TMath::Sqrt(recDecayDistMag)',
			            'TMath::Min(10., recDecayDistSign)'
                    ),
                    spectatorVariables = cms.vstring(
			            ##'recTauPt',
			            'leadPFChargedHadrCandPt',
			            'numOfflinePrimaryVertices',
			            'genVisTauPt',
			            'genTauPt',
			            'byIsolationMVArun2v1DBoldDMwLTraw'#,
			            #'byLooseCombinedIsolationDeltaBetaCorr3Hits',
			            #'byMediumCombinedIsolationDeltaBetaCorr3Hits',
			            #'byTightCombinedIsolationDeltaBetaCorr3Hits'
                    ),
                    gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT")
                )
            ),                                       
            outputFileType = cms.string("GBRForest"),                                      
            outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root")
        ),                                                 
        cms.PSet(
            categories = cms.VPSet(
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V2/tauId_v3_0/trainfilesfinal_newDMs_v1/weights/mvaIsolation3HitsDeltaR05opt1bLTDB_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
			            'TMath::Log(TMath::Max(1., recTauPt))',
			            'TMath::Abs(recTauEta)',
			            'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
			            'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum))',
			            'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
			            'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone))',
			            'recTauDecayMode',
			            'TMath::Min(30., recTauNphoton)',
			            'TMath::Min(0.5, recTauPtWeightedDetaStrip)',
			            'TMath::Min(0.5, recTauPtWeightedDphiStrip)',
			            'TMath::Min(0.5, recTauPtWeightedDrSignal)',
			            'TMath::Min(0.5, recTauPtWeightedDrIsolation)',
			            'TMath::Min(100., recTauLeadingTrackChi2)',
			            'TMath::Min(1., recTauEratio)',
			            'TMath::Sign(+1., recImpactParam)',
			            'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
			            'TMath::Min(10., TMath::Abs(recImpactParamSign))',
			            'TMath::Sign(+1., recImpactParam3D)',
			            'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
			            'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
			            'hasRecDecayVertex',
			            'TMath::Sqrt(recDecayDistMag)',
			            'TMath::Min(10., recDecayDistSign)'
                        ),
                    spectatorVariables = cms.vstring(
			            ##'recTauPt',
			            'leadPFChargedHadrCandPt',
			            'numOfflinePrimaryVertices',
			            'genVisTauPt',
			            'genTauPt',
			            'byIsolationMVArun2v1DBnewDMwLTraw'#,
			            #'byLooseCombinedIsolationDeltaBetaCorr3Hits',
			            #'byMediumCombinedIsolationDeltaBetaCorr3Hits',
			            #'byTightCombinedIsolationDeltaBetaCorr3Hits'
                    ),
                    gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT")
                )
            ),
            outputFileType = cms.string("GBRForest"),                                      
            outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root")
        )
    )
)

process.p = cms.Path(process.gbrForestWriter)

#  LocalWords:  recTauEta
