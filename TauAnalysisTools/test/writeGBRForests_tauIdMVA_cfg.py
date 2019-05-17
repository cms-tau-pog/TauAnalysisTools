import FWCore.ParameterSet.Config as cms

process = cms.Process("writeGBRForests")

process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32(1) # CV: needs to be set to 1 so that GBRForestWriter::analyze method gets called exactly once
)

process.source = cms.Source("EmptySource")

process.gbrForestWriter = cms.EDAnalyzer("GBRForestWriter",
	jobs=cms.VPSet(
		# cms.PSet(
		# 	categories = cms.VPSet(
		# 		cms.PSet(
		# 			inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_8_0_26_patch1/src/TauAnalysisTools/TauAnalysisTools/test/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.weights.xml'),
		# 			inputFileType = cms.string("XML"),
		# 			inputVariables = cms.vstring(
		# 				'TMath::Log(TMath::Max(1., recTauPt))',
		# 				'TMath::Abs(recTauEta)',
		# 				'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, neutralIsoPtsum_ptGt1.0))',
		# 				'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))',
		# 				'recTauDecayMode',
		# 				'TMath::Min(30., recTauNphoton_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)',
		# 				'TMath::Min(1., recTauEratio)',
		# 				'TMath::Sign(+1., recImpactParam)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign))',
		# 				'TMath::Sign(+1., recImpactParam3D)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
		# 				'hasRecDecayVertex',
		# 				'TMath::Sqrt(recDecayDistMag)',
		# 				'TMath::Min(10., recDecayDistSign)',
		# 				'TMath::Max(-1.,recTauGJangleDiff)'
		# 			),
		# 			spectatorVariables = cms.vstring(
		# 				'leadPFChargedHadrCandPt',
		# 				'numOfflinePrimaryVertices',
		# 				'genVisTauPt',
		# 				'genTauPt',
		# 				'byIsolationMVArun2v1DBoldDMwLTraw',
		# 				'recTauLeadingTrackChi2'
		# 			),
		# 			gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1")
		# 		)
		# 	),
		# 	outputFileType = cms.string("GBRForest"),
		# 	outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2016_pt_0p1.root")
		# ),
		# cms.PSet(
		# 	categories = cms.VPSet(
		# 		cms.PSet(
		# 			inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_2_4/src/TauAnalysisTools/TauAnalysisTools/test/dataset/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.weights.xml'),
		# 			inputFileType = cms.string("XML"),
		# 			inputVariables = cms.vstring(
		# 				'TMath::Log(TMath::Max(1., recTauPt))',
		# 				'TMath::Abs(recTauEta)',
		# 				'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, neutralIsoPtsum_ptGt1.0))',
		# 				'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))',
		# 				'recTauDecayMode',
		# 				'TMath::Min(30., recTauNphoton_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)',
		# 				'TMath::Min(1., recTauEratio)',
		# 				'TMath::Sign(+1., recImpactParam)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign))',
		# 				'TMath::Sign(+1., recImpactParam3D)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
		# 				'hasRecDecayVertex',
		# 				'TMath::Sqrt(recDecayDistMag)',
		# 				'TMath::Min(10., recDecayDistSign)',
		# 				'TMath::Max(-1.,recTauGJangleDiff)'
		# 				),
		# 			spectatorVariables = cms.vstring(
		# 				'leadPFChargedHadrCandPt',
		# 				'numOfflinePrimaryVertices',
		# 				'genVisTauPt',
		# 				'genTauPt',
		# 				'byIsolationMVArun2v1DBoldDMwLTraw',
		# 				'byIsolationMVArun2v1DBoldDMwLTraw2016'
		# 			),
		# 			gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1")
		# 		)
		# 	),
		# 	outputFileType = cms.string("GBRForest"),
		# 	outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017_pt_0p1.root")
		# )
		#
		# # 2017v2 Old DM 0.5 cone
		# cms.PSet(
		# 	categories = cms.VPSet(
		# 		cms.PSet(
		# 			inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/src/TauAnalysisTools/TauAnalysisTools/test/dataset/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.weights.xml'),
		# 			inputFileType = cms.string("XML"),
		# 			inputVariables = cms.vstring(
		# 				'TMath::Log(TMath::Max(1., recTauPt))',
		# 				'TMath::Abs(recTauEta)',
		# 				'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))',
		# 				'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))',
		# 				'recTauDecayMode',
		# 				'TMath::Min(30., recTauNphoton_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)',
		# 				'TMath::Min(1., recTauEratio)',
		# 				'TMath::Sign(+1., recImpactParam)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign))',
		# 				'TMath::Sign(+1., recImpactParam3D)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
		# 				'hasRecDecayVertex',
		# 				'TMath::Sqrt(recDecayDistMag)',
		# 				'TMath::Min(10., recDecayDistSign)',
		# 				'TMath::Max(-1.,recTauGJangleDiff)'
		# 				),
		# 			spectatorVariables = cms.vstring(
		# 	            'recTauPt',
		# 	            'leadPFChargedHadrCandPt',
		# 	            'numOfflinePrimaryVertices',
		# 	            'genVisTauPt',
		# 	            'genTauPt',
		# 	            'byIsolationMVArun2v1DBdR03oldDMwLTraw',
		# 	            'byIsolationMVArun2v1DBoldDMwLTraw',
		# 	            'byIsolationMVArun2v1DBoldDMwLTraw2016',
		# 	            'byIsolationMVArun2017v1DBoldDMwLTraw2017',
		# 	            'byIsolationMVArun2v1DBnewDMwLTraw',
		# 	            'byIsolationMVArun2v1DBnewDMwLTraw2016',
		# 	            'byCombinedIsolationDeltaBetaCorrRaw3Hits',
		# 	            'byLooseCombinedIsolationDeltaBetaCorr3Hits',
		# 	            'byMediumCombinedIsolationDeltaBetaCorr3Hits',
		# 	            'byTightCombinedIsolationDeltaBetaCorr3Hits',
		# 	            'byIsolationMVArun2v1DBoldDMwLTraw',
		# 	            'byIsolationMVArun2v1DBoldDMwLTraw2016',
		# 	            'byIsolationMVArun2017v1DBoldDMwLTraw2017',
		# 	            'recTauNphoton',
		# 	            'recTauNphoton_ptGt1.0',
		# 	            'recTauNphoton_ptGt1.5',
		# 	            'photonPtSumOutsideSignalCone_ptGt1.0',
		# 	            'photonPtSumOutsideSignalCone_ptGt1.5',
		# 	            'photonPtSumOutsideSignalConedRgt0p1_ptGt1.0',
		# 	            'photonPtSumOutsideSignalConedRgt0p1_ptGt1.5',
		# 	            'neutralIsoPtSum_ptGt1.0',
		# 	            'neutralIsoPtSum_ptGt1.5',
		# 	            'recTauPtWeightedDetaStrip_ptGt1.0',
		# 	            'recTauPtWeightedDetaStrip_ptGt1.5',
		# 	            'recTauPtWeightedDphiStrip_ptGt1.0',
		# 	            'recTauPtWeightedDphiStrip_ptGt1.5',
		# 	            'recTauPtWeightedDrSignal_ptGt1.0',
		# 	            'recTauPtWeightedDrSignal_ptGt1.5',
		# 	            'recTauPtWeightedDrIsolation_ptGt1.0',
		# 	            'recTauPtWeightedDrIsolation_ptGt1.5',
		# 	            'chargedIsoPtSumdR03',
		# 	            'neutralIsoPtSumdR03',
		# 	            'neutralIsoPtSum_IsoConeR0p3_ptGt1.0',
		# 	            'neutralIsoPtSum_IsoConeR0p3_ptGt1.5',
		# 	            'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0',
		# 	            'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.5'
		# 			),
		# 			gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT2017v2")
		# 		)
		# 	),
		# 	outputFileType = cms.string("GBRForest"),
		# 	outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017v2_dR0p5.root")
		# ),

		# # 2017v2 Old DM 0.3 cone
		# cms.PSet(
		# 	categories = cms.VPSet(
		# 		cms.PSet(
		# 			inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/src/TauAnalysisTools/TauAnalysisTools/test/dataset/weights/mvaIsolation3HitsDeltaR03opt2aLTDB_BDTG.weights.xml'),
		# 			inputFileType = cms.string("XML"),
		# 			inputVariables = cms.vstring(
		# 				'TMath::Log(TMath::Max(1., recTauPt))',
		# 				'TMath::Abs(recTauEta)',
		# 				'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSumdR03))',
		# 				'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSumdR03))',
		# 				'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalConedR03))',
		# 				'recTauDecayMode',
		# 				'TMath::Min(30., recTauNphoton)',
		# 				'TMath::Min(0.5, recTauPtWeightedDetaStrip)',
		# 				'TMath::Min(0.5, recTauPtWeightedDphiStrip)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrSignal)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrIsolation)',
		# 				'TMath::Min(1., recTauEratio)',
		# 				'TMath::Sign(+1., recImpactParam)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign))',
		# 				'TMath::Sign(+1., recImpactParam3D)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
		# 				'hasRecDecayVertex',
		# 				'TMath::Sqrt(recDecayDistMag)',
		# 				'TMath::Min(10., recDecayDistSign)',
		# 				'TMath::Max(-1.,recTauGJangleDiff)'
		# 				),
		# 			spectatorVariables = cms.vstring(
		# 				'recTauPt',
		# 				'leadPFChargedHadrCandPt',
		# 				'numOfflinePrimaryVertices',
		# 				'genVisTauPt',
		# 				'genTauPt',
		# 				'byIsolationMVArun2v1DBdR03oldDMwLTraw',
		# 				'byIsolationMVArun2v1DBoldDMwLTraw',
		# 				'byIsolationMVArun2v1DBoldDMwLTraw2016',
		# 				'byIsolationMVArun2017v1DBoldDMwLTraw2017',
		# 				'byIsolationMVArun2v1DBnewDMwLTraw',
		# 				'byIsolationMVArun2v1DBnewDMwLTraw2016',
		# 				'byCombinedIsolationDeltaBetaCorrRaw3Hits',
		# 				'byLooseCombinedIsolationDeltaBetaCorr3Hits',
		# 				'byMediumCombinedIsolationDeltaBetaCorr3Hits',
		# 				'byTightCombinedIsolationDeltaBetaCorr3Hits',
		# 				'byIsolationMVArun2v1DBdR03oldDMwLTraw',
		# 				'recTauNphoton',
		# 				'recTauNphoton_ptGt1.0',
		# 				'recTauNphoton_ptGt1.5',
		# 				'photonPtSumOutsideSignalCone_ptGt1.0',
		# 				'photonPtSumOutsideSignalCone_ptGt1.5',
		# 				'photonPtSumOutsideSignalConedRgt0p1_ptGt1.0',
		# 				'photonPtSumOutsideSignalConedRgt0p1_ptGt1.5',
		# 				'neutralIsoPtSum_ptGt1.0',
		# 				'neutralIsoPtSum_ptGt1.5',
		# 				'recTauPtWeightedDetaStrip_ptGt1.0',
		# 				'recTauPtWeightedDetaStrip_ptGt1.5',
		# 				'recTauPtWeightedDphiStrip_ptGt1.0',
		# 				'recTauPtWeightedDphiStrip_ptGt1.5',
		# 				'recTauPtWeightedDrSignal_ptGt1.0',
		# 				'recTauPtWeightedDrSignal_ptGt1.5',
		# 				'recTauPtWeightedDrIsolation_ptGt1.0',
		# 				'recTauPtWeightedDrIsolation_ptGt1.5',
		# 				'chargedIsoPtSumdR03',
		# 				'neutralIsoPtSumdR03',
		# 				'neutralIsoPtSum_IsoConeR0p3_ptGt1.0',
		# 				'neutralIsoPtSum_IsoConeR0p3_ptGt1.5',
		# 				'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0',
		# 				'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.5'
		# 			),
		# 			gbrForestName = cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2017v2")
		# 		)
		# 	),
		# 	outputFileType = cms.string("GBRForest"),
		# 	outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017v2_dR0p3.root")
		# ),
		# #
		# # 2017v2 New DM 0.5 cone
		# cms.PSet(
		# 	categories = cms.VPSet(
		# 		cms.PSet(
		# 			inputFileName = cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/src/TauAnalysisTools/TauAnalysisTools/test/dataset/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_BDTG.weights.xml'),
		# 			inputFileType = cms.string("XML"),
		# 			inputVariables = cms.vstring(
		# 				'TMath::Log(TMath::Max(1., recTauPt))',
		# 				'TMath::Abs(recTauEta)',
		# 				'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))',
		# 				'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
		# 				'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))',
		# 				'recTauDecayMode',
		# 				'TMath::Min(30., recTauNphoton_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)',
		# 				'TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)',
		# 				'TMath::Min(1., recTauEratio)',
		# 				'TMath::Sign(+1., recImpactParam)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign))',
		# 				'TMath::Sign(+1., recImpactParam3D)',
		# 				'TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))',
		# 				'TMath::Min(10., TMath::Abs(recImpactParamSign3D))',
		# 				'hasRecDecayVertex',
		# 				'TMath::Sqrt(recDecayDistMag)',
		# 				'TMath::Min(10., recDecayDistSign)',
		# 				'TMath::Max(-1.,recTauGJangleDiff)'
		# 				),
		# 			spectatorVariables = cms.vstring(
		# 	            'recTauPt',
		# 	            'leadPFChargedHadrCandPt',
		# 	            'numOfflinePrimaryVertices',
		# 	            'genVisTauPt',
		# 	            'genTauPt',
		# 	            'byIsolationMVArun2v1DBdR03oldDMwLTraw',
		# 	            'byIsolationMVArun2v1DBoldDMwLTraw',
		# 	            'byIsolationMVArun2v1DBoldDMwLTraw2016',
		# 	            'byIsolationMVArun2017v1DBoldDMwLTraw2017',
		# 	            'byIsolationMVArun2v1DBnewDMwLTraw',
		# 	            'byIsolationMVArun2v1DBnewDMwLTraw2016',
		# 	            'byCombinedIsolationDeltaBetaCorrRaw3Hits',
		# 	            'byLooseCombinedIsolationDeltaBetaCorr3Hits',
		# 	            'byMediumCombinedIsolationDeltaBetaCorr3Hits',
		# 	            'byTightCombinedIsolationDeltaBetaCorr3Hits',
		# 	            'byIsolationMVArun2v1DBnewDMwLTraw',
		# 	            'byIsolationMVArun2v1DBnewDMwLTraw2016',
		# 	            'byIsolationMVArun2017v1DBoldDMwLTraw2017'
		# 			),
		# 			gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT2017v2")
		# 		)
		# 	),
		# 	outputFileType = cms.string("GBRForest"),
		# 	outputFileName = cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT_2017v2_dR0p5.root")
		# )
		# 2018 Old DM 0.5 cone
		cms.PSet(
			categories=cms.VPSet(
				cms.PSet(
					inputFileName=cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/dataset_oldDM_tauId_dR05_old_v2/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.weights.xml'),
					inputFileType=cms.string("XML"),
					inputVariables=cms.vstring(
						'TMath::Log(TMath::Max(1., recTauPt))',
						'TMath::Abs(recTauEta)',
						'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
						'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))',
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
					spectatorVariables=cms.vstring(
			            'recTauPt',
			            'leadPFChargedHadrCandPt',
			            'numOfflinePrimaryVertices',
			            'genVisTauPt',
			            'genTauPt',
			            'byIsolationMVArun2v1DBdR03oldDMwLTraw',
			            'byIsolationMVArun2v1DBoldDMwLTraw',
			            'byIsolationMVArun2v1DBoldDMwLTraw2016',
			            'byIsolationMVArun2017v1DBoldDMwLTraw2017',
			            'byIsolationMVArun2v1DBnewDMwLTraw',
			            'byIsolationMVArun2v1DBnewDMwLTraw2016',
			            'byCombinedIsolationDeltaBetaCorrRaw3Hits',
			            'byLooseCombinedIsolationDeltaBetaCorr3Hits',
			            'byMediumCombinedIsolationDeltaBetaCorr3Hits',
			            'byTightCombinedIsolationDeltaBetaCorr3Hits',
			            'byIsolationMVArun2v1DBoldDMwLTraw',
			            'byIsolationMVArun2v1DBoldDMwLTraw2016',
			            'byIsolationMVArun2017v1DBoldDMwLTraw2017',
			            'recTauNphoton',
			            'recTauNphoton_ptGt1.0',
			            'recTauNphoton_ptGt1.5',
			            'photonPtSumOutsideSignalCone_ptGt1.0',
			            'photonPtSumOutsideSignalCone_ptGt1.5',
			            'photonPtSumOutsideSignalConedRgt0p1_ptGt1.0',
			            'photonPtSumOutsideSignalConedRgt0p1_ptGt1.5',
			            'neutralIsoPtSum_ptGt1.0',
			            'neutralIsoPtSum_ptGt1.5',
			            'recTauPtWeightedDetaStrip_ptGt1.0',
			            'recTauPtWeightedDetaStrip_ptGt1.5',
			            'recTauPtWeightedDphiStrip_ptGt1.0',
			            'recTauPtWeightedDphiStrip_ptGt1.5',
			            'recTauPtWeightedDrSignal_ptGt1.0',
			            'recTauPtWeightedDrSignal_ptGt1.5',
			            'recTauPtWeightedDrIsolation_ptGt1.0',
			            'recTauPtWeightedDrIsolation_ptGt1.5',
			            'chargedIsoPtSumdR03',
			            'neutralIsoPtSumdR03',
			            'neutralIsoPtSum_IsoConeR0p3_ptGt1.0',
			            'neutralIsoPtSum_IsoConeR0p3_ptGt1.5',
			            'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0',
			            'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.5'
					),
					gbrForestName=cms.string("tauIdMVAIsoDBoldDMwLT2018")  # consistent with TauAnalysisTools/TauAnalysisTools/macros/plotTauIdMVAEfficiency_and_FakeRate.C
				)
			),
			outputFileType=cms.string("GBRForest"),
			outputFileName=cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2018_dR0p5.root")  #arbitrary
		),
		#
		# 2018 New DM 0.5 cone
		cms.PSet(
			categories=cms.VPSet(
				cms.PSet(
					inputFileName=cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/dataset_newDM_tauId_dR05_new_v2/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_BDTG.weights.xml'),
					inputFileType=cms.string("XML"),
					inputVariables=cms.vstring(
						'TMath::Log(TMath::Max(1., recTauPt))',
						'TMath::Abs(recTauEta)',
						'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))',
						'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))',
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
					spectatorVariables=cms.vstring(
			            'recTauPt',
			            'leadPFChargedHadrCandPt',
			            'numOfflinePrimaryVertices',
			            'genVisTauPt',
			            'genTauPt',
			            'byIsolationMVArun2v1DBdR03oldDMwLTraw',
			            'byIsolationMVArun2v1DBoldDMwLTraw',
			            'byIsolationMVArun2v1DBoldDMwLTraw2016',
			            'byIsolationMVArun2017v1DBoldDMwLTraw2017',
			            'byIsolationMVArun2v1DBnewDMwLTraw',
			            'byIsolationMVArun2v1DBnewDMwLTraw2016',
			            'byCombinedIsolationDeltaBetaCorrRaw3Hits',
			            'byLooseCombinedIsolationDeltaBetaCorr3Hits',
			            'byMediumCombinedIsolationDeltaBetaCorr3Hits',
			            'byTightCombinedIsolationDeltaBetaCorr3Hits',
			            'byIsolationMVArun2v1DBnewDMwLTraw',
			            'byIsolationMVArun2v1DBnewDMwLTraw2016',
			            'byIsolationMVArun2017v1DBoldDMwLTraw2017'
					),
					gbrForestName=cms.string("tauIdMVAIsoDBnewDMwLT2018")  # consistent with TauAnalysisTools/TauAnalysisTools/macros/plotTauIdMVAEfficiency_and_FakeRate.C
				)
			),
			outputFileType=cms.string("GBRForest"),
			outputFileName=cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT_2018_dR0p5.root")
		),
		#
		# 2018 Old DM 0.3 cone
		cms.PSet(
			categories=cms.VPSet(
				cms.PSet(
					inputFileName=cms.string('/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/dataset_oldDM_tauId_dR03_old_v2/weights/mvaIsolation3HitsDeltaR03opt2aLTDB_BDTG.weights.xml'),
					inputFileType=cms.string("XML"),
					inputVariables=cms.vstring(
						'TMath::Log(TMath::Max(1., recTauPt))',
						'TMath::Abs(recTauEta)',
						'TMath::Log(TMath::Max(1.e-2, chargedIsoPtSumdR03))',
						'TMath::Log(TMath::Max(1.e-2, neutralIsoPtSumdR03))',
						'TMath::Log(TMath::Max(1.e-2, puCorrPtSum))',
						'TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalConedR03))',
						'recTauDecayMode',
						'TMath::Min(30., recTauNphoton)',
						'TMath::Min(0.5, recTauPtWeightedDetaStrip)',
						'TMath::Min(0.5, recTauPtWeightedDphiStrip)',
						'TMath::Min(0.5, recTauPtWeightedDrSignal)',
						'TMath::Min(0.5, recTauPtWeightedDrIsolation)',
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
					spectatorVariables=cms.vstring(
						'recTauPt',
						'leadPFChargedHadrCandPt',
						'numOfflinePrimaryVertices',
						'genVisTauPt',
						'genTauPt',
						'byIsolationMVArun2v1DBdR03oldDMwLTraw',
						'byIsolationMVArun2v1DBoldDMwLTraw',
						'byIsolationMVArun2v1DBoldDMwLTraw2016',
						'byIsolationMVArun2017v1DBoldDMwLTraw2017',
						'byIsolationMVArun2v1DBnewDMwLTraw',
						'byIsolationMVArun2v1DBnewDMwLTraw2016',
						'byCombinedIsolationDeltaBetaCorrRaw3Hits',
						'byLooseCombinedIsolationDeltaBetaCorr3Hits',
						'byMediumCombinedIsolationDeltaBetaCorr3Hits',
						'byTightCombinedIsolationDeltaBetaCorr3Hits',
						'byIsolationMVArun2v1DBdR03oldDMwLTraw',
						'recTauNphoton',
						'recTauNphoton_ptGt1.0',
						'recTauNphoton_ptGt1.5',
						'photonPtSumOutsideSignalCone_ptGt1.0',
						'photonPtSumOutsideSignalCone_ptGt1.5',
						'photonPtSumOutsideSignalConedRgt0p1_ptGt1.0',
						'photonPtSumOutsideSignalConedRgt0p1_ptGt1.5',
						'neutralIsoPtSum_ptGt1.0',
						'neutralIsoPtSum_ptGt1.5',
						'recTauPtWeightedDetaStrip_ptGt1.0',
						'recTauPtWeightedDetaStrip_ptGt1.5',
						'recTauPtWeightedDphiStrip_ptGt1.0',
						'recTauPtWeightedDphiStrip_ptGt1.5',
						'recTauPtWeightedDrSignal_ptGt1.0',
						'recTauPtWeightedDrSignal_ptGt1.5',
						'recTauPtWeightedDrIsolation_ptGt1.0',
						'recTauPtWeightedDrIsolation_ptGt1.5',
						'chargedIsoPtSumdR03',
						'neutralIsoPtSumdR03',
						'neutralIsoPtSum_IsoConeR0p3_ptGt1.0',
						'neutralIsoPtSum_IsoConeR0p3_ptGt1.5',
						'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0',
						'photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.5'
					),
					gbrForestName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018")  # consistent with TauAnalysisTools/TauAnalysisTools/macros/plotTauIdMVAEfficiency_and_FakeRate.C
				)
			),
			outputFileType=cms.string("GBRForest"),
			outputFileName=cms.string("gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2018_dR0p3.root")
		),
	)
)

process.p=cms.Path(process.gbrForestWriter)
