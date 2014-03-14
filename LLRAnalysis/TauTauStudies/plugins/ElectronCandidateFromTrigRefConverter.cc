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
#include "DataFormats/EgammaCandidates/interface/Electron.h"

//
// class declaration
//

class ElectronCandidateFromTrigRefConverter : public edm::EDProducer {
public:
  explicit ElectronCandidateFromTrigRefConverter(const edm::ParameterSet&);
  ~ElectronCandidateFromTrigRefConverter();
  
  virtual void produce(edm::Event&, const edm::EventSetup&);

  // access to config
  edm::ParameterSet config() const { return theConfig_; }
  edm::InputTag triggerFilterElectronsSrc_;

private:
  edm::ParameterSet theConfig_;
  bool verbose_;
};

//
// class implementation
//                                                                                                         
ElectronCandidateFromTrigRefConverter::ElectronCandidateFromTrigRefConverter(const edm::ParameterSet& conf) 
  : theConfig_(conf){

  edm::LogInfo("DebugInfo") 
    << "Initializing  ElectronCandidateFromTrigRefConverter" << "\n";
  verbose_ = conf.getUntrackedParameter<bool>("verbose", false);
  triggerFilterElectronsSrc_ = conf.getParameter<edm::InputTag>("triggerFilterElectronsSrc");
 
  produces<std::vector<reco::Electron> >();

}

ElectronCandidateFromTrigRefConverter::~ElectronCandidateFromTrigRefConverter(){}

void ElectronCandidateFromTrigRefConverter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){

  using namespace edm;

  std::auto_ptr<std::vector<reco::Electron> > result(new std::vector<reco::Electron>);
  std::vector<reco::Electron> outColl;

  edm::Handle<trigger::TriggerFilterObjectWithRefs> triggerFilter;
  iEvent.getByLabel(triggerFilterElectronsSrc_, triggerFilter);
  std::vector<reco::ElectronRef> recoCandidates;
  triggerFilter->getObjects(trigger::TriggerElectron,recoCandidates);
  for(unsigned i = 0; i < recoCandidates.size(); ++i){
    const reco::Electron *aCand = recoCandidates.at(i).get();
    if(aCand) outColl.push_back(*aCand);
  }
  
  *result = outColl;
  iEvent.put(result);

}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ElectronCandidateFromTrigRefConverter);
