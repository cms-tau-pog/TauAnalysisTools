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
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_NoEleMatch_woGwoGSF_Barrel_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_dCrackEta',
                        'Tau_dCrackPhi'
                    ),
                    gbrForestName = cms.string("gbr_NoEleMatch_woGwoGSF_BL")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_NoEleMatch_wGwoGSF_Barrel_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_NumGammaCandsIn',
                        'Tau_NumGammaCandsOut',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_GammaEtaMomIn',
                        'Tau_GammaEtaMomOut',
                        'Tau_GammaPhiMomIn',
                        'Tau_GammaPhiMomOut',
                        'Tau_GammaEnFracIn',
                        'Tau_GammaEnFracOut',
                        'Tau_dCrackEta',
                        'Tau_dCrackPhi'
                    ),
                    gbrForestName = cms.string("gbr_NoEleMatch_wGwoGSF_BL")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_woGwGSF_Barrel_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'TMath::Max(-0.1, Elec_EtotOverPin)',
                        'TMath::Log(Elec_Chi2NormGSF)',
                        'Elec_GSFNumHits',
                        'TMath::Log(Elec_GSFTrackResol)',
                        'Elec_GSFTracklnPt',
                        '(Elec_GSFNumHits - Elec_KFNumHits)/(Elec_GSFNumHits + Elec_KFNumHits)',
                        'TMath::Log(Elec_Chi2NormKF)',
                        'TMath::Min(TMath::Abs(Elec_Pin - Elec_Pout)/Elec_Pin, 1.)',
                        'TMath::Min(Elec_Eecal/Elec_Pout, 20.)',
                        'Elec_DeltaEta',
                        'Elec_DeltaPhi',
                        'TMath::Min(Elec_MvaInSigmaEtaEta, 0.01)',
                        'TMath::Min(Elec_MvaInHadEnergy, 20)',
                        'TMath::Min(Elec_MvaInDeltaEta, 0.1)',
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_dCrackEta',
                        'Tau_dCrackPhi'
                    ),
                    gbrForestName = cms.string("gbr_woGwGSF_BL")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_wGwGSF_Barrel_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'TMath::Max(-0.1, Elec_EtotOverPin)',
                        'TMath::Log(Elec_Chi2NormGSF)',
                        'Elec_GSFNumHits',
                        'TMath::Log(Elec_GSFTrackResol)',
                        'Elec_GSFTracklnPt',
                        '(Elec_GSFNumHits - Elec_KFNumHits)/(Elec_GSFNumHits + Elec_KFNumHits)',
                        'TMath::Log(Elec_Chi2NormKF)',
                        'TMath::Min(TMath::Abs(Elec_Pin - Elec_Pout)/Elec_Pin, 1.)',
                        'TMath::Min(Elec_Eecal/Elec_Pout, 20.)',
                        'Elec_DeltaEta',
                        'Elec_DeltaPhi',
                        'TMath::Min(Elec_MvaInSigmaEtaEta, 0.01)',
                        'TMath::Min(Elec_MvaInHadEnergy, 20)',
                        'TMath::Min(Elec_MvaInDeltaEta, 0.1)',
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_NumGammaCandsIn',
                        'Tau_NumGammaCandsOut',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_GammaEtaMomIn',
                        'Tau_GammaEtaMomOut',
                        'Tau_GammaPhiMomIn',
                        'Tau_GammaPhiMomOut',
                        'Tau_GammaEnFracIn',
                        'Tau_GammaEnFracOut',
                        'Tau_dCrackEta',
                        'Tau_dCrackPhi'
                    ),
                    gbrForestName = cms.string("gbr_wGwGSF_BL")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_NoEleMatch_woGwoGSF_Endcap_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_dCrackEta'
                    ),
                    gbrForestName = cms.string("gbr_NoEleMatch_woGwoGSF_EC")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_NoEleMatch_wGwoGSF_Endcap_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_NumGammaCandsIn',
                        'Tau_NumGammaCandsOut',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_GammaEtaMomIn',
                        'Tau_GammaEtaMomOut',
                        'Tau_GammaPhiMomIn',
                        'Tau_GammaPhiMomOut',
                        'Tau_GammaEnFracIn',
                        'Tau_GammaEnFracOut',
                        'Tau_dCrackEta'
                    ),
                    gbrForestName = cms.string("gbr_NoEleMatch_wGwoGSF_EC")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_woGwGSF_Endcap_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'TMath::Max(-0.1, Elec_EtotOverPin)',
                        'TMath::Log(Elec_Chi2NormGSF)',
                        'Elec_GSFNumHits',
                        'TMath::Log(Elec_GSFTrackResol)',
                        'Elec_GSFTracklnPt',
                        '(Elec_GSFNumHits - Elec_KFNumHits)/(Elec_GSFNumHits + Elec_KFNumHits)',
                        'TMath::Log(Elec_Chi2NormKF)',
                        'TMath::Min(TMath::Abs(Elec_Pin - Elec_Pout)/Elec_Pin, 1.)',
                        'TMath::Min(Elec_Eecal/Elec_Pout, 20.)',
                        'Elec_DeltaEta',
                        'Elec_DeltaPhi',
                        'TMath::Min(Elec_MvaInSigmaEtaEta, 0.01)',
                        'TMath::Min(Elec_MvaInHadEnergy, 20)',
                        'TMath::Min(Elec_MvaInDeltaEta, 0.1)',
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_dCrackEta'
                    ),
                    gbrForestName = cms.string("gbr_woGwGSF_EC")
                ),
                cms.PSet(
                    inputFileName = cms.string('/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim/weights/mvaAntiElectronDiscr5_wGwGSF_Endcap_BDTG.weights.xml'),
                    inputFileType = cms.string("XML"),
                    inputVariables = cms.vstring(
                        'TMath::Max(-0.1, Elec_EtotOverPin)',
                        'TMath::Log(Elec_Chi2NormGSF)',
                        'Elec_GSFNumHits',
                        'TMath::Log(Elec_GSFTrackResol)',
                        'Elec_GSFTracklnPt',
                        '(Elec_GSFNumHits - Elec_KFNumHits)/(Elec_GSFNumHits + Elec_KFNumHits)',
                        'TMath::Log(Elec_Chi2NormKF)',
                        'TMath::Min(TMath::Abs(Elec_Pin - Elec_Pout)/Elec_Pin, 1.)',
                        'TMath::Min(Elec_Eecal/Elec_Pout, 20.)',
                        'Elec_DeltaEta',
                        'Elec_DeltaPhi',
                        'TMath::Min(Elec_MvaInSigmaEtaEta, 0.01)',
                        'TMath::Min(Elec_MvaInHadEnergy, 20)',
                        'TMath::Min(Elec_MvaInDeltaEta, 0.1)',
                        'Tau_EtaAtEcalEntrance',
                        'Tau_LeadChargedPFCandEtaAtEcalEntrance',
                        'TMath::Min(2., Tau_LeadChargedPFCandPt/TMath::Max(1., Tau_Pt))',
                        'TMath::Log(TMath::Max(1., Tau_Pt))',
                        'Tau_EmFraction',
                        'Tau_NumGammaCandsIn',
                        'Tau_NumGammaCandsOut',
                        'Tau_HadrHoP',
                        'Tau_HadrEoP',
                        'Tau_VisMassIn',
                        'Tau_GammaEtaMomIn',
                        'Tau_GammaEtaMomOut',
                        'Tau_GammaPhiMomIn',
                        'Tau_GammaPhiMomOut',
                        'Tau_GammaEnFracIn',
                        'Tau_GammaEnFracOut',
                        'Tau_dCrackEta'
                    ),
                    gbrForestName = cms.string("gbr_wGwGSF_EC")
                )
            ),
            outputFileType = cms.string("GBRForest"),                                      
            outputFileName = cms.string("gbrDiscriminationAgainstElectronMVA6.root")
        )
    )
)

spectatorVariables = [
    ##'Tau_Pt',
    'Tau_Eta',
    'Tau_DecayMode',
    'Tau_LeadHadronPt',
    'Tau_LooseComb3HitsIso',
    'NumPV',
    'Tau_Category'
]

for job in process.gbrForestWriter.jobs:
    for category in job.categories:
        setattr(category, "spectatorVariables", cms.vstring(spectatorVariables))

process.p = cms.Path(process.gbrForestWriter)
