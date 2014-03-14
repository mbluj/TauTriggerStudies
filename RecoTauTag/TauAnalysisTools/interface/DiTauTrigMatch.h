#ifndef RecoTauTag_TauAnalysisTools_DiTauTrigMatch_h
#define RecoTauTag_TauAnalysisTools_DiTauTrigMatch_h

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Provenance/interface/EventID.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"

class DiTauTrigMatch {
  public:
    // Default needed for persistency
    DiTauTrigMatch(); 

    DiTauTrigMatch(const reco::CompositeCandidate* diTau, 
		   const pat::MET* met,
		   std::vector<const reco::Candidate*>* tauTrigObj,
                   std::vector<const reco::Candidate*>* lepTrigObj,
		   //const reco::Candidate* genLeptonMatch, //
		   //const reco::Candidate* genTauMatch, //needed? 
		   unsigned int index, 
		   unsigned int nTotalObjects,
		   unsigned int nVtx=0,
                   std::vector<const pat::Tau*>* matchedTau=0,
                   float rho=-99,
		   std::vector<const reco::Candidate*>* matchedL1=0);
    ~DiTauTrigMatch(){};

    // Get ditau object
    const reco::CompositeCandidate* diTau() const;

    // Get tag tau object
    const pat::Tau* tagTau() const;

    // Get lepton object
    const reco::Candidate* tagLepton() const;
    int leptonPdgId() const;

    const pat::MET* getMEt() const;

    const reco::Candidate* genTauMatch() const; 
    bool genTauMatchTest() const;

    // return true if pat::tau is matched to a hadronically decaying Gen Tau
    bool genHadTauMatch() const;

    const reco::Candidate* genTauJet() const; 

    const reco::Candidate* genLeptonMatch() const; 
    bool genLeptonMatchTest() const;

    // Get match status of trigger filter object
    bool trigObjMatch(int a) const;
    bool lepTrigObjMatch(int a) const;

    // Get matched pat::Tau and its Pt, Eta, and Discriminator
    const pat::Tau* getMatchedTau(unsigned int a) const;
    float matchedTauPt(unsigned int a) const;
    float matchedTauTrkPt(unsigned int a) const;
    float matchedTauTrkVz(unsigned int a) const;
    float matchedTauEta(unsigned int a) const;
    float matchedTauID(unsigned int a, std::string discriminatorName) const;

    const reco::Candidate* getMatchedL1(unsigned int a) const;
    float matchedL1Pt(unsigned int a) const;
    float matchedL1Eta(unsigned int a) const;

    // Get status of Discriminator 
    float tagTauID(std::string discriminatorName) const;

    // Get user float 
    float tagTauUserFloat(std::string name) const;
    float tagLepUserFloat(std::string name) const;

    // Get the index of this match in the event.
    unsigned int index() const;

    // Get the total number of reco objects in this event.
    unsigned int nTotalObjects() const;

    unsigned int nVtx() const { return nVtx_; };

    float getMt() const;

    float rho() const { return rho_; };

  private:
    const reco::CompositeCandidate* diTau_;
    const pat::Tau* tagTau_;
    const reco::Candidate* tagLepton_;
    const pat::MET* met_;
    std::vector<const reco::Candidate*>* tauTrigObj_;
    std::vector<const reco::Candidate*>* lepTrigObj_;
    unsigned int index_;
    unsigned int nTotalObjects_;
    unsigned int nVtx_;
    std::vector<const pat::Tau*>* matchedTau_;
    float rho_;
    std::vector<const reco::Candidate*>* matchedL1_;
    const reco::Candidate* genLeptonMatch_;
    const reco::Candidate* genTauMatch_;
    reco::Candidate* dummyCandidate_;

};

#endif 
