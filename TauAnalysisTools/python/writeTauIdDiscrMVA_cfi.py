import FWCore.ParameterSet.Config as cms

writeTauIdDiscrSequence = cms.Sequence()

writeTauIdDiscrMVAs = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("tauIdMVAIsoDBoldDMwLT"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("tauIdMVAIsoDBoldDMwLT")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            inputFileType = cms.string("GBRForest"),            
            gbrForestName = cms.string("tauIdMVAIsoDBnewDMwLT"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("tauIdMVAIsoDBnewDMwLT")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            inputFileType = cms.string("GBRForest"),                                       
            gbrForestName = cms.string("tauIdMVAIsoPWoldDMwLT"),
            outputFileType = cms.string("SQLLite"),                                     
            outputRecord = cms.string("tauIdMVAIsoPWoldDMwLT")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            inputFileType = cms.string("GBRForest"),                                       
            gbrForestName = cms.string("tauIdMVAIsoPWnewDMwLT"),
            outputFileType = cms.string("SQLLite"), 
            outputRecord = cms.string("tauIdMVAIsoPWnewDMwLT")
        )                                             
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAs)

writeTauIdDiscrWPs = cms.EDAnalyzer("TGraphWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName = cms.string("isoDBoldDMwLTEff90"),
            outputRecord = cms.string("isoDBoldDMwLTEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff80"),
            outputRecord = cms.string("isoDBoldDMwLTEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff70"),
            outputRecord = cms.string("isoDBoldDMwLTEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff60"),
            outputRecord = cms.string("isoDBoldDMwLTEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff50"),
            outputRecord = cms.string("isoDBoldDMwLTEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            graphName =cms.string("isoDBoldDMwLTEff40"),
            outputRecord = cms.string("isoDBoldDMwLTEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff90"),
            outputRecord = cms.string("isoDBnewDMwLTEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff80"),
            outputRecord = cms.string("isoDBnewDMwLTEff80")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff70"),
            outputRecord = cms.string("isoDBnewDMwLTEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff60"),
            outputRecord = cms.string("isoDBnewDMwLTEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff50"),
            outputRecord = cms.string("isoDBnewDMwLTEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            graphName =cms.string("isoDBnewDMwLTEff40"),
            outputRecord = cms.string("isoDBnewDMwLTEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff90"),
            outputRecord = cms.string("isoPWoldDMwLTEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff80"),
            outputRecord = cms.string("isoPWoldDMwLTEff80")
            ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff70"),
            outputRecord = cms.string("isoPWoldDMwLTEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff60"),
            outputRecord = cms.string("isoPWoldDMwLTEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff50"),
            outputRecord = cms.string("isoPWoldDMwLTEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            graphName =cms.string("isoPWoldDMwLTEff40"),
            outputRecord = cms.string("isoPWoldDMwLTEff40")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff90"),
            outputRecord = cms.string("isoPWnewDMwLTEff90")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff80"),
            outputRecord = cms.string("isoPWnewDMwLTEff80")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff70"),
            outputRecord = cms.string("isoPWnewDMwLTEff70")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff60"),
            outputRecord = cms.string("isoPWnewDMwLTEff60")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff50"),
            outputRecord = cms.string("isoPWnewDMwLTEff50")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            graphName =cms.string("isoPWnewDMwLTEff40"),
            outputRecord = cms.string("isoPWnewDMwLTEff40")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrWPs)

writeTauIdDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBoldDMwLT"),
            outputRecord = cms.string("mvaOutput_normalization_isoDBoldDMwLT")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoDBnewDMwLT"),
            outputRecord = cms.string("mvaOutput_normalization_isoDBnewDMwLT")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoPWoldDMwLT"),
            outputRecord = cms.string("mvaOutput_normalization_isoPWoldDMwLT")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            formulaName = cms.string("mvaOutput_normalization_isoPWnewDMwLT"),
            outputRecord = cms.string("mvaOutput_normalization_isoPWnewDMwLT")
        )
    )
)

writeTauIdDiscrSequence += cms.Sequence(writeTauIdDiscrMVAoutputNormalizations)
