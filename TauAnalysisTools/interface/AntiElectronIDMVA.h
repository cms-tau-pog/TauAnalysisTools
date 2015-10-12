#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CondFormats/EgammaObjects/interface/GBRForest.h"


class AntiElectronIDMVA
{
  public:

   AntiElectronIDMVA(const edm::ParameterSet&);
   ~AntiElectronIDMVA(); 

   bool isInitialized();
 
   double MVAValue(Int_t TauCategory,
                   Float_t TauPt,
                   Float_t TauEtaAtEcalEntrance,
                   Float_t TauLeadChargedPFCandPt,
                   Float_t TauEmFraction,
                   Float_t TauLeadPFChargedHadrHoP,
                   Float_t TauLeadPFChargedHadrEoP,
                   Float_t TauVisMassIn,
                   Float_t TaudCrackEta,
                   Float_t TaudCrackPhi,
                   Int_t TauSignalPFGammaCandsIn,
                   Int_t TauSignalPFGammaCandsOut,
                   Float_t TauGammaEtaMomIn,
                   Float_t TauGammaEtaMomOut,
                   Float_t TauGammaPhiMomIn,
                   Float_t TauGammaPhiMomOut,
                   Float_t TauGammaEnFracIn,
                   Float_t TauGammaEnFracOut,
                   Float_t ElecEtotOverPin,
                   Float_t ElecChi2NormGSF,
                   Float_t ElecChi2NormKF,
                   Int_t ElecGSFNumHits,
                   Int_t ElecKFNumHits,
                   Float_t ElecGSFTrackResol,
                   Float_t ElecGSFTracklnPt,
                   Float_t ElecPin,
                   Float_t ElecPout,
                   Float_t ElecEecal,
                   Float_t ElecDeltaEta,
                   Float_t ElecDeltaPhi,
                   Float_t ElecMvaInSigmaEtaEta,
                   Float_t ElecMvaInHadEnergy,
                   Float_t ElecMvaInDeltaEta
                  );
   
 private:

   bool isInitialized_;
   std::string weightFilePath_;

   std::string mvaName_NoEleMatch_woGwoGSF_BL_;
   std::string mvaName_NoEleMatch_wGwoGSF_BL_;
   std::string mvaName_woGwGSF_BL_;
   std::string mvaName_wGwGSF_BL_;
   std::string mvaName_NoEleMatch_woGwoGSF_EC_;
   std::string mvaName_NoEleMatch_wGwoGSF_EC_;
   std::string mvaName_woGwGSF_EC_;
   std::string mvaName_wGwGSF_EC_;

   Float_t* Var_NoEleMatch_woGwoGSF_Barrel_;
   Float_t* Var_NoEleMatch_wGwoGSF_Barrel_;
   Float_t* Var_woGwGSF_Barrel_;
   Float_t* Var_wGwGSF_Barrel_;
   Float_t* Var_NoEleMatch_woGwoGSF_Endcap_;
   Float_t* Var_NoEleMatch_wGwoGSF_Endcap_;
   Float_t* Var_woGwGSF_Endcap_;
   Float_t* Var_wGwGSF_Endcap_;
   
   const GBRForest* mva_NoEleMatch_woGwoGSF_BL_;
   const GBRForest* mva_NoEleMatch_wGwoGSF_BL_ ;
   const GBRForest* mva_woGwGSF_BL_ ;
   const GBRForest* mva_wGwGSF_BL_ ;
   const GBRForest* mva_NoEleMatch_woGwoGSF_EC_ ;
   const GBRForest* mva_NoEleMatch_wGwoGSF_EC_ ;
   const GBRForest* mva_woGwGSF_EC_ ;
   const GBRForest* mva_wGwGSF_EC_ ;

   int verbosity_;
};

