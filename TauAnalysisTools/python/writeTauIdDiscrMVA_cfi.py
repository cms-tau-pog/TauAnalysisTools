import FWCore.ParameterSet.Config as cms

writeTauIdDiscrSequence = cms.Sequence()

writeTauIdDiscrMVAs = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2016_pt_0p1.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT_2017_pt_0p1.root'),
            inputFileType = cms.string("GBRForest"),            
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAs)

writeTauIdDiscrWPs = cms.EDAnalyzer("TGraphWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName = cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff95"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff95")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName = cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2016_pt_0p1Eff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff40")
        ),

        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff95"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff95")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff80")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            graphName =cms.string("tauIdMVAIsoDBoldDMwLT_2017_pt_0p1Eff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff40")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrWPs)

writeTauIdDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1.root'),
            formulaName = cms.string("mvaOutput_normalization_tauIdMVAIsoDBoldDMwLT_2016_pt_0p1"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1.root'),
            formulaName = cms.string("mvaOutput_normalization_tauIdMVAIsoDBoldDMwLT_2017_pt_0p1"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_mvaOutput_normalization")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAoutputNormalizations)
