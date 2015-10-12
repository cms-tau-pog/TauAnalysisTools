#include "TauAnalysisTools/TauAnalysisTools/interface/AntiElectronIDMVA.h"

#include <TFile.h>


namespace
{
  const GBRForest* loadMVAfromFile(const std::string& pathName, const std::string& mvaName)
  {
    std::string fileName = pathName + "/trainAntiElectronDiscrMVA_" + mvaName + "_gbr.root";

    TFile inputFile(fileName.data());    
    if ( inputFile.IsZombie())
      throw cms::Exception("AntiElectronIDMVA::loadMVA")
        << " File " << inputFile.GetName() << " not found !!\n";

    const GBRForest* mva = (GBRForest*)inputFile.Get(mvaName.data());
    if ( !mva )
      throw cms::Exception("AntiElectronIDMVA::loadMVA")
        << " Failed to load MVA = " << mvaName.data() << " from file " << inputFile.GetName() << " !!\n";

    return mva;
  }
}

AntiElectronIDMVA::AntiElectronIDMVA(const edm::ParameterSet& cfg)
  : isInitialized_(false)
{
  if(cfg.exists("mvaWeightPath"))
    weightFilePath_ = cfg.getParameter<std::string>("mvaWeightPath");
  else
    throw cms::Exception("MVA input path not found") << "Requested to load tau MVA input, but no 'mvaWeightPath' provided in cfg file";

  if ( !weightFilePath_.empty() ) {

    mvaName_NoEleMatch_woGwoGSF_BL_ = cfg.getParameter<std::string>("mvaName_NoEleMatch_woGwoGSF_BL");
    mvaName_NoEleMatch_wGwoGSF_BL_  = cfg.getParameter<std::string>("mvaName_NoEleMatch_wGwoGSF_BL");
    mvaName_woGwGSF_BL_             = cfg.getParameter<std::string>("mvaName_woGwGSF_BL");
    mvaName_wGwGSF_BL_              = cfg.getParameter<std::string>("mvaName_wGwGSF_BL");
    mvaName_NoEleMatch_woGwoGSF_EC_ = cfg.getParameter<std::string>("mvaName_NoEleMatch_woGwoGSF_EC");
    mvaName_NoEleMatch_wGwoGSF_EC_  = cfg.getParameter<std::string>("mvaName_NoEleMatch_wGwoGSF_EC");
    mvaName_woGwGSF_EC_             = cfg.getParameter<std::string>("mvaName_woGwGSF_EC");
    mvaName_wGwGSF_EC_              = cfg.getParameter<std::string>("mvaName_wGwGSF_EC");

    mva_NoEleMatch_woGwoGSF_BL_ = loadMVAfromFile(weightFilePath_, mvaName_NoEleMatch_woGwoGSF_BL_);
    mva_NoEleMatch_wGwoGSF_BL_  = loadMVAfromFile(weightFilePath_, mvaName_NoEleMatch_wGwoGSF_BL_); 
    mva_woGwGSF_BL_             = loadMVAfromFile(weightFilePath_, mvaName_woGwGSF_BL_);
    mva_wGwGSF_BL_              = loadMVAfromFile(weightFilePath_, mvaName_wGwGSF_BL_);
    mva_NoEleMatch_woGwoGSF_EC_ = loadMVAfromFile(weightFilePath_, mvaName_NoEleMatch_woGwoGSF_EC_);
    mva_NoEleMatch_wGwoGSF_EC_  = loadMVAfromFile(weightFilePath_, mvaName_NoEleMatch_wGwoGSF_EC_);
    mva_woGwGSF_EC_             = loadMVAfromFile(weightFilePath_, mvaName_woGwGSF_EC_);
    mva_wGwGSF_EC_              = loadMVAfromFile(weightFilePath_, mvaName_wGwGSF_EC_);

    isInitialized_ = true;
  }

  Var_NoEleMatch_woGwoGSF_Barrel_ = new Float_t[9];
  Var_NoEleMatch_wGwoGSF_Barrel_  = new Float_t[17];
  Var_woGwGSF_Barrel_             = new Float_t[23];
  Var_wGwGSF_Barrel_              = new Float_t[31];
  Var_NoEleMatch_woGwoGSF_Endcap_ = new Float_t[8];
  Var_NoEleMatch_wGwoGSF_Endcap_  = new Float_t[16];
  Var_woGwGSF_Endcap_             = new Float_t[22];
  Var_wGwGSF_Endcap_              = new Float_t[30];
    
  verbosity_ = 0;
}

AntiElectronIDMVA::~AntiElectronIDMVA()
{
  delete [] Var_NoEleMatch_woGwoGSF_Barrel_;
  delete [] Var_NoEleMatch_wGwoGSF_Barrel_;
  delete [] Var_woGwGSF_Barrel_;
  delete [] Var_wGwGSF_Barrel_;
  delete [] Var_NoEleMatch_woGwoGSF_Endcap_;
  delete [] Var_NoEleMatch_wGwoGSF_Endcap_;
  delete [] Var_woGwGSF_Endcap_;
  delete [] Var_wGwGSF_Endcap_;

  delete mva_NoEleMatch_woGwoGSF_BL_;
  delete mva_NoEleMatch_wGwoGSF_BL_;
  delete mva_woGwGSF_BL_;
  delete mva_wGwGSF_BL_;
  delete mva_NoEleMatch_woGwoGSF_EC_;
  delete mva_NoEleMatch_wGwoGSF_EC_;
  delete mva_woGwGSF_EC_;
  delete mva_wGwGSF_EC_;
}

bool AntiElectronIDMVA::isInitialized()
{
  return isInitialized_;
}

double AntiElectronIDMVA::MVAValue(Int_t TauCategory,
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
                                  )
{
  double mvaValue = -99.;

  if (TauCategory == 0){
    Var_NoEleMatch_woGwoGSF_Barrel_[0] = TauEtaAtEcalEntrance;
    Var_NoEleMatch_woGwoGSF_Barrel_[1] = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_NoEleMatch_woGwoGSF_Barrel_[2] = std::log(std::max(float(1.), TauPt));
    Var_NoEleMatch_woGwoGSF_Barrel_[3] = TauEmFraction;
    Var_NoEleMatch_woGwoGSF_Barrel_[4] = TauLeadPFChargedHadrHoP;
    Var_NoEleMatch_woGwoGSF_Barrel_[5] = TauLeadPFChargedHadrEoP;
    Var_NoEleMatch_woGwoGSF_Barrel_[6] = TauVisMassIn;
    Var_NoEleMatch_woGwoGSF_Barrel_[7] = TaudCrackEta;
    Var_NoEleMatch_woGwoGSF_Barrel_[8] = TaudCrackPhi;
    mvaValue = mva_NoEleMatch_woGwoGSF_BL_->GetClassifier(Var_NoEleMatch_woGwoGSF_Barrel_);
  }

  if (TauCategory == 2){
    Var_NoEleMatch_wGwoGSF_Barrel_[0]  = TauEtaAtEcalEntrance;
    Var_NoEleMatch_wGwoGSF_Barrel_[1]  = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_NoEleMatch_wGwoGSF_Barrel_[2]  = std::log(std::max(float(1.), TauPt));
    Var_NoEleMatch_wGwoGSF_Barrel_[3]  = TauEmFraction;
    Var_NoEleMatch_wGwoGSF_Barrel_[4]  = TauSignalPFGammaCandsIn;
    Var_NoEleMatch_wGwoGSF_Barrel_[5]  = TauSignalPFGammaCandsOut;
    Var_NoEleMatch_wGwoGSF_Barrel_[6]  = TauLeadPFChargedHadrHoP;
    Var_NoEleMatch_wGwoGSF_Barrel_[7]  = TauLeadPFChargedHadrEoP;
    Var_NoEleMatch_wGwoGSF_Barrel_[8]  = TauVisMassIn;
    Var_NoEleMatch_wGwoGSF_Barrel_[9]  = TauGammaEtaMomIn;
    Var_NoEleMatch_wGwoGSF_Barrel_[10] = TauGammaEtaMomOut;
    Var_NoEleMatch_wGwoGSF_Barrel_[11] = TauGammaPhiMomIn;
    Var_NoEleMatch_wGwoGSF_Barrel_[12] = TauGammaPhiMomOut;
    Var_NoEleMatch_wGwoGSF_Barrel_[13] = TauGammaEnFracIn;
    Var_NoEleMatch_wGwoGSF_Barrel_[14] = TauGammaEnFracOut;
    Var_NoEleMatch_wGwoGSF_Barrel_[15] = TaudCrackEta;
    Var_NoEleMatch_wGwoGSF_Barrel_[16] = TaudCrackPhi;
    mvaValue = mva_NoEleMatch_wGwoGSF_BL_->GetClassifier(Var_NoEleMatch_wGwoGSF_Barrel_);
  }

  if (TauCategory == 5){
    Var_woGwGSF_Barrel_[0]  = std::max(float(-0.1), ElecEtotOverPin);
    Var_woGwGSF_Barrel_[1]  = std::log(ElecChi2NormGSF);
    Var_woGwGSF_Barrel_[2]  = ElecGSFNumHits;
    Var_woGwGSF_Barrel_[3]  = std::log(ElecGSFTrackResol);
    Var_woGwGSF_Barrel_[4]  = ElecGSFTracklnPt;
    Var_woGwGSF_Barrel_[5]  = ((ElecGSFNumHits - ElecKFNumHits)/(ElecGSFNumHits + ElecKFNumHits));
    Var_woGwGSF_Barrel_[6]  = std::log(ElecChi2NormKF);
    Var_woGwGSF_Barrel_[7]  = std::min(std::abs(ElecPin - ElecPout)/ElecPin, float(1.));
    Var_woGwGSF_Barrel_[8]  = std::min(ElecEecal/ElecPout, float(20.));
    Var_woGwGSF_Barrel_[9]  = ElecDeltaEta;
    Var_woGwGSF_Barrel_[10] = ElecDeltaPhi;
    Var_woGwGSF_Barrel_[11] = std::min(ElecMvaInSigmaEtaEta, float(0.01));
    Var_woGwGSF_Barrel_[12] = std::min(ElecMvaInHadEnergy, float(20.));
    Var_woGwGSF_Barrel_[13] = std::min(ElecMvaInDeltaEta, float(0.1));
    Var_woGwGSF_Barrel_[14] = TauEtaAtEcalEntrance; 
    Var_woGwGSF_Barrel_[15] = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_woGwGSF_Barrel_[16] = std::log(std::max(float(1.), TauPt));
    Var_woGwGSF_Barrel_[17] = TauEmFraction;
    Var_woGwGSF_Barrel_[18] = TauLeadPFChargedHadrHoP;
    Var_woGwGSF_Barrel_[19] = TauLeadPFChargedHadrEoP;
    Var_woGwGSF_Barrel_[20] = TauVisMassIn;
    Var_woGwGSF_Barrel_[21] = TaudCrackEta;
    Var_woGwGSF_Barrel_[22] = TaudCrackPhi;
    mvaValue = mva_woGwGSF_BL_->GetClassifier(Var_woGwGSF_Barrel_);
  }

  if (TauCategory == 7){
    Var_wGwGSF_Barrel_[0]  = std::max(float(-0.1), ElecEtotOverPin);
    Var_wGwGSF_Barrel_[1]  = std::log(ElecChi2NormGSF);
    Var_wGwGSF_Barrel_[2]  = ElecGSFNumHits;
    Var_wGwGSF_Barrel_[3]  = std::log(ElecGSFTrackResol);
    Var_wGwGSF_Barrel_[4]  = ElecGSFTracklnPt;
    Var_wGwGSF_Barrel_[5]  = ((ElecGSFNumHits - ElecKFNumHits)/(ElecGSFNumHits + ElecKFNumHits));
    Var_wGwGSF_Barrel_[6]  = std::log(ElecChi2NormKF);
    Var_wGwGSF_Barrel_[7]  = std::min(std::abs(ElecPin - ElecPout)/ElecPin, float(1.));
    Var_wGwGSF_Barrel_[8]  = std::min(ElecEecal/ElecPout, float(20.));
    Var_wGwGSF_Barrel_[9]  = ElecDeltaEta;
    Var_wGwGSF_Barrel_[10] = ElecDeltaPhi;
    Var_wGwGSF_Barrel_[11] = std::min(ElecMvaInSigmaEtaEta, float(0.01));
    Var_wGwGSF_Barrel_[12] = std::min(ElecMvaInHadEnergy, float(20.));
    Var_wGwGSF_Barrel_[13] = std::min(ElecMvaInDeltaEta, float(0.1));
    Var_wGwGSF_Barrel_[14] = TauEtaAtEcalEntrance;
    Var_wGwGSF_Barrel_[15] = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_wGwGSF_Barrel_[16] = std::log(std::max(float(1.), TauPt));
    Var_wGwGSF_Barrel_[17] = TauEmFraction;
    Var_wGwGSF_Barrel_[18] = TauSignalPFGammaCandsIn;
    Var_wGwGSF_Barrel_[19] = TauSignalPFGammaCandsOut;
    Var_wGwGSF_Barrel_[20] = TauLeadPFChargedHadrHoP;
    Var_wGwGSF_Barrel_[21] = TauLeadPFChargedHadrEoP;
    Var_wGwGSF_Barrel_[22] = TauVisMassIn;
    Var_wGwGSF_Barrel_[23] = TauGammaEtaMomIn;
    Var_wGwGSF_Barrel_[24] = TauGammaEtaMomOut;
    Var_wGwGSF_Barrel_[25] = TauGammaPhiMomIn;
    Var_wGwGSF_Barrel_[26] = TauGammaPhiMomOut;
    Var_wGwGSF_Barrel_[27] = TauGammaEnFracIn;
    Var_wGwGSF_Barrel_[28] = TauGammaEnFracOut;
    Var_wGwGSF_Barrel_[29] = TaudCrackEta;
    Var_wGwGSF_Barrel_[30] = TaudCrackPhi;
    mvaValue = mva_wGwGSF_BL_->GetClassifier(Var_wGwGSF_Barrel_);
  }

  if (TauCategory == 8){
    Var_NoEleMatch_woGwoGSF_Endcap_[0] = TauEtaAtEcalEntrance;
    Var_NoEleMatch_woGwoGSF_Endcap_[1] = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_NoEleMatch_woGwoGSF_Endcap_[2] = std::log(std::max(float(1.), TauPt));
    Var_NoEleMatch_woGwoGSF_Endcap_[3] = TauEmFraction;
    Var_NoEleMatch_woGwoGSF_Endcap_[4] = TauLeadPFChargedHadrHoP;
    Var_NoEleMatch_woGwoGSF_Endcap_[5] = TauLeadPFChargedHadrEoP;
    Var_NoEleMatch_woGwoGSF_Endcap_[6] = TauVisMassIn;
    Var_NoEleMatch_woGwoGSF_Endcap_[7] = TaudCrackEta;
    mvaValue = mva_NoEleMatch_woGwoGSF_EC_->GetClassifier(Var_NoEleMatch_woGwoGSF_Endcap_);
  }

  if (TauCategory == 10){
    Var_NoEleMatch_wGwoGSF_Endcap_[0]  = TauEtaAtEcalEntrance;
    Var_NoEleMatch_wGwoGSF_Endcap_[1]  = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_NoEleMatch_wGwoGSF_Endcap_[2]  = std::log(std::max(float(1.), TauPt));
    Var_NoEleMatch_wGwoGSF_Endcap_[3]  = TauEmFraction;
    Var_NoEleMatch_wGwoGSF_Endcap_[4]  = TauSignalPFGammaCandsIn;
    Var_NoEleMatch_wGwoGSF_Endcap_[5]  = TauSignalPFGammaCandsOut;
    Var_NoEleMatch_wGwoGSF_Endcap_[6]  = TauLeadPFChargedHadrHoP;
    Var_NoEleMatch_wGwoGSF_Endcap_[7]  = TauLeadPFChargedHadrEoP;
    Var_NoEleMatch_wGwoGSF_Endcap_[8]  = TauVisMassIn;
    Var_NoEleMatch_wGwoGSF_Endcap_[9]  = TauGammaEtaMomIn;
    Var_NoEleMatch_wGwoGSF_Endcap_[10] = TauGammaEtaMomOut;
    Var_NoEleMatch_wGwoGSF_Endcap_[11] = TauGammaPhiMomIn;
    Var_NoEleMatch_wGwoGSF_Endcap_[12] = TauGammaPhiMomOut;
    Var_NoEleMatch_wGwoGSF_Endcap_[13] = TauGammaEnFracIn;
    Var_NoEleMatch_wGwoGSF_Endcap_[14] = TauGammaEnFracOut;
    Var_NoEleMatch_wGwoGSF_Endcap_[15] = TaudCrackEta;
    mvaValue = mva_NoEleMatch_wGwoGSF_EC_->GetClassifier(Var_NoEleMatch_wGwoGSF_Endcap_);
  }

  if (TauCategory == 13){
    Var_woGwGSF_Endcap_[0]  = std::max(float(-0.1), ElecEtotOverPin);
    Var_woGwGSF_Endcap_[1]  = std::log(ElecChi2NormGSF);
    Var_woGwGSF_Endcap_[2]  = ElecGSFNumHits;
    Var_woGwGSF_Endcap_[3]  = std::log(ElecGSFTrackResol);
    Var_woGwGSF_Endcap_[4]  = ElecGSFTracklnPt;
    Var_woGwGSF_Endcap_[5]  = ((ElecGSFNumHits - ElecKFNumHits)/(ElecGSFNumHits + ElecKFNumHits));
    Var_woGwGSF_Endcap_[6]  = std::log(ElecChi2NormKF);
    Var_woGwGSF_Endcap_[7]  = std::min(std::abs(ElecPin - ElecPout)/ElecPin, float(1.));
    Var_woGwGSF_Endcap_[8]  = std::min(ElecEecal/ElecPout, float(20.));
    Var_woGwGSF_Endcap_[9]  = ElecDeltaEta;
    Var_woGwGSF_Endcap_[10] = ElecDeltaPhi;
    Var_woGwGSF_Endcap_[11] = std::min(ElecMvaInSigmaEtaEta, float(0.01));
    Var_woGwGSF_Endcap_[12] = std::min(ElecMvaInHadEnergy, float(20.));
    Var_woGwGSF_Endcap_[13] = std::min(ElecMvaInDeltaEta, float(0.1));
    Var_woGwGSF_Endcap_[14] = TauEtaAtEcalEntrance; 
    Var_woGwGSF_Endcap_[15] = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_woGwGSF_Endcap_[16] = std::log(std::max(float(1.), TauPt));
    Var_woGwGSF_Endcap_[17] = TauEmFraction;
    Var_woGwGSF_Endcap_[18] = TauLeadPFChargedHadrHoP;
    Var_woGwGSF_Endcap_[19] = TauLeadPFChargedHadrEoP;
    Var_woGwGSF_Endcap_[20] = TauVisMassIn;
    Var_woGwGSF_Endcap_[21] = TaudCrackEta;
    mvaValue = mva_woGwGSF_EC_->GetClassifier(Var_woGwGSF_Endcap_);
  }

  if (TauCategory == 15){
    Var_wGwGSF_Endcap_[0]  = std::max(float(-0.1), ElecEtotOverPin);
    Var_wGwGSF_Endcap_[1]  = std::log(ElecChi2NormGSF);
    Var_wGwGSF_Endcap_[2]  = ElecGSFNumHits;
    Var_wGwGSF_Endcap_[3]  = std::log(ElecGSFTrackResol);
    Var_wGwGSF_Endcap_[4]  = ElecGSFTracklnPt;
    Var_wGwGSF_Endcap_[5]  = ((ElecGSFNumHits - ElecKFNumHits)/(ElecGSFNumHits + ElecKFNumHits));
    Var_wGwGSF_Endcap_[6]  = std::log(ElecChi2NormKF);
    Var_wGwGSF_Endcap_[7]  = std::min(std::abs(ElecPin - ElecPout)/ElecPin, float(1.));
    Var_wGwGSF_Endcap_[8]  = std::min(ElecEecal/ElecPout, float(20.));
    Var_wGwGSF_Endcap_[9]  = ElecDeltaEta;
    Var_wGwGSF_Endcap_[10] = ElecDeltaPhi;
    Var_wGwGSF_Endcap_[11] = std::min(ElecMvaInSigmaEtaEta, float(0.01));
    Var_wGwGSF_Endcap_[12] = std::min(ElecMvaInHadEnergy, float(20.));
    Var_wGwGSF_Endcap_[13] = std::min(ElecMvaInDeltaEta, float(0.1));
    Var_wGwGSF_Endcap_[14] = TauEtaAtEcalEntrance;
    Var_wGwGSF_Endcap_[15] = std::min(float(2.), TauLeadChargedPFCandPt/std::max(float(1.), TauPt));
    Var_wGwGSF_Endcap_[16] = std::log(std::max(float(1.), TauPt));
    Var_wGwGSF_Endcap_[17] = TauEmFraction;
    Var_wGwGSF_Endcap_[18] = TauSignalPFGammaCandsIn;
    Var_wGwGSF_Endcap_[19] = TauSignalPFGammaCandsOut;
    Var_wGwGSF_Endcap_[20] = TauLeadPFChargedHadrHoP;
    Var_wGwGSF_Endcap_[21] = TauLeadPFChargedHadrEoP;
    Var_wGwGSF_Endcap_[22] = TauVisMassIn;
    Var_wGwGSF_Endcap_[23] = TauGammaEtaMomIn;
    Var_wGwGSF_Endcap_[24] = TauGammaEtaMomOut;
    Var_wGwGSF_Endcap_[25] = TauGammaPhiMomIn;
    Var_wGwGSF_Endcap_[26] = TauGammaPhiMomOut;
    Var_wGwGSF_Endcap_[27] = TauGammaEnFracIn;
    Var_wGwGSF_Endcap_[28] = TauGammaEnFracOut;
    Var_wGwGSF_Endcap_[29] = TaudCrackEta;
    mvaValue = mva_wGwGSF_EC_->GetClassifier(Var_wGwGSF_Endcap_);
  }

  return mvaValue;
}

