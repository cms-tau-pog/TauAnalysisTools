#include "TauAnalysisTools/TauAnalysisTools/plugins/TauIdMVATrainingNtupleProducerMiniAOD.h"

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"
#include "TrackingTools/IPTools/interface/IPTools.h"

#include <TPRegexp.h>
#include <TObjArray.h>
#include <TObjString.h>
#include <TString.h>
#include <TMath.h>
#include <TROOT.h>

#include <iostream>
#include <fstream>

TauIdMVATrainingNtupleProducerMiniAOD::TauIdMVATrainingNtupleProducerMiniAOD(const edm::ParameterSet& cfg)
	: moduleLabel_(cfg.getParameter<std::string>("@module_label")),
	maxChargedHadrons_(3),
	maxPiZeros_(1), // only 1 piZero can be reconstructed from signalGammaCands in MiniAOD
	loosePFJetIdAlgo_(0),
	maxWarnings_(3),
	ntuple_(0)
{
	srcRecTaus_ = cfg.getParameter<edm::InputTag>("srcRecTaus");
	tokenRecTaus_ = consumes<pat::TauCollection>(edm::InputTag(srcRecTaus_));

	srcPrunedGenParticles_ = cfg.getParameter<edm::InputTag>("srcPrunedGenParticles");
	tokenPrunedGenParticles_ = consumes<reco::GenParticleCollection>(srcPrunedGenParticles_);
	srcPackedGenParticles_ = cfg.getParameter<edm::InputTag>("srcPackedGenParticles");
	tokenPackedGenParticles_ = consumes<pat::PackedGenParticleCollection>(srcPackedGenParticles_);

	srcRecJets_ = cfg.getParameter<edm::InputTag>("srcRecJets");
	tokenRecJets_ = consumes<pat::JetCollection>(edm::InputTag(srcRecJets_));

	minGenVisPt_ = cfg.getParameter<double>("minGenVisPt");
	dRmatch_ = cfg.getParameter<double>("dRmatch");

	pdgIdsGenTau_.push_back(-15);
	pdgIdsGenTau_.push_back(+15);

	pdgIdsGenElectron_.push_back(-11);
	pdgIdsGenElectron_.push_back(+11);

	pdgIdsGenMuon_.push_back(-13);
	pdgIdsGenMuon_.push_back(+13);

	pdgIdsGenQuarkOrGluon_.push_back(-6);
	pdgIdsGenQuarkOrGluon_.push_back(-5);
	pdgIdsGenQuarkOrGluon_.push_back(-4);
	pdgIdsGenQuarkOrGluon_.push_back(-3);
	pdgIdsGenQuarkOrGluon_.push_back(-2);
	pdgIdsGenQuarkOrGluon_.push_back(-1);
	pdgIdsGenQuarkOrGluon_.push_back(+1);
	pdgIdsGenQuarkOrGluon_.push_back(+2);
	pdgIdsGenQuarkOrGluon_.push_back(+3);
	pdgIdsGenQuarkOrGluon_.push_back(+4);
	pdgIdsGenQuarkOrGluon_.push_back(+5);
	pdgIdsGenQuarkOrGluon_.push_back(+6);
	pdgIdsGenQuarkOrGluon_.push_back(+21);

	edm::ParameterSet tauIdDiscriminators = cfg.getParameter<edm::ParameterSet>("tauIdDiscriminators");
	typedef std::vector<std::string> vstring;
	vstring tauIdDiscriminatorNames = tauIdDiscriminators.getParameterNamesForType<std::string>();
	for(vstring::const_iterator name = tauIdDiscriminatorNames.begin(); name != tauIdDiscriminatorNames.end(); ++name)
	{
		std::string src = tauIdDiscriminators.getParameter<std::string>(*name);
		tauIdDiscrEntries_.push_back(tauIdDiscrEntryType(*name, src));
	}

	edm::ParameterSet isolationPtSums = cfg.getParameter<edm::ParameterSet>("isolationPtSums");
	vstring isolationPtSumNames = isolationPtSums.getParameterNamesForType<std::string>();
	for(vstring::const_iterator name = isolationPtSumNames.begin(); name != isolationPtSumNames.end(); ++name)
	{
		std::string src = isolationPtSums.getParameter<std::string>(*name);
		tauIsolationEntries_.push_back(tauIsolationEntryType(*name, src));
	}

	edm::ParameterSet vertexCollections = cfg.getParameter<edm::ParameterSet>("vertexCollections");
	vstring vertexCollectionNames = vertexCollections.getParameterNamesForType<edm::InputTag>();
	for(vstring::const_iterator name = vertexCollectionNames.begin(); name != vertexCollectionNames.end(); ++name)
	{
		edm::InputTag src = vertexCollections.getParameter<edm::InputTag>(*name);
		edm::EDGetTokenT<reco::VertexCollection> token = consumes<reco::VertexCollection>(src);
		vertexCollectionEntries_.push_back(vertexCollectionEntryType(*name, token));
	}

	vertexToken_ = consumes<reco::VertexCollection>(edm::InputTag("offlineSlimmedPrimaryVertices"));

	edm::ParameterSet cfgPFJetIdAlgo;
	cfgPFJetIdAlgo.addParameter<std::string>("version", "FIRSTDATA");
	cfgPFJetIdAlgo.addParameter<std::string>("quality", "LOOSE");
	loosePFJetIdAlgo_ = new PFJetIDSelectionFunctor(cfgPFJetIdAlgo);

	isMC_ = cfg.getParameter<bool>("isMC");
	if (isMC_)
	{
		srcGenPileUpSummary_ = cfg.getParameter<edm::InputTag>("srcGenPileUpSummary");
		tokenGenPileupSummary_ = consumes<std::vector<PileupSummaryInfo> >(srcGenPileUpSummary_);
	}
	/*
		else // FIXME: this does not work since the TauAnalysis/RecoTools does not exist (anymore?)
		{
			edm::FileInPath inputFileName = cfg.getParameter<edm::FileInPath>("inputFileNameLumiCalc");
			if (inputFileName.location() != edm::FileInPath::Local / *!inputFileName.isLocal()* /)
				throw cms::Exception("UnclEnCalibrationNtupleProducer") << " Failed to find File = " << inputFileName << " !!\n";
			std::ifstream inputFile(inputFileName.fullPath().data());

			std::string header_pattern = std::string(
			"\\|\\s*Run:Fill\\s*\\|\\s*LS\\s*\\|\\s*UTCTime\\s*\\|\\s*Beam Status\\s*\\|\\s*E\\(GeV\\)\\s*\\|\\s*Del\\(/nb\\)\\s*\\|\\s*Rec\\(/nb\\)\\s*\\|\\s*avgPU\\s*\\|\\s*");
			TPRegexp header_regexp(header_pattern.data());

			std::string pileUpInfo_pattern = std::string(
			"\\|\\s*([0-9]+):[0-9]+\\s*\\|\\s*([0-9]+):[0-9]+\\s*\\|\\s*[0-9/: ]+\\s*\\|\\s*[a-zA-Z0-9 ]+\\s*\\|\\s*[0-9.]+\\s*\\|\\s*[0-9.]+\\s*\\|\\s*[0-9.]+\\s*\\|\\s*([0-9.]+)\\s*\\|\\s*");
			TPRegexp pileUpInfo_regexp(pileUpInfo_pattern.data());

			int iLine = 0;
			bool foundHeader = false;
			while ( !(inputFile.eof() || inputFile.bad()))
			{
				std::string line;
				getline(inputFile, line);
				++iLine;
				TString line_tstring = line.data();
				if (header_regexp.Match(line_tstring) == 1) foundHeader = true;
				if (!foundHeader) continue;
				TObjArray* subStrings = pileUpInfo_regexp.MatchS(line_tstring);
				if (subStrings->GetEntries() == 4)
				{
					edm::RunNumber_t run = ((TObjString*)subStrings->At(1))->GetString().Atoll();
					edm::LuminosityBlockNumber_t ls = ((TObjString*)subStrings->At(2))->GetString().Atoll();
					float numPileUp_mean = ((TObjString*)subStrings->At(3))->GetString().Atof();
					//std::cout << "run = " << run << ", ls = " << ls << ": numPileUp_mean = " << numPileUp_mean << std::endl;
					pileUpByLumiCalc_[run][ls] = numPileUp_mean;
				}
			}
			if (!foundHeader)
				throw cms::Exception("UnclEnCalibrationNtupleProducer") << " Failed to find header in File = " << inputFileName.fullPath().data() << " !!\n";
		}
	*/

	isSignal_ = cfg.getParameter<bool>("isSignal");
	dRClean_ = cfg.getParameter<double>("dRClean");
	ptCleanMin_ = cfg.getParameter<double>("ptCleanMin");
	matchGenTauVis_ = cfg.getParameter<bool>("matchGenTauVis");

	srcWeights_ = cfg.getParameter<vInputTag>("srcWeights");

	tokenGenInfoProduct_ = consumes<GenEventInfoProduct>(edm::InputTag("generator","","SIM"));

	ptMin_allPhotonsVariables = cfg.getParameter<std::vector<std::string> >("ptMin_allPhotonsVariables");
	ptMin_nPhotons_ = cfg.getParameter<std::vector<std::string> >("ptMin_nPhotons");
	ptMin_photonPtSumOutsideSignalCone = cfg.getParameter<std::vector<std::string> >("ptMin_photonPtSumOutsideSignalCone");
	ptMin_photonPtSumOutsideSignalConedRgt0p1 = cfg.getParameter<std::vector<std::string> >("ptMin_photonPtSumOutsideSignalConedRgt0p1");

	verbosity_ = (cfg.exists("verbosity")) ? cfg.getParameter<int>("verbosity") : 0;

	STIP = new SignedTransverseImpactParameter();
}

TauIdMVATrainingNtupleProducerMiniAOD::~TauIdMVATrainingNtupleProducerMiniAOD() {}

void TauIdMVATrainingNtupleProducerMiniAOD::beginJob()
{
	//--- create TTree
	edm::Service<TFileService> fs;
	ntuple_ = fs->make<TTree>("tauIdMVATrainingNtupleMiniAOD", "tauIdMVATrainingNtupleMiniAOD");

	//--- add branches
	addBranchI("run");
	addBranchI("event");
	addBranchI("lumi");
	addBranchF("genEvtWeight");

	addBranch_EnPxPyPz("recTau");
	addBranch_EnPxPyPz("recTauAlternate");
	addBranchI("recTauDecayMode");
	addBranchF("recTauVtxZ");
	addBranch_EnPxPyPz("recJet");
	addBranchI("recJetLooseId");
	addBranch_EnPxPyPz("leadPFCand");
	addBranch_EnPxPyPz("leadPFChargedHadrCand");

	for(unsigned idx = 0; idx < maxChargedHadrons_; ++idx)
		addBranch_chargedHadron(Form("chargedHadron%i", idx + 1));

	for(unsigned idx = 0; idx < maxPiZeros_; ++idx)
		addBranch_piZero(Form("piZero%i", idx + 1));

	for(std::vector<tauIdDiscrEntryType>::const_iterator tauIdDiscriminator = tauIdDiscrEntries_.begin(); tauIdDiscriminator != tauIdDiscrEntries_.end(); ++tauIdDiscriminator)
		addBranchF(tauIdDiscriminator->branchName_);

	for(std::vector<tauIsolationEntryType>::const_iterator tauIsolation = tauIsolationEntries_.begin(); tauIsolation != tauIsolationEntries_.end(); ++tauIsolation)
		addBranchF(tauIsolation->branchName_);
		/*
			addBranchF(tauIsolation->branchNameChargedIsoPtSum_);
			addBranchF(tauIsolation->branchNameNeutralIsoPtSum_);
			addBranchF(tauIsolation->branchNamePUcorrPtSum_);
			addBranchF(tauIsolation->branchNameNeutralIsoPtSumWeight_);
			addBranchF(tauIsolation->branchNameFootprintCorrection_);
			addBranchF(tauIsolation->branchNamePhotonPtSumOutsideSignalCone_);
		*/

	addBranch_XYZ("recImpactParamPCA");
	addBranchF("recImpactParam");
	addBranchF("recImpactParamSign");
	addBranch_XYZ("recImpactParamPCA3D");
	addBranchF("recImpactParam3D");
	addBranchF("recImpactParamSign3D");

	//additional variables from Francesco///
	addBranchF("recImpactParamZ");
	addBranchF("recImpactParamSignZ");
	addBranchF("recImpactParamTk2");
	addBranchF("recImpactParamSignTk2");
	addBranchF("recImpactParam3DTk2");
	addBranchF("recImpactParamSign3DTk2");
	addBranchF("recImpactParamZTk2");
	addBranchF("recImpactParamSignZTk2");
	addBranchF("recImpactParamTk3");
	addBranchF("recImpactParamSignTk3");
	addBranchF("recImpactParam3DTk3");
	addBranchF("recImpactParamSign3DTk3");
	addBranchF("recImpactParamZTk3");
	addBranchF("recImpactParamSignZTk3");
	addBranchF("recDecayLengthTk1");
	addBranchF("recDecayLengthSignTk1");
	addBranchF("recDecayLengthTk2");
	addBranchF("recDecayLengthSignTk2");
	addBranchF("recDecayLengthTk3");
	addBranchF("recDecayLengthSignTk3");
	addBranchF("recDecayDist2D");
	addBranchF("recDecayDistSign2D");
	addBranchF("recChi2DiffEvtVertex");
	///////////////////////////////////
	addBranchI("hasRecDecayVertex");
	addBranch_XYZ("recDecayVertex");
	addBranch_Cov("recDecayVertexCov");
	addBranchF("recDecayVertexChi2");
	addBranch_XYZ("recDecayDist");
	addBranch_Cov("recDecayDistCov");
	addBranchF("recDecayDistSign");
	addBranch_XYZ("recEvtVertex");
	addBranch_Cov("recEvtVertexCov");

	for(std::vector<vertexCollectionEntryType>::const_iterator vertexCollection = vertexCollectionEntries_.begin(); vertexCollection != vertexCollectionEntries_.end(); ++vertexCollection)
	{
		addBranchI(vertexCollection->branchName_multiplicity_);
		addBranch_XYZ(vertexCollection->branchName_position_);
	}

	addBranchF("recTauPtWeightedDetaStrip");
	addBranchF("recTauPtWeightedDphiStrip");
	addBranchF("recTauPtWeightedDrSignal");
	addBranchF("recTauPtWeightedDrIsolation");

	for(unsigned iPtMin = 0; iPtMin < ptMin_allPhotonsVariables.size(); iPtMin++)
	{
		addBranchF("neutralIsoPtSum_IsoConeR0p3_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("neutralIsoPtSum_IsoConeR0p5_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("photonPtSumOutsideSignalCone_IsoConeR0p5_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));

		addBranchF("neutralIsoPtSum_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("recTauPtWeightedDetaStrip_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("recTauPtWeightedDphiStrip_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("recTauPtWeightedDrSignal_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		addBranchF("recTauPtWeightedDrIsolation_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
	}

	addBranchI("recTauNphoton");
	for(unsigned iPtMin = 0; iPtMin < ptMin_nPhotons_.size(); iPtMin++)
		addBranchI("recTauNphoton_ptGt"+ptMin_nPhotons_.at(iPtMin));

	addBranchF("photonPtSumOutsideSignalCone_default");
	for(unsigned iPtMin = 0; iPtMin < ptMin_photonPtSumOutsideSignalCone.size(); iPtMin++)
		addBranchF("photonPtSumOutsideSignalCone_ptGt" + ptMin_photonPtSumOutsideSignalCone.at(iPtMin));

	addBranchF("photonPtSumOutsideSignalConedRgt0p1_default");
	for(unsigned iPtMin = 0; iPtMin < ptMin_photonPtSumOutsideSignalConedRgt0p1.size(); iPtMin++)
		addBranchF("photonPtSumOutsideSignalConedRgt0p1_ptGt" + ptMin_photonPtSumOutsideSignalConedRgt0p1.at(iPtMin));

	addBranchF("recTauEratio");
	addBranchF("recTauLeadingTrackChi2");
	addBranchI("recTauNphotonSignal");
	addBranchI("recTauNphotonIso");
	addBranchI("recTauNphotonTotal");
	addBranchF("recTauGJangleMeasured");
	addBranchF("recTauGJangleDiff");
	addBranchF("numPileUp");
	addBranch_EnPxPyPz("genTau");
	addBranchF("genTauDeltaR");
	addBranch_EnPxPyPz("genVisTau");
	addBranchF("genVisTauDeltaR");
	addBranchI("genTauDecayMode");
	addBranchI("genTauMatch");
	addBranchF("genImpactParam");
	addBranch_XYZ("genDecayVertex");
	addBranch_XYZ("genEvtVertex");
	addBranch_EnPxPyPz("genElectron");
	addBranchI("genElectronMatch");
	addBranchF("genElectronDeltaR");
	addBranchI("genElectronPdgId");
	addBranch_EnPxPyPz("genMuon");
	addBranchI("genMuonMatch");
	addBranchF("genMuonDeltaR");
	addBranchI("genMuonPdgId");
	addBranch_EnPxPyPz("genQuarkOrGluon");
	addBranchI("genQuarkOrGluonMatch");
	addBranchF("genQuarkOrGluonDeltaR");
	addBranchI("genQuarkOrGluonPdgId");
	addBranchF("evtWeight");

	// Needed for maxLiklyhood
	addBranchVF("recTau_isolationChargedHadrCands_dz");
	addBranchVF("recTau_isolationChargedHadrCands_pt");
	addBranchVF("recTau_isolationChargedHadrCands_dxy");
	addBranchVF("recTau_isolationChargedHadrCands_dRs");
	// addBranchI("recTau_isolationGammaCands_size"); -> recTauNphotonIso
	addBranchVF("recTau_isolationGammaCands_pt");
	addBranchVF("recTau_isolationGammaCands_dR");
}

namespace
{
	//varibales from Yuta
	reco::CandidatePtrVector getGammas(const pat::Tau& tau, bool signal = true)
	{
		if (signal) return tau.signalGammaCands();
		return tau.isolationGammaCands();
	}

	bool isInside(float photon_pt, float deta, float dphi)
	{

		if (photon_pt==0) return false;

		if ((dphi < TMath::Min(0.3, TMath::Max(0.05, 0.352476*TMath::Power(photon_pt, -0.707716)))) &&
			(deta < TMath::Min(0.15, TMath::Max(0.05, 0.197077*TMath::Power(photon_pt, -0.658701)))))
			return true;

		return false;
	}

	float returnChi2(const pat::Tau& tau)
	{
		return tau.leadingTrackNormChi2();
	}

	float returnEratio(const pat::Tau& tau)
	{
		Float_t total = tau.ecalEnergy() + tau.hcalEnergy();
		if (total==0) return -1;
		else return tau.ecalEnergy()/total;
	}

	float pt_weighted_dx(const pat::Tau& tau, int mode = 0, int var = 0, int decaymode = -1, float ptMin = 0.5)
	{
		float sum_pt(0), sum_dx_pt(0);
		float signalrad = std::max(std::min(0.1, 3.0 / tau.pt()), 0.05);
		int is3prong = (decaymode == 10);

		const auto cands = getGammas(tau, mode < 2);

		for(const auto& cand : cands)
		{
			// only look at electrons/photons with pT > 0.5
			if (cand->pt() < ptMin) continue;
			float dr = reco::deltaR(*cand, tau);
			float deta = std::abs(cand->eta() - tau.eta());
			float dphi = std::abs(reco::deltaPhi(cand->phi(), tau.phi()));
			float pt = cand->pt();

			bool flag = isInside(pt, deta, dphi);

			if ((is3prong == 0 && (mode == 2 || (mode == 0 && dr < signalrad) || (mode == 1 && dr > signalrad))) ||
			     (is3prong != 0 && ((mode == 2 && flag == false) || (mode == 1 && flag == true) || mode == 0)))
			{
				sum_pt += pt;

				if (var == 0)      sum_dx_pt += pt * dr;
				else if (var == 1) sum_dx_pt += pt * deta;
				else if (var == 2) sum_dx_pt += pt * dphi;
			}
		}

		if (sum_pt > 0.) return sum_dx_pt / sum_pt;
		return 0.;
	}

	float pt_weighted_dr_signal(const pat::Tau& tau, int dm = -1, float ptMin = 0.5)
	{
		return pt_weighted_dx(tau, 0, 0, dm, ptMin);
	}

	float pt_weighted_deta_strip(const pat::Tau& tau, int dm = -1, float ptMin = 0.5)
	{
		if (dm == 10) return pt_weighted_dx(tau, 2, 1, dm, ptMin);
		return pt_weighted_dx(tau, 1, 1, dm, ptMin);
	}

	float pt_weighted_dphi_strip(const pat::Tau& tau, int dm = -1, float ptMin = 0.5)
	{
		if (dm == 10) return pt_weighted_dx(tau, 2, 2, dm, ptMin);
		return pt_weighted_dx(tau, 1, 2, dm, ptMin);
	}

	float pt_weighted_dr_iso(const pat::Tau& tau, int dm = -1, float ptMin = 0.5)
	{
		return pt_weighted_dx(tau, 2, 0, dm, ptMin);
	}

	unsigned int n_photons_total(const pat::Tau& tau)
	{
		unsigned int n_photons = 0;
		for(auto& cand : tau.signalGammaCands())
			if (cand->pt() > 0.5) ++n_photons;

		for(auto& cand : tau.isolationGammaCands())
			if (cand->pt() > 0.5) ++n_photons;

		return n_photons;
	}

	unsigned int n_photons_total(const pat::Tau& tau, double ptMin)
	{
		unsigned int n_photons = 0;

		for(auto& cand : tau.signalGammaCands())
			if (cand->pt() > ptMin) ++n_photons;

		for(auto& cand : tau.isolationGammaCands())
			if (cand->pt() > ptMin) ++n_photons;

		return n_photons;
	}

	float getPhotonPtSumOutsideSignalCone(const pat::Tau& tau, float ptMin = -1, float signalCone = -1, float isolationCone = -1)
	{
		float photonSumPt_outsideSignalCone = 0.;

		// definition of the reco::PFTau signalConeSize()
		if (signalCone < 0)
			signalCone = std::max(std::min(0.1, 3.0 / tau.pt()), 0.05);

		// Respectie member in AOD reco::PFTau : signalPFGammaCands(empty for miniAOD)
		// see: https://github.com/cms-tau-pog/cmssw/blob/ad72bdacd2af21aa7fc7abfe362af89d6faab361/RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByIsolation.cc#L579-L586
		for(auto& cand :  tau.signalGammaCands())
		{
			double dR = deltaR(tau.eta(), tau.phi(), cand->eta(), cand->phi());

			if ((dR > signalCone && cand->pt() > ptMin) && (isolationCone < 0 || dR <= isolationCone))
				photonSumPt_outsideSignalCone += cand->pt();
		}

		return photonSumPt_outsideSignalCone;
	}

	float getNeutralIsoPtsum(const pat::Tau& tau, float ptMin = -1, float dRiso = -1)
	{
		float neutralIsoPtsum = 0;
		for(auto& cand : tau.isolationGammaCands())
			if (cand->pt() > ptMin && !(dRiso > 0 && deltaR(tau.eta(), tau.phi(), cand->eta(), cand->phi()) > dRiso))
				neutralIsoPtsum += cand->pt();

		return neutralIsoPtsum;
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::setRecTauValues(const pat::TauRef& recTau, const pat::JetRef& recJet, const edm::Event& evt, const edm::EventSetup& es)
{
	setValue_EnPxPyPz("recTau", recTau->p4());
	setValue_EnPxPyPz("recTauAlternate", recTau->alternatLorentzVect());
	setValueI("recTauDecayMode", recTau->decayMode());
	setValueF("recTauVtxZ", recTau->vertex().z());
	if (recJet.isNonnull() && deltaR(recTau->p4(), recJet->p4()) < 0.4)
	{
		//setValue_EnPxPyPz("recJet", recTau->jetRef()->p4()); //jetRef does not exist in MiniAOD
		setValue_EnPxPyPz("recJet", recJet->p4());
		//int recJetLooseId = ((*loosePFJetIdAlgo_)(*recTau->jetRef())) ? 1 : 0; //jetRef does not exist in MiniAOD
		int recJetLooseId = ((*loosePFJetIdAlgo_)(*recJet)) ? 1 : 0;
		setValueI("recJetLooseId", recJetLooseId);
	}
	else
	{
		setValue_EnPxPyPz("recJet", reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueI("recJetLooseId", 1);
	}

	if (recTau->leadCand().isNonnull())
		 setValue_EnPxPyPz("leadPFCand", recTau->leadCand()->p4());
	else setValue_EnPxPyPz("leadPFCand", reco::Candidate::LorentzVector(0.,0.,0.,0.));

	if (recTau->leadChargedHadrCand().isNonnull())
		 setValue_EnPxPyPz("leadPFChargedHadrCand", recTau->leadChargedHadrCand()->p4());
	else setValue_EnPxPyPz("leadPFChargedHadrCand", reco::Candidate::LorentzVector(0.,0.,0.,0.));

	for(unsigned idx = 0; idx < maxChargedHadrons_; ++idx)
	{
		std::string branchName = Form("chargedHadron%i", idx + 1);
		if (recTau->signalChargedHadrCands().size() > idx)
			setValue_chargedHadron(branchName, recTau->signalChargedHadrCands()[idx]);
		//else setValue_chargedHadron(branchName, 0); // TODO: implement sensible else statement
	}
	for(unsigned idx = 0; idx < maxPiZeros_; ++idx)
	{
		std::string branchName = Form("piZero%i", idx + 1);
		if (recTau->signalGammaCands().size() > idx)
			setValue_piZero(branchName, recTau->signalGammaCands()); // only 1 piZero can be reconstructed on MiniAOD
	}

	setValue_XYZ("recImpactParamPCA", recTau->dxy_PCA());
	setValueF("recImpactParam", recTau->dxy());
	setValueF("recImpactParamSign", recTau->dxy_Sig());

	//setValue_XYZ("recImpactParamPCA3D", recTauLifetimeInfo.ip3d_PCA()); // TODO: does not exist in pat::Tau. needed?
	setValue_XYZ("recImpactParamPCA3D", pat::tau::TauPFEssential::Point(0.,0.,0.));
	setValueF("recImpactParam3D", recTau->ip3d());
	setValueF("recImpactParamSign3D", recTau->ip3d_Sig());
	setValueI("hasRecDecayVertex", recTau->hasSecondaryVertex());
	setValue_XYZ("recDecayVertex", recTau->secondaryVertexPos()); // not filled in PATTauProducer.cc !!!
	setValue_Cov("recDecayVertexCov", recTau->secondaryVertexCov()); // not filled in PATTauProducer.cc !!!
	const reco::VertexRef secVertex = recTau->secondaryVertex(); // not filled in PATTauProducer.cc !!!

	if (secVertex.isNonnull())
		 setValueF("recDecayVertexChi2", recTau->secondaryVertex()->normalizedChi2());
	else setValueF("recDecayVertexChi2",  999.);

	setValue_XYZ("recDecayDist", recTau->flightLength());
	setValue_Cov("recDecayDistCov", recTau->flightLengthCov()); // since neither primaryVertexCov nor secondaryVertexCov are filled by PATTauProducer.cc this is always 0 !!!
	setValueF("recDecayDistSign", recTau->flightLengthSig());
	setValue_XYZ("recEvtVertex", recTau->primaryVertexPos()); // not filled in PATTauProducer.cc !!!
	setValue_Cov("recEvtVertexCov", recTau->primaryVertexCov()); // not filled in PATTauProducer.cc !!!

	//1d IP & Variables from Francesco
	GlobalVector direction(recTau->p4().px(), recTau->p4().py(), recTau->p4().pz());
	if (recTau->hasSecondaryVertex())
	{
		// primaryVertex is not filled in PATTauProducer.cc !!!
		/*float recDecayDist2D_ = reco::SecondaryVertex::computeDist2d(*(recTau->primaryVertex()), *secVertex, direction, true).value();
		float recDecayDistSign2D_ = reco::SecondaryVertex::computeDist2d(*(recTau->primaryVertex()), *secVertex, direction, true).significance();
		setValueF("recDecayDist2D", recDecayDist2D_);
		setValueF("recDecayDistSign2D", recDecayDistSign2D_);*/
		setValueF("recDecayDist2D", -999.);
		setValueF("recDecayDistSign2D", -999.);
		// 3-prong+pi0 does not originate from a1 decay!
		if (recTau->decayMode() == 10)
		{
			// calculate difference between maximally allowed Gottfried-Jackson angle (angle between tau and a1 momentum)
			// and measured Gottfried-Jackson angle from flightlength vector and tau momentum
			// thetaGJmax = arcsin( ( m_tau^2 - m_a1^2) / ( 2 * m_tau * mag(p_a1) ))
			// thetaGJmeasured is simply the angle between the flightLength vector and the tau momentum
			double mTau = 1.77682;
			double mAOne = recTau->p4().M();
			double flightLengthMag = recTau->flightLength().Mag2();
			double pAOneMag = recTau->p();
			double thetaGJmax = TMath::ASin( (TMath::Power(mTau,2) - TMath::Power(mAOne,2)) / ( 2 * mTau * pAOneMag) );
			double thetaGJmeasured = TMath::ACos( ( recTau->p4().px() * recTau->flightLength().x() + recTau->p4().py() * recTau->flightLength().y() + recTau->p4().pz() * recTau->flightLength().z()) / ( pAOneMag * TMath::Sqrt(flightLengthMag)) );
			setValueF("recTauGJangleMeasured", thetaGJmeasured);
			setValueF("recTauGJangleDiff", thetaGJmeasured - thetaGJmax);
		}
		else
		{
			setValueF("recTauGJangleMeasured", -999.);
			setValueF("recTauGJangleDiff", -999.);
		}
	}
	else
	{
		setValueF("recDecayDist2D", -999.);
		setValueF("recDecayDistSign2D", -999.);
		setValueF("recTauGJangleMeasured", -999.);
		setValueF("recTauGJangleDiff", -999.);
	}

	edm::ESHandle<TransientTrackBuilder> transTrackBuilder;
	es.get<TransientTrackRecord>().get("TransientTrackBuilder",transTrackBuilder);

	setValueF("recImpactParamZ", -999.);
	setValueF("recImpactParamSignZ", -999.);
	setValueF("recDecayLengthTk1", -999.);
	setValueF("recDecayLengthSignTk1", -999.);
	/*
		if (recTau->leadChargedHadrCand().isNonnull() && recTau->leadChargedHadrCand()->bestTrack() != 0)
		{
			// primaryVertex is not filled in PATTauProducer.cc !!!
			const reco::Track* leadtrk = recTau->leadChargedHadrCand()->bestTrack();
			reco::TransientTrack ttrk = transTrackBuilder->build(&*leadtrk);
			std::pair<bool,Measurement1D> ip_z = STIP->zImpactParameter ( ttrk, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParamZ", (!isnan(ip_z.second.value())) ? ip_z.second.value() : -899.);
			setValueF("recImpactParamSignZ", (!isnan(ip_z.second.significance())) ? ip_z.second.significance() : -899.);
			std::pair<bool,Measurement1D> dl_tk1 = IPTools::signedDecayLength3D(ttrk, direction, *(recTau->primaryVertex()) );
			setValueF("recDecayLengthTk1", dl_tk1.second.value());
			setValueF("recDecayLengthSignTk1", dl_tk1.second.significance());
		}
		else
		{
			setValueF("recImpactParamZ", -999.);
			setValueF("recImpactParamSignZ", -999.);
			setValueF("recDecayLengthTk1", -999.);
			setValueF("recDecayLengthSignTk1", -999.);
		}
	*/

	if (recTau->signalChargedHadrCands().size() > 1)
	{
		const reco::CandidatePtrVector SigChCands = recTau->signalChargedHadrCands();
		const reco::Track* leadtrk2 = SigChCands[1]->bestTrack();
		if (leadtrk2)
		{
			// primaryVertex is not filled in PATTauProducer.cc !!!
			/*reco::TransientTrack ttrk2 = transTrackBuilder->build(&*leadtrk2);
			GlobalVector direction(recTau->p4().px(), recTau->p4().py(), recTau->p4().pz());
			std::pair<bool,Measurement1D> ip_z = STIP->zImpactParameter ( ttrk2, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParamZTk2", (!isnan(ip_z.second.value())) ? ip_z.second.value() : -899.);
			setValueF("recImpactParamSignZTk2", (!isnan(ip_z.second.significance())) ? ip_z.second.significance() : -899.);
			std::pair<bool,Measurement1D> ip_xy = IPTools::signedTransverseImpactParameter(ttrk2, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParamTk2", ip_xy.second.value());
			setValueF("recImpactParamSignTk2", (ip_xy.second.error() != 0) ? ip_xy.second.value()/ip_xy.second.error() : 0.);
			std::pair<bool,Measurement1D> ip_3d = IPTools::signedImpactParameter3D(ttrk2, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParam3DTk2", ip_3d.second.value());
			setValueF("recImpactParamSign3DTk2", (ip_3d.second.error() != 0) ? ip_3d.second.value()/ip_3d.second.error() : 0.);
			std::pair<bool,Measurement1D> dl_tk2 = IPTools::signedDecayLength3D(ttrk2, direction, *(recTau->primaryVertex()) );
			setValueF("recDecayLengthTk2", dl_tk2.second.value());
			setValueF("recDecayLengthSignTk2", dl_tk2.second.significance());*/
			setValueF("recImpactParamTk2", -999.);
			setValueF("recImpactParamSignTk2", -999.);
			setValueF("recImpactParam3DTk2", -999.);
			setValueF("recImpactParamSign3DTk2", -999.);
			setValueF("recImpactParamZTk2", -999.);
			setValueF("recImpactParamSignZTk2", -999.);
			setValueF("recDecayLengthTk2", -999.);
			setValueF("recDecayLengthSignTk2", -999.);
		}
		else{
			setValueF("recImpactParamTk2", -999.);
			setValueF("recImpactParamSignTk2", -999.);
			setValueF("recImpactParam3DTk2", -999.);
			setValueF("recImpactParamSign3DTk2", -999.);
			setValueF("recImpactParamZTk2", -999.);
			setValueF("recImpactParamSignZTk2", -999.);
			setValueF("recDecayLengthTk2", -999.);
			setValueF("recDecayLengthSignTk2", -999.);
		}
	}
	else{
		setValueF("recImpactParamTk2", -999.);
		setValueF("recImpactParamSignTk2", -999.);
		setValueF("recImpactParam3DTk2", -999.);
		setValueF("recImpactParamSign3DTk2", -999.);
		setValueF("recImpactParamZTk2", -999.);
		setValueF("recImpactParamSignZTk2", -999.);
		setValueF("recDecayLengthTk2", -999.);
		setValueF("recDecayLengthSignTk2", -999.);
	}
	if (recTau->signalChargedHadrCands().size() > 2){
		const reco::CandidatePtrVector SigChCands = recTau->signalChargedHadrCands();
		const reco::Track* leadtrk3= SigChCands[2]->bestTrack();
		if (leadtrk3){
			// primaryVertex is not filled in PATTauProducer.cc !!!
			/*reco::TransientTrack ttrk3 = transTrackBuilder->build(&*leadtrk3);
			GlobalVector direction(recTau->p4().px(), recTau->p4().py(), recTau->p4().pz());
			std::pair<bool,Measurement1D> ip_z = STIP->zImpactParameter ( ttrk3, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParamZTk3", (!isnan(ip_z.second.value())) ? ip_z.second.value() : -899.);
			setValueF("recImpactParamSignZTk3", (!isnan(ip_z.second.significance())) ? ip_z.second.significance() : -899.);
			std::pair<bool,Measurement1D> ip_xy = IPTools::signedTransverseImpactParameter(ttrk3, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParamTk3", ip_xy.second.value());
			setValueF("recImpactParamSignTk3", (ip_xy.second.error() != 0) ? ip_xy.second.value()/ip_xy.second.error() : 0.);
			std::pair<bool,Measurement1D> ip_3d = IPTools::signedImpactParameter3D(ttrk3, direction, *(recTau->primaryVertex()) );
			setValueF("recImpactParam3DTk3", ip_3d.second.value());
			setValueF("recImpactParamSign3DTk3", (ip_3d.second.error() != 0) ? ip_3d.second.value()/ip_3d.second.error() : 0.);
			std::pair<bool,Measurement1D> dl_tk3 = IPTools::signedDecayLength3D(ttrk3, direction, *(recTau->primaryVertex()) );
			setValueF("recDecayLengthTk3", dl_tk3.second.value());
			setValueF("recDecayLengthSignTk3", dl_tk3.second.significance());*/
			setValueF("recImpactParamTk3", -999.);
			setValueF("recImpactParamSignTk3", -999.);
			setValueF("recImpactParam3DTk3", -999.);
			setValueF("recImpactParamSign3DTk3", -999.);
			setValueF("recImpactParamZTk3", -999.);
			setValueF("recImpactParamSignZTk3", -999.);
			setValueF("recDecayLengthTk3", -999.);
			setValueF("recDecayLengthSignTk3", -999.);
		}
		else{
			setValueF("recImpactParamTk3", -999.);
			setValueF("recImpactParamSignTk3", -999.);
			setValueF("recImpactParam3DTk3", -999.);
			setValueF("recImpactParamSign3DTk3", -999.);
			setValueF("recImpactParamZTk3", -999.);
			setValueF("recImpactParamSignZTk3", -999.);
			setValueF("recDecayLengthTk3", -999.);
			setValueF("recDecayLengthSignTk3", -999.);
		}
	}
	else{
		setValueF("recImpactParamTk3", -999.);
		setValueF("recImpactParamSignTk3", -999.);
		setValueF("recImpactParam3DTk3", -999.);
		setValueF("recImpactParamSign3DTk3", -999.);
		setValueF("recImpactParamZTk3", -999.);
		setValueF("recImpactParamSignZTk3", -999.);
		setValueF("recDecayLengthTk3", -999.);
		setValueF("recDecayLengthSignTk3", -999.);
	}
	/////////////////////////////////////////////
	for(std::vector<tauIdDiscrEntryType>::const_iterator tauIdDiscriminator = tauIdDiscrEntries_.begin();
			tauIdDiscriminator != tauIdDiscrEntries_.end(); ++tauIdDiscriminator)
	{
		setValueF(tauIdDiscriminator->branchName_, recTau->tauID(tauIdDiscriminator->src_));
	}
	for(std::vector<tauIsolationEntryType>::const_iterator tauIsolation = tauIsolationEntries_.begin();
			tauIsolation != tauIsolationEntries_.end(); ++tauIsolation)
	{
		/*setValueF(tauIsolation->branchNameChargedIsoPtSum_, recTau->tauID(tauIsolation->branchNameChargedIsoPtSum_));
		setValueF(tauIsolation->branchNameNeutralIsoPtSum_, recTau->tauID(tauIsolation->branchNameNeutralIsoPtSum_));
		setValueF(tauIsolation->branchNamePUcorrPtSum_, recTau->tauID(tauIsolation->branchNamePUcorrPtSum_));
		setValueF(tauIsolation->branchNameNeutralIsoPtSumWeight_, recTau->tauID(tauIsolation->branchNameNeutralIsoPtSumWeight_));
		setValueF(tauIsolation->branchNameFootprintCorrection_, recTau->tauID(tauIsolation->branchNameFootprintCorrection_));
		setValueF(tauIsolation->branchNamePhotonPtSumOutsideSignalCone_, recTau->tauID(tauIsolation->branchNamePhotonPtSumOutsideSignalCone_));*/
		setValueF(tauIsolation->branchName_, recTau->tauID(tauIsolation->src_));
	}
	//variables from Yuta for dynamic strip
	int tau_decaymode = recTau->decayMode();

	setValueF("recTauPtWeightedDetaStrip", pt_weighted_deta_strip(*recTau, tau_decaymode));
	setValueF("recTauPtWeightedDphiStrip", pt_weighted_dphi_strip(*recTau, tau_decaymode));
	setValueF("recTauPtWeightedDrSignal", pt_weighted_dr_signal(*recTau, tau_decaymode));
	setValueF("recTauPtWeightedDrIsolation", pt_weighted_dr_iso(*recTau, tau_decaymode));
	for(unsigned iPtMin = 0; iPtMin < ptMin_allPhotonsVariables.size(); iPtMin++)
	{

		setValueF("neutralIsoPtSum_IsoConeR0p3_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), getNeutralIsoPtsum(*recTau, std::stof(ptMin_allPhotonsVariables.at(iPtMin)), 0.3));
		setValueF("neutralIsoPtSum_IsoConeR0p5_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), getNeutralIsoPtsum(*recTau, std::stof(ptMin_allPhotonsVariables.at(iPtMin)), 0.5));
		//setValueF("chargedIsoPtSumdR03_ptGt" + ptMin_allPhotonsVariables.at(iPtMin));
		setValueF("photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), getPhotonPtSumOutsideSignalCone(*recTau, std::stof(ptMin_photonPtSumOutsideSignalCone.at(iPtMin)), -1, 0.3));
		setValueF("photonPtSumOutsideSignalCone_IsoConeR0p5_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), getPhotonPtSumOutsideSignalCone(*recTau, std::stof(ptMin_photonPtSumOutsideSignalCone.at(iPtMin)), -1, 0.5));

		setValueF("neutralIsoPtSum_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), getNeutralIsoPtsum(*recTau, std::stof(ptMin_allPhotonsVariables.at(iPtMin))));
		setValueF("recTauPtWeightedDetaStrip_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), pt_weighted_deta_strip(*recTau, tau_decaymode, std::stof(ptMin_allPhotonsVariables.at(iPtMin))));
		setValueF("recTauPtWeightedDphiStrip_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), pt_weighted_dphi_strip(*recTau, tau_decaymode, std::stof(ptMin_allPhotonsVariables.at(iPtMin))));
		setValueF("recTauPtWeightedDrSignal_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), pt_weighted_dr_signal(*recTau, tau_decaymode, std::stof(ptMin_allPhotonsVariables.at(iPtMin))));
		setValueF("recTauPtWeightedDrIsolation_ptGt" + ptMin_allPhotonsVariables.at(iPtMin), pt_weighted_dr_iso(*recTau, tau_decaymode, std::stof(ptMin_allPhotonsVariables.at(iPtMin))));

	}

	setValueI("recTauNphoton", n_photons_total(*recTau));
	for(unsigned iPtMin = 0; iPtMin < ptMin_nPhotons_.size(); iPtMin++)
	{
		setValueI("recTauNphoton_ptGt"+ptMin_nPhotons_.at(iPtMin), n_photons_total(*recTau, std::stof(ptMin_nPhotons_.at(iPtMin))));
	}

	setValueF("photonPtSumOutsideSignalCone_default", getPhotonPtSumOutsideSignalCone(*recTau));
	for(unsigned iPtMin = 0; iPtMin < ptMin_photonPtSumOutsideSignalCone.size(); iPtMin++)
		setValueF("photonPtSumOutsideSignalCone_ptGt" + ptMin_photonPtSumOutsideSignalCone.at(iPtMin), getPhotonPtSumOutsideSignalCone(*recTau, std::stof(ptMin_photonPtSumOutsideSignalCone.at(iPtMin))));

	setValueF("photonPtSumOutsideSignalConedRgt0p1_default", getPhotonPtSumOutsideSignalCone(*recTau, -1, 0.1));
	for(unsigned iPtMin = 0; iPtMin < ptMin_photonPtSumOutsideSignalConedRgt0p1.size(); iPtMin++)
		setValueF("photonPtSumOutsideSignalConedRgt0p1_ptGt" + ptMin_photonPtSumOutsideSignalConedRgt0p1.at(iPtMin),
			getPhotonPtSumOutsideSignalCone(*recTau, std::stof(ptMin_photonPtSumOutsideSignalConedRgt0p1.at(iPtMin)), 0.1));

	setValueF("recTauEratio", returnEratio(*recTau));
	setValueF("recTauLeadingTrackChi2", returnChi2(*recTau));
	setValueI("recTauNphotonSignal", recTau->signalGammaCands().size());
	setValueI("recTauNphotonIso", recTau->isolationGammaCands().size());
	setValueI("recTauNphotonTotal", recTau->signalGammaCands().size()+recTau->isolationGammaCands().size());

	edm::Handle<reco::VertexCollection> vertices;
	evt.getByToken(vertexToken_, vertices);
	if (vertices->size() >= 1)
	{
		// primaryVertex is not filled in PATTauProducer.cc !!!
		//float recChi2DiffEvtVertex_ = (vertices->front().normalizedChi2() - recTau->primaryVertex()->normalizedChi2());
		//setValueF("recChi2DiffEvtVertex", recChi2DiffEvtVertex_);
		setValueF("recChi2DiffEvtVertex", -999.);
	}
	else{ setValueF("recChi2DiffEvtVertex", -999.); }

}

void TauIdMVATrainingNtupleProducerMiniAOD::setGenTauMatchValues(
	const reco::Candidate::LorentzVector& recTauP4, const pat::PackedGenParticle* genTau, const reco::Candidate::LorentzVector& genVisTauP4, int genTauDecayMode)
{
	if (genTau)
	{
		setValue_EnPxPyPz("genTau", genTau->p4());
		setValueF("genTauDeltaR", deltaR(genTau->p4(), recTauP4));
		setValue_EnPxPyPz("genVisTau", genVisTauP4);
		setValueF("genVisTauDeltaR", deltaR(genVisTauP4, recTauP4));
		setValueI("genTauDecayMode", genTauDecayMode);
		setValueI("genTauMatch", 1);
	} else {
		setValue_EnPxPyPz("genTau", reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueF("genTauDeltaR", 1.e+3);
		setValue_EnPxPyPz("genVisTau", reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueF("genVisTauDeltaR", 1.e+3);
		setValueI("genTauDecayMode", -1);
		setValueI("genTauMatch", 0);
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::setGenTauMatchValues(
	const reco::Candidate::LorentzVector& recTauP4, const reco::GenParticle* genTau, const reco::Candidate::LorentzVector& genVisTauP4, int genTauDecayMode)
{
	if (genTau)
	{
		setValue_EnPxPyPz("genTau", genTau->p4());
		setValueF("genTauDeltaR", deltaR(genTau->p4(), recTauP4));
		setValue_EnPxPyPz("genVisTau", genVisTauP4);
		setValueF("genVisTauDeltaR", deltaR(genVisTauP4, recTauP4));
		setValueI("genTauDecayMode", genTauDecayMode);
		setValueI("genTauMatch", 1);
	} else {
		setValue_EnPxPyPz("genTau", reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueF("genTauDeltaR", 1.e+3);
		setValue_EnPxPyPz("genVisTau", reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueF("genVisTauDeltaR", 1.e+3);
		setValueI("genTauDecayMode", -1);
		setValueI("genTauMatch", 0);
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::setGenParticleMatchValues(const std::string& branchName, const reco::Candidate::LorentzVector& recTauP4, const pat::PackedGenParticle* genParticle)
{
	if (genParticle)
	{
		setValue_EnPxPyPz(branchName, genParticle->p4());
		setValueI(std::string(branchName).append("Match"), 1);
		setValueF(std::string(branchName).append("DeltaR"), deltaR(genParticle->p4(), recTauP4));
		setValueI(std::string(branchName).append("PdgId"), genParticle->pdgId());
	} else {
		setValue_EnPxPyPz(branchName, reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueI(std::string(branchName).append("Match"), 0);
		setValueF(std::string(branchName).append("DeltaR"), 1.e+3);
		setValueI(std::string(branchName).append("PdgId"), 0);
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::setGenParticleMatchValues(const std::string& branchName, const reco::Candidate::LorentzVector& recTauP4, const reco::GenParticle* genParticle)
{
	if (genParticle)
	{
		setValue_EnPxPyPz(branchName, genParticle->p4());
		setValueI(std::string(branchName).append("Match"), 1);
		setValueF(std::string(branchName).append("DeltaR"), deltaR(genParticle->p4(), recTauP4));
		setValueI(std::string(branchName).append("PdgId"), genParticle->pdgId());
	} else {
		setValue_EnPxPyPz(branchName, reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueI(std::string(branchName).append("Match"), 0);
		setValueF(std::string(branchName).append("DeltaR"), 1.e+3);
		setValueI(std::string(branchName).append("PdgId"), 0);
	}
}

namespace
{
	void findDaughters(const pat::PackedGenParticle* mother, std::vector<const pat::PackedGenParticle*>& daughters, int status)
	{
		unsigned numDaughters = mother->numberOfDaughters();
		for(unsigned iDaughter = 0; iDaughter < numDaughters; ++iDaughter)
		{
			const pat::PackedGenParticle* daughter = dynamic_cast<const pat::PackedGenParticle*>(mother->daughter(iDaughter));
			if (status == -1 || daughter->status() == status) daughters.push_back(daughter);
			findDaughters(daughter, daughters, status);
		}
	}

	void findDaughters(const reco::GenParticle* mother, std::vector<const reco::GenParticle*>& daughters, int status)
	{
		unsigned numDaughters = mother->numberOfDaughters();
		for(unsigned iDaughter = 0; iDaughter < numDaughters; ++iDaughter)
		{
			const reco::GenParticle* daughter = mother->daughterRef(iDaughter).get();
			if (status == -1 || daughter->status() == status) daughters.push_back(daughter);
			findDaughters(daughter, daughters, status);
		}
	}

	bool isNeutrino(const reco::GenParticle* daughter)
	{
		return ( TMath::Abs(daughter->pdgId()) == 12 || TMath::Abs(daughter->pdgId()) == 14 || TMath::Abs(daughter->pdgId()) == 16 );
	}

	reco::Candidate::LorentzVector getVisMomentum(const std::vector<const reco::GenParticle*>& daughters, int status)
	{
		reco::Candidate::LorentzVector p4Vis(0,0,0,0);
		for(std::vector<const reco::GenParticle*>::const_iterator daughter = daughters.begin();
				daughter != daughters.end(); ++daughter)
		{
			if ((status == -1 || (*daughter)->status() == status) && !isNeutrino(*daughter))
			{
				p4Vis += (*daughter)->p4();
			}
		}
		return p4Vis;
	}

	reco::Candidate::LorentzVector getVisMomentum(const reco::GenParticle* genTau)
	{
		std::vector<const reco::GenParticle*> stableDaughters;
		findDaughters(genTau, stableDaughters, 1);
		reco::Candidate::LorentzVector genVisTauP4 = getVisMomentum(stableDaughters, 1);
		return genVisTauP4;
	}

	void countDecayProducts(const pat::PackedGenParticle* genParticle,
		int& numElectrons, int& numElecNeutrinos, int& numMuons, int& numMuNeutrinos,
		int& numChargedHadrons, int& numPi0s, int& numOtherNeutralHadrons, int& numPhotons)
	{
		int absPdgId = TMath::Abs(genParticle->pdgId());
		int status   = genParticle->status();
		int charge   = genParticle->charge();

		if (absPdgId == 111) ++numPi0s;
		else if (status == 1)
		{
			if      ( absPdgId == 11) ++numElectrons;
			else if (absPdgId == 12) ++numElecNeutrinos;
			else if (absPdgId == 13) ++numMuons;
			else if (absPdgId == 14) ++numMuNeutrinos;
			else if (absPdgId == 15)
			{
				edm::LogError ("countDecayProducts")
				<< "Found tau lepton with status code 1 !!";
				return;
			}
			else if (absPdgId == 16) return; // no need to count tau neutrinos
			else if (absPdgId == 22) ++numPhotons;
			else if (charge   !=  0) ++numChargedHadrons;
			else                       ++numOtherNeutralHadrons;
		} else {
			unsigned numDaughters = genParticle->numberOfDaughters();
			for(unsigned iDaughter = 0; iDaughter < numDaughters; ++iDaughter)
			{
				const pat::PackedGenParticle* daughter = dynamic_cast<const pat::PackedGenParticle*>(genParticle->daughter(iDaughter));

				countDecayProducts(daughter,
					numElectrons, numElecNeutrinos, numMuons, numMuNeutrinos,
					numChargedHadrons, numPi0s, numOtherNeutralHadrons, numPhotons);
			}
		}
	}

	void countDecayProducts(const reco::GenParticle* genParticle,
		int& numElectrons, int& numElecNeutrinos, int& numMuons, int& numMuNeutrinos,
		int& numChargedHadrons, int& numPi0s, int& numOtherNeutralHadrons, int& numPhotons)
	{
		int absPdgId = TMath::Abs(genParticle->pdgId());
		int status   = genParticle->status();
		int charge   = genParticle->charge();

		if (absPdgId == 111) ++numPi0s;
		else if (status == 1)
		{
			if      ( absPdgId == 11) ++numElectrons;
			else if (absPdgId == 12) ++numElecNeutrinos;
			else if (absPdgId == 13) ++numMuons;
			else if (absPdgId == 14) ++numMuNeutrinos;
			else if (absPdgId == 15)
			{
				edm::LogError ("countDecayProducts")
				<< "Found tau lepton with status code 1 !!";
				return;
			}
			else if (absPdgId == 16) return; // no need to count tau neutrinos
			else if (absPdgId == 22) ++numPhotons;
			else if (charge   !=  0) ++numChargedHadrons;
			else                       ++numOtherNeutralHadrons;
		} else {
			unsigned numDaughters = genParticle->numberOfDaughters();
			for(unsigned iDaughter = 0; iDaughter < numDaughters; ++iDaughter)
			{
				const reco::GenParticle* daughter = genParticle->daughterRef(iDaughter).get();

				countDecayProducts(daughter,
					numElectrons, numElecNeutrinos, numMuons, numMuNeutrinos,
					numChargedHadrons, numPi0s, numOtherNeutralHadrons, numPhotons);
			}
		}
	}

	std::string getGenTauDecayMode(const reco::GenParticle* genTau)
	{
		//--- determine generator level tau decay mode
		//
		//    NOTE:
		//        (1) function implements logic defined in PhysicsTools/JetMCUtils/src/JetMCTag::genTauDecayMode
		//            for different type of argument
		//        (2) this implementation should be more robust to handle cases of tau --> tau + gamma radiation
		//
		int numElectrons           = 0;
		int numElecNeutrinos       = 0;
		int numMuons               = 0;
		int numMuNeutrinos         = 0;
		int numChargedHadrons      = 0;
		int numPi0s                = 0;
		int numOtherNeutralHadrons = 0;
		int numPhotons             = 0;

		countDecayProducts(genTau,
			numElectrons, numElecNeutrinos, numMuons, numMuNeutrinos,
			numChargedHadrons, numPi0s, numOtherNeutralHadrons, numPhotons);

		if      ( numElectrons == 1 && numElecNeutrinos == 1) return std::string("electron");
		else if (numMuons     == 1 && numMuNeutrinos   == 1) return std::string("muon");

		switch ( numChargedHadrons)
		{
		case 1 :
			if (numOtherNeutralHadrons != 0) return std::string("oneProngOther");
			switch ( numPi0s)
			{
			case 0:
				return std::string("oneProng0Pi0");
			case 1:
				return std::string("oneProng1Pi0");
			case 2:
				return std::string("oneProng2Pi0");
			default:
				return std::string("oneProngOther");
			}
			case 3 :
				if (numOtherNeutralHadrons != 0) return std::string("threeProngOther");
				switch ( numPi0s)
				{
				case 0:
					return std::string("threeProng0Pi0");
				case 1:
					return std::string("threeProng1Pi0");
				default:
					return std::string("threeProngOther");
				}
				default:
					return std::string("rare");
		}
	}

	const reco::GenParticle* getGenLeadChargedDecayProduct(const reco::GenParticle* genTau)
	{
		std::vector<const reco::GenParticle*> genTauDecayProducts;
		findDaughters(genTau, genTauDecayProducts, 1);
		const reco::GenParticle* genLeadChargedDecayProduct = 0;
		double genLeadChargedDecayProductPt = -1.;
		for(std::vector<const reco::GenParticle*>::const_iterator genTauDecayProduct = genTauDecayProducts.begin();
				genTauDecayProduct != genTauDecayProducts.end(); ++genTauDecayProduct)
		{
			if (TMath::Abs((*genTauDecayProduct)->charge()) > 0.5 && (*genTauDecayProduct)->pt() > genLeadChargedDecayProductPt)
			{
				genLeadChargedDecayProduct = (*genTauDecayProduct);
				genLeadChargedDecayProductPt = (*genTauDecayProduct)->pt();
			}
		}
		return genLeadChargedDecayProduct;
	}

	const pat::PackedGenParticle* findMatchingGenParticle(const reco::Candidate::LorentzVector& recTauP4,
						   const pat::PackedGenParticleCollection& genParticles, double minGenVisPt, const std::vector<int>& pdgIds, double dRmatch)
	{
		const pat::PackedGenParticle* genParticle_matched = 0;
		double dRmin = dRmatch;
		for(pat::PackedGenParticleCollection::const_iterator genParticle = genParticles.begin();
				genParticle != genParticles.end(); ++genParticle)
		{
			if (!(genParticle->pt() > minGenVisPt)) continue;
			double dR = deltaR(genParticle->p4(), recTauP4);
			if (dR < dRmin)
			{
				bool matchedPdgId = false;
				for(std::vector<int>::const_iterator pdgId = pdgIds.begin();
					pdgId != pdgIds.end(); ++pdgId)
				{
					if (genParticle->pdgId() == (*pdgId))
					{
						matchedPdgId = true;
						break;
					}
				}
				if (matchedPdgId)
				{
					genParticle_matched = &(*genParticle);
					dRmin = dR;
				}
			}
		}
		return genParticle_matched;
	}

	const reco::GenParticle* findMatchingGenParticle(const reco::Candidate::LorentzVector& recTauP4,
	   const reco::GenParticleCollection& genParticles, double minGenVisPt, const std::vector<int>& pdgIds, double dRmatch)
	{
		const reco::GenParticle* genParticle_matched = 0;
		double dRmin = dRmatch;
		for(reco::GenParticleCollection::const_iterator genParticle = genParticles.begin(); genParticle != genParticles.end(); ++genParticle)
		{
			if (!(genParticle->pt() > minGenVisPt)) continue;
			double dR = deltaR(genParticle->p4(), recTauP4);
			if (dR < dRmin)
			{
				bool matchedPdgId = false;
				for(std::vector<int>::const_iterator pdgId = pdgIds.begin();
						pdgId != pdgIds.end(); ++pdgId)
				{
					if (genParticle->pdgId() == (*pdgId))
					{
						matchedPdgId = true;
						break;
					}
				}
				if (matchedPdgId)
				{
					genParticle_matched = &(*genParticle);
					dRmin = dR;
				}
			}
		}
		return genParticle_matched;
	}

	void findMatchingGenTauJet(const reco::Candidate::LorentzVector& recTauP4,
		const reco::GenParticleCollection& genParticles, double minGenVisPt, const std::vector<int>& pdgIds, double dRmatch,
		const reco::GenParticle*& genTau_matched, reco::Candidate::LorentzVector& genVisTauP4_matched, int& genTauDecayMode_matched, bool matchWithVisibleP4=false)
	{
		double dRmin = dRmatch;
		for(reco::GenParticleCollection::const_iterator genParticle = genParticles.begin(); genParticle != genParticles.end(); ++genParticle)
		{
			if (!genParticle->isPromptDecayed()) continue;
			bool matchedPdgId = false;
			for(std::vector<int>::const_iterator pdgId = pdgIds.begin(); pdgId != pdgIds.end(); ++pdgId)
			{
				if (genParticle->pdgId() == (*pdgId))
				{
					matchedPdgId = true;
					break;
				}
			}
			if (!matchedPdgId) continue;
			reco::Candidate::LorentzVector genVisTauP4 = getVisMomentum(&(*genParticle));
			if (!(genVisTauP4.pt() > minGenVisPt)) continue;
			std::string genTauDecayMode_string = getGenTauDecayMode(&(*genParticle));
			int genTauDecayMode = -1;
			if      ( genTauDecayMode_string == "oneProng0Pi0"  ) genTauDecayMode = reco::PFTau::kOneProng0PiZero;
			else if (genTauDecayMode_string == "oneProng1Pi0"   ) genTauDecayMode = reco::PFTau::kOneProng1PiZero;
			else if (genTauDecayMode_string == "oneProng2Pi0"   ) genTauDecayMode = reco::PFTau::kOneProng2PiZero;
			else if (genTauDecayMode_string == "threeProng0Pi0" ) genTauDecayMode = reco::PFTau::kThreeProng0PiZero;
			else if (genTauDecayMode_string == "threeProng1Pi0" ) genTauDecayMode = reco::PFTau::kThreeProng1PiZero;
			else if (genTauDecayMode_string == "oneProngOther"   ||
					 genTauDecayMode_string == "threeProngOther" ||
					 genTauDecayMode_string == "rare"           ) genTauDecayMode = reco::PFTau::kRareDecayMode;
			if (genTauDecayMode == -1) continue; // skip leptonic tau decays
			double dR = deltaR(genParticle->p4(), recTauP4);
			if (matchWithVisibleP4) dR = deltaR(genVisTauP4, recTauP4);
			if (dR < dRmin)
			{
				genTau_matched = &(*genParticle);
				genVisTauP4_matched = genVisTauP4;
				genTauDecayMode_matched = genTauDecayMode;
			}
		}
	}

	// find the closest reconstructed jet to the tau using deltaR as a criterion
	pat::JetRef findMatchingJet(const reco::Candidate::LorentzVector& recTauP4, const edm::Handle<pat::JetCollection>& recJets)
	{
		pat::JetRef matchedJet;
		double minDR = 999.;

		for(size_t iRecJet = 0; iRecJet < recJets->size(); ++iRecJet)
		{
			pat::JetRef recJet(recJets, iRecJet);
			double tmpDR = deltaR(recTauP4, recJet->p4());
			if (tmpDR < minDR)
			{
				minDR = tmpDR;
				matchedJet = recJet;
			}
		}

		return matchedJet;
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::setNumPileUpValue(const edm::Event& evt)
{
	double numPileUp_mean = -1.;
	if (isMC_)
	{
		typedef std::vector<PileupSummaryInfo> PileupSummaryInfoCollection;
		edm::Handle<PileupSummaryInfoCollection> genPileUpInfos;
		evt.getByToken(tokenGenPileupSummary_, genPileUpInfos);
		for(PileupSummaryInfoCollection::const_iterator genPileUpInfo = genPileUpInfos->begin(); genPileUpInfo != genPileUpInfos->end(); ++genPileUpInfo)
		{
			// CV: in-time PU is stored in getBunchCrossing = 0,
			//    cf. https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupInformation
			int bx = genPileUpInfo->getBunchCrossing();
			if (bx == 0) numPileUp_mean = genPileUpInfo->getTrueNumInteractions();
		}
	}
	/*
		else
		{ // FIXME: this does not work since the TauAnalysis/RecoTools does not exist (anymore?)
		edm::RunNumber_t run = evt.id().run();
		edm::LuminosityBlockNumber_t ls = evt.luminosityBlock();
		if (pileUpByLumiCalc_.find(run) == pileUpByLumiCalc_.end() || pileUpByLumiCalc_[run].find(ls) == pileUpByLumiCalc_[run].end())
		{
			if (numWarnings_[run][ls] < maxWarnings_)
				edm::LogWarning("TauIdMVATrainingNtupleProducerMiniAOD") << "No inst. Luminosity information available for run = " << run << ", ls = " << ls << " --> skipping !!" << std::endl;

			++numWarnings_[run][ls];
			return;
		}
		numPileUp_mean = pileUpByLumiCalc_[run][ls];
	}*/
	setValueF("numPileUp", numPileUp_mean);
}

void TauIdMVATrainingNtupleProducerMiniAOD::produce(edm::Event& evt, const edm::EventSetup& es)
{
	assert(ntuple_);

	edm::Handle<pat::TauCollection> recTaus;
	evt.getByToken(tokenRecTaus_, recTaus);

	edm::Handle<reco::GenParticleCollection> prunedGenParticles;
	edm::Handle<pat::PackedGenParticleCollection> packedGenParticles;
	if (isMC_)
	{
		evt.getByToken(tokenPrunedGenParticles_, prunedGenParticles);
		evt.getByToken(tokenPackedGenParticles_, packedGenParticles);
	}

	edm::Handle<pat::JetCollection> recJets;
	evt.getByToken(tokenRecJets_, recJets);

	double evtWeight = 1.0;
	// TODO: check if these are available in MiniAOD
	for(vInputTag::const_iterator srcWeight = srcWeights_.begin();
			srcWeight != srcWeights_.end(); ++srcWeight)
	{
		edm::Handle<double> weight;
		evt.getByLabel(*srcWeight, weight);
		evtWeight *= (*weight);
	}

	//weight from MC@NLO
	double weightevt = 1;
	try{
		edm::Handle<GenEventInfoProduct> genEvt;
		evt.getByToken(tokenGenInfoProduct_,genEvt);
		weightevt = genEvt->weight();
		//if (verbosity_) std::cout << " mc@nlo weight " << weightevt<<std::endl;
	}
	catch(std::exception &e){ std::cerr << e.what();}

	size_t numRecTaus = recTaus->size();
	for(size_t iRecTau = 0; iRecTau < numRecTaus; ++iRecTau)
	{
		pat::TauRef recTau(recTaus, iRecTau);

		// clean tau against leptons / genTauJets depending on
		// whether event is signal or background
		if (isMC_)
		{
			const reco::GenParticle* genTau_matched_for_cleaning = 0;
			reco::Candidate::LorentzVector genVisTauP4_matched_for_cleaning(0.,0.,0.,0.);
			int genTauDecayMode_matched_for_cleaning = -1;

			findMatchingGenTauJet(recTau->p4(), *prunedGenParticles, ptCleanMin_, pdgIdsGenTau_, dRClean_, genTau_matched_for_cleaning, genVisTauP4_matched_for_cleaning, genTauDecayMode_matched_for_cleaning, matchGenTauVis_);
			const pat::PackedGenParticle* genElectron_matched_for_cleaning = findMatchingGenParticle(recTau->p4(), *packedGenParticles, ptCleanMin_, pdgIdsGenElectron_, dRClean_);
			const pat::PackedGenParticle* genMuon_matched_for_cleaning = findMatchingGenParticle(recTau->p4(), *packedGenParticles, ptCleanMin_, pdgIdsGenMuon_, dRClean_);

			if (isSignal_ && !genTau_matched_for_cleaning) continue; // pass only if recTau matches genTauJet within deltaR cone specified in config file
			else
			{
				// pass only if recTau matches none of the following objects within deltaR cone specified in config file
				// - generated electrons
				// - generated muons
				// - genTauJets
				if (genTau_matched_for_cleaning || genElectron_matched_for_cleaning || genMuon_matched_for_cleaning) continue;
			}

			// need to find the closest reconstructed jet manually
			// since recTau->jetRef() is not saved in MiniAOD
			// TODO: this is not 100% efficient! find other solution
			pat::JetRef recJet = findMatchingJet(recTau->p4(), recJets);

			setRecTauValues(recTau, recJet, evt, es);

			const reco::GenParticle* genTau_matched = 0;
			reco::Candidate::LorentzVector genVisTauP4_matched(0.,0.,0.,0.);
			int genTauDecayMode_matched = -1;

			findMatchingGenTauJet(recTau->p4(), *prunedGenParticles, minGenVisPt_, pdgIdsGenTau_, dRmatch_, genTau_matched, genVisTauP4_matched, genTauDecayMode_matched, matchGenTauVis_);
			setGenTauMatchValues(recTau->p4(), genTau_matched, genVisTauP4_matched, genTauDecayMode_matched);

			if (genTau_matched)
			{
				reco::Candidate::Point genEvtVertex = genTau_matched->vertex();
				const reco::GenParticle* genLeadChargedHadron = getGenLeadChargedDecayProduct(genTau_matched);
				assert(genLeadChargedHadron);
				reco::Candidate::Point genDecayVertex = genLeadChargedHadron->vertex();
				double flightPathPx = genDecayVertex.x() - genEvtVertex.x();
				double flightPathPy = genDecayVertex.y() - genEvtVertex.y();
				double genImpactParam = TMath::Abs(flightPathPx*genLeadChargedHadron->py() - flightPathPy*genLeadChargedHadron->px())/genLeadChargedHadron->pt();
				setValueF("genImpactParam", genImpactParam);
				setValue_XYZ("genDecayVertex", genDecayVertex);
				setValue_XYZ("genEvtVertex", genDecayVertex);
			}
			else
			{
				setValueF("genImpactParam", -1.);
				setValue_XYZ("genDecayVertex", reco::Candidate::Point(0.,0.,0.));
				setValue_XYZ("genEvtVertex", reco::Candidate::Point(0.,0.,0.));
			}

			const pat::PackedGenParticle* genElectron_matched = findMatchingGenParticle(recTau->p4(), *packedGenParticles, minGenVisPt_, pdgIdsGenElectron_, dRmatch_);
			setGenParticleMatchValues("genElectron", recTau->p4(), genElectron_matched);

			const pat::PackedGenParticle* genMuon_matched = findMatchingGenParticle(recTau->p4(), *packedGenParticles, minGenVisPt_, pdgIdsGenMuon_, dRmatch_);
			setGenParticleMatchValues("genMuon", recTau->p4(), genMuon_matched);

			const reco::GenParticle* genQuarkOrGluon_matched = findMatchingGenParticle(recTau->p4(), *prunedGenParticles, minGenVisPt_, pdgIdsGenQuarkOrGluon_, dRmatch_);
			setGenParticleMatchValues("genQuarkOrGluon", recTau->p4(), genQuarkOrGluon_matched);

			int numHypotheses = 0;
			if (genTau_matched         ) ++numHypotheses;
			if (genElectron_matched    ) ++numHypotheses;
			if (genMuon_matched        ) ++numHypotheses;
			if (genQuarkOrGluon_matched) ++numHypotheses;
			if (numHypotheses > 1)
				edm::LogWarning("TauIdMVATrainingNtupleProducerMiniAOD::analyze") << " Matching between reconstructed PFTau and generator level tau-jets, electrons, muons and quark/gluon jets is ambiguous !!";

			setValueI("run" ,evt.run());
			setValueI("event", (evt.eventAuxiliary()).event());
			setValueI("lumi", evt.luminosityBlock());

			for(std::vector<vertexCollectionEntryType>::const_iterator vertexCollection = vertexCollectionEntries_.begin(); vertexCollection != vertexCollectionEntries_.end(); ++vertexCollection)
			{
				edm::Handle<reco::VertexCollection> vertices;
				evt.getByToken(vertexCollection->token_, vertices);
				setValueI(vertexCollection->branchName_multiplicity_, vertices->size());
				if (vertices->size() >= 1)
					setValue_XYZ(vertexCollection->branchName_position_, vertices->front().position()); // CV: first entry is vertex with highest sum(trackPt), take as "the" event vertex
				else
					setValue_XYZ(vertexCollection->branchName_position_, reco::Candidate::Point(0.,0.,0.));
			}

			setNumPileUpValue(evt);

			setValueF("evtWeight", evtWeight);
			setValueF("genEvtWeight", weightevt);

			// Needed for maxLiklyhood METHOD
			if (verbosity_) std::cout<< "produce::maxLike \n";
			maxLike(*recTau);// const pat::TauRef& rectau

			/*
				branchMap::iterator branch = branches_.find("recTau_isolationChargedHadrCands_dz");
				if (verbosity_) std::cout<< "produce::before Fill: ";
				if (verbosity_) std::cout << branch->second.valueVFloat_.size() << "; " << branch->second.valueVFloat_.back() << std::endl;
				if (branch->second.valueVFloat_.size() != 0)
				{
					if (verbosity_) std::cout << branch->second.pvalueVFloat_->size() << "; " << branch->second.pvalueVFloat_->back() << std::endl;
					if (branch->second.valueVFloat_.size() != branch->second.pvalueVFloat_->size())
						exit(0);
				}
				if (verbosity_) std::cout << "produce::before Fill: 3\n";
			*/

			//--- fill all computed quantities into TTree
			assert(ntuple_);
			if (verbosity_) std::cout << "produce::before fill\n";
			ntuple_->Fill();
			if (verbosity_) std::cout << "produce::end\n\n";
		}
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::addBranchF(const std::string& name)
{
	assert(branches_.count(name) == 0);
	std::string name_and_format = name + "/F";
	ntuple_->Branch(name.c_str(), &branches_[name].valueF_, name_and_format.c_str());
}

void TauIdMVATrainingNtupleProducerMiniAOD::addBranchI(const std::string& name)
{
	assert(branches_.count(name) == 0);
	std::string name_and_format = name + "/I";
	ntuple_->Branch(name.c_str(), &branches_[name].valueI_, name_and_format.c_str());
}


void TauIdMVATrainingNtupleProducerMiniAOD::addBranchVF(const std::string& name)
{
	assert(branches_.count(name) == 0);
	std::string name_and_format = name;

	//https://root-forum.cern.ch/t/vector-in-branch/12796/4
	gROOT->ProcessLine("#include <vector>");
	ntuple_->Branch(name.c_str(), &(branches_[name].valueVFloat_));
	ntuple_->SetBranchAddress(name.c_str(), &(branches_[name].pvalueVFloat_));

	// if (verbosity_) std::cout << "addBranchVF:"<< std::endl;
	// ntuple_->Print();
	// exit(1);
}

void TauIdMVATrainingNtupleProducerMiniAOD::printBranches(std::ostream& stream)
{
	stream << "<TauIdMVATrainingNtupleProducerMiniAOD::printBranches>:" << std::endl;
	stream << " registered branches for module = " << moduleLabel_ << std::endl;
	for(branchMap::const_iterator branch = branches_.begin(); branch != branches_.end(); ++branch)
		stream << " " << branch->first << std::endl;
	stream << std::endl;
}

void TauIdMVATrainingNtupleProducerMiniAOD::setValueF(const std::string& name, double value)
{
	if (verbosity_) std::cout << "branch = " << name << ": value = " << value << std::endl;

	branchMap::iterator branch = branches_.find(name);

	if (branch != branches_.end()) branch->second.valueF_ = value;
	else throw cms::Exception("InvalidParameter") << "No branch with name = " << name << " defined !!\n";
}

void TauIdMVATrainingNtupleProducerMiniAOD::tempSetValueVF(const std::string& name, const std::vector<Float_t>& value = {})
{
	if (verbosity_) std::cout << "tempSetValueVF;\n";
	// if (verbosity_) std::cout << "temp::" << name << " " << value.size() << "; ";
	// if (verbosity_) std::cout << "temp::" << value.back() << std::endl;branchMap::iterator branch = branches_.find(name);

	branchMap::iterator branch = branches_.find(name);
	if (branch != branches_.end())
	{
		if (verbosity_) std::cout << "\n\t\tsetting...\n" << std::endl;
		branch->second.valueVFloat_ = std::vector<Float_t>();
		branch->second.pvalueVFloat_ = &(branch->second.valueVFloat_);
		if (verbosity_) std::cout << "\t\tsett\n" << std::endl;
	}
	else throw cms::Exception("InvalidParameter") << "No branch with name = " << name << " defined !!\n";

	if (verbosity_) std::cout << "\tend tempSetValueVF\n";
}

void TauIdMVATrainingNtupleProducerMiniAOD::setValueVF(const std::string& name, const std::vector<Float_t>& value = {})
{
	if (verbosity_) std::cout << "\tsetValueVF; ";
	// if (verbosity_) std::cout << "branch = " << name << ": value = " << value << std::endl;
	if (verbosity_) std::cout << name << " " << value.size() << "; ";
	if (verbosity_) std::cout << value.back() << std::endl;

	branchMap::iterator branch = branches_.find(name);

	if (branch != branches_.end())
	{
		if (verbosity_) std::cout << "\n\t\tsetting...\n" << std::endl;
		branch->second.valueVFloat_ = value;
		branch->second.pvalueVFloat_ = &(branch->second.valueVFloat_);
		if (verbosity_) std::cout << "\t\tsett\n" << std::endl;
	}
	else throw cms::Exception("InvalidParameter") << "No branch with name = " << name << " defined !!\n";

	if (verbosity_) std::cout << "\tend setValueVF\n";
}

void TauIdMVATrainingNtupleProducerMiniAOD::setValueI(const std::string& name, int value)
{
	if (verbosity_) std::cout << "branch = " << name << ": value = " << value << std::endl;

	branchMap::iterator branch = branches_.find(name);

	if (branch != branches_.end())
		branch->second.valueI_ = value;
	else throw cms::Exception("InvalidParameter") << "No branch with name = " << name << " defined !!\n";
}

//
//-------------------------------------------------------------------------------
//

void TauIdMVATrainingNtupleProducerMiniAOD::addBranch_EnPxPyPz(const std::string& name)
{
	addBranchF(std::string(name).append("En"));
	addBranchF(std::string(name).append("P"));
	addBranchF(std::string(name).append("Px"));
	addBranchF(std::string(name).append("Py"));
	addBranchF(std::string(name).append("Pz"));
	addBranchF(std::string(name).append("M"));
	addBranchF(std::string(name).append("Eta"));
	addBranchF(std::string(name).append("Phi"));
	addBranchF(std::string(name).append("Pt"));
}

void TauIdMVATrainingNtupleProducerMiniAOD::addBranch_XYZ(const std::string& name)
{
	addBranchF(std::string(name).append("X"));
	addBranchF(std::string(name).append("Y"));
	addBranchF(std::string(name).append("Z"));
	addBranchF(std::string(name).append("R"));
	addBranchF(std::string(name).append("Mag"));
}

void TauIdMVATrainingNtupleProducerMiniAOD::addBranch_Cov(const std::string& name)
{
	addBranchF(std::string(name).append("Cxx"));
	addBranchF(std::string(name).append("Cxy"));
	addBranchF(std::string(name).append("Cxz"));
	addBranchF(std::string(name).append("Cyy"));
	addBranchF(std::string(name).append("Cyz"));
	addBranchF(std::string(name).append("Czz"));
}

void TauIdMVATrainingNtupleProducerMiniAOD::addBranch_chargedHadron(const std::string& name)
{
	addBranch_EnPxPyPz(name);
	addBranchI(std::string(name).append("Algo"));
}

void TauIdMVATrainingNtupleProducerMiniAOD::addBranch_piZero(const std::string& name)
{
	addBranch_EnPxPyPz(name);
	addBranchI(std::string(name).append("NumPFGammas"));
	addBranchI(std::string(name).append("NumPFElectrons"));
	addBranchF(std::string(name).append("MaxDeltaEta"));
	addBranchF(std::string(name).append("MaxDeltaPhi"));
}

//
//-------------------------------------------------------------------------------
//

void TauIdMVATrainingNtupleProducerMiniAOD::setValue_EnPxPyPz(const std::string& name, const reco::Candidate::LorentzVector& p4)
{
	setValueF(std::string(name).append("En"), p4.E());
	setValueF(std::string(name).append("P"), p4.P());
	setValueF(std::string(name).append("Px"), p4.px());
	setValueF(std::string(name).append("Py"), p4.py());
	setValueF(std::string(name).append("Pz"), p4.pz());
	setValueF(std::string(name).append("M"), p4.M());
	setValueF(std::string(name).append("Eta"), p4.eta());
	setValueF(std::string(name).append("Phi"), p4.phi());
	setValueF(std::string(name).append("Pt"), p4.pt());
}

template <typename T>
void TauIdMVATrainingNtupleProducerMiniAOD::setValue_XYZ(const std::string& name, const T& pos)
{
	double x = pos.x();
	double y = pos.y();
	double z = pos.z();
	double r = TMath::Sqrt(x*x + y*y);
	double mag = TMath::Sqrt(r*r + z*z);
	setValueF(std::string(name).append("X"), x);
	setValueF(std::string(name).append("Y"), y);
	setValueF(std::string(name).append("Z"), z);
	setValueF(std::string(name).append("R"), r);
	setValueF(std::string(name).append("Mag"), mag);
}

void TauIdMVATrainingNtupleProducerMiniAOD::setValue_Cov(const std::string& name, const pat::tau::TauPFEssential::CovMatrix& cov)
{
	setValueF(std::string(name).append("Cxx"), cov(0,0));
	setValueF(std::string(name).append("Cxy"), cov(0,1));
	setValueF(std::string(name).append("Cxz"), cov(0,2));
	setValueF(std::string(name).append("Cyy"), cov(1,1));
	setValueF(std::string(name).append("Cyz"), cov(1,2));
	setValueF(std::string(name).append("Czz"), cov(2,2));
}

void TauIdMVATrainingNtupleProducerMiniAOD::setValue_chargedHadron(const std::string& name, const reco::CandidatePtr chargedHadron)
{
	if (chargedHadron.isNonnull())
	{
		setValue_EnPxPyPz(name, chargedHadron->p4());
		//setValueI(std::string(name).append("Algo"), chargedHadron->algo()); // not available in MiniAOD
		setValueI(std::string(name).append("Algo"), -1);
	}
	else
	{
		setValue_EnPxPyPz(name, reco::Candidate::LorentzVector(0.,0.,0.,0.));
		setValueI(std::string(name).append("Algo"), -1);
	}
}

void TauIdMVATrainingNtupleProducerMiniAOD::setValue_piZero(const std::string& name, const reco::CandidatePtrVector signalGammas)
{
	// need to recompute piZero candidates from signalGammas saved in MiniAOD
	// downside: only one piZero can be reconstructed
	// however, with the dynamic strip reco, we anyhow never get >1 piZero...
	reco::Candidate::LorentzVector piZero(0.,0.,0.,0.);
	int nGamma = 0;
	int nElectron = 0;
	for(const auto& cand : signalGammas)
	{
		piZero += cand->p4();
		if (fabs(cand->pdgId()) == 11) nElectron++;
		if (fabs(cand->pdgId()) == 22) nGamma++;
	}
	double maxDPhi = 0;
	double maxDEta = 0;
	for(const auto& cand: signalGammas)
	{
		double dPhi = std::fabs(reco::deltaPhi(piZero.phi(), cand->p4().phi()));
		double dEta = std::fabs(piZero.eta() - cand->p4().eta());
		if (dPhi > maxDPhi) maxDPhi = dPhi;
		if (dEta > maxDEta) maxDEta = dEta;
	}
	setValue_EnPxPyPz(name, piZero);
	setValueI(std::string(name).append("NumPFGammas"), nGamma);
	setValueI(std::string(name).append("NumPFElectrons"), nElectron);
	setValueF(std::string(name).append("MaxDeltaEta"), maxDEta);
	setValueF(std::string(name).append("MaxDeltaPhi"), maxDPhi);
}

void TauIdMVATrainingNtupleProducerMiniAOD::maxLike(const pat::Tau& recTau)
{
	if (verbosity_) std::cout<< "maxLike begin \n";
	std::vector<Float_t> recTau_isolationChargedHadrCands_dz = {};
	std::vector<Float_t> recTau_isolationChargedHadrCands_pt = {};
	std::vector<Float_t> recTau_isolationChargedHadrCands_dxy = {};
	std::vector<Float_t> recTau_isolationChargedHadrCands_dRs = {};
	std::vector<Float_t> recTau_isolationGammaCands_pt = {};
	std::vector<Float_t> recTau_isolationGammaCands_dR = {};

	const auto cands = recTau.isolationChargedHadrCands();
	for(const auto& charged_hadr_cands : cands)
	{
		// wrong: float b = ((pat::PackedCandidate*)(recTau.leadChargedHadrCand()))->dz(charged_hadr_cands->vertex());
		recTau_isolationChargedHadrCands_dz.push_back(recTau.leadChargedHadrCand()->bestTrack()->dz(charged_hadr_cands->vertex()));
		recTau_isolationChargedHadrCands_dxy.push_back(recTau.leadChargedHadrCand()->bestTrack()->dxy(charged_hadr_cands->vertex()));
		recTau_isolationChargedHadrCands_pt.push_back(charged_hadr_cands->pt());
		recTau_isolationChargedHadrCands_dRs.push_back(reco::deltaR(*charged_hadr_cands, recTau));//float dr = reco::deltaR(*cand, tau);
	}

	const auto candsgamma = recTau.isolationGammaCands();
	for(const auto& iso_gamma_cands : candsgamma)
	{
		recTau_isolationGammaCands_pt.push_back(iso_gamma_cands->pt());
		recTau_isolationGammaCands_dR.push_back(reco::deltaR(*iso_gamma_cands, recTau));
	}

	if (recTau_isolationChargedHadrCands_dz.size() != 0)
	{
		setValueVF("recTau_isolationChargedHadrCands_dz", recTau_isolationChargedHadrCands_dz);
		setValueVF("recTau_isolationChargedHadrCands_pt", recTau_isolationChargedHadrCands_pt);
		setValueVF("recTau_isolationChargedHadrCands_dxy", recTau_isolationChargedHadrCands_dxy);
		setValueVF("recTau_isolationChargedHadrCands_dRs", recTau_isolationChargedHadrCands_dRs);
	}
	else
	{
		tempSetValueVF("recTau_isolationChargedHadrCands_dz");
		tempSetValueVF("recTau_isolationChargedHadrCands_dxy");
		tempSetValueVF("recTau_isolationChargedHadrCands_pt");
		tempSetValueVF("recTau_isolationChargedHadrCands_dRs");
	}

	if (recTau_isolationGammaCands_pt.size() != 0)
	{
		setValueVF("recTau_isolationGammaCands_pt", recTau_isolationGammaCands_pt);
		setValueVF("recTau_isolationGammaCands_dR", recTau_isolationGammaCands_dR);
	}
	else
	{
		tempSetValueVF("recTau_isolationGammaCands_pt");
		tempSetValueVF("recTau_isolationGammaCands_dR");
	}

	/*
		if (verbosity_) std::cout << "Chech on propper storing" << std::endl;
		branchMap::iterator branch = branches_.find("recTau_isolationChargedHadrCands_dz");
		if (verbosity_) std::cout << "\tmaxLike: " << branch->second.valueVFloat_.size() << "; " << branch->second.valueVFloat_.back() << std::endl;
		if (verbosity_) std::cout << "\tmaxLike: ";
		if (branch->second.valueVFloat_.size() != 0)
		if (verbosity_) std::cout << branch->second.pvalueVFloat_->size() << "; " << branch->second.pvalueVFloat_->back() << std::endl;
	 */
	
	if (verbosity_) std::cout<< "maxLike end \n";
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(TauIdMVATrainingNtupleProducerMiniAOD);
