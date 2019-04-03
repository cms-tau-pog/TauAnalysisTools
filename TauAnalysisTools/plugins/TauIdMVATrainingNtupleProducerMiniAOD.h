#ifndef TauAnalysisTools_TauAnalysisTools_TauIdMVATrainingNtupleProducerMiniAOD_h
#define TauAnalysisTools_TauAnalysisTools_TauIdMVATrainingNtupleProducerMiniAOD_h

/*
 * \class TauIdMVATrainingNtupleProducerMiniAOD
 *
 * Produce an nTuple containing input variables
 * from MiniAOD for training tau isolation MVA
 *
 * Modified copy of TauIdMVATrainingNtupleProducer
 *
 * \author Alexander Nehrkorn, RWTH Aachen University
 */

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"

#include "RecoBTag/BTagTools/interface/SignedTransverseImpactParameter.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

// #include "TMVA.h"
// #include "TMVA/DataLoader.h"
// #include "TMVA/MethodBase.h"
// #include "TMVA/Tools.h"
// #include "TMVA/Reader.h"

#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
using namespace TMVA;

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include <TTree.h>
#include <TMatrixD.h>
#include <TString.h>

#include <map>
#include <string>
#include <vector>
#include <ostream>

// #TauAnalysisTools/TauAnalysisTools
//needed for import of IClassifierReader
#include "TauAnalysisTools/TauAnalysisTools/data/dataset_oldDM_tauId_dR05_old_v2/weights/mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_BDTG.class.C"
// #ifndef IClassifierReader__def
// #define IClassifierReader__def

// class IClassifierReader {

//  public:

//    // constructor
//    IClassifierReader() : fStatusIsClean( true ) {}
//    virtual ~IClassifierReader() {}

//    // return classifier response
//    virtual double GetMvaValue( const std::vector<double>& inputValues ) const = 0;

//    // returns classifier status
//    bool IsStatusClean() const { return fStatusIsClean; }

//  protected:

//    bool fStatusIsClean;
// };

// #endif


class TauIdMVATrainingNtupleProducerMiniAOD : public edm::EDProducer
{
public:

	TauIdMVATrainingNtupleProducerMiniAOD(const edm::ParameterSet&);
	~TauIdMVATrainingNtupleProducerMiniAOD();

	void produce(edm::Event&, const edm::EventSetup&);
	void beginJob();

private:

	void setRecTauValues(const pat::TauRef&, const pat::JetRef&, const edm::Event&, const edm::EventSetup&);
	void setGenTauMatchValues(const reco::Candidate::LorentzVector&, const reco::GenParticle*, const reco::Candidate::LorentzVector&, int);
	void setGenTauMatchValues(const reco::Candidate::LorentzVector&, const pat::PackedGenParticle*, const reco::Candidate::LorentzVector&, int);
	void setGenParticleMatchValues(const std::string&, const reco::Candidate::LorentzVector&, const reco::GenParticle*);
	void setGenParticleMatchValues(const std::string&, const reco::Candidate::LorentzVector&, const pat::PackedGenParticle*);
	void setNumPileUpValue(const edm::Event&);

	void addBranchF(const std::string&);
	void addBranchI(const std::string&);
	void addBranchVF(const std::string&);

	void addBranch_EnPxPyPz(const std::string&);
	void addBranch_XYZ(const std::string&);
	void addBranch_Cov(const std::string&);
	void addBranch_chargedHadron(const std::string&);
	void addBranch_piZero(const std::string&);

	void printBranches(std::ostream&);

	void setValueF(const std::string&, double);
	void setValueI(const std::string&, int);
	void setValueVF(const std::string&, const std::vector<Float_t>&);
	void tempSetValueVF(const std::string&, const std::vector<Float_t>&);

	void setValue_EnPxPyPz(const std::string&, const reco::Candidate::LorentzVector&);
	template <typename T>
	void setValue_XYZ(const std::string&, const T&);
	void setValue_Cov(const std::string&, const pat::tau::TauPFEssential::CovMatrix&);
	void setValue_chargedHadron(const std::string&, const reco::CandidatePtr);
	void setValue_piZero(const std::string&, const reco::CandidatePtrVector);
	void maxLike(const pat::Tau&);
	std::string moduleLabel_;

	edm::InputTag srcRecTaus_;
	edm::EDGetTokenT<pat::TauCollection> tokenRecTaus_;

	edm::InputTag srcPrunedGenParticles_;
	edm::EDGetTokenT<reco::GenParticleCollection> tokenPrunedGenParticles_;
	edm::InputTag srcPackedGenParticles_;
	edm::EDGetTokenT<pat::PackedGenParticleCollection> tokenPackedGenParticles_;

	edm::InputTag srcRecJets_;
	edm::EDGetTokenT<pat::JetCollection> tokenRecJets_;

	double minGenVisPt_;
	double dRmatch_;

	unsigned maxChargedHadrons_;
	unsigned maxPiZeros_;

	struct tauIdDiscrEntryType
	{
		tauIdDiscrEntryType(const std::string& name, const std::string& src)
		{
			src_ = src;
			branchName_ = name;
		}
		~tauIdDiscrEntryType() {}
		std::string src_;
		std::string branchName_;
	};
	std::vector<tauIdDiscrEntryType> tauIdDiscrEntries_;

	struct tauIsolationEntryType
	{
		tauIsolationEntryType(const std::string& name, const std::string& src)
		{
		      /*branchNameChargedIsoPtSum_ = name.data();//Form("%sChargedIsoPtSum", name.data());
		      branchNameNeutralIsoPtSum_ = name.data();//Form("%sNeutralIsoPtSum", name.data());
		      branchNamePUcorrPtSum_     = name.data();//Form("%sPUcorrPtSum", name.data());
		      branchNameNeutralIsoPtSumWeight_ = name.data();//Form("%sNeutralIsoPtSumWeight", name.data());
		      branchNameFootprintCorrection_   = name.data();//Form("%sFootprintCorrection", name.data());
		      branchNamePhotonPtSumOutsideSignalCone_ = name.data();//Form("%sPhotonPtSumOutsideSignalCone", name.data());*/
			src_ = src;
			branchName_ = name;
		}
		~tauIsolationEntryType() {}
		/*std::string branchNameChargedIsoPtSum_;
		std::string branchNameNeutralIsoPtSum_;
		std::string branchNamePUcorrPtSum_;
		std::string branchNameNeutralIsoPtSumWeight_;
		std::string branchNameFootprintCorrection_;
		std::string branchNamePhotonPtSumOutsideSignalCone_;*/
		std::string src_;
		std::string branchName_;
	};
	std::vector<tauIsolationEntryType> tauIsolationEntries_;

	struct vertexCollectionEntryType
	{
		vertexCollectionEntryType(const std::string& name, const edm::EDGetTokenT<reco::VertexCollection>& token)
		{
			token_ = token;
			assert(name.length() > 0);
			std::string name_capitalized = name;
			name_capitalized[0] = toupper(name_capitalized[0]);
			branchName_multiplicity_ = Form("num%s", name_capitalized.data());
			branchName_position_ = TString(name.data()).ReplaceAll("Vertices", "Vertex").Data();
		}
		~vertexCollectionEntryType() {}
		edm::EDGetTokenT<reco::VertexCollection> token_;
		std::string branchName_multiplicity_;
		std::string branchName_position_;
	};
	std::vector<vertexCollectionEntryType> vertexCollectionEntries_;

	edm::EDGetTokenT<reco::VertexCollection> vertexToken_;

	std::vector<int> pdgIdsGenTau_;
	std::vector<int> pdgIdsGenElectron_;
	std::vector<int> pdgIdsGenMuon_;
	std::vector<int> pdgIdsGenQuarkOrGluon_;

	PFJetIDSelectionFunctor* loosePFJetIdAlgo_;

	bool isMC_;
	bool isSignal_;
	bool includeMaxLikeVar_;
	double dRClean_;
	double ptCleanMin_;
	bool matchGenTauVis_;
	edm::InputTag srcGenPileUpSummary_;
	edm::EDGetTokenT<std::vector<PileupSummaryInfo> > tokenGenPileupSummary_;
	//std::map<edm::RunNumber_t, std::map<edm::LuminosityBlockNumber_t, float> > pileUpByLumiCalc_; // key = run, lumi-section
	//std::map<edm::RunNumber_t, std::map<edm::LuminosityBlockNumber_t, int> > numWarnings_;
	int maxWarnings_;

	typedef std::vector<edm::InputTag> vInputTag;
	vInputTag srcWeights_;

	edm::EDGetTokenT<GenEventInfoProduct> tokenGenInfoProduct_;

	std::vector<std::string> ptMin_allPhotonsVariables;
	std::vector<std::string> ptMin_nPhotons_;
	std::vector<std::string> ptMin_photonPtSumOutsideSignalCone;
	std::vector<std::string> ptMin_photonPtSumOutsideSignalConedRgt0p1;

	std::string tmvaMacro;
	std::string tmvaMacroBranch;
	std::vector<std::string> tmvaMacroVariables;
	std::vector<std::string> inputVars;
	std::vector<double> inputVec;
	IClassifierReader* loadedResponse;

	struct branchEntryType {

		branchEntryType(): valueF_(0.), valueI_(0.), valueVFloat_(std::vector<Float_t>()), pvalueVFloat_(0) {}

		~branchEntryType() {}

		Float_t valueF_;
		Int_t valueI_;
		std::vector<Float_t> valueVFloat_;
		std::vector<Float_t> * pvalueVFloat_;
	};

	typedef std::map<std::string, branchEntryType> branchMap; // key = branch name
	branchMap branches_;

	TTree* ntuple_;

	int verbosity_;

	SignedTransverseImpactParameter* STIP;

};

#endif
