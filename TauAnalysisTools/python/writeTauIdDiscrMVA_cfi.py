import FWCore.ParameterSet.Config as cms

writeTauIdDiscrSequence = cms.Sequence()

writeTauIdDiscrMVAs = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            inputFileType = cms.string("GBRForest"),            
            gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAs)

writeTauIdDiscrWPs = cms.EDAnalyzer("TGraphWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName = cms.string("isoDBoldDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff80")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff40")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrWPs)

writeTauIdDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBoldDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/test/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBnewDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_mvaOutput_normalization")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAoutputNormalizations)
