import FWCore.ParameterSet.Config as cms

writeAntiElectronDiscrSequence = cms.Sequence()

writeAntiElectronDiscrMVAs = cms.EDAnalyzer("GBRForestWriter",
    jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("gbr_NoEleMatch_woGwoGSF_BL"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),            
            gbrForestName = cms.string("gbr_NoEleMatch_wGwoGSF_BL"),
            outputFileType = cms.string("SQLLite"),                                      
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),                                       
            gbrForestName = cms.string("gbr_woGwGSF_BL"),
            outputFileType = cms.string("SQLLite"),                                     
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),                                       
            gbrForestName = cms.string("gbr_wGwGSF_BL"),
            outputFileType = cms.string("SQLLite"), 
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("gbr_NoEleMatch_woGwoGSF_EC"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("gbr_NoEleMatch_wGwoGSF_EC"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("gbr_woGwGSF_EC"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/gbrDiscriminationAgainstElectronMVA6.root'),
            inputFileType = cms.string("GBRForest"),
            gbrForestName = cms.string("gbr_wGwGSF_EC"),
            outputFileType = cms.string("SQLLite"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC")
        )
    )
)

writeAntiElectronDiscrSequence += cms.Sequence(writeAntiElectronDiscrMVAs)

writeAntiElectronDiscrWPs = cms.EDAnalyzer("TGraphWriter",
       jobs = cms.VPSet(
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat0"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat0"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat0"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat0"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat0"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat2"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat2"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat2"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat2"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat2"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat5"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat5"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat5"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat5"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat5"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat7"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat7"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat7"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat7"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat7"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat8"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat8"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat8"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat8"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat8"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat10"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat10"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat10"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat10"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat10"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat13"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat13"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat13"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat13"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat13"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff79")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff99cat15"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff99")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff96cat15"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff96")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff91cat15"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff91")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff85cat15"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff85")
        ),
        cms.PSet(
            inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationAgainstElectronMVA6.root'),
            graphName = cms.string("eff79cat15"),
            outputRecord = cms.string("RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff79")
        )
    )
)

writeAntiElectronDiscrSequence += cms.Sequence(writeAntiElectronDiscrWPs)

#writeAntiElectronDiscrMVAoutputNormalizations = cms.EDAnalyzer("TFormulaWriter",
       #jobs = cms.VPSet(
        #cms.PSet(
            #inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBoldDMwLT.root'),
            #formulaName = cms.string("mvaOutput_normalization_isoDBoldDMwLT"),
            #outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLTv1_mvaOutput_normalization")
        #),
        #cms.PSet(
            #inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBnewDMwLT.root'),
            #formulaName = cms.string("mvaOutput_normalization_isoDBnewDMwLT"),
            #outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLTv1_mvaOutput_normalization")
        #),
        #cms.PSet(
            #inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWoldDMwLT.root'),
            #formulaName = cms.string("mvaOutput_normalization_isoPWoldDMwLT"),
            #outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWoldDMwLTv1_mvaOutput_normalization")
        #),
        #cms.PSet(
            #inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWnewDMwLT.root'),
            #formulaName = cms.string("mvaOutput_normalization_isoPWnewDMwLT"),
            #outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWnewDMwLTv1_mvaOutput_normalization")
        #),
        #cms.PSet(
            #inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoDBR03oldDMwLT.root'),
            #formulaName = cms.string("mvaOutput_normalization_isoDBR03oldDMwLT"),
            #outputRecord = cms.string("RecoTauTag_tauIdMVAIsoDBR03oldDMwLTv1_mvaOutput_normalization")
        #),
        #cms.PSet(
            #inputFileName = cms.FileInPath('TauAnalysisTools/TauAnalysisTools/data/wpDiscriminationByIsolationMVA1Run2_isoPWR03oldDMwLT.root'),
            #formulaName = cms.string("mvaOutput_normalization_isoPWR03oldDMwLT"),
            #outputRecord = cms.string("RecoTauTag_tauIdMVAIsoPWR03oldDMwLTv1_mvaOutput_normalization")
        #)
    #)
#)

#writeAntiElectronDiscrSequence += cms.Sequence(writeAntiElectronDiscrMVAoutputNormalizations)
