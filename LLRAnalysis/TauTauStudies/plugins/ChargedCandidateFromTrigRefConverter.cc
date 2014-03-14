#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"

//
// class declaration
//

class ChargedCandidateFromTrigRefConverter : public edm::EDProducer {
public:
  explicit ChargedCandidateFromTrigRefConverter(const edm::ParameterSet&);
  ~ChargedCandidateFromTrigRefConverter();
  
  virtual void produce(edm::Event&, const edm::EventSetup&);

  // access to config
  edm::ParameterSet config() const { return theConfig_; }
  edm::InputTag triggerFilterMuonsSrc_;

private:
  edm::ParameterSet theConfig_;
  bool verbose_;
};

//
// class implementation
//                                                                                                         
ChargedCandidateFromTrigRefConverter::ChargedCandidateFromTrigRefConverter(const edm::ParameterSet& conf) 
  : theConfig_(conf){

  edm::LogInfo("DebugInfo") 
    << "Initializing  ChargedCandidateFromTrigRefConverter" << "\n";
  verbose_ = conf.getUntrackedParameter<bool>("verbose", false);
  triggerFilterMuonsSrc_ = conf.getParameter<edm::InputTag>("triggerFilterMuonsSrc");
 
  produces<std::vector<reco::RecoChargedCandidate> >();

}

ChargedCandidateFromTrigRefConverter::~ChargedCandidateFromTrigRefConverter(){}

void ChargedCandidateFromTrigRefConverter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

  using namespace edm;

  std::auto_ptr<std::vector<reco::RecoChargedCandidate> > result(new std::vector<reco::RecoChargedCandidate>);
  std::vector<reco::RecoChargedCandidate> outColl;

  edm::Handle<trigger::TriggerFilterObjectWithRefs> triggerFilter;
  iEvent.getByLabel(triggerFilterMuonsSrc_, triggerFilter);
  std::vector<reco::RecoChargedCandidateRef> recoCandidates;
  triggerFilter->getObjects(trigger::TriggerMuon,recoCandidates);
  for(unsigned i = 0; i < recoCandidates.size(); ++i){
    const reco::RecoChargedCandidate *aCand = recoCandidates.at(i).get();
    if(aCand) outColl.push_back(*aCand);
  }
  
  *result = outColl;
  iEvent.put(result);

}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ChargedCandidateFromTrigRefConverter);
