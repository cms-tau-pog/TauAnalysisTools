#include "TauAnalysisTools/TauAnalysisTools/plugins/ParticleAntiOverlapSelector.h"

#include "CommonTools/UtilAlgos/interface/ObjectSelector.h"

#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/PFJet.h"

typedef ObjectSelector<ParticleAntiOverlapSelector<reco::CaloJet> > CaloJetAntiOverlapSelector;
typedef ObjectSelector<ParticleAntiOverlapSelector<reco::PFJet> > PFJetAntiOverlapSelector;

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(CaloJetAntiOverlapSelector);
DEFINE_FWK_MODULE(PFJetAntiOverlapSelector);
