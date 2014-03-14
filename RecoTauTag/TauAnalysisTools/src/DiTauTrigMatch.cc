
#include "RecoTauTag/TauAnalysisTools/interface/DiTauTrigMatch.h"
#include <TLorentzVector.h>
#include "Math/GenVector/LorentzVector.h"
#include "DataFormats/Math/interface/deltaR.h"

DiTauTrigMatch::DiTauTrigMatch(const reco::CompositeCandidate* diTau,
			       const pat::MET* met, 
			       std::vector<const reco::Candidate*>* tauTrigObj, 
			       std::vector<const reco::Candidate*>* lepTrigObj, 
			       //const reco::Candidate* genLeptonMatch,//
			       //const reco::Candidate* genTauMatch,//
			       unsigned int index, 
			       unsigned int nTotalObjects,
			       unsigned int nVtx,
                               std::vector<const pat::Tau*>* matchedTau,
                               float rho,
			       std::vector<const reco::Candidate*>* matchedL1):
  diTau_(diTau), met_(met), tauTrigObj_(tauTrigObj), lepTrigObj_(lepTrigObj), /*genTauMatch_(genTauMatch),*/index_(index), nTotalObjects_(nTotalObjects), nVtx_(nVtx), matchedTau_(matchedTau), rho_(rho), matchedL1_(matchedL1){
  
  //use convention that the first leg is lepton tag, the second one is tau
  tagLepton_ = diTau->daughter(0);
  tagTau_    = dynamic_cast<const pat::Tau*>(diTau->daughter(1)->masterClone().get() );
  genTauMatch_ = tagTau_->genParticleRef().isNonnull() ? tagTau_->genParticleRef().get() : 0 ;
  //MB unused int lepType = 0;
  if(dynamic_cast<const pat::Muon*>(diTau->daughter(0)->masterClone().get() ) ) {
    //MB unused lepType=13;
    const pat::Muon* aLep = dynamic_cast<const pat::Muon*>(diTau->daughter(0)->masterClone().get() );
    genLeptonMatch_ = aLep->genParticleRef().isNonnull() ? aLep->genParticleRef().get() : 0 ;
  }
  else if(dynamic_cast<const pat::Electron*>(diTau->daughter(0)->masterClone().get() ) ) {
    //MB unused lepType=11;
    const pat::Electron* aLep = dynamic_cast<const pat::Electron*>(diTau->daughter(0)->masterClone().get() );
    genLeptonMatch_ = aLep->genParticleRef().isNonnull() ? aLep->genParticleRef().get() : 0 ;
  }
  else if(dynamic_cast<const pat::Tau*>(diTau->daughter(0)->masterClone().get() ) ) {
    //MB unused lepType=15;
    const pat::Tau* aLep = dynamic_cast<const pat::Tau*>(diTau->daughter(0)->masterClone().get() );
    genLeptonMatch_ = aLep->genParticleRef().isNonnull() ? aLep->genParticleRef().get() : 0 ;
  }
  else{
    genLeptonMatch_ = 0;
  }

  // Create a dummy reco::Candidate Object with unrealistic LorentzVector values as a default output to return in case of a failed matching.  
  dummyCandidate_ = dynamic_cast<reco::Candidate* >(diTau->clone() );
  math::XYZTLorentzVector *v = new math::XYZTLorentzVector();
  v->SetPxPyPzE(-999.,-999.,-9999.,-999.);
  dummyCandidate_->setP4( ( (const math::XYZTLorentzVector) *v) ); 
}

DiTauTrigMatch::DiTauTrigMatch(){}

unsigned int DiTauTrigMatch::index() const {
  return index_;
}

unsigned int DiTauTrigMatch::nTotalObjects() const {
  return nTotalObjects_;
}
const reco::CompositeCandidate* DiTauTrigMatch::diTau() const {
  return diTau_;
}

const reco::Candidate* DiTauTrigMatch::tagLepton() const {
  return tagLepton_;
}

int DiTauTrigMatch::leptonPdgId() const {
  return tagLepton_->pdgId();
}

const pat::Tau* DiTauTrigMatch::tagTau() const {
  return tagTau_;
}

const pat::MET* DiTauTrigMatch::getMEt() const {
  return met_;
}

float DiTauTrigMatch::getMt() const {
  float mt2 = 2*met_->et()*tagLepton_->pt()*(1.-cos(reco::deltaPhi(met_->phi(), tagLepton_->phi() ) ) );
  
  return sqrt(mt2);
}

const reco::Candidate* DiTauTrigMatch::genLeptonMatch() const {
  if(genLeptonMatch_ != NULL) return genLeptonMatch_;
  else return dummyCandidate_; // Careful! Method return dummy object to ensure successfull termination of program. Only use genTauMatch values if "bool DiTauTrigMatch::genHadTauMatch()" returns "true"
}

const reco::Candidate* DiTauTrigMatch::genTauMatch() const {
  if(genTauMatch_ != NULL) return genTauMatch_;
  else return dummyCandidate_; // Careful! Method return dummy object to ensure successfull termination of program. Only use genTauMatch values if "bool DiTauTrigMatch::genHadTauMatch()" returns "true"
}

const reco::Candidate* DiTauTrigMatch::genTauJet() const {
  if(tagTau_->genJet() != NULL) return tagTau_->genJet();
  else return dummyCandidate_; // Careful!  Method return dummy object to ensure successfull termination of program. Only use genTauJet values if "bool DiTauTrigMatch::genHadTauMatch()" returns "true"

}

bool DiTauTrigMatch::genLeptonMatchTest() const {
  return genLeptonMatch_ != NULL;
}

bool DiTauTrigMatch::genTauMatchTest() const {
  return genTauMatch_ != NULL;
}

bool DiTauTrigMatch::genHadTauMatch() const {
  return tagTau_->genJet() != NULL;
}

bool DiTauTrigMatch::trigObjMatch(int a) const {
  return tauTrigObj_->at(a) != NULL;
}

bool DiTauTrigMatch::lepTrigObjMatch(int a) const {
  return lepTrigObj_->at(a) != NULL;
}

const pat::Tau* DiTauTrigMatch::getMatchedTau(unsigned int a) const {
  return (a < matchedTau_->size() ) ? matchedTau_->at(a) : NULL;
}
float DiTauTrigMatch::matchedTauPt(unsigned int a) const {
  return (getMatchedTau(a) != NULL) ? getMatchedTau(a)->pt() : -99.0;
}
float DiTauTrigMatch::matchedTauTrkPt(unsigned int a) const {
  return (getMatchedTau(a) != NULL) ? (getMatchedTau(a)->leadPFChargedHadrCand().isNonnull() ? getMatchedTau(a)->leadPFChargedHadrCand()->pt() : -99.0 ) : -99.0;
}
float DiTauTrigMatch::matchedTauTrkVz(unsigned int a) const {
  return (getMatchedTau(a) != NULL) ? (getMatchedTau(a)->leadPFChargedHadrCand().isNonnull() ? getMatchedTau(a)->leadPFChargedHadrCand()->vz() : -99.0 ) : -99.0;
}
float DiTauTrigMatch::matchedTauEta(unsigned int a) const {
  return (getMatchedTau(a) != NULL) ? getMatchedTau(a)->eta() : -99.0;
}
float DiTauTrigMatch::matchedTauID(unsigned int a, std::string discriminatorName) const {
  return (getMatchedTau(a) != NULL) ? getMatchedTau(a)->tauID(discriminatorName) : -99.0;
}

const reco::Candidate* DiTauTrigMatch::getMatchedL1(unsigned int a) const {
  return (a < matchedL1_->size() ) ? matchedL1_->at(a) : NULL;
}
float DiTauTrigMatch::matchedL1Pt(unsigned int a) const {
  return (getMatchedL1(a) != NULL) ? getMatchedL1(a)->pt() : -99.0;
}
float DiTauTrigMatch::matchedL1Eta(unsigned int a) const {
  return (getMatchedL1(a) != NULL) ? getMatchedL1(a)->eta() : -99.0;
}


float DiTauTrigMatch::tagTauID(std::string discriminatorName) const{
 return tagTau_->tauID(discriminatorName);  
}    

float DiTauTrigMatch::tagTauUserFloat(std::string name) const{
  return tagTau_->userFloat(name);  
}    

float DiTauTrigMatch::tagLepUserFloat(std::string name) const{
  const pat::Muon *aMu = dynamic_cast<const pat::Muon*>(diTau_->daughter(0)->masterClone().get() );
  if(aMu) return aMu->userFloat(name);
  const pat::Electron *aEl = dynamic_cast<const pat::Electron*>(diTau_->daughter(0)->masterClone().get() );
  if(aEl) return aEl->userFloat(name);
  return -99;  
} 
