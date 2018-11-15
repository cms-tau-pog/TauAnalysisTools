#ifndef TauAnalysisTools_TauAnalysisTools_AntiElectronDiscrMVATrainingNtupleProducer_h
#define TauAnalysisTools_TauAnalysisTools_AntiElectronDiscrMVATrainingNtupleProducer_h

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateElectronExtra.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateElectronExtraFwd.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/CaloRecHit/interface/CaloCluster.h"
#include "DataFormats/CaloRecHit/interface/CaloClusterFwd.h"
#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
//#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

//#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
//#include "DataFormats/PatCandidates/interface/VIDCutFlowResult.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include <TFile.h>
#include <TTree.h>
#include <TMath.h>

#include <vector>
#include <string>


class AntiElectronDiscrMVATrainingNtupleProducer : public edm::EDAnalyzer
{
 public:
  // constructor 
  explicit AntiElectronDiscrMVATrainingNtupleProducer(const edm::ParameterSet&);
    
  // destructor
  ~AntiElectronDiscrMVATrainingNtupleProducer();
  
 private:
  void beginJob();
  void analyze(const edm::Event&, const edm::EventSetup&);
  void endJob();

  edm::EDGetTokenT<pat::TauCollection> tauToken_;
  edm::EDGetTokenT<pat::ElectronCollection> electronToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate> > genElectronToken_;
  edm::EDGetTokenT<edm::View<reco::Candidate> > genTauToken_;
  edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
  edm::EDGetTokenT<edm::ValueMap<bool> > electronTightIdMapToken_;
  std::string eleIdVetoName_;

  //EffectiveAreas _effectiveAreas;

  struct tauIdDiscrEntryType
  {
    tauIdDiscrEntryType(const std::string& name)
      : branchName_(name)
    {}
    ~tauIdDiscrEntryType() {}
    std::string branchName_;
    float value_;
  };

  std::vector<tauIdDiscrEntryType> tauIdDiscrEntries_;

  /*
  typedef std::vector<edm::InputTag> vInputTag;
  vInputTag srcWeights_;
  */  

  int verbosity_;
  
  TTree* tree_;

  unsigned long run_;
  unsigned long event_;
  unsigned long lumi_;
  int NumPV_;
  int NumGsfEle_;
  int NumPFTaus_;
  int NumPatTaus_;
  int NumGenEle_;
  int NumGenHad_;
  int NumGenJet_;

  std::vector<float> GammasdEtaInSigCone_;
  std::vector<float> GammasdPhiInSigCone_;
  std::vector<float> GammasPtInSigCone_;
  std::vector<float> GammasdEtaOutSigCone_;
  std::vector<float> GammasdPhiOutSigCone_;
  std::vector<float> GammasPtOutSigCone_;
  int Tau_GsfEleMatch_;
  int Tau_GenEleMatch_;
  int Tau_GenHadMatch_;
  float Tau_Eta_;
  float Tau_EtaAtEcalEntrance_;
  float Tau_PhiAtEcalEntrance_;
  float Tau_EtaAtEcalEntranceEcalEnWeighted_;
  float Tau_PhiAtEcalEntranceEcalEnWeighted_;
  float Tau_LeadNeutralPFCandEtaAtEcalEntrance_;
  float Tau_LeadNeutralPFCandPhiAtEcalEntrance_;
  float Tau_LeadNeutralPFCandPt_;
  float Tau_LeadChargedPFCandEtaAtEcalEntrance_;
  float Tau_LeadChargedPFCandPhiAtEcalEntrance_;
  float Tau_LeadChargedPFCandPt_;
  float Tau_Pt_;
  float Tau_LeadHadronPt_;
  float Tau_Phi_;
  int Tau_HasGsf_; 
  float Tau_GSFChi2_; 
  int Tau_GSFNumHits_; 
  int Tau_GSFNumPixelHits_; 
  int Tau_GSFNumStripHits_; 
  float Tau_GSFTrackResol_; 
  float Tau_GSFTracklnPt_; 
  float Tau_GSFTrackEta_; 
  int Tau_HasKF_; 
  float Tau_KFChi2_; 
  int Tau_KFNumHits_; 
  int Tau_KFNumPixelHits_; 
  int Tau_KFNumStripHits_; 
  float Tau_KFTrackResol_; 
  float Tau_KFTracklnPt_; 
  float Tau_KFTrackEta_; 
  float Tau_EmFraction_; 
  float Tau_EmFraction_PFCharged_;
  int Tau_NumChargedCands_;
  int Tau_NumGammaCandsIn_;
  int Tau_NumGammaCandsOut_;
  float Tau_HadrHoP_; 
  float Tau_HadrEoP_; 
  float Tau_VisMass_;
  float Tau_VisMassIn_; 
  float Tau_GammaEtaMomIn_;
  float Tau_GammaEtaMomOut_;
  float Tau_GammaPhiMomIn_;
  float Tau_GammaPhiMomOut_;
  float Tau_GammaEnFracIn_;
  float Tau_GammaEnFracOut_;
  float Tau_HadrMvaOut_;
  float Tau_HadrMvaOutIsolated_;
  int Tau_DecayMode_;
  int Tau_MatchElePassVeto_;
  float Tau_VtxZ_;
  float Tau_zImpact_;
  float Tau_GenEle_Pt_;
  float Tau_GenEle_Eta_;


  int Elec_GenEleMatch_;
  int Elec_GenEleFromZMatch_;
  int Elec_GenEleFromZTauTauMatch_;
  int Elec_GenHadMatch_;
  int Elec_GenJetMatch_;
  float Elec_Eta_;
  float Elec_Pt_;
  int Elec_HasSC_;
  float Elec_MvaOut_;
  float Elec_MvaOutIsolated_;
  float Elec_Ee_;
  float Elec_Egamma_;
  float Elec_Pin_;
  float Elec_Pout_;
  float Elec_EtotOverPin_;
  float Elec_EeOverPout_;
  float Elec_EgammaOverPdif_;
  int Elec_MvaInEarlyBrem_;
  int Elec_MvaInLateBrem_;
  float Elec_MvaInSigmaEtaEta_;
  float Elec_MvaInHadEnergy_;
  float Elec_MvaInDeltaEta_;
  int Elec_MvaInNClusterOutMustache_;
  float Elec_MvaInEtOutMustache_;
  float Elec_Iso_;
  float Elec_IsoRel_;
  float Elec_SigmaEtaEta_;
  float Elec_SigmaEtaEta_full5x5_; 
  float Elec_HoHplusE_;
  float Elec_Fbrem_;
  float Elec_Eecal_;
  float Elec_DeltaEta_;
  float Elec_DeltaPhi_;
  float Elec_DeltaEtaAtVtx_;
  float Elec_DeltaPhiAtVtx_;
  int Elec_HasKF_;
  float Elec_Chi2KF_;
  float Elec_Chi2NormKF_;
  int Elec_KFNumHits_;
  int Elec_KFNumPixelHits_;
  int Elec_KFNumStripHits_;
  float Elec_KFTrackResol_;
  float Elec_KFTracklnPt_;
  float Elec_KFTrackEta_;
  int Elec_HasGSF_;
  float Elec_Chi2GSF_;
  float Elec_Chi2NormGSF_;
  int Elec_GSFNumHits_;
  int Elec_GSFNumPixelHits_;
  int Elec_GSFNumStripHits_;
  float Elec_GSFTrackResol_;
  float Elec_GSFTracklnPt_;
  float Elec_GSFTrackEta_;

  int ElecVeto_N_;
  float ElecVeto_Pt_;
  float ElecVeto_Eta_;
  float ElecVeto_Phi_;

  float evtWeight_;

  float GenEle_Pt_;
  float GenEle_Eta_;
};

#endif   
