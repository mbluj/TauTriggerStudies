
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h" 
//#include <GeneratorTau.h>
#include "L1Trigger/UCT2015/interface/ExpressionNtuple.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TH1.h"
#include <memory>
#include <math.h>

#include "RecoTauTag/TauAnalysisTools/interface/DiTauTrigMatch.h"


//////////////
// Class definition

class DiTauMatchTool : public edm::EDAnalyzer {

public:
  explicit DiTauMatchTool(const edm::ParameterSet&);
  ~DiTauMatchTool();

private:

  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;

  bool getCollections(const edm::Event&);

  uct::ExpressionNtuple<DiTauTrigMatch> ntuple_;

  edm::InputTag diTauSrc_;
  typedef std::vector<edm::InputTag> VInputTag;
  VInputTag trgTauSrc_;
  VInputTag l1TauSrc_;
  
  edm::InputTag metSrc_;
  VInputTag vtxSrc_;
  edm::InputTag rhoSrc_;
  edm::InputTag triggerSrc_;
  double maxDR_;
  std::vector<std::string> tauFiltNames ;
  std::vector<std::string> lepFiltNames ;

  bool isMC_;

  std::vector<const reco::CompositeCandidate*> diTaus_;
  std::vector<edm::Handle<std::vector<pat::Tau> > > trgTauHandle_;
  std::vector<edm::Handle<edm::View<reco::Candidate> > > l1TauHandle_;
  const pat::MET* met_;
  std::vector<edm::Handle<reco::VertexCollection> > vertices_;
  std::vector<float> vz_;
  unsigned int run_, event_, lumi_;
  //FIXMEstd::vector<float> rhos_;
  double rho_;
  edm::Handle<pat::TriggerEvent> triggerEv_;

};

//////////////
// Helper functions

// Get vector of collections of TriggerFilterObjects
//
std::vector<const reco::Candidate*> getTrigObjCandCollections(edm::Handle<pat::TriggerEvent> triggerEv, const std::string& filtername, trigger::TriggerObjectType type=trigger::TriggerTau){
  std::vector<const reco::Candidate*> output;
  pat::TriggerObjectRefVector filterObjects = triggerEv->filterObjects(filtername);

  for(unsigned int i=0; i<filterObjects.size(); ++i){
    if( !(filterObjects.at(i)->hasTriggerObjectType(type) ) ) continue;
    const reco::Candidate &object = dynamic_cast<const reco::Candidate&>(*(filterObjects.at(i) ) );
    output.push_back(&object);
  }
  return output;
}

// Method to find the best match between tag tau and trigger filter object. The best matched filter object will be returned. If there is no match within a DR < 0.5, a null pointer is returned
int findBestMatch(const reco::Candidate* tagObj,
		  std::vector<const reco::Candidate*>& filterSelection, 
		  double maxDR){
  int idx = -1;
  double bestDeltaR = -1;
  for(size_t i=0; i<filterSelection.size(); ++i){
    double deltaR = reco::deltaR(*tagObj, *filterSelection[i]);
    if(deltaR < maxDR){
      if(idx<0 || deltaR < bestDeltaR){
	idx = i;
        bestDeltaR = deltaR;
      }
    }
  }
  return idx;
}
int findBestMatch(const reco::Candidate* tagObj,
		  std::vector<const pat::Tau*>& filterSelection, 
		  double maxDR){
  int idx = -1;
  double bestDeltaR = -1;
  for(size_t i=0; i<filterSelection.size(); ++i){
    double deltaR = reco::deltaR(*tagObj, *filterSelection[i]);
    if(deltaR < maxDR){
      if(idx<0 || deltaR < bestDeltaR){
	idx = i;
        bestDeltaR = deltaR;
      }
    }
  }
  return idx;
}
//////////////
// Class implementation

DiTauMatchTool::DiTauMatchTool(const edm::ParameterSet& iConfig):
  ntuple_(iConfig.getParameterSet("ntuple") ){

  edm::Service<TFileService> fs;
  //ntuple_.initialize(*fs);
  ntuple_.initialize( fs->tFileDirectory() );

  diTauSrc_     =   iConfig.getParameter<edm::InputTag>("diTauSrc");
  trgTauSrc_    =   iConfig.getUntrackedParameter<VInputTag>("trgTauSrc",VInputTag() );
  l1TauSrc_     =   iConfig.getUntrackedParameter<VInputTag>("l1TauSrc",VInputTag() );
  triggerSrc_   =   iConfig.getParameter<edm::InputTag>("trigSrc");
  metSrc_       =   iConfig.getParameter<edm::InputTag>("metSrc");
  vtxSrc_       =   iConfig.getParameter<VInputTag>("vtxSrc");
  rhoSrc_       =   iConfig.getParameter<edm::InputTag>("rhoSrc");
  maxDR_        =   iConfig.getParameter<double>("maxDR");
  tauFiltNames  =   iConfig.getParameter< std::vector<std::string> >("tauFilterNames");
  lepFiltNames  =   iConfig.getParameter< std::vector<std::string> >("leptonFilterNames");
  isMC_         =   iConfig.getUntrackedParameter<bool>("isMC",true);

  ntuple_.tree()->Branch("vz", &vz_);
  ntuple_.tree()->Branch("run", &run_, "run/i");
  ntuple_.tree()->Branch("event", &event_, "event/i");
  ntuple_.tree()->Branch("LS", &lumi_, "LS/i");

}


DiTauMatchTool::~DiTauMatchTool(){}


void DiTauMatchTool::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  /// Get objects from Event
  getCollections(iEvent);
  if(diTaus_.size()==0) return;

  /// Get trigger objects  
  std::vector<std::vector<const reco::Candidate*> > allTauTrigObjects;
  std::vector<std::vector<const reco::Candidate*> > allLepTrigObjects;
   
  for(unsigned int i=0; i<tauFiltNames.size(); ++i){
    std::vector<const reco::Candidate*> trigObjects = getTrigObjCandCollections(triggerEv_, tauFiltNames[i], trigger::TriggerTau);
    allTauTrigObjects.push_back(trigObjects); // enter collection of trigger objects for each filter in a vector
  }

  int lepPdgId = abs(diTaus_[0]->daughter(0)->pdgId() );
  trigger::TriggerObjectType lepTrgType = trigger::TriggerMuon;
  if(lepPdgId==11)
    lepTrgType = trigger::TriggerElectron;
  else if(lepPdgId==15)
    lepTrgType = trigger::TriggerTau;
  for(unsigned int i = 0; i < lepFiltNames.size(); ++i){
    std::vector<const reco::Candidate*> trigObjects = getTrigObjCandCollections(triggerEv_, lepFiltNames[i], lepTrgType);
    allLepTrigObjects.push_back(trigObjects); // enter collection of trigger objects for each filter in a vector
  }

  //std::vector<DiTauTrigMatch*> matches;
  DiTauTrigMatch *theMatch = NULL;

  for(unsigned int i=0; i<diTaus_.size(); ++i){
    const reco::CompositeCandidate* diTau = diTaus_[i];
    std::vector<const reco::Candidate* > allBestTauFilterMatches;
    std::vector<const reco::Candidate* > allBestLepFilterMatches;
    std::vector<const pat::Tau*> allBestTrigTauMatches;
    std::vector<const reco::Candidate* > allBestL1TauMatches;

    for(unsigned int j=0; j<allTauTrigObjects.size(); ++j){
      const reco::Candidate* bestFilterMatch = NULL;
      int idx = findBestMatch(diTau->daughter(1), allTauTrigObjects[j], maxDR_);
      if( !(idx<0) )
	bestFilterMatch = (allTauTrigObjects[j])[idx];
      allBestTauFilterMatches.push_back(bestFilterMatch); // enter the best matched trigger object for each filter into a vector                    
    }    
    for(unsigned int j=0; j<allLepTrigObjects.size(); ++j){
      const reco::Candidate* bestFilterMatch = NULL;
      int idx = findBestMatch(diTau->daughter(0), allLepTrigObjects[j], maxDR_);
      if( !(idx<0) )
	bestFilterMatch = (allLepTrigObjects[j])[idx];
      allBestLepFilterMatches.push_back(bestFilterMatch); // enter the best matched trigger object for each filter into a vector                    
    }    
    for(unsigned int j=0; j<trgTauHandle_.size(); ++j){
      const pat::Tau* bestMatch = NULL;
      std::vector<const pat::Tau*> trigTaus;
      for(size_t k=0; k < (trgTauHandle_[j])->size(); ++k){
        const pat::Tau& aTau = (trgTauHandle_[j])->at(k);
        trigTaus.push_back(&aTau);
      } 
      int idx = findBestMatch(diTau->daughter(1), trigTaus, maxDR_);
      if( !(idx<0) )
	bestMatch = trigTaus[idx];
      allBestTrigTauMatches.push_back(bestMatch); // enter the best matched trigger object for each filter into a vector                    
    }       
    for(unsigned int j=0; j<l1TauHandle_.size(); ++j){
      const reco::Candidate* bestMatch = NULL;
      std::vector<const reco::Candidate*> l1Taus;
      for(size_t k=0; k < (l1TauHandle_[j])->size(); ++k){
        const reco::Candidate& aL1 = (l1TauHandle_[j])->at(k);
        l1Taus.push_back(&aL1);
      } 
      int idx = findBestMatch(diTau->daughter(1), l1Taus, maxDR_);
      if( !(idx<0) )
	bestMatch = l1Taus[idx];
      allBestL1TauMatches.push_back(bestMatch); // enter the best matched trigger object for each filter into a vector                    
    }       

    theMatch = new DiTauTrigMatch(diTau,
				  met_,
				  &allBestTauFilterMatches,
                                  &allBestLepFilterMatches,
				  i,//matches.size(),
				  diTaus_.size(),
				  (vertices_[0])->size(),
				  &allBestTrigTauMatches,
                                  rho_,
				  &allBestL1TauMatches); // create a DiTauTrigMatch object for each di-tau pair
    //matches.push_back(theMatch); 
    ntuple_.fill(*theMatch); //fill TTree
  }
//   std::cout<<"\t[DiTauMatchTool::analyze] Fill ntuple... "
// 	   <<std::flush;
//   for(size_t i = 0; i < matches.size(); ++i){
//     ntuple_.fill(*matches.at(i) );  // create TTree
//   }
  diTaus_.clear();
}

void DiTauMatchTool::beginJob(){}

void DiTauMatchTool::endJob(){}

bool DiTauMatchTool::getCollections(const edm::Event& iEvent){
  
  /// Get di-taus
  edm::Handle< std::vector<reco::CompositeCandidate> > diTauHandle;
  iEvent.getByLabel(diTauSrc_, diTauHandle);
  // Loop over objects in current collection
  diTaus_.clear();
  for(size_t j=0; j < diTauHandle->size(); ++j){
    const reco::CompositeCandidate& object = diTauHandle->at(j);
    if(object.daughter(0)->pt()>10. && fabs(object.daughter(0)->eta() )<3. &&
       object.daughter(1)->pt()>10. && fabs(object.daughter(1)->eta() )<3. &&
       reco::deltaR(object.daughter(0)->eta(), object.daughter(0)->phi(), 
		    object.daughter(1)->eta(), object.daughter(1)->phi() )>0.3 ){
      diTaus_.push_back(&object);

    }
  }
  /// Get trigger taus
  trgTauHandle_.clear();
  for(VInputTag::const_iterator trgTauSrc_it = trgTauSrc_.begin();
	  trgTauSrc_it != trgTauSrc_.end(); ++trgTauSrc_it){

    edm::Handle< std::vector<pat::Tau> > aTrgTauHandle;
    iEvent.getByLabel(*trgTauSrc_it, aTrgTauHandle);
    trgTauHandle_.push_back(aTrgTauHandle);
  }
  /// Get l1 taus
  l1TauHandle_.clear();
  for(VInputTag::const_iterator l1TauSrc_it = l1TauSrc_.begin();
	  l1TauSrc_it != l1TauSrc_.end(); ++l1TauSrc_it){

    edm::Handle<edm::View<reco::Candidate> > aL1TauHandle;
    iEvent.getByLabel(*l1TauSrc_it, aL1TauHandle);
    l1TauHandle_.push_back(aL1TauHandle);
  }

  /// Get trigger event
  iEvent.getByLabel(triggerSrc_, triggerEv_);

  /// Get MEt
  edm::Handle< std::vector<pat::MET> > metHandle;
  iEvent.getByLabel(metSrc_, metHandle);
  met_ = &(metHandle->at(0) );

  /// Get vertexes
  vertices_.clear();
  vz_.clear();
  for(VInputTag::const_iterator vtxSrc_it = vtxSrc_.begin();
      vtxSrc_it != vtxSrc_.end(); ++vtxSrc_it){

    edm::Handle<reco::VertexCollection> aVtxHandle;
    iEvent.getByLabel(*vtxSrc_it, aVtxHandle);
    vertices_.push_back(aVtxHandle);
    float aVz = (aVtxHandle->at(0) ).z();
    vz_.push_back(aVz);
  }


  /// Get rho
  edm::Handle<double> rhoHandle;
  iEvent.getByLabel(rhoSrc_, rhoHandle);
  rho_ = *(rhoHandle.product() );

  //event
  run_ = iEvent.id().run();
  event_ = iEvent.id().event();
  lumi_ = iEvent.id().luminosityBlock();

  return true;
}

//////////////
// Define plugin
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(DiTauMatchTool);
