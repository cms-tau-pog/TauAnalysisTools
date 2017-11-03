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
					inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_8_0_26_patch1/src/TauAnalysisTools/TauAnalysisTools/test/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.weights.xml'),
					inputFileType = cms.string("XML"),
					inputVariables = cms.vstring(
						'TMath::Log(TMath::Max(1., recTauPt))',
						'TMath::Abs(recTauEta)',
						'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
						'TMath::Log(TMath::Max(1.e-2, neutralIsoPtsum_ptGt1.0))',
						'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
						'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))',
						'recTauDecayMode',
						'TMath::Min(30., recTauNphoton_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)',
						'TMath::Min(1., recTauEratio)',
						'TMath::Sign(+1., recImpactParam)',
						'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
						'TMath::Min(10., TMath::Abs(recImpactParamSign))',
						'TMath::Sign(+1., recImpactParam3D)',
						'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
						'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
						'hasRecDecayVertex',
						'TMath::Sqrt(recDecayDistMag)',
						'TMath::Min(10., recDecayDistSign)',
						'TMath::Max(-1.,recTauGJangleDiff)'
					),
					spectatorVariables = cms.vstring(
						'leadPFChargedHadrCandPt',
						'numOfflinePrimaryVertices',
						'genVisTauPt',
						'genTauPt',
						'byIsolationMVArun2v1DBoldDMwLTraw',
						'recTauLeadingTrackChi2'
					),
					gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1")
				)
			),
			outputFileType = cms.string("GBRForest"),
			outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2016_pt_0p1.root")
		),
		cms.PSet(
			categories = cms.VPSet(
				cms.PSet(
					inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_2_4/src/TauAnalysisTools/TauAnalysisTools/test/dataset/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.weights.xml'),
					inputFileType = cms.string("XML"),
					inputVariables = cms.vstring(
						'TMath::Log(TMath::Max(1., recTauPt))',
						'TMath::Abs(recTauEta)',
						'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
						'TMath::Log(TMath::Max(1.e-2, neutralIsoPtsum_ptGt1.0))',
						'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
						'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))',
						'recTauDecayMode',
						'TMath::Min(30., recTauNphoton_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)',
						'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)',
						'TMath::Min(1., recTauEratio)',
						'TMath::Sign(+1., recImpactParam)',
						'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
						'TMath::Min(10., TMath::Abs(recImpactParamSign))',
						'TMath::Sign(+1., recImpactParam3D)',
						'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
						'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
						'hasRecDecayVertex',
						'TMath::Sqrt(recDecayDistMag)',
						'TMath::Min(10., recDecayDistSign)',
						'TMath::Max(-1.,recTauGJangleDiff)'
						),
					spectatorVariables = cms.vstring(
						'leadPFChargedHadrCandPt',
						'numOfflinePrimaryVertices',
						'genVisTauPt',
						'genTauPt',
						'byIsolationMVArun2v1DBoldDMwLTraw',
						'byIsolationMVArun2v1DBoldDMwLTraw2016'
					),
					gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1")
				)
			),
			outputFileType = cms.string("GBRForest"),                                      
			outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017_pt_0p1.root")
		)
	)
)

process.p = cms.Path(process.gbrForestWriter)