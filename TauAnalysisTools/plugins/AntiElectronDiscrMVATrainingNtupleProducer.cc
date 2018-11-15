#include "TauAnalysisTools/TauAnalysisTools/plugins/AntiElectronDiscrMVATrainingNtupleProducer.h"

#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/GeometryVector/interface/VectorUtil.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Handle.h"

AntiElectronDiscrMVATrainingNtupleProducer::AntiElectronDiscrMVATrainingNtupleProducer(const edm::ParameterSet& cfg)// :
//_effectiveAreas( ((cfg.getParameter<edm::FileInPath>("effAreasConfigFile")).fullPath()) )//,
{
  tauToken_ = consumes<pat::TauCollection>(cfg.getParameter<edm::InputTag>("srcPFTaus"));
  electronToken_ = consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("srcGsfElectrons"));
  genElectronToken_ = consumes<edm::View<reco::Candidate> >(cfg.getParameter<edm::InputTag>("srcGenElectrons"));
  genTauToken_ = consumes<edm::View<reco::Candidate> >(cfg.getParameter<edm::InputTag>("srcGenTaus"));
  vertexToken_ = consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("srcPrimaryVertex"));
  electronTightIdMapToken_ = consumes<edm::ValueMap<bool> >(cfg.getParameter<edm::InputTag>("eleTightIdMap"));
  eleIdVetoName_ =  cfg.getParameter<std::string>("electronIdVeto");

  typedef std::vector<std::string> vstring;
  vstring tauIdDiscriminatorNames = cfg.getParameter<vstring>("tauIdDiscriminators");
  for ( vstring::const_iterator name = tauIdDiscriminatorNames.begin();
	name != tauIdDiscriminatorNames.end(); ++name ) {
    std::cout << "tauIdDiscriminators "<< *name <<std::endl;
    tauIdDiscrEntries_.push_back(tauIdDiscrEntryType(*name));
  }

  verbosity_ = ( cfg.exists("verbosity") ) ?
    cfg.getParameter<int>("verbosity") : 0;

  //edm::InputTag rhoTag = edm::InputTag("fixedGridRhoFastjetAll","");
} 

void AntiElectronDiscrMVATrainingNtupleProducer::beginJob()
{ 
  edm::Service<TFileService> fs;
  tree_ = fs->make<TTree>("tree", "AntiEMVA tree");

  // counters
  tree_->Branch("run", &run_, "run/l");
  tree_->Branch("event", &event_, "event/l");
  tree_->Branch("lumi", &lumi_, "lumi/l");
  tree_->Branch("NumPV", &NumPV_, "NumPV/I");
  tree_->Branch("NumGsfEle", &NumGsfEle_, "NumGsfEle/I");
  tree_->Branch("NumGenEle", &NumGenEle_, "NumGenEle/I");
  tree_->Branch("NumPFTaus", &NumPFTaus_, "NumPFTaus/I");
  tree_->Branch("NumGenHad", &NumGenHad_, "NumGenHad/I");

  // GsfElectron variables
  tree_->Branch("Elec_GenEleMatch", &Elec_GenEleMatch_, "Elec_GenEleMatch/I");
  tree_->Branch("Elec_GenHadMatch", &Elec_GenHadMatch_, "Elec_GenHadMatch/I");
  tree_->Branch("Elec_Eta", &Elec_Eta_, "Elec_Eta/F");
  tree_->Branch("Elec_Pt", &Elec_Pt_, "Elec_Pt/F");
  tree_->Branch("Elec_HasSC", &Elec_HasSC_, "Elec_HasSC/I");
  tree_->Branch("Elec_MvaOut", &Elec_MvaOut_, "Elec_MvaOut/F");
  tree_->Branch("Elec_MvaOutIsolated", &Elec_MvaOutIsolated_, "Elec_MvaOutIsolated/F");
  tree_->Branch("Elec_Ee", &Elec_Ee_, "Elec_Ee/F");
  tree_->Branch("Elec_Egamma", &Elec_Egamma_, "Elec_Egamma/F");
  tree_->Branch("Elec_Pin", &Elec_Pin_, "Elec_Pin/F");
  tree_->Branch("Elec_Pout", &Elec_Pout_, "Elec_Pout/F");
  tree_->Branch("Elec_EtotOverPin", &Elec_EtotOverPin_, "Elec_EtotOverPin/F");
  tree_->Branch("Elec_EeOverPout", &Elec_EeOverPout_, "Elec_EeOverPout/F");
  tree_->Branch("Elec_EgammaOverPdif", &Elec_EgammaOverPdif_, "Elec_EgammaOverPdif/F");
  tree_->Branch("Elec_MvaInEarlyBrem", &Elec_MvaInEarlyBrem_, "Elec_MvaInEarlyBrem/I");
  tree_->Branch("Elec_MvaInLateBrem", &Elec_MvaInLateBrem_, "Elec_MvaInLateBrem/I");
  tree_->Branch("Elec_MvaInSigmaEtaEta", &Elec_MvaInSigmaEtaEta_, "Elec_MvaInSigmaEtaEta/F");
  tree_->Branch("Elec_MvaInHadEnergy", &Elec_MvaInHadEnergy_, "Elec_MvaInHadEnergy/F");
  tree_->Branch("Elec_MvaInDeltaEta", &Elec_MvaInDeltaEta_, "Elec_MvaInDeltaEta/F");
  tree_->Branch("Elec_MvaInNClusterOutMustache", &Elec_MvaInNClusterOutMustache_, "Elec_MvaInNClusterOutMustache/I");
  tree_->Branch("Elec_MvaInEtOutMustache", &Elec_MvaInEtOutMustache_, "Elec_MvaInEtOutMustache/F");
  tree_->Branch("Elec_Iso", &Elec_Iso_, "Elec_Iso/F");
  tree_->Branch("Elec_IsoRel", &Elec_IsoRel_, "Elec_IsoRel/F");

  tree_->Branch("Elec_SigmaEtaEta", &Elec_SigmaEtaEta_, "Elec_SigmaEtaEta/F");
  tree_->Branch("Elec_SigmaEtaEta_full5x5", &Elec_SigmaEtaEta_full5x5_, "Elec_SigmaEtaEta_full5x5/F");
  tree_->Branch("Elec_HoHplusE", &Elec_HoHplusE_, "Elec_HoHplusE/F");
  tree_->Branch("Elec_Fbrem", &Elec_Fbrem_, "Elec_Fbrem/F");
  tree_->Branch("Elec_Eecal", &Elec_Eecal_, "Elec_Eecal/F");
  tree_->Branch("Elec_DeltaEta", &Elec_DeltaEta_, "Elec_DeltaEta/F");
  tree_->Branch("Elec_DeltaPhi", &Elec_DeltaPhi_, "Elec_DeltaPhi/F"); 
  tree_->Branch("Elec_DeltaEtaAtVtx", &Elec_DeltaEtaAtVtx_, "Elec_DeltaEtaAtVtx/F");
  tree_->Branch("Elec_DeltaPhiAtVtx", &Elec_DeltaPhiAtVtx_, "Elec_DeltaPhiAtVtx/F");
  tree_->Branch("Elec_HasKF", &Elec_HasKF_, "Elec_HasKF/I");
  tree_->Branch("Elec_Chi2KF",&Elec_Chi2KF_,"Elec_Chi2KF/F");
  tree_->Branch("Elec_Chi2NormKF",&Elec_Chi2NormKF_,"Elec_Chi2NormKF/F");
  tree_->Branch("Elec_KFNumHits", &Elec_KFNumHits_, "Elec_KFNumHits/I");
  tree_->Branch("Elec_KFNumPixelHits", &Elec_KFNumPixelHits_, "Elec_KFNumPixelHits/I");
  tree_->Branch("Elec_KFNumStripHits", &Elec_KFNumStripHits_, "Elec_KFNumStripHits/I");
  tree_->Branch("Elec_KFTrackResol", &Elec_KFTrackResol_, "Elec_KFTrackResol/F");
  tree_->Branch("Elec_KFTracklnPt", &Elec_KFTracklnPt_, "Elec_KFTracklnPt/F");
  tree_->Branch("Elec_KFTrackEta", &Elec_KFTrackEta_, "Elec_KFTrackEta/F");
  tree_->Branch("Elec_HasGSF", &Elec_HasGSF_, "Elec_HasGSF/I");
  tree_->Branch("Elec_Chi2GSF", &Elec_Chi2GSF_, "Elec_Chi2GSF/F");
  tree_->Branch("Elec_Chi2NormGSF", &Elec_Chi2NormGSF_, "Elec_Chi2NormGSF/F");
  tree_->Branch("Elec_GSFNumHits", &Elec_GSFNumHits_, "Elec_GSFNumHits/I");
  tree_->Branch("Elec_GSFNumPixelHits", &Elec_GSFNumPixelHits_, "Elec_GSFNumPixelHits/I");
  tree_->Branch("Elec_GSFNumStripHits", &Elec_GSFNumStripHits_, "Elec_GSFNumStripHits/I");
  tree_->Branch("Elec_GSFTrackResol", &Elec_GSFTrackResol_, "Elec_GSFTrackResol/F");
  tree_->Branch("Elec_GSFTracklnPt", &Elec_GSFTracklnPt_, "Elec_GSFTracklnPt/F");
  tree_->Branch("Elec_GSFTrackEta", &Elec_GSFTrackEta_, "Elec_GSFTrackEta/F");
 
  tree_->Branch("ElecVeto_N", &ElecVeto_N_, "ElecVeto_N/I");
  tree_->Branch("ElecVeto_Pt", &ElecVeto_Pt_, "ElecVeto_Pt/F");
  tree_->Branch("ElecVeto_Eta", &ElecVeto_Eta_, "ElecVeto_Eta/F");
  tree_->Branch("ElecVeto_Phi", &ElecVeto_Phi_, "ElecVeto_Phi/F");

  // PFTau variables
  tree_->Branch("Tau_GenEle_Pt", &Tau_GenEle_Pt_, "Tau_GenEle_Pt/F");
  tree_->Branch("Tau_GenEle_Eta", &Tau_GenEle_Eta_, "Tau_GenEle_Eta/F");

  tree_->Branch("Tau_GsfEleMatch", &Tau_GsfEleMatch_, "Tau_GsfEleMatch/I");
  tree_->Branch("Tau_GenEleMatch", &Tau_GenEleMatch_, "Tau_GenEleMatch/I");
  tree_->Branch("Tau_GenHadMatch", &Tau_GenHadMatch_, "Tau_GenHadMatch/I");
  tree_->Branch("Tau_Eta", &Tau_Eta_, "Tau_Eta/F");
  tree_->Branch("Tau_EtaAtEcalEntrance", &Tau_EtaAtEcalEntrance_, "Tau_EtaAtEcalEntrance/F");
  tree_->Branch("Tau_PhiAtEcalEntrance", &Tau_PhiAtEcalEntrance_, "Tau_PhiAtEcalEntrance/F");
  tree_->Branch("Tau_EtaAtEcalEntranceEcalEnWeighted", &Tau_EtaAtEcalEntranceEcalEnWeighted_, "Tau_EtaAtEcalEntranceEcalEnWeighted/F");
  tree_->Branch("Tau_PhiAtEcalEntranceEcalEnWeighted", &Tau_PhiAtEcalEntranceEcalEnWeighted_, "Tau_PhiAtEcalEntranceEcalEnWeighted/F");
  tree_->Branch("Tau_LeadNeutralPFCandEtaAtEcalEntrance", &Tau_LeadNeutralPFCandEtaAtEcalEntrance_, "Tau_LeadNeutralPFCandEtaAtEcalEntrance/F");
  tree_->Branch("Tau_LeadNeutralPFCandPhiAtEcalEntrance", &Tau_LeadNeutralPFCandPhiAtEcalEntrance_, "Tau_LeadNeutralPFCandPhiAtEcalEntrance/F");
  tree_->Branch("Tau_LeadNeutralPFCandPt", &Tau_LeadNeutralPFCandPt_, "Tau_LeadNeutralPFCandPt/F");
  tree_->Branch("Tau_LeadChargedPFCandEtaAtEcalEntrance", &Tau_LeadChargedPFCandEtaAtEcalEntrance_, "Tau_LeadChargedPFCandEtaAtEcalEntrance/F");
  tree_->Branch("Tau_LeadChargedPFCandPhiAtEcalEntrance", &Tau_LeadChargedPFCandPhiAtEcalEntrance_, "Tau_LeadChargedPFCandPhiAtEcalEntrance/F");
  tree_->Branch("Tau_LeadChargedPFCandPt", &Tau_LeadChargedPFCandPt_, "Tau_LeadChargedPFCandPt/F");
  tree_->Branch("Tau_Phi", &Tau_Phi_, "Tau_Phi/F");
  tree_->Branch("Tau_Pt", &Tau_Pt_, "Tau_Pt/F");
  tree_->Branch("Tau_LeadHadronPt", &Tau_LeadHadronPt_, "Tau_LeadHadronPt/F");
  tree_->Branch("Tau_HasGsf", &Tau_HasGsf_, "Tau_HasGsf/I");
  tree_->Branch("Tau_GSFChi2", &Tau_GSFChi2_, "Tau_GSFChi2/F");
  tree_->Branch("Tau_GSFNumHits", &Tau_GSFNumHits_, "Tau_GSFNumHits/I");
  tree_->Branch("Tau_GSFNumPixelHits", &Tau_GSFNumPixelHits_, "Tau_GSFNumPixelHits/I");
  tree_->Branch("Tau_GSFNumStripHits", &Tau_GSFNumStripHits_, "Tau_GSFNumStripHits/I");
  tree_->Branch("Tau_GSFTrackResol", &Tau_GSFTrackResol_, "Tau_GSFTrackResol/F");
  tree_->Branch("Tau_GSFTracklnPt", &Tau_GSFTracklnPt_, "Tau_GSFTracklnPt/F");
  tree_->Branch("Tau_GSFTrackEta", &Tau_GSFTrackEta_, "Tau_GSFTrackEta/F");
  tree_->Branch("Tau_HasKF", &Tau_HasKF_, "Tau_HasKF/I");
  tree_->Branch("Tau_KFChi2", &Tau_KFChi2_, "Tau_KFChi2/F");
  tree_->Branch("Tau_KFNumHits", &Tau_KFNumHits_, "Tau_KFNumHits/I");
  tree_->Branch("Tau_KFNumPixelHits", &Tau_KFNumPixelHits_, "Tau_KFNumPixelHits/I");
  tree_->Branch("Tau_KFNumStripHits", &Tau_KFNumStripHits_, "Tau_KFNumStripHits/I");
  tree_->Branch("Tau_KFTrackResol", &Tau_KFTrackResol_, "Tau_KFTrackResol/F");
  tree_->Branch("Tau_KFTracklnPt", &Tau_KFTracklnPt_, "Tau_KFTracklnPt/F");
  tree_->Branch("Tau_KFTrackEta", &Tau_KFTrackEta_, "Tau_KFTrackEta/F");
  tree_->Branch("Tau_EmFraction", &Tau_EmFraction_, "Tau_EmFraction/F");
  tree_->Branch("Tau_EmFraction_PFCharged", &Tau_EmFraction_PFCharged_, "Tau_EmFraction_PFCharged/F");
  tree_->Branch("Tau_NumChargedCands", &Tau_NumChargedCands_, "Tau_NumChargedCands/I");
  tree_->Branch("Tau_NumGammaCandsIn", &Tau_NumGammaCandsIn_, "Tau_NumGammaCandsIn/I");
  tree_->Branch("Tau_NumGammaCandsOut", &Tau_NumGammaCandsOut_, "Tau_NumGammaCandsOut/I");
  tree_->Branch("Tau_HadrHoP", &Tau_HadrHoP_, "Tau_HadrHoP/F");
  tree_->Branch("Tau_HadrEoP", &Tau_HadrEoP_, "Tau_HadrEoP/F");
  tree_->Branch("Tau_VisMass", &Tau_VisMass_, "Tau_VisMass/F");
  tree_->Branch("Tau_VisMassIn", &Tau_VisMassIn_, "Tau_VisMassIn/F");
  tree_->Branch("Tau_GammaEtaMomIn", &Tau_GammaEtaMomIn_, "Tau_GammaEtaMomIn/F");
  tree_->Branch("Tau_GammaEtaMomOut", &Tau_GammaEtaMomOut_, "Tau_GammaEtaMomOut/F");
  tree_->Branch("Tau_GammaPhiMomIn", &Tau_GammaPhiMomIn_, "Tau_GammaPhiMomIn/F");
  tree_->Branch("Tau_GammaPhiMomOut", &Tau_GammaPhiMomOut_, "Tau_GammaPhiMomOut/F");
  tree_->Branch("Tau_GammaEnFracIn", &Tau_GammaEnFracIn_, "Tau_GammaEnFracIn/F");
  tree_->Branch("Tau_GammaEnFracOut", &Tau_GammaEnFracOut_, "Tau_GammaEnFracOut/F");
  tree_->Branch("Tau_HadrMvaOut", &Tau_HadrMvaOut_, "Tau_HadrMvaOut/F");
  tree_->Branch("Tau_HadrMvaOutIsolated", &Tau_HadrMvaOutIsolated_, "Tau_HadrMvaOutIsolated/F");

  for ( std::vector<tauIdDiscrEntryType>::iterator tauIdDiscriminator = tauIdDiscrEntries_.begin();
	tauIdDiscriminator != tauIdDiscrEntries_.end(); ++tauIdDiscriminator ) {
    tree_->Branch(Form("Tau_%s", tauIdDiscriminator->branchName_.data()), &tauIdDiscriminator->value_, Form("Tau_%s/F", tauIdDiscriminator->branchName_.data()));
  std::cout <<"branch "  << tauIdDiscriminator->branchName_.data() << std::endl;
  }

  tree_->Branch("Tau_DecayMode", &Tau_DecayMode_, "Tau_DecayMode/I");
  tree_->Branch("Tau_MatchElePassVeto", &Tau_MatchElePassVeto_, "Tau_MatchElePassVeto/I");
  tree_->Branch("Tau_VtxZ", &Tau_VtxZ_, "Tau_VtxZ/F");
  tree_->Branch("Tau_zImpact", &Tau_zImpact_, "Tau_zImpact/F");

  tree_->Branch("evtWeight", &evtWeight_, "evtWeight/F");

  tree_->Branch("GenEle_Pt",&GenEle_Pt_,"GenEle_Pt/F");
  tree_->Branch("GenEle_Eta",&GenEle_Eta_,"GenEle_Eta/F");
}

void AntiElectronDiscrMVATrainingNtupleProducer::analyze(const edm::Event& evt, const edm::EventSetup& es)
{
  run_ = evt.run();
  event_ = (evt.eventAuxiliary()).event();
  lumi_ = evt.luminosityBlock();

  edm::Handle<pat::ElectronCollection> gsfElectrons;
  evt.getByToken(electronToken_,gsfElectrons);
  
  edm::Handle<pat::TauCollection> taus;
  evt.getByToken(tauToken_, taus);

  typedef edm::View<reco::Candidate> CandidateView;
  edm::Handle<CandidateView> genElectrons;
  evt.getByToken(genElectronToken_, genElectrons);

  edm::Handle<CandidateView> genTaus;
  evt.getByToken(genTauToken_, genTaus);

  edm::Handle<reco::VertexCollection> vertices;
  evt.getByToken(vertexToken_, vertices);
  NumPV_ = vertices->size();

  evtWeight_ = 1.0;

  //edm::Handle< double > rhoHandle;
  //edm::InputTag rhoTag = edm::InputTag("fixedGridRhoFastjetAll","");
  //evt.getByLabel(rhoTag,rhoHandle);

  edm::Handle<edm::ValueMap<bool> > tight_id_decisions2;
  evt.getByToken(electronTightIdMapToken_,tight_id_decisions2);
  //-----------------------------------------------------------------------------
    GenEle_Eta_ = -99. ;
    GenEle_Pt_  = -99. ;

    Tau_GsfEleMatch_ = 0;

    Tau_EtaAtEcalEntrance_ = -99;
    Tau_PhiAtEcalEntrance_ = -99;
    Tau_EtaAtEcalEntranceEcalEnWeighted_ = -99;
    Tau_PhiAtEcalEntranceEcalEnWeighted_ = -99;
    Tau_LeadNeutralPFCandEtaAtEcalEntrance_ = -99;
    Tau_LeadNeutralPFCandPhiAtEcalEntrance_ = -99;
    Tau_LeadNeutralPFCandPt_ = -99;
    Tau_LeadChargedPFCandEtaAtEcalEntrance_ = -99;
    Tau_LeadChargedPFCandPhiAtEcalEntrance_ = -99;
    Tau_Eta_ = -99;
    Tau_Phi_ = -99;
    Tau_Pt_ = -99;
    Tau_LeadHadronPt_ = -99;
    Tau_HasGsf_ = -99;
    Tau_GSFChi2_ = -99;
    Tau_GSFNumHits_ = -99;
    Tau_GSFNumPixelHits_ = -99;
    Tau_GSFNumStripHits_ = -99;
    Tau_GSFTrackResol_ = -99;
    Tau_GSFTracklnPt_ = -99;
    Tau_GSFTrackEta_ = -99;
    Tau_HasKF_ = -99;
    Tau_KFChi2_ = -99;
    Tau_KFNumHits_ = -99;
    Tau_KFNumPixelHits_ = -99;
    Tau_KFNumStripHits_ = -99;
    Tau_KFTrackResol_ = -99;
    Tau_KFTracklnPt_ = -99;
    Tau_KFTrackEta_ = -99;
    Tau_EmFraction_ = -99;
    Tau_EmFraction_PFCharged_ = -99;
    Tau_NumChargedCands_ = -99;
    Tau_NumGammaCandsIn_ = -99;
    Tau_NumGammaCandsOut_ = -99;
    Tau_HadrHoP_ = -99;
    Tau_HadrEoP_ = -99;
    Tau_VisMass_ = -99;
    Tau_VisMassIn_ = -99;
    Tau_GammaEtaMomIn_ = -99;
    Tau_GammaEtaMomOut_ = -99;
    Tau_GammaPhiMomIn_ = -99;
    Tau_GammaPhiMomOut_ = -99;
    Tau_GammaEnFracIn_ = -99;
    Tau_GammaEnFracOut_ = -99;
    Tau_HadrMvaOut_ = -99;
    Tau_HadrMvaOutIsolated_= -99.;
    Tau_MatchElePassVeto_ = -99;
    Tau_DecayMode_ = -99;
    Tau_MatchElePassVeto_ = -99;
    Tau_VtxZ_ = -99;
    Tau_zImpact_ = -99;
    Tau_LeadChargedPFCandPt_ = -99;

    // Matchings
    Tau_GenEleMatch_ = 0;
    Tau_GenHadMatch_ = 0;

    Tau_GenEle_Pt_ = -99.;
    Tau_GenEle_Eta_ = -99.;

    NumGenEle_ = 0;
    NumGenHad_ = 0;
    
    Elec_Eta_ = -99;
    Elec_Pt_ = -99;
    Elec_MvaOut_ = -99;
    Elec_MvaOutIsolated_ = -99;
    Elec_MvaInEarlyBrem_ =  -99;
    Elec_MvaInLateBrem_=  -99;
    Elec_MvaInSigmaEtaEta_ =  -99;
    Elec_MvaInHadEnergy_ = -99;
    Elec_MvaInDeltaEta_ = -99;
    Elec_MvaInNClusterOutMustache_ = -99;
    Elec_Iso_ = -99;
    Elec_IsoRel_ = -99;
    Elec_MvaInEtOutMustache_ = -99;
    Elec_SigmaEtaEta_ = -99;
    Elec_SigmaEtaEta_full5x5_ = -99;
    Elec_Fbrem_ = -99;
    Elec_Eecal_ = -99.;
    Elec_DeltaEta_ = -99.;
    Elec_DeltaPhi_ = -99.;
    Elec_DeltaEtaAtVtx_ = -99.;
    Elec_DeltaPhiAtVtx_ = -99.;
    // Variables related to the SC
    Elec_HasSC_ = -99;
    Elec_Ee_ = -99;
    Elec_Egamma_ = -99;
    Elec_Pin_ = -99;
    Elec_Pout_ = -99;
    Elec_EtotOverPin_ = -99;
    Elec_EeOverPout_ = -99;
    Elec_EgammaOverPdif_ = -99;
    Elec_HoHplusE_ = -99;
    Elec_HasKF_ = -99;
    Elec_Chi2KF_ = -99;
    Elec_Chi2NormKF_ = -99;
    Elec_KFNumHits_ = -99;
    Elec_KFNumPixelHits_ = -99;
    Elec_KFNumStripHits_ = -99;
    Elec_KFTrackResol_ = -99;
    Elec_KFTracklnPt_ = -99;
    Elec_KFTrackEta_ = -99;
    Elec_HasGSF_ = -99;
    Elec_Chi2GSF_ = -99;
    Elec_Chi2NormGSF_ = -99;
    Elec_GSFNumHits_ = -99;
    Elec_GSFNumPixelHits_ = -99;
    Elec_GSFNumStripHits_ = -99;
    Elec_GSFTrackResol_ = -99;
    Elec_GSFTracklnPt_ = -99;
    Elec_GSFTrackEta_ = -99;

    ElecVeto_N_ = 0;
    ElecVeto_Pt_ = -99;
    ElecVeto_Eta_ = -99;
    ElecVeto_Phi_ = -99;

    // Matchings
    Elec_GenEleMatch_ = 0;
    Elec_GenHadMatch_ = 0; 
    
    NumPFTaus_ = 0;
    NumGsfEle_ = 0;

    //
    size_t numPFTaus = taus->size();
    for ( size_t idxPFTau = 0; idxPFTau < numPFTaus; ++idxPFTau )
    {
      const pat::Tau& tau = taus->at(idxPFTau);

    //MB: not mandatory as it is MiniAOD selection, but kept for completness
    if ( tau.pt() < 18. || tau.tauID("decayModeFindingNewDMs")<0.5 ) continue;

    //
    int matchedElectronIdx = -1;
    int nEle = gsfElectrons->size();
    for (int ie = 0; ie < nEle; ie++) {
      const pat::Electron& el = gsfElectrons->at(ie);
      if ( deltaR(tau.p4(), el.p4()) < 0.2 && el.pt() > 10. &&
	   (matchedElectronIdx == -1 || (matchedElectronIdx > -1 && el.pt() > gsfElectrons->at(matchedElectronIdx).pt())) ) {
	matchedElectronIdx = ie;
	Tau_GsfEleMatch_ = 1;
      }
      ++NumGsfEle_;
     }

    //-----------------------------------------------------------------------------
    // GSF electron variables
    //-----------------------------------------------------------------------------

    if ( matchedElectronIdx != -1 )
    {
      //Is electron matched to gen info ?
      for ( reco::CandidateView::const_iterator genElectron = genElectrons->begin();
	    genElectron != genElectrons->end(); ++genElectron ) {
	++NumGenEle_;
	if ( deltaR(gsfElectrons->at(matchedElectronIdx).eta(), gsfElectrons->at(matchedElectronIdx).phi(), genElectron->eta(), genElectron->phi()) < 0.2 ) {
	  Elec_GenEleMatch_ = 1;
	  break;
	}
      }
      for ( reco::CandidateView::const_iterator genTau = genTaus->begin();
	    genTau != genTaus->end(); ++genTau ) {
	++NumGenHad_;
	if ( deltaR(gsfElectrons->at(matchedElectronIdx).eta(), gsfElectrons->at(matchedElectronIdx).phi(), genTau->eta(), genTau->phi()) < 0.2 ) {
	  Elec_GenHadMatch_ = 1;
	  break;
	}
      }

      // Matchings
      Elec_Eta_ = gsfElectrons->at(matchedElectronIdx).eta();
      Elec_Pt_ = gsfElectrons->at(matchedElectronIdx).pt();
      Elec_MvaOut_ = TMath::Max(gsfElectrons->at(matchedElectronIdx).mvaOutput().mva_e_pi, float(-1.0));
      Elec_MvaOutIsolated_ = TMath::Max(gsfElectrons->at(matchedElectronIdx).mvaOutput().mva_Isolated, float(-1.0));
      Elec_MvaInEarlyBrem_ = gsfElectrons->at(matchedElectronIdx).mvaInput().earlyBrem;
      Elec_MvaInLateBrem_= gsfElectrons->at(matchedElectronIdx).mvaInput().lateBrem;
      Elec_MvaInSigmaEtaEta_ = gsfElectrons->at(matchedElectronIdx).mvaInput().sigmaEtaEta;
      Elec_MvaInHadEnergy_ = gsfElectrons->at(matchedElectronIdx).mvaInput().hadEnergy;
      Elec_MvaInDeltaEta_ = gsfElectrons->at(matchedElectronIdx).mvaInput().deltaEta;
      Elec_MvaInNClusterOutMustache_ = gsfElectrons->at(matchedElectronIdx).mvaInput().nClusterOutsideMustache;
      Elec_MvaInEtOutMustache_ = gsfElectrons->at(matchedElectronIdx).mvaInput().etOutsideMustache;

      //double absEta = std::abs(gsfElectrons->at(matchedElectronIdx).superCluster()->eta());
      //const float eA = _effectiveAreas.getEffectiveArea( absEta );
      //const float rho = rhoHandle.isValid() ? (float)(*rhoHandle) : 0;

      Elec_Iso_ = gsfElectrons->at(matchedElectronIdx).pfIsolationVariables().sumChargedHadronPt
      + std::max(0.0,
      gsfElectrons->at(matchedElectronIdx).pfIsolationVariables().sumNeutralHadronEt +
      gsfElectrons->at(matchedElectronIdx).pfIsolationVariables().sumPhotonEt
      -0.5*gsfElectrons->at(matchedElectronIdx).pfIsolationVariables().sumPUPt);
      //- rho*eA);

      Elec_IsoRel_ = Elec_Iso_;
      if (Elec_Pt_>0.) Elec_IsoRel_ = Elec_Iso_ /Elec_Pt_;

      Elec_SigmaEtaEta_ = gsfElectrons->at(matchedElectronIdx).sigmaEtaEta();
      Elec_SigmaEtaEta_full5x5_ = gsfElectrons->at(matchedElectronIdx).full5x5_sigmaEtaEta();
      Elec_Fbrem_ = gsfElectrons->at(matchedElectronIdx).fbrem();
      Elec_Eecal_ = gsfElectrons->at(matchedElectronIdx).ecalEnergy();
      Elec_DeltaEta_ = gsfElectrons->at(matchedElectronIdx).deltaEtaSeedClusterTrackAtCalo();
      Elec_DeltaPhi_ = gsfElectrons->at(matchedElectronIdx).deltaPhiSeedClusterTrackAtCalo();
      Elec_DeltaEtaAtVtx_ = gsfElectrons->at(matchedElectronIdx).deltaEtaSuperClusterTrackAtVtx();
      Elec_DeltaPhiAtVtx_ = gsfElectrons->at(matchedElectronIdx).deltaPhiSuperClusterTrackAtVtx();

      // Variables related to the SC
      Elec_HasSC_ = 0;
      reco::SuperClusterRef pfSuperCluster = gsfElectrons->at(matchedElectronIdx).superCluster();
      if ( pfSuperCluster.isNonnull() && pfSuperCluster.isAvailable() ) {
	Elec_HasSC_ = 1;
	Elec_Ee_ = 0.;
	Elec_Egamma_ = 0.;
	for ( reco::CaloCluster_iterator pfCluster = pfSuperCluster->clustersBegin();
	      pfCluster != pfSuperCluster->clustersEnd(); ++pfCluster ) {
	  float pfClusterEn = (*pfCluster)->energy();
	  if ( pfCluster == pfSuperCluster->clustersBegin() ) Elec_Ee_ += pfClusterEn;
	  else Elec_Egamma_ += pfClusterEn;
	}
	Elec_Pin_ = TMath::Sqrt(gsfElectrons->at(matchedElectronIdx).trackMomentumAtVtx().Mag2());
	Elec_Pout_ = TMath::Sqrt(gsfElectrons->at(matchedElectronIdx).trackMomentumOut().Mag2());
	Elec_EtotOverPin_ = (Elec_Ee_ + Elec_Egamma_)/Elec_Pin_;
	Elec_EeOverPout_ = Elec_Ee_/Elec_Pout_;
	Elec_EgammaOverPdif_ = Elec_Egamma_/(Elec_Pin_ - Elec_Pout_);
	Elec_HoHplusE_ = gsfElectrons->at(matchedElectronIdx).mvaInput().hadEnergy/(gsfElectrons->at(matchedElectronIdx).mvaInput().hadEnergy+Elec_Ee_) ;
      }

      // Variables related to the CtfTrack
      Elec_HasKF_ = 0;

      const reco::TrackRef trackref = gsfElectrons->at(matchedElectronIdx).closestCtfTrackRef();
      const reco::Track* track = gsfElectrons->at(matchedElectronIdx).closestCtfTrackRef().get();
      if (track != 0 && trackref.isNonnull()) {
	Elec_HasKF_ = 1;
	Elec_Chi2KF_ = track->chi2();
	Elec_Chi2NormKF_ = track->normalizedChi2();
	Elec_KFNumHits_ = track->numberOfValidHits();
	Elec_KFNumPixelHits_ = track->hitPattern().numberOfValidPixelHits();
	Elec_KFNumStripHits_ = track->hitPattern().numberOfValidStripHits();
	Elec_KFTrackResol_ = track->ptError()/track->pt();
	Elec_KFTracklnPt_ = log(track->pt())*TMath::Ln10();
	Elec_KFTrackEta_ = track->eta();
      }

      // Variables related to the GsfTrack
      Elec_HasGSF_ = 0;

      if ( gsfElectrons->at(matchedElectronIdx).gsfTrack().isNonnull() ) {
	Elec_HasGSF_ = 1;
	Elec_Chi2GSF_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->chi2();
	Elec_Chi2NormGSF_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->normalizedChi2();
	Elec_GSFNumHits_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->numberOfValidHits();
	Elec_GSFNumPixelHits_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->hitPattern().numberOfValidPixelHits();
	Elec_GSFNumStripHits_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->hitPattern().numberOfValidStripHits();
	Elec_GSFTrackResol_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->ptError()/gsfElectrons->at(matchedElectronIdx).gsfTrack()->pt();
	Elec_GSFTracklnPt_ = log(gsfElectrons->at(matchedElectronIdx).gsfTrack()->pt())*TMath::Ln10();
	Elec_GSFTrackEta_ = gsfElectrons->at(matchedElectronIdx).gsfTrack()->eta();
      }

      if ( verbosity_ ) {
	std::cout << "Elec_Eta: " << Elec_Eta_ << std::endl;
	std::cout << "Elec_Pt: " << Elec_Pt_ << std::endl;
	std::cout << "Elec_HasSC: " << Elec_HasSC_ << std::endl;
	std::cout << "Elec_Ee: " << Elec_Ee_ << ", Elec_Egamma: " << Elec_Egamma_ << ", Elec_Eecal: " << Elec_Eecal_ << std::endl;
	std::cout << "Elec_Pin: " << Elec_Pin_ << ", Elec_Pout: " << Elec_Pout_ << std::endl;
	std::cout << "Elec_HasKF: " << Elec_HasKF_ << std::endl;
	std::cout << "Elec_HasGSF: " << Elec_HasGSF_ << std::endl;
	std::cout << "Elec_MvaOut: " << Elec_MvaOut_ << std::endl;
	std::cout << "Elec_MvaOutIsolated: " << Elec_MvaOutIsolated_ << std::endl;
	std::cout << "Elec_EtotOverPin: " << Elec_EtotOverPin_ << std::endl;
	std::cout << "Elec_EeOverPout: " << Elec_EeOverPout_ << std::endl;
	std::cout << "Elec_EgammaOverPdif: " << Elec_EgammaOverPdif_ << std::endl;
	std::cout << "Elec_MvaInEarlyBrem: " << Elec_MvaInEarlyBrem_ << std::endl;
	std::cout << "Elec_MvaInLateBrem: " << Elec_MvaInLateBrem_ << std::endl;
	std::cout << "Elec_MvaInSigmaEtaEta: " << Elec_MvaInSigmaEtaEta_ << std::endl;
	std::cout << "Elec_MvaInHadEnergy: " << Elec_MvaInHadEnergy_ << std::endl;
	std::cout << "Elec_MvaInDeltaEta: " << Elec_MvaInDeltaEta_ << std::endl;
	std::cout << "Elec_MvaInNClusterOutMustache: " << Elec_MvaInNClusterOutMustache_ << std::endl;
	std::cout << "Elec_MvaInEtOutMustache: " << Elec_MvaInEtOutMustache_ << std::endl;
	std::cout << "Elec_SigmaEtaEta: " << Elec_SigmaEtaEta_ << std::endl;
	std::cout << "Elec_SigmaEtaEta_full5x5: " << Elec_SigmaEtaEta_full5x5_ << std::endl; 
	std::cout << "Elec_HoHplusE: " << Elec_HoHplusE_ << std::endl;
	std::cout << "Elec_FBrem: " << Elec_Fbrem_ << std::endl;
	std::cout << "Elec_DeltaEta: " << Elec_DeltaEta_ << ", Elec_DeltaPhi: " << Elec_DeltaPhi_ << std::endl;
	std::cout << "Elec_DeltaEtaAtVtx: " << Elec_DeltaEtaAtVtx_ << ", Elec_DeltaPhiAtVtx: " << Elec_DeltaPhiAtVtx_ << std::endl;
	std::cout << "Elec_Chi2KF: " << Elec_Chi2KF_ << ", Elec_Chi2NormKF: " << Elec_Chi2NormKF_ << std::endl;
	std::cout << "Elec_Chi2GSF: " << Elec_Chi2GSF_ << ", Elec_Chi2NormGSF: " << Elec_Chi2NormGSF_ << std::endl;
	std::cout << "Elec_GSFNumHits: " << Elec_GSFNumHits_ << std::endl;
	std::cout << "Elec_GSFNumPixelHits: " << Elec_GSFNumPixelHits_ << std::endl;
	std::cout << "Elec_GSFNumStripHits: " << Elec_GSFNumStripHits_ << std::endl;
	std::cout << "Elec_GSFTrackResol: " << Elec_GSFTrackResol_ << std::endl;
	std::cout << "Elec_GSFTracklnPt: " << Elec_GSFTracklnPt_ << std::endl;
	std::cout << "Elec_GSFTrackEta: " << Elec_GSFTrackEta_ << std::endl;
	std::cout << std::endl;
      }

    } // end if matchedElectron

    //-----------------------------------------------------------------------------
    // PFTau variables
    //-----------------------------------------------------------------------------

    // is tau matched to gen info ?
    //
    for ( reco::CandidateView::const_iterator genElectron = genElectrons->begin();
	  genElectron != genElectrons->end(); ++genElectron ) {
      if ( deltaR(tau.eta(), tau.phi(), genElectron->eta(), genElectron->phi()) < 0.2 ) {
	Tau_GenEleMatch_ = 1;
	Tau_GenEle_Pt_  = genElectron->pt();
	Tau_GenEle_Eta_ = genElectron->eta();
      }
    }
    for ( reco::CandidateView::const_iterator genTau = genTaus->begin();
	  genTau != genTaus->end(); ++genTau ) {
      if ( deltaR(tau.eta(), tau.phi(), genTau->eta(), genTau->phi()) < 0.2 ) {
	Tau_GenHadMatch_ = 1;
	break;
      }
    }

    //
    const reco::CandidatePtrVector signalCands = tau.signalCands();
    for (unsigned int o = 0; o < signalCands.size(); o++ ) {
//     pat::PackedCandidate const*  signalCand = dynamic_cast<pat::PackedCandidate const*> (signalCands[o].get());
       if ( signalCands[o]->pt() > Tau_LeadNeutralPFCandPt_ ) {
         Tau_LeadNeutralPFCandPt_ = signalCands[o]->pt();
       }
    }
    Tau_LeadChargedPFCandEtaAtEcalEntrance_ = tau.etaAtEcalEntranceLeadChargedCand();
    Tau_EtaAtEcalEntrance_   = tau.etaAtEcalEntrance();
    Tau_PhiAtEcalEntrance_   = tau.phiAtEcalEntrance();
    Tau_LeadChargedPFCandPt_ = tau.ptLeadChargedCand();
    Tau_Eta_ = tau.eta();
    Tau_Pt_  = tau.pt();
    Tau_Phi_ = tau.phi();
    Tau_EmFraction_ = TMath::Max(tau.emFraction_MVA(), float(0.));
    Tau_NumChargedCands_ = tau.signalChargedHadrCands().size();

    pat::PackedCandidate const* packedLeadTauCand = dynamic_cast<pat::PackedCandidate const*>(tau.leadChargedHadrCand().get());
    Tau_LeadHadronPt_ = packedLeadTauCand->pt();
    if( std::abs(packedLeadTauCand->pdgId()) == 11 )
    {
      Tau_HasGsf_ = 1;
      if (packedLeadTauCand->hasTrackDetails()) {
	const reco::Track & pseudoTrack = packedLeadTauCand->pseudoTrack();
	Tau_GSFChi2_ = pseudoTrack.normalizedChi2();
	Tau_GSFNumHits_ = pseudoTrack.numberOfValidHits();
	Tau_GSFNumPixelHits_ = pseudoTrack.hitPattern().numberOfValidPixelHits();
	Tau_GSFNumStripHits_ = pseudoTrack.hitPattern().numberOfValidStripHits();
	Tau_GSFTrackResol_ = pseudoTrack.ptError()/pseudoTrack.pt();
	Tau_GSFTracklnPt_ = log(pseudoTrack.pt())*TMath::Ln10();
	Tau_GSFTrackEta_ = pseudoTrack.eta();
      }
    }
    if ( std::abs(packedLeadTauCand->pdgId()) != 11 ) {
      Tau_HasKF_ = 0;
      if (packedLeadTauCand->hasTrackDetails()) {
	const reco::Track & pseudoTrack = packedLeadTauCand->pseudoTrack();
	Tau_KFChi2_ = pseudoTrack.normalizedChi2();
	Tau_KFNumHits_ = pseudoTrack.numberOfValidHits();
	Tau_KFNumPixelHits_ = pseudoTrack.hitPattern().numberOfValidPixelHits();
	Tau_KFNumStripHits_ = pseudoTrack.hitPattern().numberOfValidStripHits();
	Tau_KFTrackResol_ = pseudoTrack.ptError()/pseudoTrack.pt();
	Tau_KFTracklnPt_ = log(pseudoTrack.pt())*TMath::Ln10();
	Tau_KFTrackEta_ = pseudoTrack.eta();
      }
    }

    Tau_HadrHoP_ = tau.hcalEnergyLeadChargedHadrCand()/packedLeadTauCand->p();
    Tau_HadrEoP_ = tau.ecalEnergyLeadChargedHadrCand()/packedLeadTauCand->p();

    if ( tau.hcalEnergyLeadChargedHadrCand()+tau.ecalEnergyLeadChargedHadrCand() != 0. ) {
      Tau_EmFraction_PFCharged_ = TMath::Max(tau.ecalEnergyLeadChargedHadrCand()/(tau.hcalEnergyLeadChargedHadrCand()+tau.ecalEnergyLeadChargedHadrCand()), float(0.));
    } else { Tau_EmFraction_PFCharged_ = 0.; }

    GammasdEtaInSigCone_.clear();
    GammasdPhiInSigCone_.clear();
    GammasPtInSigCone_.clear();
    GammasdEtaOutSigCone_.clear();
    GammasdPhiOutSigCone_.clear();
    GammasPtOutSigCone_.clear();

    reco::Candidate::LorentzVector pfGammaSum(0,0,0,0);

    const reco::CandidatePtrVector signalGammaCands = tau.signalGammaCands();
    for ( reco::CandidatePtrVector::const_iterator pfGamma = signalGammaCands.begin();
	  pfGamma != signalGammaCands.end(); ++pfGamma ) {

      float dR = deltaR((*pfGamma)->p4(), tau.leadChargedHadrCand()->p4());

      // gammas inside the tau signal cone
      if (dR < std::max(0.05, std::min(0.10, 3.0/tau.pt()))) {
        if ( tau.leadChargedHadrCand().isNonnull() ) {
	  GammasdEtaInSigCone_.push_back((*pfGamma)->eta() - tau.leadChargedHadrCand()->eta());
	  GammasdPhiInSigCone_.push_back((*pfGamma)->phi() - tau.leadChargedHadrCand()->phi());
        } 
        else {
	  GammasdEtaInSigCone_.push_back((*pfGamma)->eta() - tau.eta());
	  GammasdPhiInSigCone_.push_back((*pfGamma)->phi() - tau.phi());
        }
        GammasPtInSigCone_.push_back((*pfGamma)->pt());
        pfGammaSum += (*pfGamma)->p4();
      }
      // gammas outside the tau signal cone
      else {
        if ( tau.leadChargedHadrCand().isNonnull() ) {
	  GammasdEtaOutSigCone_.push_back((*pfGamma)->eta() - tau.leadChargedHadrCand()->eta());
	  GammasdPhiOutSigCone_.push_back((*pfGamma)->phi() - tau.leadChargedHadrCand()->phi());
        } 
        else {
	  GammasdEtaOutSigCone_.push_back((*pfGamma)->eta() - tau.eta());
	  GammasdPhiOutSigCone_.push_back((*pfGamma)->phi() - tau.phi());
        }
        GammasPtOutSigCone_.push_back((*pfGamma)->pt());
      }
    }

    Tau_NumGammaCandsIn_ = GammasPtInSigCone_.size();
    Tau_NumGammaCandsOut_ = GammasPtOutSigCone_.size();

    float sumPt  = 0.;
    float dEta   = 0.;
    float dEta2  = 0.;
    float dPhi   = 0.;
    float dPhi2  = 0.;
    float sumPt2 = 0.;
    size_t numPFGammas = GammasPtInSigCone_.size();
    assert(GammasdEtaInSigCone_.size() == numPFGammas);
    assert(GammasdPhiInSigCone_.size() == numPFGammas);
    for ( size_t idxPFGamma = 0; idxPFGamma < numPFGammas; ++idxPFGamma ) {
      float gamma_pt  = GammasPtInSigCone_[idxPFGamma];
      float gamma_dPhi = GammasdPhiInSigCone_[idxPFGamma];
      if ( gamma_dPhi > TMath::Pi() ) gamma_dPhi -= 2.*TMath::Pi();
      else if ( gamma_dPhi < -TMath::Pi() ) gamma_dPhi += 2.*TMath::Pi();
      float gamma_dEta = GammasdEtaInSigCone_[idxPFGamma];
      sumPt  +=  gamma_pt;
      sumPt2 += (gamma_pt*gamma_pt);
      dEta   += (gamma_pt*gamma_dEta);
      dEta2  += (gamma_pt*gamma_dEta*gamma_dEta);
      dPhi   += (gamma_pt*gamma_dPhi);
      dPhi2  += (gamma_pt*gamma_dPhi*gamma_dPhi);  
    }
    
    float gammadPt = sumPt/tau.pt();
	    
    if ( sumPt > 0. ) {
      dEta  /= sumPt;
      dPhi  /= sumPt;
      dEta2 /= sumPt;
      dPhi2 /= sumPt;
    }

    Tau_GammaEtaMomIn_ = TMath::Sqrt(dEta2)*TMath::Sqrt(gammadPt)*tau.pt();
    Tau_GammaPhiMomIn_ = TMath::Sqrt(dPhi2)*TMath::Sqrt(gammadPt)*tau.pt();
    Tau_GammaEnFracIn_ = gammadPt;

    sumPt  = 0.;
    dEta   = 0.;
    dEta2  = 0.;
    dPhi   = 0.;
    dPhi2  = 0.;
    sumPt2 = 0.;
    numPFGammas = GammasPtOutSigCone_.size();

    assert(GammasdEtaOutSigCone_.size() == numPFGammas);
    assert(GammasdPhiOutSigCone_.size() == numPFGammas);

    for ( size_t idxPFGamma = 0; idxPFGamma < numPFGammas; ++idxPFGamma ) {
      float gamma_pt  = GammasPtOutSigCone_[idxPFGamma];
      float gamma_dPhi = GammasdPhiOutSigCone_[idxPFGamma];
      if ( gamma_dPhi > TMath::Pi() ) gamma_dPhi -= 2.*TMath::Pi();
      else if ( gamma_dPhi < -TMath::Pi() ) gamma_dPhi += 2.*TMath::Pi();
      float gamma_dEta = GammasdEtaOutSigCone_[idxPFGamma];
      sumPt  +=  gamma_pt;
      sumPt2 += (gamma_pt*gamma_pt);
      dEta   += (gamma_pt*gamma_dEta);
      dEta2  += (gamma_pt*gamma_dEta*gamma_dEta);
      dPhi   += (gamma_pt*gamma_dPhi);
      dPhi2  += (gamma_pt*gamma_dPhi*gamma_dPhi);  
    }
    
    gammadPt = sumPt/tau.pt();
	    
    if ( sumPt > 0. ) {
      dEta  /= sumPt;
      dPhi  /= sumPt;
      dEta2 /= sumPt;
      dPhi2 /= sumPt;
    }

    Tau_GammaEtaMomOut_ = TMath::Sqrt(dEta2)*TMath::Sqrt(gammadPt)*tau.pt();
    Tau_GammaPhiMomOut_ = TMath::Sqrt(dPhi2)*TMath::Sqrt(gammadPt)*tau.pt();
    Tau_GammaEnFracOut_ = gammadPt;

    reco::Candidate::LorentzVector pfChargedSum(0,0,0,0);

    const reco::CandidatePtrVector signalChargedCands = tau.signalChargedHadrCands();
    for ( reco::CandidatePtrVector::const_iterator pfCharged = signalChargedCands.begin();
	  pfCharged != signalChargedCands.end(); ++pfCharged ) {

      float dR = deltaR((*pfCharged)->p4(), tau.leadChargedHadrCand()->p4());

      // charged particles inside the tau signal cone
      if (dR < std::max(0.05, std::min(0.10, 3.0/tau.pt()))) {
        pfChargedSum += (*pfCharged)->p4();
      }
    }

    Tau_VisMass_ = tau.mass();
    Tau_VisMassIn_ = (pfGammaSum + pfChargedSum).mass();

    if ( tau.leadPFChargedHadrCand().isNonnull() ) {
      Tau_HadrMvaOut_ = TMath::Max(tau.leadPFChargedHadrCand()->mva_e_pi(), float(-1.));
      Tau_HadrMvaOutIsolated_ = TMath::Max(tau.leadPFChargedHadrCand()->mva_Isolated(), float(-1.));
    }

    if ( verbosity_ ) {
      std::cout << "GammaEtaMomIn: " << Tau_GammaEtaMomIn_ << std::endl;
      std::cout << "GammaEtaMomOut: " << Tau_GammaEtaMomOut_ << std::endl;
      std::cout << "GammaPhiMomIn: " << Tau_GammaPhiMomIn_ << std::endl;
      std::cout << "GammaPhiMomOut: " << Tau_GammaPhiMomOut_ << std::endl;
      std::cout << "GammaPt: " << sumPt << std::endl;
      std::cout << "TauPt: " << tau.pt() << std::endl;
      std::cout << "TauEta: " << tau.eta() << std::endl;
      //std::cout << "sumEtaTimesEnergy: " << sumEtaTimesEnergy << std::endl;
      //std::cout << "sumEnergy: " << sumEnergy << std::endl;
      std::cout << "GammaEnFracIn: " << Tau_GammaEnFracIn_ << std::endl;
      std::cout << "GammaEnFracOut: " << Tau_GammaEnFracOut_ << std::endl;
      std::cout << std::endl;
    }


    for ( std::vector<tauIdDiscrEntryType>::iterator tauIdDiscriminator = tauIdDiscrEntries_.begin();
	  tauIdDiscriminator != tauIdDiscrEntries_.end(); ++tauIdDiscriminator ) {
      if( tau.isTauIDAvailable(tauIdDiscriminator->branchName_) )
	tauIdDiscriminator->value_ = tau.tauID(tauIdDiscriminator->branchName_);
      else {
	tauIdDiscriminator->value_ = -99;
	if ( verbosity_ ) {
	  std::cout << "TauID called "<<tauIdDiscriminator->branchName_ << " is not present" << std::endl;
	}
      }
    }

    Tau_DecayMode_ = tau.decayMode();

    Tau_VtxZ_ = tau.vertex().z();
    if ( std::abs(TMath::Tan(tau.theta())) > 1.e-3 ) {
      const double rECAL = 130; // approx. ECAL radius in cm
      Tau_zImpact_ = tau.vertex().z() + rECAL/TMath::Tan(tau.theta());
      }
    
    // Tau is matched to a gsfElectron passing selection criteria for SecondElectronVeto
    /*bool matchElectronCutsVeto = false;

    int idxGSFElectron = 0;
    for(int ie=0;ie<nEle;ie++) {      
      if(gsfElectrons->at(ie).gsfTrack().isNonnull()) { 
        float nHits = gsfElectrons->at(ie).gsfTrack()->hitPattern().numberOfAllHits(reco::HitPattern::MISSING_INNER_HITS);//}
	float dPhi  = std::abs(gsfElectrons->at(ie).deltaPhiSuperClusterTrackAtVtx());
	float dEta  = std::abs(gsfElectrons->at(ie).deltaEtaSuperClusterTrackAtVtx());
	float sihih = gsfElectrons->at(ie).sigmaIetaIeta();
	float HoE   = gsfElectrons->at(ie).hadronicOverEm();
	if ( verbosity_ ) {
	  std::cout << "gsfElectron #: " << idxGSFElectron << std::endl;
	  std::cout << "gsfElectron nHits: " << nHits << std::endl;
	  std::cout << "gsfElectron pt: " << gsfElectrons->at(ie).pt() << std::endl;
	  std::cout << "gsfElectron eta: " << gsfElectrons->at(ie).eta() << std::endl;
	  std::cout << "gsfElectron dPhi: " << dPhi << std::endl;
	  std::cout << "gsfElectron dEta: " << dEta << std::endl;
	  std::cout << "gsfElectron sihih: " << sihih << std::endl;
	  std::cout << "gsfElectron HoE: " << HoE << std::endl;
	  std::cout << std::endl;
	}
	bool ElectronPassCutsVeto = false;
	if ( nHits <= 999 &&
	     ((std::abs(gsfElectrons->at(ie).eta()) < 1.5 &&
	       sihih < 0.010 &&
	       dPhi < 0.80 &&
	       dEta < 0.007 &&
	       HoE < 0.15) ||
	      (std::abs(gsfElectrons->at(ie).eta()) > 1.5 && std::abs(gsfElectrons->at(ie).eta()) < 2.3 &&
	       sihih < 0.030 &&
	       dPhi < 0.70 &&
	       dEta < 0.010 &&
	       HoE < 999))
	     ) ElectronPassCutsVeto = true;
	if ( verbosity_ ) {
	  if ( ElectronPassCutsVeto ) std::cout << "gsfElectrons->at(ie) passes 2nd electron selection." << std::endl;
	  else std::cout << "gsfElectrons->at(ie) fails 2nd electron selection." << std::endl;
	}
	double ElePt = gsfElectrons->at(ie).pt();
	if ( (deltaR(tau.eta(), tau.phi(), gsfElectrons->at(ie).eta(), gsfElectrons->at(ie).phi()) < 0.3) && ElectronPassCutsVeto && ElePt > ElecVeto_Pt_ ) {
	  matchElectronCutsVeto = true;
	  ElecVeto_Pt_ = ElePt;
	  ElecVeto_Eta_ = gsfElectrons->at(ie).eta();
	  ElecVeto_Phi_ = gsfElectrons->at(ie).phi();
	  ++ElecVeto_N_;
	} 
	++idxGSFElectron;}
    } // end loop over gsfElectrons
    Tau_MatchElePassVeto_ = matchElectronCutsVeto;

    if ( verbosity_ ) {
      std::cout << "Tau: Pt = " << tau.pt() << ", eta = " << tau.eta() << ", phi = " << tau.phi() << std::endl;
      std::cout << "matchElectronCutsVeto = " << matchElectronCutsVeto << std::endl;
    }
    */
    bool matchElectronCutsVeto = false;

    //int idxGSFElectron = 0;
    //std::cout <<" safety " << nEle << " " << electrons->size() << std::endl;
    for(int ie=0;ie<nEle;ie++) {
       if(gsfElectrons->at(ie).gsfTrack().isNonnull()) {
	 int nHits = gsfElectrons->at(ie).gsfTrack()->hitPattern().numberOfAllHits(reco::HitPattern::MISSING_INNER_HITS);
	 float dxy = 99;
	 float dz  = 99;
	 const reco::Vertex* vertex = 0;
	 if (vertices->size()>0) {
	   vertex = &(vertices->front());
	   dxy = (gsfElectrons->at(ie).gsfTrack()->dxy(vertex->position()));
	   dz  = (gsfElectrons->at(ie).gsfTrack()->dz(vertex->position()));
	 } 
	 bool passConversionVeto = gsfElectrons->at(ie).passConversionVeto();
	 float iso = gsfElectrons->at(ie).pfIsolationVariables().sumChargedHadronPt
	   + std::max(0.0,
		      gsfElectrons->at(ie).pfIsolationVariables().sumNeutralHadronEt +
		      gsfElectrons->at(ie).pfIsolationVariables().sumPhotonEt
		      -0.5*gsfElectrons->at(ie).pfIsolationVariables().sumPUPt);

	 double ElePt = gsfElectrons->at(ie).pt();
	 if (ElePt> 0.) iso = iso/ElePt;
	 int isEleIDVeto = 0;
	 if(gsfElectrons->at(ie).isElectronIDAvailable(eleIdVetoName_))
	   isEleIDVeto = gsfElectrons->at(ie).electronID(eleIdVetoName_);
	 else if(tight_id_decisions2.isValid())
	   isEleIDVeto = (*tight_id_decisions2)[edm::Ptr<pat::Electron>(gsfElectrons,ie)];

	 //std::cout << nHits << " " << std::abs(gsfElectrons->at(ie).eta())<<" "<< ElePt<<" " << dxy<<" " << dz <<" "<< passConversionVeto<< " " << iso << " " << isEleIDVeto << std::endl;
	 
	 bool ElectronPassCutsVeto = false;
	 //MB: some cuts below look redundant with isEleIdVeto
	 if ( nHits <= 10 && //MB: used explicitely only in 3rd lepton veto (<=1), a cut-based ID for 2nd electron veto already cuts on this (<=2/3 EB/EE), so dummy cut here
	      std::abs(gsfElectrons->at(ie).eta()) < 2.5 &&
	      ElePt >10. &&
	      std::abs(dxy) < 0.045 &&
	      std::abs(dz) < 0.2 &&
	      passConversionVeto == true && //looks redundant with cut based vetoes
	      iso < 0.3 &&
	      isEleIDVeto == 1 ) ElectronPassCutsVeto = true;

	 if ( (deltaR(tau.eta(), tau.phi(), gsfElectrons->at(ie).eta(), gsfElectrons->at(ie).phi()) < 0.2) && ElectronPassCutsVeto ) {
	   matchElectronCutsVeto = true;
	   ElecVeto_Pt_ = ElePt;
	   ElecVeto_Eta_ = gsfElectrons->at(ie).eta();
	   ElecVeto_Phi_ = gsfElectrons->at(ie).phi();
	   ++ElecVeto_N_;
	 }
	 //++idxGSFElectron;
       }
    } // end loop over gsfElectrons
    Tau_MatchElePassVeto_ = matchElectronCutsVeto;

    if ( verbosity_ ) {
      std::cout << "Tau: Pt = " << tau.pt() << ", eta = " << tau.eta() << ", phi = " << tau.phi() << std::endl;
      std::cout << "matchElectronCutsVeto = " << matchElectronCutsVeto << std::endl;
    }

    ++NumPFTaus_;

    }//end loop over taus

    tree_->Fill();

}

AntiElectronDiscrMVATrainingNtupleProducer::~AntiElectronDiscrMVATrainingNtupleProducer()
{
// nothing to be done yet...
}

void AntiElectronDiscrMVATrainingNtupleProducer::endJob()
{
// nothing to be done yet...
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(AntiElectronDiscrMVATrainingNtupleProducer);
