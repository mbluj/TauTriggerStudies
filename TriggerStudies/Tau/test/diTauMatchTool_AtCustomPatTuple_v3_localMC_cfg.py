#import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.coreTools import *

#runOnMC = False
runOnMC = True

noFilters = False
#noFilters = True

useParent = False
#useParent = True

if runOnMC:
    print "Running on MC"
else:
    print "Running on Data"

process = cms.Process("TriggerMatch")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.extend(['MatchTool'])
process.MessageLogger.cerr.default.limit = -1
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options   = cms.untracked.PSet( 
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring('ProductNotFound'), #MB potentailly danger
)


#-- Calibration tag -----------------------------------------------------------
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

if runOnMC:
    #process.GlobalTag.globaltag = cms.string('START53_V7F::All')
    #process.GlobalTag.globaltag = cms.string('START53_V19D::All')
    process.GlobalTag.globaltag = cms.string('START70_V6::All')
else:
    process.GlobalTag.globaltag = cms.string('GR_P_V43D::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

#-- PAT standard config -------------------------------------------------------
#process.load("PhysicsTools.PatAlgos.patSequences_cff")
#process.load("RecoVertex.Configuration.RecoVertex_cff")


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## Dummy output for PAT. Not used in the analysis ##
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName       = cms.untracked.string('dummy.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    dropMetaData   = cms.untracked.string('DROPPED'),
    outputCommands = cms.untracked.vstring('keep *')
    )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:./patTuple.root',
    ),
    secondaryFileNames = cms.untracked.vstring(),                           
#    eventsToSkip = cms.untracked.VEventRange('203912:253:308838634',
#                                             '203912:260:316528485',
#                                             '203912:792:880340063',
#                                             '203912:1214:1244871082',
#                                             ),                           
###
#   eventsToProcess = cms.untracked.VEventRange('1:57494144',
#                                               ),
)
if runOnMC:
    process.source.fileNames = ['file:./patTuple_MC.root']

#process.load("PhysicsTools/PatAlgos/patSequences_cff")

#from PhysicsTools.PatAlgos.tools.tauTools import *
#switchToPFTauHPS(process) #create HPS Taus from the pat default sequence


# switch on PAT trigger
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger(process) #create pat trigger objects

#process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")



process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('TriggerEfficiencyTree-diTau_v8p3.root') #output file
                                                                                  )
if runOnMC:
    process.TFileService.fileName = 'TriggerEfficiencyTree-diTau_MC_v8p3.root'

###############################################
#############    User input  ##################
###############################################

# Enter a list with all trigger filter names you want to investigate.
# A bool with the same name will be created for each filter which denotes if a filter object is matched to the tag tau
tauFilterName = [
    "hltOverlapFilterIsoMu17PFTau20",
    "hltOverlapFilterIsoMu17PFTau20Track",
    "hltOverlapFilterIsoMu17LooseIsoPFTau20",
    "hltOverlapFilterIsoMu17PFTau20StdVtx",
    "hltOverlapFilterIsoMu17PFTau20TrackStdVtx",
    "hltOverlapFilterIsoMu17LooseIsoPFTau20StdVtx",
    "hltOverlapFilterIsoMu17PFTau20NP",
    "hltOverlapFilterIsoMu17PFTau20TrackNP",
    "hltOverlapFilterIsoMu17LooseIsoPFTau20NP",
    ]
lepFilterName = [
    "hltL3crIsoL1sMu14erORMu16erL1f0L2f14QL3f17QL3crIsoRhoFiltered0p15",
    "hltL3crIsoL1sMu12Eta2p1L1f0L2f12QL3f15QL3crIsoRhoFiltered0p15" #this can not work as a corresponding path is not present in a custom HLT menu
    ]

hltTau = [
    "selectedHltPatTausHPS",
    "selectedHltPatTausNP",
    "selectedHltPatTausOnlNP",
    "selectedHltPatTausOnl2NP",
    "selectedHltPatTausPxlNP",
    "selectedHltPatTausPxl2NP",
    "selectedHltPatTausPxl2R18NInfNP",
]
hltTauIDName = [
               "decayModeFinding",
               "byIsolation",
               "byIsolation5hits",
               "byIsolation3hits",
               "byECalIsolation",
               "byTrkIsolation",
               "byTrkIsolation5hits",
               "byTrkIsolation3hits",
               "againstMuonLoose",
               "againstMuonHoP",
]

l1Tau = [
    ["l1extraParticles:Central","l1Central"],
    ["l1extraParticles:Tau","l1Tau"],
    #["UCT2015Producer:RelaxedTauUnpacked","l1NewRelTau"],
    #["UCT2015Producer:IsolatedTauUnpacked","l1NewIsoTau"],
    ["uct2015L1ExtraParticles:RelaxedTau","l1NewRelTau"],
    ["uct2015L1ExtraParticles:IsolatedTau","l1NewIsoTau"],
]

#Enter a list of HPS discriminators you want to store in the output tree for the tag tau
IDName = [  
               "decayModeFinding",
               "byLooseCombinedIsolationDeltaBetaCorr3Hits",
               "byMediumCombinedIsolationDeltaBetaCorr3Hits",
               "byTightCombinedIsolationDeltaBetaCorr3Hits",
               "byCombinedIsolationDeltaBetaCorrRaw3Hits",
               "againstMuonTight",
               "againstMuonMedium",
               "againstElectronLoose",
               ]
IDNameFC = [
    "byLeadingPion",
    "byTrackIsolation",
    "byIsolation",
    "chargedIsoPtSum",
    "againstMuon",
    "againstElectron",
    ]
common_ntuple_branches = cms.PSet(
    index = cms.string("index"), # Index of reco object in the event
    nDiTaus = cms.string("nTotalObjects"), # Number of reco objects in the event
    nVtx = cms.string("nVtx"),
    rho  = cms.string("rho"),
    diTauMass = cms.string("diTau.mass"),
    diTauCharge = cms.string("diTau.charge"),

    tagTauPt = cms.string("tagTau.pt"),
    tagTauEta = cms.string("tagTau.eta"),
    tagTauPhi = cms.string("tagTau.phi"),
    tagTauMass = cms.string("tagTau.mass"),
    tagTauCharge = cms.string("tagTau.charge"),
    tagTauDecayMode = cms.string("tagTau.decayMode"),
    #tagTauTrkPt = cms.string("tagTau.leadPFChargedHadrCand.pt"),
    #tagTauTrkVz = cms.string("tagTau.leadPFChargedHadrCand.vz"),
    ##user floats
    tagTauDz = cms.string("tagTauUserFloat('dzWrtPV')"),
    
    tagLepPt = cms.string("tagLepton.pt"),
    tagLepEta = cms.string("tagLepton.eta"),
    tagLepPhi = cms.string("tagLepton.phi"),
    tagLepCharge = cms.string("tagLepton.charge"),
    tagLepPdgId = cms.string("leptonPdgId"),
    tagLepIso = cms.string("tagLepUserFloat('PFRelIsoDB04v2')"),
    ##tagLepIso = cms.string("tagLepton.userFloat('PFRelIsoDB04v2')"), #FIXME add them as tauID's #not trivial as there is not well defined base class for patLepton

    mT = cms.string("getMt"),

    tagTauGenTauJetMatch = cms.string("genHadTauMatch"),
    tagTauGenParticleMatch = cms.string("genTauMatchTest"),

    # Careful! Only use GenTauJet (returns the values of the generated tau Jet) values if "bool TauTrigMatch::GenHadTauMatch()" returns "true". Otherwise it contains (unrealsitic) default values
    genTauJetPt = cms.string("genTauJet.pt"),
    genTauJetEta = cms.string("genTauJet.eta"),
    genTauJetPhi = cms.string("genTauJet.phi"),

    # Careful! Only use GenTauMatch (returns the values of the generator particle matched to the tagTau) values if "bool TauTrigMatch::GenTauMatchTest()" returns "true". Otherwise it contains (unrealsitic) default values
    genParticleMatchPt = cms.string("genTauMatch.pt"),
    genParticleMatchEta = cms.string("genTauMatch.eta"),
    genParticleMatchPhi = cms.string("genTauMatch.phi"),
    genParticelMatchpdgId = cms.string("genTauMatch.pdgId"),
)


process.triggerMatch = cms.EDAnalyzer(
    "DiTauMatchTool",
    diTauSrc          = cms.InputTag("selectedDiTaus"),
    trgTauSrc         = cms.untracked.VInputTag(),
    l1TauSrc          = cms.untracked.VInputTag(),
    trigSrc           = cms.InputTag("patTriggerEvent"),
    metSrc            = cms.InputTag("patMETs"),
    vtxSrc            = cms.VInputTag("offlinePrimaryVertices","hltIsoMuonVertex","hltOnlinePrimaryVertices","hltPixelVertices"),
    #vtxSrc            = cms.VInputTag("offlinePrimaryVertices","hltIsoMuonVertex","hltPixelVertices"),
    rhoSrc            = cms.InputTag("hltKT6PFJetsForTaus:rho"),
    #rhoSrc            = cms.InputTag("kt6PFJets:rho"),
    ntuple            = common_ntuple_branches,
    maxDR             = cms.double(0.5), #The DeltaR parameter used for the trigger matching
    tauFilterNames    = cms.vstring(),
    leptonFilterNames = cms.vstring(),
    isMC              = cms.untracked.bool(False),
)

###############################################
common_ntuple_branchesFC = common_ntuple_branches.clone()
process.triggerMatchFC = process.triggerMatch.clone()
process.triggerMatchFC.diTauSrc = "selectedDiTausFC"
process.triggerMatchFC.ntuple = common_ntuple_branchesFC

for j in range(len(tauFilterName)):
    setattr(common_ntuple_branches, tauFilterName[j], cms.string( "trigObjMatch(%i)"%j) )
    setattr(common_ntuple_branchesFC, tauFilterName[j], cms.string( "trigObjMatch(%i)"%j) )

for j in range(len(lepFilterName)):
    setattr(common_ntuple_branches, lepFilterName[j], cms.string( "lepTrigObjMatch(%i)"%j) )
    setattr(common_ntuple_branchesFC, lepFilterName[j], cms.string( "lepTrigObjMatch(%i)"%j) )

for j in range(len(IDName)):
    setattr(common_ntuple_branches, IDName[j], cms.string( "tagTauID(\"%s\")"%IDName[j]) )
for j in range(len(IDNameFC)):
    setattr(common_ntuple_branchesFC, IDNameFC[j], cms.string( "tagTauID(\"%s\")"%IDNameFC[j]) )

for j in range(len(hltTau)):
    process.triggerMatch.trgTauSrc.append(hltTau[j])
    setattr(common_ntuple_branches, hltTau[j]+"Pt", cms.string( "matchedTauPt(%i)"%j) )
    setattr(common_ntuple_branches, hltTau[j]+"TrkPt", cms.string( "matchedTauTrkPt(%i)"%j) )
    setattr(common_ntuple_branches, hltTau[j]+"TrkVz", cms.string( "matchedTauTrkVz(%i)"%j) )
    setattr(common_ntuple_branches, hltTau[j]+"Eta", cms.string( "matchedTauEta(%i)"%j) )
    process.triggerMatchFC.trgTauSrc.append(hltTau[j])
    setattr(common_ntuple_branchesFC, hltTau[j]+"Pt", cms.string( "matchedTauPt(%i)"%j) )
    setattr(common_ntuple_branchesFC, hltTau[j]+"TrkPt", cms.string( "matchedTauTrkPt(%i)"%j) )
    setattr(common_ntuple_branchesFC, hltTau[j]+"TrkVz", cms.string( "matchedTauTrkVz(%i)"%j) )
    setattr(common_ntuple_branchesFC, hltTau[j]+"Eta", cms.string( "matchedTauEta(%i)"%j) )
    for k in range(len(hltTauIDName)):
        setattr(common_ntuple_branches, hltTau[j]+hltTauIDName[k], cms.string( "matchedTauID(%i,"%j+"\"%s\")"%hltTauIDName[k]) )
        setattr(common_ntuple_branchesFC, hltTau[j]+hltTauIDName[k], cms.string( "matchedTauID(%i,"%j+"\"%s\")"%hltTauIDName[k]) )

for j in range(len(l1Tau)):
    process.triggerMatch.l1TauSrc.append(l1Tau[j][0])
    setattr(common_ntuple_branches, l1Tau[j][1]+"Pt", cms.string( "matchedL1Pt(%i)"%j) )
    setattr(common_ntuple_branches, l1Tau[j][1]+"Eta", cms.string( "matchedL1Eta(%i)"%j) )
    process.triggerMatchFC.l1TauSrc.append(l1Tau[j][0])
    setattr(common_ntuple_branchesFC, l1Tau[j][1]+"Pt", cms.string( "matchedL1Pt(%i)"%j) )
    setattr(common_ntuple_branchesFC, l1Tau[j][1]+"Eta", cms.string( "matchedL1Eta(%i)"%j) )

process.triggerMatch.tauFilterNames = cms.vstring(tauFilterName)
process.triggerMatch.leptonFilterNames = cms.vstring(lepFilterName)
process.triggerMatchFC.tauFilterNames = cms.vstring(tauFilterName)
process.triggerMatchFC.leptonFilterNames = cms.vstring(lepFilterName)

#FIXME process.triggerMatch2.tauFilterNames = cms.vstring(tauFilterName)
#FIXME process.triggerMatch2.leptonFilterNames = cms.vstring(lepFilterName)

process.isolatedMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("selectedMuons"),
    cut = cms.string("pt>15 && abs(eta)<2.1 && isGlobalMuon && isPFMuon && isTrackerMuon && userFloat('PFRelIsoDB04v2')<0.15"),
    #cut = cms.string("pt>17 && abs(eta)<2.1 && userFloat('PFRelIsoDB04v2')<0.15"),
    filter = cms.bool(False)
    )
process.isolatedMuonsCounter = cms.EDFilter(
    #"CandViewCountFilter",
    "PATCandViewCountFilter",
    src = cms.InputTag("isolatedMuons"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(12345),
)
process.isolatedTaus  = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("selectedTaus"),
    cut = cms.string("pt>17 && abs(eta)<2.3 && tauID('decayModeFinding')>0.5 && tauID('byLooseCombinedIsolationDeltaBetaCorr')>0.5"),
    #cut = cms.string("pt>18 && abs(eta)<2.3 && tauID('decayModeFinding')>0.5 && tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits')<1.5 && tauID('againstMuonTight')>0.5 && tauID('againstElectronLoose')>0.5"),
    filter = cms.bool(False)
    )
process.isolatedTausFC  = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("selectedTausFixedCone"),
    cut = cms.string("pt>17 && abs(eta)<2.3 && tauID('byLeadingPion')>0.5 &&\
    tauID('chargedIsoPtSum')<3.0"),
    filter = cms.bool(False)
    )
process.isolatedTausCounter = cms.EDFilter(
    #"CandViewCountFilter",
    "PATCandViewCountFilter",
    src = cms.InputTag("isolatedTaus"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(12345),
)
process.isolatedTausCounterFC = process.isolatedTausCounter.clone()
process.isolatedTausCounterFC.src = "isolatedTausFC"

process.selectedDiTaus = cms.EDProducer(
    "CandViewShallowCloneCombiner",
    decay = cms.string("isolatedMuons isolatedTaus"),
    cut = cms.string("sqrt((daughter(0).eta-daughter(1).eta)*(daughter(0).eta-daughter(1).eta)+  min( abs(daughter(0).phi-daughter(1).phi), 2*3.1415926 - abs(daughter(0).phi-daughter(1).phi)  ) *  min( abs(daughter(0).phi-daughter(1).phi), 2*3.1415926 - abs(daughter(0).phi-daughter(1).phi)  )  )>0.5"),
    checkCharge = cms.bool(False)
    )
process.selectedDiTausFC = process.selectedDiTaus.clone()
process.selectedDiTausFC.decay = "isolatedMuons isolatedTausFC"
process.selectedDiTausCounter = cms.EDFilter(
        "CandViewCountFilter",
        #"PATCandViewCountFilter",
        src = cms.InputTag("selectedDiTaus"),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(12345),
        )
process.selectedDiTausCounterFC = process.selectedDiTausCounter.clone()
process.selectedDiTausCounterFC.src = "selectedDiTausFC"

process.isolatedMuonsLoose = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("selectedMuons"),
    cut = cms.string("pt>15 && abs(eta)<2.4 && isGlobalMuon && userFloat('PFRelIsoDB04v2')<0.3"),
    #cut = cms.string("pt>17 && abs(eta)<2.1 && userFloat('PFRelIsoDB04v2')<0.3"),
    filter = cms.bool(False)
    )

process.secondMuVeto = cms.EDFilter(
    #"CandViewCountFilter",
    "PATCandViewCountFilter",
    src = cms.InputTag("isolatedMuonsLoose"),
    minNumber = cms.uint32(0),
    maxNumber = cms.uint32(1),
)

#execfile('online-tau-offlineVtx.py')
process.p = cms.Path(
    #process.recoTauClassicHPSSequence*
    #process.patDefaultSequence*
    process.isolatedMuons+process.isolatedMuonsCounter+
    process.isolatedMuonsLoose+process.secondMuVeto+#swapped with muon counting
    process.isolatedTaus+process.isolatedTausCounter+
    process.selectedDiTaus+process.selectedDiTausCounter+
    #process.hltTauSequence + #to be moved after selection
    process.triggerMatch
    #+process.triggerMatch2
    )
process.pFC = cms.Path(
    #process.recoTauClassicHPSSequence*
    #process.patDefaultSequence*
    process.isolatedMuons+process.isolatedMuonsCounter+
    process.isolatedMuonsLoose+process.secondMuVeto+#swapped with muon counting
    process.isolatedTausFC+process.isolatedTausCounterFC+
    process.selectedDiTausFC+process.selectedDiTausCounterFC+
    #process.hltTauSequence + #to be moved after selection
    process.triggerMatchFC
    #+process.triggerMatch2
    )


process.end = cms.EndPath(
#    process.out
    )

process.out.fileName = 'patTuple_final.root'
process.out.outputCommands = [
    'drop *',
    'keep *_selectedHltPatTaus*_*_*',
    'keep *_isolatedMuons_*_*',
    'keep *_isolatedMuonsLoose_*_*',
    'keep *_isolatedTaus_*_*',
    'keep *_selectedDiTaus_*_*',
    'keep *_muMEtPairforMt_*_*',
    'keep *_patMETsPF_*_*',

    'keep *_hltIsoMuonVertex_*_*',
    'keep *_hltPixelVertices_*_*',
    'keep *_hltOnlinePrimaryVertices_*_*',
    'drop *_hltOnlinePrimaryVertices_WithBS_*',
    'keep *_offlinePrimaryVertices_*_*',
    'keep *_selectedPrimaryVertices_*_*',
    
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_patTriggerEvent_*_*',
    'keep *_patTrigger_*_*',
    ]

#MB local input
process.source.fileNames = [
    'file:./patTuple.root',
    #'file:./patTuple_625c1.root',
]

if useParent:
    print "Using parent files"
    process.source.secondaryFileNames.extend( [
        ] )
    

if noFilters: #remove filtering
    print "Removing offline filters"
    process.p.remove(process.isolatedMuonsCounter)
    process.p.remove(process.secondMuVeto)
    process.p.remove(process.isolatedTausCounter)
    process.p.remove(process.selectedDiTausCounter)

