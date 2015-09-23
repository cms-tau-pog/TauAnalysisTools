import FWCore.ParameterSet.Config as cms

writeTauIdDiscrSequence = cms.Sequence()

writeTauIdDiscrMVAs = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            inputFileType = cms.string("GBRForest"),            
            gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),                                       
            gbrForestName = cms.string("tauIdMVAIsoPWoldDMwLT"),
            outputFileType = cms.string("SQLLite"),                                     
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            inputFileType = cms.string("GBRForest"),                                       
            gbrForestName = cms.string("tauIdMVAIsoPWnewDMwLT"),
            outputFileType = cms.string("SQLLite"), 
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBR03oldDMwLT"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoPWR03oldDMwLT"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAs)

writeTauIdDiscrWPs = cms.EDAnalyzer("TGraphWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName = cms.string("isoDBoldDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_WPEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_WPEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_WPEff80")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_WPEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_WPEff80")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_WPEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_WPEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_WPEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            graphName = cms.string("isoDBR03oldDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_WPEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            graphName =cms.string("isoDBR03oldDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_WPEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            graphName =cms.string("isoDBR03oldDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            graphName =cms.string("isoDBR03oldDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            graphName =cms.string("isoDBR03oldDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            graphName =cms.string("isoDBR03oldDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_WPEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            graphName = cms.string("isoPWR03oldDMwLTEff90"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_WPEff90")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            graphName =cms.string("isoPWR03oldDMwLTEff80"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_WPEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            graphName =cms.string("isoPWR03oldDMwLTEff70"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_WPEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            graphName =cms.string("isoPWR03oldDMwLTEff60"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_WPEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            graphName =cms.string("isoPWR03oldDMwLTEff50"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_WPEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            graphName =cms.string("isoPWR03oldDMwLTEff40"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_WPEff40")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrWPs)

writeTauIdDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBoldDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBnewDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoPWoldDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoPWnewDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBR03oldDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_mvaOutput_normalization")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoPWR03oldDMwLT"),
            outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_mvaOutput_normalization")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAoutputNormalizations)
