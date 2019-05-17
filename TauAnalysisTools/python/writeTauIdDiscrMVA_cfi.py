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
        # # 2017v2 Old DM 0.5 cone
        # cms.PSet(
        #     inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017v2_dR0p5.root'),
        #     inputFileType = cms.string("GBRForest"),
        #     gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p5"),
        #     outputFileType = cms.string("SQLLite"),
        #     outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2")
        # ),
        # #
        # # 2017v2 Old DM 0.3 cone
        # cms.PSet(
        #     inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017v2_dR0p3.root'),
        #     inputFileType = cms.string("GBRForest"),
        #     gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017v2_dR0p3"),
        #     outputFileType = cms.string("SQLLite"),
        #     outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2")
        # ),
        # #
        # # 2017v2 New DM 0.5 cone
        # cms.PSet(
        #     inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT_2017v2_dR0p5.root'),
        #     inputFileType = cms.string("GBRForest"),
        #     gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT_2017v2_dR0p5"),
        #     outputFileType = cms.string("SQLLite"),
        #     outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2")
        # )
        # 2018 Old DM 0.5 cone
        cms.PSet(
            inputFileName=cms.FileInPath('gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2018_dR0p5.root'),
            inputFileType=cms.string("GBRForest"),
            gbrForestName=cms.string("tauIdMVAIsoDBoldDMwLT2018"),
            outputFileType=cms.string("SQLLite"),
            outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018")
        ),
        #
        # 2018 New DM 0.5 cone
        cms.PSet(
            inputFileName=cms.FileInPath('gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT_2018_dR0p5.root'),
            inputFileType=cms.string("GBRForest"),
            gbrForestName=cms.string("tauIdMVAIsoDBnewDMwLT2018"),
            outputFileType=cms.string("SQLLite"),
            outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018")
        ),
        #
        # 2018 Old DM 0.3 cone
        cms.PSet(
            inputFileName=cms.FileInPath('gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2018_dR0p3.root'),
            inputFileType=cms.string("GBRForest"),
            gbrForestName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018"),
            outputFileType=cms.string("SQLLite"),
            outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018")
        ),
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAs)

writeTauIdDiscrWPs = cms.EDAnalyzer("TGraphWriter",
    jobs=cms.VPSet(
        # 2017v2 Old DM 0.5 cone
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff95"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff95")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff90"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff90")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff80"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff80")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff70"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff70")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff60"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff60")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff50"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff50")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMwLT2018Eff40"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff40")
            ),

        # 2018 Old DM 0.3 cone
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff95"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff95")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff90"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff90")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff80"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff80")
                ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff70"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff70")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff60"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff60")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff50"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff50")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBoldDMdR0p3wLT2018Eff40"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff40")
            ),

        # 2018 New DM 0.5 cone
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff95"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff95")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff90"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff90")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff80"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff80")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff70"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff70")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff60"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff60")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff50"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff50")
            ),
            cms.PSet(
                inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
                graphName=cms.string("tauIdMVAIsoDBnewDMwLT2018Eff40"),
                outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff40")
            )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrWPs)

writeTauIdDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
    jobs=cms.VPSet(
        cms.PSet(
            inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT2018.root'),
            formulaName=cms.string("mvaOutput_normalization_tauIdMVAIsoDBoldDMwLT2018"),
            outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_mvaOutput_normalization")  # RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_mvaOutput_normalization
        ),
        cms.PSet(
            inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMdR0p3wLT2018.root'),
            formulaName=cms.string("mvaOutput_normalization_tauIdMVAIsoDBoldDMdR0p3wLT2018"),
            outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_mvaOutput_normalization")  # RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_mvaOutput_normalization
        ),
        cms.PSet(
            inputFileName=cms.FileInPath('wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBnewDMwLT2018.root'),
            formulaName=cms.string("mvaOutput_normalization_tauIdMVAIsoDBnewDMwLT2018"),
            outputRecord=cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_mvaOutput_normalization")  # RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_mvaOutput_normalization
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAoutputNormalizations)
