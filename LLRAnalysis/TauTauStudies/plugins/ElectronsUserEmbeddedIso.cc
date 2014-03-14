#include "LLRAnalysis/TauTauStudies/interface/ElectronsUserEmbeddedIso.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/GeometryVector/interface/VectorUtil.h"

using namespace edm;
using namespace std;
using namespace reco;


ElectronsUserEmbeddedIso::ElectronsUserEmbeddedIso(const edm::ParameterSet & iConfig){

  electronTag_ = iConfig.getParameter<edm::InputTag>("electronTag");
 
  produces<pat::ElectronCollection>("");

}

ElectronsUserEmbeddedIso::~ElectronsUserEmbeddedIso(){}

void ElectronsUserEmbeddedIso::produce(edm::Event & iEvent, const edm::EventSetup & iSetup){

  edm::Handle<pat::ElectronCollection> electronsHandle;
  iEvent.getByLabel(electronTag_,electronsHandle);
  const pat::ElectronCollection* electrons = electronsHandle.product();

  std::auto_ptr< pat::ElectronCollection > electronsUserEmbeddedColl( new pat::ElectronCollection() ) ;

  for(unsigned int i = 0; i < electrons->size(); i++){

    pat::Electron aElectron( (*electrons)[i] );
    //MB unused const reco::GsfElectron* aGsf = static_cast<reco::GsfElectron*>(&aElectron); 

    // iso deposits   
    reco::isodeposit::AbsVetos vetos2012EBPFIdCharged; 
    reco::isodeposit::AbsVetos vetos2012EBPFIdNeutral;  
    reco::isodeposit::AbsVetos vetos2012EBPFIdPhotons;
    reco::isodeposit::AbsVetos vetos2012EEPFIdCharged; 
    reco::isodeposit::AbsVetos vetos2012EEPFIdNeutral;  
    reco::isodeposit::AbsVetos vetos2012EEPFIdPhotons;

    reco::isodeposit::AbsVetos vetos2012EBNoPFIdCharged; 
    reco::isodeposit::AbsVetos vetos2012EBNoPFIdNeutral;  
    reco::isodeposit::AbsVetos vetos2012EBNoPFIdPhotons;
    reco::isodeposit::AbsVetos vetos2012EENoPFIdCharged; 
    reco::isodeposit::AbsVetos vetos2012EENoPFIdNeutral;  
    reco::isodeposit::AbsVetos vetos2012EENoPFIdPhotons;

    // safe recommended: PFId
    vetos2012EBPFIdCharged.push_back(new reco::isodeposit::ConeVeto(reco::isodeposit::Direction(aElectron.eta(),aElectron.phi()),0.010));
    vetos2012EBPFIdPhotons.push_back(new reco::isodeposit::ConeVeto(reco::isodeposit::Direction(aElectron.eta(),aElectron.phi()),0.08));
    vetos2012EEPFIdCharged.push_back(new reco::isodeposit::ConeVeto(reco::isodeposit::Direction(aElectron.eta(),aElectron.phi()),0.015));
    vetos2012EEPFIdPhotons.push_back(new reco::isodeposit::ConeVeto(reco::isodeposit::Direction(aElectron.eta(),aElectron.phi()),0.08));
  
    // POG recommended: NoPFId
    vetos2012EENoPFIdCharged.push_back(new reco::isodeposit::ConeVeto(reco::isodeposit::Direction(aElectron.eta(),aElectron.phi()),0.015));
    vetos2012EENoPFIdPhotons.push_back(new reco::isodeposit::ConeVeto(reco::isodeposit::Direction(aElectron.eta(),aElectron.phi()),0.08));
  

    float chIso03EBPFId = 
      aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.3, vetos2012EBPFIdCharged).first;
    float nhIso03EBPFId = 
      aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.3, vetos2012EBPFIdNeutral).first;
    float phIso03EBPFId = 
      aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.3, vetos2012EBPFIdPhotons).first;
    float nhIsoPU03EBPFId = 
      aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EBPFIdNeutral).first;
    //MB unused float phIsoPU03EBPFId = 
    //MB unused  aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EBPFIdPhotons).first;

    float chIso03EEPFId = 
      aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.3, vetos2012EEPFIdCharged).first;
    float nhIso03EEPFId = 
      aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.3, vetos2012EEPFIdNeutral).first;
    float phIso03EEPFId = 
      aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.3, vetos2012EEPFIdPhotons).first;
    float nhIsoPU03EEPFId = 
      aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EEPFIdNeutral).first;
    //MB unused float phIsoPU03EEPFId = 
    //MB unused  aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EEPFIdPhotons).first;


    //MB unused float chIso03EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.3, vetos2012EBNoPFIdCharged).first;
    //MB unused float nhIso03EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.3, vetos2012EBNoPFIdNeutral).first;
    //MB unused float phIso03EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.3, vetos2012EBNoPFIdPhotons).first;
    //MB unused float nhIsoPU03EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EBNoPFIdNeutral).first;
    //MB unused float phIsoPU03EBNoPFId = 
    //MB unused  aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EBNoPFIdPhotons).first;

    //MB unused float chIso03EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.3, vetos2012EENoPFIdCharged).first;
    //MB unused float nhIso03EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.3, vetos2012EENoPFIdNeutral).first;
    //MB unused float phIso03EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.3, vetos2012EENoPFIdPhotons).first;
    //MB unused float nhIsoPU03EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EENoPFIdNeutral).first;
    //MB unused float phIsoPU03EENoPFId = 
    //MB unused  aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.3, vetos2012EENoPFIdPhotons).first;


    //////////////////////////////////////////////////////////////

    float chIso04EBPFId = 
      aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.4, vetos2012EBPFIdCharged).first;
    float nhIso04EBPFId = 
      aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.4, vetos2012EBPFIdNeutral).first;
    float phIso04EBPFId = 
      aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.4, vetos2012EBPFIdPhotons).first;
    float nhIsoPU04EBPFId = 
      aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EBPFIdNeutral).first;
    //MB unused float phIsoPU04EBPFId = 
    //MB unused  aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EBPFIdPhotons).first;
    float allChIso04EBPFId =  
      aElectron.isoDeposit(pat::User1Iso)->depositAndCountWithin(0.4, vetos2012EBPFIdCharged).first;

    float chIso04EEPFId = 
      aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.4, vetos2012EEPFIdCharged).first;
    float nhIso04EEPFId = 
      aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.4, vetos2012EEPFIdNeutral).first;
    float phIso04EEPFId = 
      aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.4, vetos2012EEPFIdPhotons).first;
    float nhIsoPU04EEPFId = 
      aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EEPFIdNeutral).first;
    //MB unused float phIsoPU04EEPFId = 
    //MB unused  aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EEPFIdPhotons).first;
    float allChIso04EEPFId =  
      aElectron.isoDeposit(pat::User1Iso)->depositAndCountWithin(0.4, vetos2012EEPFIdCharged).first;

    //MB unused float chIso04EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.4, vetos2012EBNoPFIdCharged).first;
    //MB unused float nhIso04EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.4, vetos2012EBNoPFIdNeutral).first;
    //MB unused float phIso04EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.4, vetos2012EBNoPFIdPhotons).first;
    //MB unused float nhIsoPU04EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EBNoPFIdNeutral).first;
    //MB unused float phIsoPU04EBNoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EBNoPFIdPhotons).first;

    //MB unused float chIso04EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.4, vetos2012EENoPFIdCharged).first;
    //MB unused float nhIso04EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.4, vetos2012EENoPFIdNeutral).first;
    //MB unused float phIso04EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.4, vetos2012EENoPFIdPhotons).first;
    //MB unused float nhIsoPU04EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EENoPFIdNeutral).first;
    //MB unused float phIsoPU04EENoPFId = 
    //MB unused   aElectron.isoDeposit(pat::PfAllParticleIso)->depositAndCountWithin(0.4, vetos2012EENoPFIdPhotons).first;


    //////////////////////////////////////////////////////////////////////////////////////////////

    float chIso03PFId =
      (aElectron.isEB())*chIso03EBPFId + (aElectron.isEE())*chIso03EEPFId ;
    float nhIso03PFId = 
      (aElectron.isEB())*nhIso03EBPFId + (aElectron.isEE())*nhIso03EEPFId ;
    float phIso03PFId = 
      (aElectron.isEB())*phIso03EBPFId + (aElectron.isEE())*phIso03EEPFId ;
    float nhIsoPU03PFId =
      (aElectron.isEB())*nhIsoPU03EBPFId + (aElectron.isEE())*nhIsoPU03EEPFId ;

    float chIso04PFId = 
      (aElectron.isEB())*chIso04EBPFId + (aElectron.isEE())*chIso04EEPFId ;
    float nhIso04PFId =
      (aElectron.isEB())*nhIso04EBPFId + (aElectron.isEE())*nhIso04EEPFId ;
    float phIso04PFId =
      (aElectron.isEB())*phIso04EBPFId + (aElectron.isEE())*phIso04EEPFId ;
    float nhIsoPU04PFId = 
      (aElectron.isEB())*nhIsoPU04EBPFId + (aElectron.isEE())*nhIsoPU04EEPFId ;
    float allChIso04PFId =  
      (aElectron.isEB())*allChIso04EBPFId + (aElectron.isEE())*allChIso04EEPFId ;

    //MB unused float chIso03NoPFId =
    //MB unused   (aElectron.isEB())*chIso03EBNoPFId + (aElectron.isEE())*chIso03EENoPFId ;
    //MB unused float nhIso03NoPFId = 
    //MB unused   (aElectron.isEB())*nhIso03EBNoPFId + (aElectron.isEE())*nhIso03EENoPFId ;
    //MB unused float phIso03NoPFId = 
    //MB unused   (aElectron.isEB())*phIso03EBNoPFId + (aElectron.isEE())*phIso03EENoPFId ;
    //MB unused float nhIsoPU03NoPFId =
    //MB unused   (aElectron.isEB())*nhIsoPU03EBNoPFId + (aElectron.isEE())*nhIsoPU03EENoPFId ;

    //MB unused float chIso04NoPFId = 
    //MB unused   (aElectron.isEB())*chIso04EBNoPFId + (aElectron.isEE())*chIso04EENoPFId ;
    //MB unused float nhIso04NoPFId =
    //MB unused   (aElectron.isEB())*nhIso04EBNoPFId + (aElectron.isEE())*nhIso04EENoPFId ;
    //MB unused float phIso04NoPFId =
    //MB unused   (aElectron.isEB())*phIso04EBNoPFId + (aElectron.isEE())*phIso04EENoPFId ;
    //MB unused float nhIsoPU04NoPFId = 
    //MB unused   (aElectron.isEB())*nhIsoPU04EBNoPFId + (aElectron.isEE())*nhIsoPU04EENoPFId ;


    //cout << "@@@@@@@" << endl;
    //cout << "chIso04PFId = " << chIso04PFId << endl;
    //cout << "nhIso04PFId = " << nhIso04PFId << endl;
    //cout << "phIso04PFId = " << phIso04PFId << endl;
    //cout << "chIso04PFId = " << chIso04NoPFId << endl;
    //cout << "nhIso04PFId = " << nhIso04NoPFId << endl;
    //cout << "phIso04PFId = " << phIso04NoPFId << endl;
    //cout << "@@@@@@@" << endl;


    aElectron.addUserFloat("PFRelIso03v2",
			   (chIso03PFId+nhIso03PFId+phIso03PFId)/aElectron.pt());
    aElectron.addUserFloat("PFRelIsoDB03v2",
			   (chIso03PFId+std::max(nhIso03PFId+phIso03PFId-0.5*(nhIsoPU03PFId),0.0))/aElectron.pt());
  
    aElectron.addUserFloat("PFRelIso04v2",
			   (chIso04PFId+nhIso04PFId+phIso04PFId)/aElectron.pt());
    aElectron.addUserFloat("PFRelIsoDB04v2",
			   (chIso04PFId+std::max(nhIso04PFId+phIso04PFId-0.5*(nhIsoPU04PFId),0.0))/aElectron.pt());
   
    aElectron.addUserFloat("PFRelIso04v3", 
                           (allChIso04PFId+nhIso04PFId+phIso04PFId)/aElectron.pt()); 
    aElectron.addUserFloat("PFRelIsoDB04v3", 
                           (allChIso04PFId+std::max(nhIso04PFId+phIso04PFId-0.5*(nhIsoPU04PFId),0.0))/aElectron.pt());


    //add user isolation with custom configuration for x-check
    float allChIso04v4 = aElectron.userIsolation(pat::User1Iso);
    float nhIso04v4 = aElectron.userIsolation(pat::PfNeutralHadronIso);
    float phIso04v4 = aElectron.userIsolation(pat::PfGammaIso);
    float allIsoPU04v4 = aElectron.userIsolation(pat::PfAllParticleIso);
    aElectron.addUserFloat("PFRelIsoDB04v4", 
			   (allChIso04v4+std::max(nhIso04v4+phIso04v4-0.5*(allIsoPU04v4),0.0))/aElectron.pt());

    //std::cout <<" Electron Pt : "<<aElectron.pt() << " => "<<" isoV3 "<<aElectron.userFloat("PFRelIsoDB04v3")
    //          <<" isoV4 "<<aElectron.userFloat("PFRelIsoDB04v4")<<std::endl;

    // cleaning
    for(unsigned int i = 0; i <vetos2012EBPFIdCharged.size(); i++){
      delete vetos2012EBPFIdCharged[i];
    }
    for(unsigned int i = 0; i <vetos2012EBPFIdNeutral.size(); i++){
      delete vetos2012EBPFIdNeutral[i];
    }
    for(unsigned int i = 0; i <vetos2012EBPFIdPhotons.size(); i++){
      delete vetos2012EBPFIdPhotons[i];
    }
    for(unsigned int i = 0; i <vetos2012EEPFIdCharged.size(); i++){
      delete vetos2012EEPFIdCharged[i];
    }
    for(unsigned int i = 0; i <vetos2012EEPFIdNeutral.size(); i++){
      delete vetos2012EEPFIdNeutral[i];
    }
    for(unsigned int i = 0; i <vetos2012EEPFIdPhotons.size(); i++){
      delete vetos2012EEPFIdPhotons[i];
    }
    for(unsigned int i = 0; i <vetos2012EBNoPFIdCharged.size(); i++){
      delete vetos2012EBNoPFIdCharged[i];
    }
    for(unsigned int i = 0; i <vetos2012EBNoPFIdNeutral.size(); i++){
      delete vetos2012EBNoPFIdNeutral[i];
    }
    for(unsigned int i = 0; i <vetos2012EBNoPFIdPhotons.size(); i++){
      delete vetos2012EBNoPFIdPhotons[i];
    }
    for(unsigned int i = 0; i <vetos2012EENoPFIdCharged.size(); i++){
      delete vetos2012EENoPFIdCharged[i];
    }
    for(unsigned int i = 0; i <vetos2012EENoPFIdNeutral.size(); i++){
      delete vetos2012EENoPFIdNeutral[i];
    }
    for(unsigned int i = 0; i <vetos2012EENoPFIdPhotons.size(); i++){
      delete vetos2012EENoPFIdPhotons[i];
    }

    electronsUserEmbeddedColl->push_back(aElectron);
    
  }


  iEvent.put( electronsUserEmbeddedColl );
  return;
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(ElectronsUserEmbeddedIso);


