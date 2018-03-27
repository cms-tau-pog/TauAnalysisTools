import FWCore.ParameterSet.Config as cms

writeTauIdDiscrSequence = cms.Sequence()

writeTauIdDiscrMVAs = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        # cms.PSet(
        #     inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2016_pt_0p1.root'),
        #     inputFileType = cms.string("GBRForest"),
        #     gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1"),
        #     outputFileType = cms.string("SQLLite"),
        #     outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2")
        # ),
        # cms.PSet(
        #     inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017_pt_0p1.root'),
        #     inputFileType = cms.string("GBRForest"),
        #     gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1"),
        #     outputFileType = cms.string("SQLLite"),
        #     outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1")
        # )
        #
        # 2017v2 Old DM 0.5 cone
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017v2_dR0p5.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2")
        ),
        #
        # 2017v2 Old DM 0.3 cone
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017v2_dR0p3.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2")
        ),
        #
        # 2017v2 New DM 0.5 cone
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT_2017v2_dR0p5.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAs)

writeTauIdDiscrWPs = cms.EDAnalyzer("TGraphWriter",
    jobs = cms.VPSet(
        # 2017v2 Old DM 0.5 cone
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName = cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff95"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff95")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName = cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff90"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff90")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff80"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff80")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff70"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff70")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff60"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff60")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff50"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff50")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5Eff40"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff40")
            ),

        # 2017v2 Old DM 0.3 cone
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff95"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff95")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff90"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff90")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff80"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff80")
                ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff70"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff70")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff60"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff60")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff50"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff50")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
                graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3Eff40"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff40")
            ),

        # 2017v2 New DM 0.5 cone
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName = cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff95"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff95")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName = cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff90"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff90")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff80"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff80")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff70"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff70")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff60"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff60")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff50"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff50")
            ),
            cms.PSet(
                inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
                graphName =cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5Eff40"),
                outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff40")
            )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrWPs)

writeTauIdDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
    jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5.root'),
            formulaName = cms.string("mvaOutput_normalization_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_mvaOutput_normalization")#RecoTauTag_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5_mvaOutput_normalization
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3.root'),
            formulaName = cms.string("mvaOutput_normalization_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_mvaOutput_normalization") #RecoTauTag_tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3_mvaOutput_normalization
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5.root'),
            formulaName = cms.string("mvaOutput_normalization_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_mvaOutput_normalization") #RecoTauTag_tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5_mvaOutput_normalization
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAoutputNormalizations)
