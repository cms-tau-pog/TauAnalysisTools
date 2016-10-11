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

#include <TTree.h>
#include <TMatrixD.h>
#include <TString.h>

#include <map>
#include <string>
#include <vector>
#include <ostream>

class TauIdMVATrainingNtupleProducerMiniAOD : public edm::EDProducer
{
public:

	TauIdMVATrainingNtupleProducerMiniAOD(const edm::ParameterSet&);
	~TauIdMVATrainingNtupleProducerMiniAOD();

	void produce(edm::Event&, const edm::EventSetup&);
	void beginJob();

private:

	// TODO: check which functions are actually necessary when using PAT objects

	void setRecTauValues(const pat::TauRef&, const edm::Event&, const edm::EventSetup&);
	void setGenTauMatchValues(const reco::Candidate::LorentzVector&, const pat::PackedGenParticle*, const reco::Candidate::LorentzVector&, int);
	void setGenParticleMatchValues(const std::string&, const reco::Candidate::LorentzVector&, const pat::PackedGenParticle*);
	void setNumPileUpValue(const edm::Event&);

	void addBranchF(const std::string&);
	void addBranchI(const std::string&);

	void addBranch_EnPxPyPz(const std::string&);
	void addBranch_XYZ(const std::string&);
	void addBranch_Cov(const std::string&);
	void addBranch_chargedHadron(const std::string&);
	void addBranch_piZero(const std::string&);

	void printBranches(std::ostream&);

	void setValueF(const std::string&, double);
	void setValueI(const std::string&, int);

	void setValue_EnPxPyPz(const std::string&, const reco::Candidate::LorentzVector&);
	template <typename T>
	void setValue_XYZ(const std::string&, const T&);
	void setValue_Cov(const std::string&, const pat::tau::TauPFEssential::CovMatrix&);
	void setValue_chargedHadron(const std::string&, const reco::CandidatePtr);
	void setValue_piZero(const std::string&, const reco::CandidatePtrVector);

	std::string moduleLabel_;

	edm::InputTag srcRecTaus_;
	edm::EDGetTokenT<pat::TauCollection> tokenRecTaus_;

	edm::InputTag srcGenParticles_;
	edm::EDGetTokenT<pat::PackedGenParticleCollection> tokenGenParticles_;

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
		tauIsolationEntryType(const std::string& name)
		{
		      branchNameChargedIsoPtSum_ = Form("%sChargedIsoPtSum", name.data());
		      branchNameNeutralIsoPtSum_ = Form("%sNeutralIsoPtSum", name.data());
		      branchNamePUcorrPtSum_     = Form("%sPUcorrPtSum", name.data());
		      branchNameNeutralIsoPtSumWeight_ = Form("%sNeutralIsoPtSumWeight", name.data());
		      branchNameFootprintCorrection_   = Form("%sFootprintCorrection", name.data());
		      branchNamePhotonPtSumOutsideSignalCone_ = Form("%sPhotonPtSumOutsideSignalCone", name.data());
		}
		~tauIsolationEntryType() {}
		std::string branchNameChargedIsoPtSum_;
		std::string branchNameNeutralIsoPtSum_;
		std::string branchNamePUcorrPtSum_;
		std::string branchNameNeutralIsoPtSumWeight_;
		std::string branchNameFootprintCorrection_;
		std::string branchNamePhotonPtSumOutsideSignalCone_;
	};
	std::vector<tauIsolationEntryType> tauIsolationEntries_;

	struct vertexCollectionEntryType
	{
		vertexCollectionEntryType(const std::string& name, const edm::InputTag& src)
		: src_(src)
		{
			assert(name.length() > 0);
			std::string name_capitalized = name;
			name_capitalized[0] = toupper(name_capitalized[0]);
			branchName_multiplicity_ = Form("num%s", name_capitalized.data());
			branchName_position_ = TString(name.data()).ReplaceAll("Vertices", "Vertex").Data();
		}
		~vertexCollectionEntryType() {}
		edm::InputTag src_;
		std::string branchName_multiplicity_;
		std::string branchName_position_;
	};
	std::vector<vertexCollectionEntryType> vertexCollectionEntries_;

	std::vector<int> pdgIdsGenTau_;
	std::vector<int> pdgIdsGenElectron_;
	std::vector<int> pdgIdsGenMuon_;
	std::vector<int> pdgIdsGenQuarkOrGluon_;

	PFJetIDSelectionFunctor* loosePFJetIdAlgo_;

	bool isMC_;
	edm::InputTag srcGenPileUpSummary_;
	edm::EDGetTokenT<PileupSummaryInfo> tokenGenPileupSummary_;
	std::map<edm::RunNumber_t, std::map<edm::LuminosityBlockNumber_t, float> > pileUpByLumiCalc_; // key = run, lumi-section
	std::map<edm::RunNumber_t, std::map<edm::LuminosityBlockNumber_t, int> > numWarnings_;
	int maxWarnings_;

	typedef std::vector<edm::InputTag> vInputTag;
	vInputTag srcWeights_;

	edm::EDGetTokenT<GenEventInfoProduct> tokenGenInfoProduct_;

	struct branchEntryType
	{
		branchEntryType()
		: valueF_(0.),
		  valueI_(0.)
		{}
		~branchEntryType() {}
		Float_t valueF_;
		Int_t valueI_;
	};
	typedef std::map<std::string, branchEntryType> branchMap; // key = branch name
	branchMap branches_;

	TTree* ntuple_;

	int verbosity_;

	SignedTransverseImpactParameter* STIP;

};

#endif
