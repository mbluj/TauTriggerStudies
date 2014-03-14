import ROOT
import math
import signal
import sys
import operator
from DataFormats.FWLite import Events, Handle

ROOT.TH1.SetDefaultSumw2()

class PATreader() :

  def __init__(self                                      , 
               files                                     , 
               basic_histos                              , 
               track_histos                              , 
               vertex_histos                             , 
               sorting_histos                            ,
               index                                     ,
               onlineTauCollections = ['onlTausPixVtx2'] , 
               keepAllTaus = False                       ) :

    self.events = Events ( files )
    self.declareHandles()
    self.breakLoop            = False
    self.keepAllTaus          = keepAllTaus
    self.allEvents            = 0
    self.failinRecoHLT        = 0
    self.failinDMHLT          = 0
    self.failinIsoHLT         = 0
    self.hasNoOnlineTrk       = 0 
    self.hasRegionJet         = 0
    self.hasRegionTrk         = 0
    self.hasRegion            = 0
    self.basic_histos         = basic_histos
    self.track_histos         = track_histos
    self.vertex_histos        = vertex_histos
    self.sorting_histos       = sorting_histos
    self.index                = index
    self.onlineTauCollections = onlineTauCollections
    
  def looper(self, maxEvents=-1, pickEvents=[], verbose=False) :
    
    signal.signal(signal.SIGINT, self.exit_gracefully)
    
    self.bookTree('syncTree', treetitle = 'Events')
    
    for loopId, event in enumerate(self.events):
      
      if self.breakLoop : break
      self.event = event
      
      if maxEvents > 0 : totEvents = maxEvents
      else             : totEvents = self.events.size()
      if maxEvents > 0 and loopId > maxEvents: break
      if loopId%(totEvents/20)==0 : print '=====> \t', round( float(loopId)/float(totEvents)*100., 0) ,'%'
      
      if event.eventAuxiliary().event() not in pickEvents and len(pickEvents)>0 : continue
      
      self.produceCollections(event, self.handles)
            
      off_vtx = [ vtx for vtx in offVtx   if self.selectVtx(vtx)                                                                              ]       
      off_tau = [ tau for tau in offTaus  if self.selectKinematics(tau, pt=20., eta=2.3) and self.tauID(tau) and bool(tau.genJet())           ]
      off_mu  = [ mu  for mu  in offMuons if self.selectKinematics(mu , pt=15., eta=2.1) and self.muonID(mu)                                  ]
      veto_mu = [ mu  for mu  in offMuons if self.selectKinematics(mu , pt=15., eta=2.4) and self.muonID(mu, iso_threshold=0.3, fullID=False) ]

      if len(off_vtx)  < 1                                 : continue 
      if len(off_mu)  != 1                                 : continue 
      if len(veto_mu)  > 1                                 : continue 
      if len(off_tau) != 1                                 : continue  
      if abs(off_vtx[0].z()-off_tau[0].vertex().z()) > 0.2 : continue  
      if off_tau[0].charge() * off_mu[0].charge() >= 0     : continue
      if self.deltaR(off_tau[0], off_mu[0]) < 0.5          : continue  
      
      tau = off_tau[0]
      mu  = off_mu [0]

      position, matchedVtx = self.findClosestVertex(off_vtx[0], onlPixVtx)
      self.index['position'].Fill(position)
      
      #continue

      tau.genLeadingTrack     = self.getGenLeadingTrack(self.getGenJetConstituents(tau))
      tau.genDM               = self.genDecayMode(self.getGenJetConstituents(tau))
      tau.offlineLeadingTrack = self.checkLeadingTrack(tau)
      if tau.offlineLeadingTrack is False : continue
      
      #if abs(onlPixVtx[0].z() - offVtx[0].z()) < 0.2: continue
      
      if verbose :
        print '\nevent', event.eventAuxiliary().event()   
        print 'tau pt', tau.pt(), '\teta', tau.eta(), '\tphi', tau.phi(), '\tcharge', tau.charge(), '\trecoDM', tau.decayMode(), '\tgenDM', tau.genDM   
  
      self.fillBasicHistos(self.basic_histos,'offTaus',tau, onlPixVtx[0], off_vtx[0])
      self.allEvents += 1
      
      self.fillEventBranches(self.tree, event)
      self.fillTauBranches  (self.tree, tau, 'offTaus') 

      #self.fillTree(self.tree, tau, event)
      #self.fillTree( self.tree, tau.vertex(), off_vtx)
      
      for onlTauColl in self.onlineTauCollections :
        HLTTaus = self.pickHLTTausCollection(onlTauColl)       
        onl_tau = self.best_matching([tau], HLTTaus , dR=0.5).values()[0]
        
        ## 31jan PATs are bugged, bypass the matching and keep on developing
        if self.keepAllTaus :
          try:
            onl_tau  = HLTTaus [0]
          except : continue
        ####################################################################
             
        tau.onlTau              = onl_tau
        tau.onlineLeadingTrack  = self.best_matching([tau.offlineLeadingTrack], [cand for cand in onlPFcandidates if cand.charge()!=0], dR=0.1).values()[0]
    
        self.fillTauBranches  (self.tree, onl_tau, onlTauColl)
        
        ## check whether Tau is reconstructed online
        if not onl_tau and not self.keepAllTaus :
          self.failinRecoHLT  += 1
        else :
          self.fillBasicHistos(self.basic_histos, onlTauColl+'_recoHLT' ,tau, onlPixVtx[0], off_vtx[0])
          ## check whether Tau has leading track online
          if onl_tau.tauID('decayModeFinding') < 0.5 and not self.keepAllTaus :
            self.fillBasicHistos(self.basic_histos, onlTauColl+'_failDM', tau, onlPixVtx[0], off_vtx[0]) 
            self.failinDMHLT  += 1
            TauJetsIter0       = self.doSomethingForFailingEvents( onlJets, tau.onlTau, onlTracks0, onlJetsPreTrk )['caloJetsForTracking']
            FullTrackJetIter0  = [tr for tr in onlTracks0]
            for tr in TauJetsIter0 : FullTrackJetIter0.append(tr)
            if tau.onlineLeadingTrack is not False :  
              self.fillVertexAssociationHistos(self.vertex_histos, onlTauColl+'_PixVtx_failDM_hasOnlTrk', offVtx[0], onlPixVtx[0])
              self.fillVertexAssociationHistos(self.vertex_histos, onlTauColl+'_MuVtx_failDM_hasOnlTrk' , offVtx[0], onlMuVtx [0])
              self.fillTrackHistos            (self.track_histos , onlTauColl+'_offTrk_failDM_hasOnlTrk', tau.offlineLeadingTrack, offVtx[0], onlPixVtx[0], onlMuVtx[0])
              self.fillTrackHistos            (self.track_histos , onlTauColl+'_onlTrk_failDM_hasOnlTrk', tau.onlineLeadingTrack , offVtx[0], onlPixVtx[0], onlMuVtx[0])
            else :
              self.hasNoOnlineTrk += 1
              if self.best_matching([tau.onlTau],TauJetsIter0).values()[0] is not False : self.hasRegionJet += 1 
              if self.best_matching([tau.onlTau],onlTracks0).values()[0]   is not False : self.hasRegionTrk += 1 
              if self.best_matching([tau.onlTau],TauJetsIter0).values()[0] is not False or \
                 self.best_matching([tau.onlTau],onlTracks0).values()[0]   is not False : self.hasRegion +=1
              self.fillVertexAssociationHistos(self.vertex_histos, onlTauColl+'_PixVtx_failDM_noOnlTrk', offVtx[0], onlPixVtx[0])
              self.fillVertexAssociationHistos(self.vertex_histos, onlTauColl+'_MuVtx_failDM_noOnlTrk' , offVtx[0], onlMuVtx [0])
              self.fillTrackHistos            (self.track_histos , onlTauColl+'_offTrk_failDM_noOnlTrk', tau.offlineLeadingTrack, offVtx[0], onlPixVtx[0], onlMuVtx[0])
          else :
            self.fillBasicHistos            (self.basic_histos  , onlTauColl+'_passDM'                 , tau, onlPixVtx[0], off_vtx[0]) 
            self.fillVertexAssociationHistos(self.vertex_histos , onlTauColl+'_PixVtx_passDM_hasOnlTrk', offVtx[0], onlPixVtx[0])
            self.fillVertexAssociationHistos(self.vertex_histos , onlTauColl+'_MuVtx_passDM_hasOnlTrk' , offVtx[0], onlMuVtx [0])
            self.fillSortingHistos          (self.sorting_histos, onlTauColl+'_2passDM'                , tau.genLeadingTrack, tau.onlineLeadingTrack)

          ## check whether Tau is isolated online
          if onl_tau.tauID('byIsolation') < 0.5 and not self.keepAllTaus : self.failinIsoHLT   += 1
          else                                                           : self.fillBasicHistos(self.basic_histos,onlTauColl+'_passIso',tau,onlPixVtx[0],off_vtx[0])
        
      self.fillTree(self.tree)
        
    self.writeTree(self.tree, self.treeFile)  
  
  def produceCollections(self, event, handles) :
    self.HLTTausCollections = {}
    for key in handles.keys() :
      try :
        handle = handles[key][0]
        label  = handles[key][1]
        event.getByLabel(label,handle)
        globals()[key] = handle.product()
        if 'onlTau' in key : self.HLTTausCollections.update({key:handle.product()})
      except :
        pass 

  def declareHandles(self) :

    self.handles = {}

    ## offline
    self.handles[ 'offTaus'             ] = [ Handle('std::vector<pat::Tau>'         ),'selectedTaus'                      ] # default HPS offline tau 
    self.handles[ 'offTaus2'            ] = [ Handle('std::vector<pat::Tau>'         ),'selectedTausFixedCone'             ] # fixed cone offline tau - offline reference most similar to online tau (selectedHltPatTausOnl2NP) 
    self.handles[ 'offMuons'            ] = [ Handle('std::vector<pat::Muon>'        ),'selectedMuons'                     ]
    self.handles[ 'offPFcandidates'     ] = [ Handle('std::vector<reco::PFCandidate>'),'particleFlow'                      ]
    self.handles[ 'offTracks'           ] = [ Handle('std::vector<reco::Track>'      ),'generalTracks'                     ]
    self.handles[ 'offVtx'              ] = [ Handle('std::vector<reco::Vertex>'     ),'selectedPrimaryVertices'           ]
     
    ## online     
    self.handles[ 'onlTausHPS'          ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausHPS'             ] # HPS at HLT
    #self.handles[ 'onlTausMuVtx'        ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTaus'                ] # old version
    self.handles[ 'onlTausMuVtx'        ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausNP'              ] # cone tau with muon-vertex
    self.handles[ 'onlTausDAVtx'        ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausOnlNP'           ] # cone tau with online DA vertex [0]
    self.handles[ 'onlTausDAVtx2'       ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausOnl2NP'          ] # cone tau with highest-weight online DA vertex
    #self.handles[ 'onlTausPixVtx'       ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausStdVtx'          ] # old version
    self.handles[ 'onlTausPixVtx'       ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxlNP'           ] # cone tau with pixel vertex [0]
    self.handles[ 'onlTausPixVtx2'      ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2NP'          ] # cone tau with closest-in-dZ pixel vertex (use it as a baseline)

    self.handles[ 'onlTausPixVtx2S12N3' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2NP'          ] # R_sgn=0.12, N=3 (as in setup v2)
    self.handles[ 'onlTausPixVtx2S12N5' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R12N5NP'     ] # R_sgn=0.12, N=5 
    self.handles[ 'onlTausPixVtx2S12NN' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R12NInfNP'   ] # R_sgn=0.12, N=999
    self.handles[ 'onlTausPixVtx2S15N3' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R15N3NP'     ] # R_sgn=0.15, N=3
    self.handles[ 'onlTausPixVtx2S15N5' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R15N5NP'     ] # R_sgn=0.15, N=5
    self.handles[ 'onlTausPixVtx2S15NN' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R15NInfNP'   ] # R_sgn=0.15, N=999
    self.handles[ 'onlTausPixVtx2S18N3' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R18N3NP'     ] # R_sgn=0.18, N=3
    self.handles[ 'onlTausPixVtx2S18N5' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R18N5NP'     ] # R_sgn=0.18, N=5
    self.handles[ 'onlTausPixVtx2S18NN' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2R18NInfNP'   ] # R_sgn=0.18, N=999 (as setup v1)
 
    self.handles[ 'onlPFcandidates'     ] = [ Handle('std::vector<reco::PFCandidate>'),'hltParticleFlowForTaus'            ]  
    self.handles[ 'onlPixTracks'        ] = [ Handle('std::vector<reco::Track>'      ),'hltPixelTracks'                    ]
    self.handles[ 'onlTracks0'          ] = [ Handle('std::vector<reco::Track>'      ),'hltPFlowTrackSelectionHighPurity'  ]
    self.handles[ 'onlTracksPre1'       ] = [ Handle('std::vector<reco::Track>'      ),'hltIter1PFJetCtfWithMaterialTracks']  
    self.handles[ 'onlTracks1'          ] = [ Handle('std::vector<reco::Track>'      ),'hltIter1Merged'                    ]
    self.handles[ 'onlTracksPre2'       ] = [ Handle('std::vector<reco::Track>'      ),'hltIter2PFJetCtfWithMaterialTracks']  
    self.handles[ 'onlTracks2'          ] = [ Handle('std::vector<reco::Track>'      ),'hltIter2Merged'                    ]
    self.handles[ 'onlTracksPre3'       ] = [ Handle('std::vector<reco::Track>'      ),'hltIter3PFJetCtfWithMaterialTracks']  
    self.handles[ 'onlTracks3'          ] = [ Handle('std::vector<reco::Track>'      ),'hltIter3Merged'                    ]
    self.handles[ 'onlTracksPre4'       ] = [ Handle('std::vector<reco::Track>'      ),'hltIter4PFJetCtfWithMaterialTracks']  
    self.handles[ 'onlTracks'           ] = [ Handle('std::vector<reco::Track>'      ),'hltPFMuonMerging'                  ]
           
    self.handles[ 'onlJets'             ] = [ Handle('std::vector<reco::CaloJet>'    ),'hltAntiKT5CaloJetsPFEt5'           ]
    self.handles[ 'onlJetsPreTrk'       ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltAntiKT5TrackJetsIter0'          ]
    self.handles[ 'onlTrkJets0'         ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter0'           ]
    self.handles[ 'onlTrkJets1'         ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter1'           ]
    self.handles[ 'onlTrkJets2'         ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter2'           ]
    self.handles[ 'onlTrkJets3'         ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter3'           ]
      
    self.handles[ 'onlPixVtx'      ] = [ Handle('std::vector<reco::Vertex>'     ),'hltPixelVertices'                  ]
    self.handles[ 'onlInterVtx'    ] = [ Handle('std::vector<reco::Vertex>'     ),'hltOnlineVerticesAfterIter0'       ]
    self.handles[ 'onlMuVtx'       ] = [ Handle('std::vector<reco::Vertex>'     ),'hltIsoMuonVertex'                  ]

  def selectVtx(self, vtx, ndof=4, max_z=24., max_rho=2.) :
    return vtx.ndof>ndof and abs(vtx.z())<max_z and abs(vtx.position().rho())<max_rho
    
  def selectKinematics(self, particle, pt, eta) :    
    return particle.pt()>pt and abs(particle.eta())<eta 

  def muonID(self, mu, iso_threshold=0.15, fullID=True) :
    if   fullID : id = mu.isGlobalMuon() and mu.isTrackerMuon() and mu.isPFMuon()
    else        : id = mu.isGlobalMuon() 
    isoHandle = mu.pfIsolationR04()
    iso       = ( (isoHandle.sumChargedHadronPt + max(0.,isoHandle.sumNeutralHadronEt + isoHandle.sumPhotonEt - 0.5*isoHandle.sumPUPt) ) / mu.pt() < iso_threshold)  
    return iso and id

  def tauID(self, tau) :
    return tau.tauID('decayModeFinding')                         > 0.5  and \
           tau.tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits') < 1.5  and \
           tau.tauID('againstMuonTight')                         > 0.5  and \
           tau.tauID('againstElectronLoose')                     > 0.5  

  def deltaPhi(self, phi1, phi2):
    PHI = abs(phi1-phi2)
    if (PHI<=math.pi):
      return PHI
    else:
      return 2*math.pi-PHI

  def checkLeadingTrack(self, tau) :
    try    : 
      if tau.leadPFChargedHadrCand().trackRef().isNull() :
        print 'event: ',self.event.eventAuxiliary().event(),'\t good offline Tau leading track has invalid leadPFChargedHadrCand().trackRef()\t SKIPPING' 
        return False
      else :
        return tau.leadPFChargedHadrCand().trackRef()
    except : 
      print 'WHAT THE FUCK'
      print 'event: ',self.event.eventAuxiliary().event(),'\t good offline Tau leading track has invalid leadPFChargedHadrCand().trackRef()\t SKIPPING' 
      return False

  def deltaR(self, p1, p2) :
    eta1 = p1.eta()
    phi1 = p1.phi()
    eta2 = p2.eta()
    phi2 = p2.phi()
    deta = eta1-eta2
    dphi = self.deltaPhi(phi1,phi2)
    return math.sqrt(deta*deta + dphi*dphi)

  def best_matching(self, coll1, coll2, dR=0.5) :
    association = {}
    for p1 in coll1 :
      tmp = {p1:False}
      for p2 in coll2 :
        if self.deltaR(p1,p2) < dR :
          dR = self.deltaR(p1,p2)
          tmp = {p1:p2}
      association.update(tmp)
    return association        

  def getGenJetConstituents(self, tau) :
    index = 0
    genJetConstituents = []
    while True :
      if bool(tau.genJet().getGenConstituent(index)) :
        genJetConstituents.append(tau.genJet().getGenConstituent(index))
        index += 1
      else :
        break
    return genJetConstituents 

  def genDecayMode(self, genJetConstituents) :
    pdgIds      = [ abs(constituent.pdgId()) for constituent in genJetConstituents ]
    photons   = pdgIds.count(22 )
    pizeros   = pdgIds.count(111)
    picharged = pdgIds.count(211)
    electrons = pdgIds.count(11 )
    muons     = pdgIds.count(13 )
  
    chargedHads = [ constituent.charge() for constituent in genJetConstituents if constituent.charge() != 0 and abs(constituent.pdgId()) != 11 and abs(constituent.pdgId()) != 13 ]
    neutralHads = [ constituent.charge() for constituent in genJetConstituents if constituent.charge() == 0 and abs(constituent.pdgId()) != 22 ]
  
    if   electrons == 1 or muons == 1           :             ##  leptonic decay
      print 'chargedHads', len(chargedHads)
      print 'neutralHads', len(neutralHads)
      print 'picharged'  , picharged
      print 'pizeros'    , pizeros
      print 'photons'    , photons
      print 'electrons'  , electrons
      print 'muons'      , muons
      return [ -99, 'tau decays into', electrons*'electrons'+muons*'muons'  ]  
    elif len(chargedHads) == 1 and photons == 0 : return [0  , 'oneProng0Pi0'   ]
    elif len(chargedHads) == 1 and photons == 2 : return [1  , 'oneProng1Pi0'   ]
    elif len(chargedHads) == 1 and photons == 4 : return [2  , 'oneProng2Pi0'   ]
    elif len(chargedHads) == 1                  : return [3  , 'oneProngOther'  ]
    elif len(chargedHads) == 3 and photons == 0 : return [10 , 'threeProng0Pi0' ]
    elif len(chargedHads) == 3 and photons == 2 : return [11 , 'threeProng1Pi0' ]
    elif len(chargedHads) == 3                  : return [12 , 'threeProngOther']
    else                                        : 
      print 'chargedHads', len(chargedHads)
      print 'neutralHads', len(neutralHads)
      print 'picharged'  , picharged
      print 'pizeros'    , pizeros
      print 'photons'    , photons
      print 'electrons'  , electrons
      print 'muons'      , muons
      return [ -99, 'bad tau' ]  
      
  def printSummary(self) :
    print 'allEvents      ' ,self.allEvents         
    print 'failinRecoHLT  ' ,self.failinRecoHLT  
    print 'failinDMHLT    ' ,self.failinDMHLT    
    print 'failinIsoHLT   ' ,self.failinIsoHLT   
    print 'hasNoOnlineTrk ' ,self.hasNoOnlineTrk   
    print 'hasRegionJet   ' ,self.hasRegionJet   
    print 'hasRegionTrk   ' ,self.hasRegionTrk   
    print 'hasRegion      ' ,self.hasRegion   

  def fillBasicHistos(self, histos, name, particle, pixVtx, offVtx) :
    try    : histos[name]['pt'           ].Fill(particle.pt()         )
    except : pass
    try    : histos[name]['gen_pt'       ].Fill(particle.genJet().pt())
    except : pass
    try    : histos[name]['eta'          ].Fill(particle.eta()        )
    except : pass
    try    : histos[name]['phi'          ].Fill(particle.phi()        )
    except : pass
    try    : histos[name]['charge'       ].Fill(particle.charge()     )
    except : pass
    try    : histos[name]['recoDM'       ].Fill(particle.decayMode()  )
    except : pass
    try    : histos[name]['genDM'        ].Fill(particle.genDM[1],1.  )
    except : pass
    try    : histos[name]['pixVtxSumPt2' ].Fill(self.onlPixSumPt2,1.  )
    except : pass
    try    : histos[name]['offVtxSumPt2' ].Fill(self.offSumPt2   ,1.  )
    except : pass
    try    : histos[name]['pixVtxTrkMult'].Fill(pixVtx.nTracks() ,1.  )
    except : pass
    try    : histos[name]['offVtxTrkMult'].Fill(offVtx.nTracks() ,1.  )
    except : pass

  def fillVertexAssociationHistos(self, histos, name, vtx1, vtx2) :
    try    : histos[name]['dxy(offlineVtx)'].Fill( math.sqrt( (vtx1.x()-vtx2.x())*(vtx1.x()-vtx2.x()) + 
                                                              (vtx1.y()-vtx2.y())*(vtx1.y()-vtx2.y()) ) )
    except : pass
    try    : histos[name]['dz(offlineVtx)' ].Fill( abs(vtx1.z()-vtx2.z()) )
    except : pass
   
  def fillTrackHistos(self, histos, name, track, offvtx, hltpixvtx, hltmuvtx) :
    try    : histos[name]['pt'                        ] .Fill(track.pt()                                     )
    except : pass
    try    : histos[name]['errPtOverPt'               ] .Fill(track.ptError()/track.pt()                     )
    except : pass
    try    : histos[name]['eta'                       ] .Fill(track.eta()                                    )
    except : pass
    try    : histos[name]['phi'                       ] .Fill(track.phi()                                    )
    except : pass
    try    : histos[name]['chi2'                      ] .Fill(track.chi2()                                   )
    except : pass
    try    : histos[name]['ndof'                      ] .Fill(track.ndof()                                   )
    except : pass
    try    : histos[name]['charge'                    ] .Fill(track.charge()                                 )
    except : pass
    try    : histos[name]['normalizedChi2'            ] .Fill(track.normalizedChi2()                         )
    except : pass
    try    : histos[name]['numberOfLostHits'          ] .Fill(track.numberOfLostHits()                       )
    except : pass
    try    : histos[name]['numberOfValidHits'         ] .Fill(track.numberOfValidHits()                      )
    except : pass
    try    : histos[name]['numberOfValidPixelHits'    ] .Fill(track.hitPattern().numberOfValidPixelHits()    )
    except : pass
    try    : histos[name]['pixelLayersWithMeasurement'] .Fill(track.hitPattern().pixelLayersWithMeasurement())
    except : pass
    try    : histos[name]['numberOfValidTrackerHits'  ] .Fill(track.hitPattern().numberOfValidTrackerHits()  )
    except : pass
    try    : histos[name]['dxy(offlineVtx)'           ] .Fill(track.dxy(offvtx.position())                   )
    except : pass
    try    : histos[name]['dz(offlineVtx)'            ] .Fill(track.dz(offvtx.position())                    )
    except : pass
    try    : histos[name]['dxy(hltPixVtx)'            ] .Fill(track.dxy(hltpixvtx.position())                )
    except : pass
    try    : histos[name]['dz(hltPixVtx)'             ] .Fill(track.dz(hltpixvtx.position())                 )
    except : pass
    try    : histos[name]['dxy(hltMuVtx)'             ] .Fill(track.dxy(hltmuvtx.position())                 )
    except : pass
    try    : histos[name]['dz(hltMuVtx)'              ] .Fill(track.dz(hltmuvtx.position())                  )
    except : pass
    try    : histos[name]['dRoffline'                 ] .Fill(deltaR(track,offTau)                           )
    except : pass
    try    : histos[name]['dRonline'                  ] .Fill(deltaR(track,onlTau)                           )
    except : pass
    try    : histos[name]['algo'                      ] .Fill(track.algo()-4                                 )
    except : pass
  
  def fillSortingHistos(self, histos, name, genTrk, onlTrk) :
    try    : histos[name]['differenceInverse'         ] .Fill(1./genTrk.pt()-1./onlTrk.pt()                           )
    except : pass
    try    : histos[name]['pull'                      ] .Fill((genTrk.pt()-onlTrk.pt()) / onlTrk.trackRef().ptError() )
    except : pass
    
  def doSomethingForFailingEvents(self, jetCollection, onlineTau, trackCollection, trackJetCollection) :
    stuff = {}
    caloJetsForTracking = self.filterCaloJetsForTracking(jetCollection, onlineTau, trackCollection, trackJetCollection)
    stuff.update({'caloJetsForTracking':caloJetsForTracking})
    return stuff
  
  def filterCaloJetsForTracking(self, jetCollection, onlineTau, trackCollection, trackJetCollection) :
    '''
    Mimics the filtering applied to calo jets online before using them as regions
    for seeding the tracking
    '''
    jetsForTracking = []
    for jet in onlJets :
      if self.deltaR(jet,onlineTau)>0.5 : continue
      if jet.pt() < 5.        : continue 
      if abs(jet.eta()) > 2.7 : continue
      ptIn  = 0.
      ptOut = 0.
      for tower in jet.getCaloConstituents() :
        try :
          mydR = self.deltaR(tower,jet)
          if   mydR < 0.2 : ptIn  += tower.pt()
          elif mydR < 0.5 : ptOut += tower.pt()      
        except : pass
      try    : frac = ptIn / (ptIn + ptOut)
      except : frac = 0.
      if frac < 0.7 : continue
  
      nmatch   = 0
      nmatchpt = 0.
      for trackJet in trackJetCollection :
        for trk in trackJet.tracks() :
          if trk.isNonnull() and trk.isAvailable() :
            if self.deltaR(trk, jet) < 0.5 :
              nmatch   += 1
              nmatchpt += trk.pt()
      
      if nmatch>0 or nmatchpt>1. : continue
  
      nmatch2   = 0
      nmatchpt2 = 0.
      for trk in trackCollection :
        if self.deltaR(trk, jet) < 0.5 :
          nmatch2 += 1
          nmatchpt2 += trk.pt()
          
      if nmatchpt2 / jet.pt() > 0.3 : continue
      jetsForTracking.append(jet)
    
    return jetsForTracking

  def pickHLTTausCollection(self, collectionName) :
    return self.HLTTausCollections[collectionName]

  def exit_gracefully(self, signal, frame):
    if sys.gettrace() is None : ## this bypasses the following if the pdb is working
      print '\n\nCaught ctrl-C command. I am going to break the loop gently.\n' 
      self.breakLoop = True
    else : 
      print '\n'
      sys.exit(0)
      
  def getGenLeadingTrack(self, getGenJetConstituents) :
    charged_hadrons = [ pi for pi in getGenJetConstituents if pi.charge() != 0 and abs(pi.pdgId()) != 11 and abs(pi.pdgId()) != 13 ] 
    charged_hadrons.sort(key=operator.methodcaller("pt"), reverse=True)    
    return charged_hadrons[0]

  def bookTree(self, treename, treetitle = 'myTree') :
    import numpy as n
    
    tree = ROOT.TTree(treename, treetitle)

    treeFile = ROOT.TFile.Open('tree.root','recreate')
    treeFile.cd()
    
    self.evt_run  = n.zeros(1, dtype=int)
    self.evt_lumi = n.zeros(1, dtype=int)
    self.evt_evt  = n.zeros(1, dtype=int)

    tree.Branch('run '  , self.evt_run , 'run/I'  )
    tree.Branch('lumi'  , self.evt_lumi, 'lumi/I' )
    tree.Branch('evt '  , self.evt_evt , 'evt/I'  )

    self.tauForTrees = {}
    for tauColl in self.handles.keys() :
      if 'Tau' not in tauColl : continue
      #tauColl = tauColl.replace('offTaus'       ,'')
      #tauColl = tauColl.replace('onlTausPixVtx2','')
      self.tauForTrees.update({tauColl:{}}) 
      tau_pt   = n.zeros(1, dtype=float) ; tau_pt [0] = -99.
      tau_eta  = n.zeros(1, dtype=float) ; tau_eta[0] = -99.
      tau_phi  = n.zeros(1, dtype=float) ; tau_phi[0] = -99.
      tau_q    = n.zeros(1, dtype=int  ) ; tau_q  [0] = -99
      tau_dm   = n.zeros(1, dtype=int  ) ; tau_dm [0] = -99
      tau_dmf  = n.zeros(1, dtype=int  ) ; tau_dmf[0] = -99
      variables = {
                   'pt'  : tau_pt  ,
                   'eta' : tau_eta ,
                   'phi' : tau_phi ,
                   'q'   : tau_q   ,
                   'dm'  : tau_dm  ,
                   'dmf' : tau_dmf ,
                   }
      self.tauForTrees[tauColl] = variables
      
    for tauColl in self.tauForTrees.keys() :
      tree.Branch(tauColl+'_pt' , self.tauForTrees[tauColl]['pt' ], tauColl+'_pt/D'  )
      tree.Branch(tauColl+'_eta', self.tauForTrees[tauColl]['eta'], tauColl+'_eta/D' )
      tree.Branch(tauColl+'_phi', self.tauForTrees[tauColl]['phi'], tauColl+'_phi/D' )
      tree.Branch(tauColl+'_q'  , self.tauForTrees[tauColl]['q'  ], tauColl+'_q/I'   )
      tree.Branch(tauColl+'_dm' , self.tauForTrees[tauColl]['dm' ], tauColl+'_dm/I'  )
      tree.Branch(tauColl+'_dmf', self.tauForTrees[tauColl]['dmf'], tauColl+'_dmf/I' )
        
    self.tree     = tree
    self.treeFile = treeFile

  def fillEventBranches(self, tree, event) :
    self.evt_run [0] = event.eventAuxiliary().run()
    self.evt_lumi[0] = event.eventAuxiliary().luminosityBlock()
    self.evt_evt [0] = event.eventAuxiliary().event()

  def fillTauBranches(self, tree, tau, tauColl) :
    #import pdb ; pdb.set_trace()
    if tau is not False :
      self.tauForTrees[tauColl]['pt' ][0] = tau.pt()
      self.tauForTrees[tauColl]['eta'][0] = tau.eta()
      self.tauForTrees[tauColl]['phi'][0] = tau.phi()
      self.tauForTrees[tauColl]['q'  ][0] = tau.charge()
      self.tauForTrees[tauColl]['dm' ][0] = tau.decayMode()
      self.tauForTrees[tauColl]['dmf'][0] = tau.tauID('decayModeFinding')
    else :
      self.tauForTrees[tauColl]['pt' ][0] = -99.
      self.tauForTrees[tauColl]['eta'][0] = -99.
      self.tauForTrees[tauColl]['phi'][0] = -99.
      self.tauForTrees[tauColl]['q'  ][0] = -99
      self.tauForTrees[tauColl]['dm' ][0] = -99
      self.tauForTrees[tauColl]['dmf'][0] = -99

  def fillTree(self, tree) :
    #import pdb ; pdb.set_trace()
    tree.Fill()

  def writeTree(self, tree, treeFile) :
    #import pdb ; pdb.set_trace()
    treeFile.cd()
    tree.Write()
    treeFile.Close()
    
  def findClosestVertex(self, myVtx, vtxCollection) :
    dzMax    = 9999.
    position = -1
    for i,vtx in enumerate(vtxCollection) :
      if abs(vtx.z() - myVtx.z()) < dzMax :
        dzMax      = abs(vtx.z() - myVtx.z())
        position   = i
        closestVtx = vtx
    return position,closestVtx    

  def vtxSumTrkPt(self, trkCollection, vtx, power=1, dz=0.1, lowerThreshold=2.5, upperThreshold=10.0) :
    pt = 0.
    for tr in trkCollection :
      if abs(tr.dz(vtx.position())) < dz :
        if tr.pt() < lowerThreshold                        : continue
        if tr.pt() > upperThreshold and upperThreshold > 0 : pt += math.pow(upperThreshold, power)
        else                                               : pt += math.pow(tr.pt()       , power)
    return pt    

  def sortVtxCollectionSumByPt2(self, trkCollection, vtxCollection, power=1, lowerThreshold=2.5, upperThreshold=10.0) :
    sumPt = []
    for vtx in vtxCollection :
      sumPt.append(self.vtxSumTrkPt(trkCollection, vtx, power, lowerThreshold=lowerThreshold, upperThreshold=upperThreshold))
    zipped = zip(sumPt,vtxCollection)
    zipped.sort(reverse=True)
    newVtxCollection = [ vtx for pt2, vtx in zipped ]
    #if self.event.eventAuxiliary().event() == 31539862 :    import pdb ; pdb.set_trace()
    return newVtxCollection














