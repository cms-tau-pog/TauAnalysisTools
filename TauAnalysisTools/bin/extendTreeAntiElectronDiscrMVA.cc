
/** \executable extendTreeAntiElectronDiscrMVA
 *
 * Add a few extra branches to TTree used for training MVA to discriminate hadronic tau decays from electrons.
 *
 * \author Christian Veelken, LLR
 *
 * \version $Revision: 1.1 $
 *
 * $Id: extendTreeAntiElectronDiscrMVA.cc,v 1.1 2012/03/06 17:34:42 veelken Exp $
 *
 */

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

#include "FWCore/Utilities/interface/Exception.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"
#include "DataFormats/FWLite/interface/InputSource.h"
#include "DataFormats/FWLite/interface/OutputFiles.h"

#include "TauAnalysisTools/TauAnalysisTools/interface/AntiElectronIDMVA.h"

#include <TFile.h>
#include <TChain.h>
#include <TTree.h>
#include <TTreeFormula.h>
#include <TObjArray.h>
#include <TBranch.h>
#include <TString.h>
#include <TMath.h>
#include <TBenchmark.h>

#include <iostream>
#include <string>
#include <vector>
#include <assert.h>

bool isInEcalCrack(Float_t eta) 
{
  Float_t absEta = fabs(eta);
  return ( absEta > 1.460 && absEta < 1.558 );
}

// IN: define useful auxiliary function to compute the signed distance to the closest crack 
double minimum(double a, double b) {
  if (TMath::Abs(b) < TMath::Abs(a) ) return b;
  else return a;
}

double dCrackPhi(double phi, double eta)
{
//--- compute the (unsigned) distance to the closest phi-crack in the ECAL barrel  

  double pi = TMath::Pi(); // 3.14159265358979323846;
  
  // IN: define locations of the 18 phi-cracks
  static std::vector<double> cPhi;
  if ( cPhi.size() == 0 ) {
    cPhi.resize(18, 0);
    cPhi[0] = 2.97025;
    for ( unsigned iCrack = 1; iCrack <= 17; ++iCrack ) {
      cPhi[iCrack] = cPhi[0] - 2.*iCrack*pi/18;
    }
  }

  // IN: shift of this location if eta < 0
  double delta_cPhi = 0.00638;

  double retVal = 99.; 

  if ( eta >= -1.47464 && eta <= 1.47464 ) {

    // the location is shifted
    if ( eta < 0. ) phi += delta_cPhi;

    // CV: need to bring-back phi into interval [-pi,+pi]
    if ( phi >  pi ) phi -= 2.*pi;
    if ( phi < -pi ) phi += 2.*pi;

    if ( phi >= -pi && phi <= pi ) {

      // the problem of the extrema:
      if ( phi < cPhi[17] || phi >= cPhi[0] ) {
	if ( phi < 0. ) phi += 2.*pi;
	retVal = minimum(phi - cPhi[0], phi - cPhi[17] - 2.*pi);        	
      } else {
	// between these extrema...
	bool OK = false;
	unsigned iCrack = 16;
	while( !OK ) {
	  if ( phi < cPhi[iCrack] ) {
	    retVal = minimum(phi - cPhi[iCrack + 1], phi - cPhi[iCrack]);
	    OK = true;
	  } else {
	    iCrack -= 1;
	  }
	}
      }
    } else {
      retVal = 0.; // IN: if there is a problem, we assume that we are in a crack
    }
  } else {
    return -99.;       
  }
  
  return TMath::Abs(retVal);
}

double dCrackEta(double eta)
{
//--- compute the (unsigned) distance to the closest eta-crack in the ECAL barrel
  
  // IN: define locations of the eta-cracks
  double cracks[5] = { 0., 4.44747e-01, 7.92824e-01, 1.14090e+00, 1.47464e+00 };
  
  double retVal = 99.;
  
  for ( int iCrack = 0; iCrack < 5 ; ++iCrack ) {
    double d = minimum(eta - cracks[iCrack], eta + cracks[iCrack]);
    if ( TMath::Abs(d) < TMath::Abs(retVal) ) {
      retVal = d;
    }
  }

  return TMath::Abs(retVal);
}

struct branchEntryType
{
   branchEntryType()
     : inputValueF_(0.),
       inputValueI_(0),
       inputValueL_(0),
       outputValueF_(0.),
       outputValueI_(0),
       outputValueL_(0)
  {}
  ~branchEntryType() {}
  void copyInputToOutput()
  {
    outputValueF_ = inputValueF_;
    outputValueI_ = inputValueI_;
    outputValueL_ = inputValueL_;
  }
  std::string branchName_;
  enum { kInt_t, kFloat_t, kULong64_t };
  int branchType_;
  Float_t inputValueF_;
  Int_t inputValueI_;
  ULong64_t inputValueL_;
  Float_t outputValueF_;
  Int_t outputValueI_;
  ULong64_t outputValueL_;
};

struct categoryEntryType
{
  categoryEntryType()
    : selection_(0),
      idx_(-1)
  {}
  ~categoryEntryType() { delete selection_; }
  std::string name_;
  TTreeFormula* selection_;
  int idx_;
};

typedef std::vector<std::string> vstring;

int main(int argc, char* argv[]) 
{
//--- parse command-line arguments
  if ( argc < 2 ) {
    std::cout << "Usage: " << argv[0] << " [parameters.py]" << std::endl;
    return 0;
  }

  std::cout << "<extendTreeAntiElectronDiscrMVA>:" << std::endl;

//--- keep track of time it takes the macro to execute
  TBenchmark clock;
  clock.Start("extendTreeAntiElectronDiscrMVA");

//--- read python configuration parameters
  if ( !edm::readPSetsFrom(argv[1])->existsAs<edm::ParameterSet>("process") ) 
    throw cms::Exception("extendTreeAntiElectronDiscrMVA") 
      << "No ParameterSet 'process' found in configuration file = " << argv[1] << " !!\n";

  edm::ParameterSet cfg = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("process");

  edm::ParameterSet cfgExtendTreeAntiElectronDiscrMVA = cfg.getParameter<edm::ParameterSet>("extendTreeAntiElectronDiscrMVA");
  
  std::string inputTreeName = cfgExtendTreeAntiElectronDiscrMVA.getParameter<std::string>("inputTreeName");
  std::string outputTreeName = cfgExtendTreeAntiElectronDiscrMVA.getParameter<std::string>("outputTreeName");

  vstring samples = cfgExtendTreeAntiElectronDiscrMVA.getParameter<vstring>("samples");

  fwlite::InputSource inputFiles(cfg); 
  int maxEvents = inputFiles.maxEvents();
  std::cout << " maxEvents = " << maxEvents << std::endl;
  unsigned reportEvery = inputFiles.reportAfter();

  std::string outputFileName = cfgExtendTreeAntiElectronDiscrMVA.getParameter<std::string>("outputFileName");
  std::cout << " outputFileName = " << outputFileName << std::endl;

  TChain* inputTree = new TChain(inputTreeName.data());
  for ( vstring::const_iterator inputFileName = inputFiles.files().begin();
	inputFileName != inputFiles.files().end(); ++inputFileName ) {
    bool matchesSample = false;
    for ( vstring::const_iterator sample = samples.begin();
	  sample != samples.end(); ++sample ) {
      if ( inputFileName->find(*sample) != std::string::npos ) matchesSample = true;
    }
    if ( matchesSample ) {
      std::cout << "input Tree: adding file = " << (*inputFileName) << std::endl;
      inputTree->AddFile(inputFileName->data());
    } 
  }
  
  if ( !(inputTree->GetListOfFiles()->GetEntries() >= 1) ) {
    throw cms::Exception("extendTreeAntiElectronDiscrMVA") 
      << "Failed to identify input Tree !!\n";
  }

  std::vector<branchEntryType*> branches_to_copy;
  branchEntryType* branch_Tau_EtaAtEcalEntrance = 0;
  branchEntryType* branch_Tau_PhiAtEcalEntrance = 0;
  branchEntryType* branch_Tau_Pt = 0;
  branchEntryType* branch_Tau_LeadChargedPFCandPt = 0;
  branchEntryType* branch_Tau_EmFraction = 0;
  branchEntryType* branch_Tau_HadrHoP = 0;
  branchEntryType* branch_Tau_HadrEoP = 0;
  branchEntryType* branch_Tau_VisMass = 0;
  branchEntryType* branch_Tau_NumGammaCands = 0;
  branchEntryType* branch_Tau_GammaEtaMom = 0;
  branchEntryType* branch_Tau_GammaPhiMom = 0;
  branchEntryType* branch_Tau_GammaEnFrac = 0;
  branchEntryType* branch_Elec_EtotOverPin = 0;
  branchEntryType* branch_Elec_Chi2NormGSF = 0;
  branchEntryType* branch_Elec_Chi2NormKF = 0;
  branchEntryType* branch_Elec_GSFNumHits = 0;
  branchEntryType* branch_Elec_KFNumHits = 0;
  branchEntryType* branch_Elec_GSFTrackResol = 0;
  branchEntryType* branch_Elec_GSFTracklnPt = 0;
  branchEntryType* branch_Elec_Pin = 0;
  branchEntryType* branch_Elec_Pout = 0;
  branchEntryType* branch_Elec_Eecal = 0;
  branchEntryType* branch_Elec_DeltaEta = 0;
  branchEntryType* branch_Elec_DeltaPhi = 0;
  branchEntryType* branch_Elec_MvaInSigmaEtaEta = 0;
  branchEntryType* branch_Elec_MvaInHadEnergy = 0;
  branchEntryType* branch_Elec_MvaInDeltaEta = 0;

  TObjArray* branches = inputTree->GetListOfBranches();
  int numBranches = branches->GetEntries();
  for ( int iBranch = 0; iBranch < numBranches; ++iBranch ) {
    TBranch* branch = dynamic_cast<TBranch*>(branches->At(iBranch));
    assert(branch);
    std::string branchName = branch->GetName();
    std::string branchType_string = TString(branch->GetTitle()).ReplaceAll(Form("%s/", branchName.data()), "").Data();
    //std::cout << "branch #" << iBranch << ": name = " << branchName << ", type = " << branchType_string << std::endl;
    int branchType = -1;
    if      ( branchType_string == "I" ) branchType = branchEntryType::kInt_t;
    else if ( branchType_string == "F" ) branchType = branchEntryType::kFloat_t;
    else if ( branchType_string == "l" ) branchType = branchEntryType::kULong64_t;
    else {
      std::cerr << "<extendTreeAntiElectronDiscrMVA>:" << std::endl;
      std::cerr << " Branch type = " << branchType_string << " not supported --> Branch = " << branchName << " will NOT be copied to outputTree !!" << std::endl;
      continue;
    }
    branchEntryType* branch_to_copy = new branchEntryType();
    branch_to_copy->branchName_ = branchName;
    branch_to_copy->branchType_ = branchType;
    branches_to_copy.push_back(branch_to_copy);
    if ( branchName == "Tau_EtaAtEcalEntrance" )   branch_Tau_EtaAtEcalEntrance   = branch_to_copy;
    if ( branchName == "Tau_PhiAtEcalEntrance" )   branch_Tau_PhiAtEcalEntrance   = branch_to_copy;
    if ( branchName == "Tau_Pt" )                  branch_Tau_Pt                  = branch_to_copy;
    if ( branchName == "Tau_LeadChargedPFCandPt" ) branch_Tau_LeadChargedPFCandPt = branch_to_copy;
    if ( branchName == "Tau_EmFraction" )          branch_Tau_EmFraction          = branch_to_copy;
    if ( branchName == "Tau_HadrHoP" )             branch_Tau_HadrHoP             = branch_to_copy;
    if ( branchName == "Tau_HadrEoP" )             branch_Tau_HadrEoP             = branch_to_copy;
    if ( branchName == "Tau_VisMass" )             branch_Tau_VisMass             = branch_to_copy;
    if ( branchName == "Tau_NumGammaCands" )       branch_Tau_NumGammaCands       = branch_to_copy;
    if ( branchName == "Tau_GammaEtaMom" )         branch_Tau_GammaEtaMom         = branch_to_copy;
    if ( branchName == "Tau_GammaPhiMom" )         branch_Tau_GammaPhiMom         = branch_to_copy;
    if ( branchName == "Tau_GammaEnFrac" )         branch_Tau_GammaEnFrac         = branch_to_copy;
    if ( branchName == "Elec_EtotOverPin" )        branch_Elec_EtotOverPin        = branch_to_copy;
    if ( branchName == "Elec_Chi2NormGSF" )        branch_Elec_Chi2NormGSF        = branch_to_copy;
    if ( branchName == "Elec_Chi2NormKF" )         branch_Elec_Chi2NormKF         = branch_to_copy;
    if ( branchName == "Elec_GSFNumHits" )         branch_Elec_GSFNumHits         = branch_to_copy;
    if ( branchName == "Elec_KFNumHits" )          branch_Elec_KFNumHits          = branch_to_copy;
    if ( branchName == "Elec_GSFTrackResol" )      branch_Elec_GSFTrackResol      = branch_to_copy;
    if ( branchName == "Elec_GSFTracklnPt" )       branch_Elec_GSFTracklnPt       = branch_to_copy;
    if ( branchName == "Elec_Pin" )                branch_Elec_Pin                = branch_to_copy;
    if ( branchName == "Elec_Pout" )               branch_Elec_Pout               = branch_to_copy;
    if ( branchName == "Elec_Eecal" )              branch_Elec_Eecal              = branch_to_copy;
    if ( branchName == "Elec_DeltaEta" )           branch_Elec_DeltaEta           = branch_to_copy;
    if ( branchName == "Elec_DeltaPhi" )           branch_Elec_DeltaPhi           = branch_to_copy;
    if ( branchName == "Elec_MvaInSigmaEtaEta" )   branch_Elec_MvaInSigmaEtaEta   = branch_to_copy;
    if ( branchName == "Elec_MvaInHadEnergy" )     branch_Elec_MvaInHadEnergy     = branch_to_copy;
    if ( branchName == "Elec_MvaInDeltaEta" )      branch_Elec_MvaInDeltaEta      = branch_to_copy;
  }
  if ( !(branch_Tau_EtaAtEcalEntrance && branch_Tau_PhiAtEcalEntrance) ) 
    throw cms::Exception("extendTreeAntiElectronDiscrMVA") 
      << "Failed to find Branches 'Tau_EtaAtEcalEntrance' and 'Tau_PhiAtEcalEntrance' in input Tree !!\n";

  for ( std::vector<branchEntryType*>::iterator branch = branches_to_copy.begin();
	branch != branches_to_copy.end(); ++branch ) {
    if ( (*branch)->branchType_ == branchEntryType::kInt_t ) {
      inputTree->SetBranchAddress((*branch)->branchName_.data(), &(*branch)->inputValueI_);
    } else if ( (*branch)->branchType_ == branchEntryType::kULong64_t ) {
      inputTree->SetBranchAddress((*branch)->branchName_.data(), &(*branch)->inputValueL_);
    } else if ( (*branch)->branchType_ == branchEntryType::kFloat_t ) {
      inputTree->SetBranchAddress((*branch)->branchName_.data(), &(*branch)->inputValueF_);
    } else assert(0);
  }

  std::vector<categoryEntryType*> categories;

  edm::ParameterSet cfgCategories = cfgExtendTreeAntiElectronDiscrMVA.getParameter<edm::ParameterSet>("categories");
  vstring categoryNames = cfgCategories.getParameterNamesForType<edm::ParameterSet>();
  for ( vstring::const_iterator categoryName = categoryNames.begin();
	categoryName != categoryNames.end(); ++categoryName ) {
    edm::ParameterSet cfgCategory = cfgCategories.getParameter<edm::ParameterSet>(*categoryName);
    std::string selection = cfgCategory.getParameter<std::string>("selection");
    int idx = cfgCategory.getParameter<int>("idx");
    if ( !(idx >= 0) )
      throw cms::Exception("extendTreeAntiElectronDiscrMVA") 
	<< "Invalid Configuration Parameter 'idx' = " << idx << " defined for category = " << (*categoryName) << " !!\n";
    categoryEntryType* category = new categoryEntryType();
    category->name_ = (*categoryName);
    std::string selectionName = Form("selectionCategory%i", idx);
    category->selection_ = new TTreeFormula(selectionName.data(), selection.data(), inputTree);
    category->idx_ = idx;
    categories.push_back(category);
  }

  edm::ParameterSet cfgMva = cfgExtendTreeAntiElectronDiscrMVA.getParameter<edm::ParameterSet>("mva");
  AntiElectronIDMVA* mva = new AntiElectronIDMVA(cfgMva);

  // CV: need to call TChain::LoadTree before processing first event 
  //     in order to prevent ROOT causing a segmentation violation,
  //     cf. http://root.cern.ch/phpBB3/viewtopic.php?t=10062
  inputTree->LoadTree(0);

  std::cout << "input Tree contains " << inputTree->GetEntries() << " Entries in " << inputTree->GetListOfFiles()->GetEntries() << " files." << std::endl;

  TFile* outputFile = new TFile(outputFileName.data(), "RECREATE");
  TTree* outputTree = new TTree(outputTreeName.data(), outputTreeName.data());

  for ( std::vector<branchEntryType*>::iterator branch = branches_to_copy.begin();
	branch != branches_to_copy.end(); ++branch ) {
    if ( (*branch)->branchType_ == branchEntryType::kInt_t ) {
      outputTree->Branch((*branch)->branchName_.data(), &(*branch)->outputValueI_, Form("%s/I", (*branch)->branchName_.data()));
    } else if ( (*branch)->branchType_ == branchEntryType::kULong64_t ) {
      outputTree->Branch((*branch)->branchName_.data(), &(*branch)->outputValueL_, Form("%s/l", (*branch)->branchName_.data()));
    } else if ( (*branch)->branchType_ == branchEntryType::kFloat_t ) {
      outputTree->Branch((*branch)->branchName_.data(), &(*branch)->outputValueF_, Form("%s/F", (*branch)->branchName_.data()));    
    } else assert(0);
  }

  Int_t value_Tau_isInEcalCrack;
  outputTree->Branch("Tau_isInEcalCrack", &value_Tau_isInEcalCrack, "Tau_isInEcalCrack/I");
  Float_t value_Tau_dCrackEta;
  outputTree->Branch("Tau_dCrackEta", &value_Tau_dCrackEta, "Tau_dCrackEta/F");
  Float_t value_Tau_dCrackPhi;
  outputTree->Branch("Tau_dCrackPhi", &value_Tau_dCrackPhi, "Tau_dCrackPhi/F");
  
  Int_t value_Tau_Category;
  outputTree->Branch("Tau_Category", &value_Tau_Category, "Tau_Category/I");
  Float_t value_mva;
  outputTree->Branch("mva", &value_mva, "mva/F");

  int currentTreeNumber = inputTree->GetTreeNumber();

  int numEntries = inputTree->GetEntries();
  for ( int iEntry = 0; iEntry < numEntries && (maxEvents == -1 || iEntry < maxEvents); ++iEntry ) {
    if ( iEntry > 0 && (iEntry % reportEvery) == 0 ) {
      std::cout << "processing Entry " << iEntry << std::endl;
    }
    
    inputTree->GetEntry(iEntry);

    for ( std::vector<branchEntryType*>::iterator branch = branches_to_copy.begin();
	  branch != branches_to_copy.end(); ++branch ) {
      (*branch)->copyInputToOutput();
    }

    value_Tau_isInEcalCrack = isInEcalCrack(branch_Tau_EtaAtEcalEntrance->inputValueF_);
    value_Tau_dCrackEta = dCrackEta(branch_Tau_EtaAtEcalEntrance->inputValueF_);
    value_Tau_dCrackPhi = dCrackPhi(branch_Tau_PhiAtEcalEntrance->inputValueF_, branch_Tau_EtaAtEcalEntrance->inputValueF_);

    // CV: need to call TTreeFormula::UpdateFormulaLeaves whenever input files changes in TChain
    //     in order to prevent ROOT causing a segmentation violation,
    //     cf. http://root.cern.ch/phpBB3/viewtopic.php?t=481
    if ( inputTree->GetTreeNumber() != currentTreeNumber ) {
      for ( std::vector<categoryEntryType*>::iterator category = categories.begin();
	    category != categories.end(); ++category ) {
	(*category)->selection_->UpdateFormulaLeaves();
      }
      currentTreeNumber = inputTree->GetTreeNumber();
    }
    
    value_Tau_Category = 0;
    int category_idx = -1;
    int numCategories_passed = 0;
    for ( std::vector<categoryEntryType*>::iterator category = categories.begin();
	  category != categories.end(); ++category ) {
      if ( (*category)->selection_->EvalInstance() > 0.5 ) {
	//std::cout << "Entry #" << iEntry << " passes selection for category = " << (*category)->name_ << " (idx = " << (*category)->idx_ << ")" << std::endl;
	value_Tau_Category += (1 << (*category)->idx_);
	category_idx = (*category)->idx_;
	++numCategories_passed;
      }
    }
    if ( numCategories_passed != 1 ) {
      std::cerr << "Entry #" << iEntry << " passes selection for " << numCategories_passed << " categories --> CHECK !!" << std::endl;
    }
    //std::cout << "--> value_Tau_Category = " << value_Tau_Category << std::endl;

    value_mva = -99.;
    if ( mva->isInitialized() ) {

      value_mva = mva->MVAValue(category_idx,
                                branch_Tau_Pt->inputValueF_,
                                branch_Tau_EtaAtEcalEntrance->inputValueF_,
                                branch_Tau_LeadChargedPFCandPt->inputValueF_,
                                branch_Tau_EmFraction->inputValueF_,
                                branch_Tau_HadrHoP->inputValueF_,
                                branch_Tau_HadrEoP->inputValueF_,
                                branch_Tau_VisMass->inputValueF_,
                                value_Tau_dCrackEta,
                                value_Tau_dCrackPhi,
                                branch_Tau_NumGammaCands->inputValueI_,
                                branch_Tau_GammaEtaMom->inputValueF_,
                                branch_Tau_GammaPhiMom->inputValueF_,
                                branch_Tau_GammaEnFrac->inputValueF_,
                                branch_Elec_EtotOverPin->inputValueF_,
                                branch_Elec_Chi2NormGSF->inputValueF_,
                                branch_Elec_Chi2NormKF->inputValueF_,
                                branch_Elec_GSFNumHits->inputValueI_,
                                branch_Elec_KFNumHits->inputValueI_,
                                branch_Elec_GSFTrackResol->inputValueF_,
                                branch_Elec_GSFTracklnPt->inputValueF_,
                                branch_Elec_Pin->inputValueF_,
                                branch_Elec_Pout->inputValueF_,
                                branch_Elec_Eecal->inputValueF_,
                                branch_Elec_DeltaEta->inputValueF_,
                                branch_Elec_DeltaPhi->inputValueF_,
                                branch_Elec_MvaInSigmaEtaEta->inputValueF_,
                                branch_Elec_MvaInHadEnergy->inputValueF_,
                                branch_Elec_MvaInDeltaEta->inputValueF_
                               );
    }

    outputTree->Fill();
  }

  std::cout << "--> " << outputTree->GetEntries() << " Entries processed." << std::endl;

  std::cout << "output Tree:" << std::endl;
  //outputTree->Print();
  //outputTree->Scan("*", "", "", 20, 0);

  std::cout << "writing output Tree to file = " << outputFileName << "." << std::endl;
  outputFile->cd();
  outputTree->Write();

  delete outputFile;

  delete inputTree;
  
  for ( std::vector<branchEntryType*>::iterator it = branches_to_copy.begin();
	it != branches_to_copy.end(); ++it ) {
    delete (*it);
  }
  for ( std::vector<categoryEntryType*>::iterator it = categories.begin();
	it != categories.end(); ++it ) {
    delete (*it);
  }

  clock.Show("extendTreeAntiElectronDiscrMVA");

  return 0;
}
