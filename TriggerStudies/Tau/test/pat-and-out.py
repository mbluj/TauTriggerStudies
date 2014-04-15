isMC = False
#Output module
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
process.patOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('patTuple.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output; you need a '*' to
    # unpack the list of commands 'patEventContent'
    #outputCommands = cms.untracked.vstring('drop *', *patEventContentNoCleaning )
    outputCommands = cms.untracked.vstring('drop *')
    )

#Taus
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
process.load("RecoTauTag.Configuration.FixedConePFTaus_cff")
#Customise fixed cone
process.fixedConePFTauProducer.chargedHadronSrc = cms.InputTag('ak5PFJetsRecoTauChargedHadrons')
process.fixedConePFTauProducer.builders[0].signalConeChargedHadrons = cms.string('0.12')
process.fixedConePFTauProducer.builders[0].isoConeChargedHadrons = cms.string('0.4')
process.fixedConePFTauProducer.builders[0].maxSignalConeChargedHadrons = cms.int32(3)
process.fixedConePFTauProducer.builders[0].signalConeNeutralHadrons = cms.string('0.15')
process.fixedConePFTauProducer.builders[0].isoConeNeutralHadrons = cms.string('0.4')
process.fixedConePFTauProducer.builders[0].signalConePiZeros = cms.string('0.15')
process.fixedConePFTauProducer.builders[0].isoConePiZeros = cms.string('0.4')
process.fixedConePFTauDiscriminationByLeadingPionPtCut.MinPtLeadingObject = 1
process.fixedConePFTauDiscriminationByLeadingPionPtCut.UseOnlyChargedHadrons = True
process.fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion.applyOccupancyCut = cms.bool(False)
process.fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion.applySumPtCut = cms.bool(True)
process.fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion.maximumSumPtCut = cms.double(3.0)
process.fixedConePFTauDiscriminationByIsolationUsingLeadingPion = process.hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr.clone(
    PFTauProducer = cms.InputTag('fixedConePFTauProducer'),
    Prediscriminants = process.fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion.Prediscriminants
)
process.fixedConePFTauIsolationChargedIsoPtSum = process.hpsPFTauMVA3IsolationChargedIsoPtSum.clone(
    PFTauProducer = cms.InputTag('fixedConePFTauProducer'),
    Prediscriminants = process.fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion.Prediscriminants
)
process.produceAndDiscriminateFixedConePFTaus += process.fixedConePFTauDiscriminationByIsolationUsingLeadingPion
process.produceAndDiscriminateFixedConePFTaus += process.fixedConePFTauIsolationChargedIsoPtSum
from RecoTauTag.RecoTau.RecoTauPiZeroProducer_cfi import ak5PFJetsRecoTauPiZeros
process.ak5PFJetsRecoTauPiZeros = ak5PFJetsRecoTauPiZeros
process.recoTauFixedConeSequence = cms.Sequence(
    process.ak5PFJetsRecoTauPiZeros +
    process.ak5PFJetsRecoTauChargedHadrons +
    process.produceAndDiscriminateFixedConePFTaus
    )

# process.patDefaultSequence
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.tauTools import *
#HPS
switchToPFTauHPS(process)
#Fixed cone
process.patTausFixedCone = process.patTaus.clone(
    tauSource = cms.InputTag('fixedConePFTauProducer'),
    tauIDSources = cms.PSet(
       byLeadingPion = cms.InputTag('fixedConePFTauDiscriminationByLeadingPionPtCut'),
       byTrackIsolation = cms.InputTag('fixedConePFTauDiscriminationByTrackIsolationUsingLeadingPion'),
       byIsolation = cms.InputTag('fixedConePFTauDiscriminationByIsolationUsingLeadingPion'),
       againstElectron = cms.InputTag('fixedConePFTauDiscriminationAgainstElectron'),
       againstMuon = cms.InputTag('fixedConePFTauDiscriminationAgainstMuon'),
       chargedIsoPtSum = cms.InputTag('fixedConePFTauIsolationChargedIsoPtSum')
    ),
    userIsolation = cms.PSet(),
    tauJetCorrFactorsSource = cms.VInputTag(),
    isoDeposits = cms.PSet(),
    tauTransverseImpactParameterSource = cms.InputTag(''),
    genParticleMatch = cms.InputTag('tauMatchFixedCone'),
    genJetMatch = cms.InputTag('tauGenJetMatchFixedCone')
    )
process.tauMatchFixedCone = process.tauMatch.clone(
        src = cms.InputTag('fixedConePFTauProducer')
        )
process.tauGenJetMatchFixedCone = process.tauGenJetMatch.clone(
        src = cms.InputTag('fixedConePFTauProducer')
        )
if not isMC:
    process.patTausFixedCone.addGenMatch = False
    process.patTausFixedCone.addGenJetMatch = False
else:
    process.makePatTaus += process.tauMatchFixedCone
    process.makePatTaus += process.tauGenJetMatchFixedCone
process.makePatTaus += process.patTausFixedCone
process.selectedPatTausFixedCone = process.selectedPatTaus.clone(
    src = cms.InputTag("patTausFixedCone")
)
process.patDefaultSequence.replace(process.selectedPatTaus,
                                   process.selectedPatTaus+process.selectedPatTausFixedCone)

# needed??    
# Jets
#from PhysicsTools.PatAlgos.tools.jetTools import *
#switchJetCollection(process,cms.InputTag('ak5PFJets'),
#                    doJTA        = True,
#                    doBTagging   = True,
#                    jetCorrLabel = ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])),
#                    doType1MET   = False,
#                    genJetCollection=cms.InputTag("ak5GenJets"),
#                    doJetID      = True,
#                    postfix = '',
#                    outputModules = ['patOut']
#                    )
#
# MEt
#from PhysicsTools.PatAlgos.tools.metTools import *
#addPfMET(process, 'PF')

# General settings
from PhysicsTools.PatAlgos.tools.coreTools import *
if not isMC:
    runOnData(process,postfix='',outputModules=['patOut'])
    #process.pfJetMETcorr.jetCorrLabel='ak5PFL1FastL2L3Residual'
    #process.patMETsPF.addGenMET=False
#else:
    #process.pfJetMETcorr.jetCorrLabel='ak5PFL1FastL2L3'
    #process.patMETsPF.addGenMET=True

#process.pfJetMETcorr.skipEM=False
#process.pfJetMETcorr.skipMuons=False
#process.pfJetMETcorr.skipMuonSelection='isGlobalMuon'

#removeSpecificPATObjects(process, ['Photons'],postfix='',outputModules=['patOut'])
#removeCleaning(process,postfix='',outputModules=['patOut'])
process.patDefaultSequence.remove(process.cleanPatCandidates)
process.patDefaultSequence.remove(process.countPatCandidates)
process.patDefaultSequence.remove(process.makePatPhotons)
process.patCandidateSummary.candidates.remove(cms.InputTag("patPhotons") )
process.patDefaultSequence.remove(process.selectedPatPhotons)
process.selectedPatCandidateSummary.candidates.remove(cms.InputTag("selectedPatPhotons") )

process.PFTau += process.recoTauFixedConeSequence
process.offlineSequence = cms.Sequence(
    #process.recoTauClassicHPSSequence +
    #process.produceAndDiscriminateFixedConePFTaus +
    process.PFTau +
    process.patDefaultSequence
    )

#Needed??
## pf-isolation
from CommonTools.ParticleFlow.Tools.pfIsolation import setupPFMuonIso, setupPFElectronIso
process.muIsoSequence       = cms.Sequence( setupPFMuonIso(process,'muons') )
process.electronIsoSequence = cms.Sequence( setupPFElectronIso(process,'gedGsfElectrons') )
from CommonTools.ParticleFlow.pfParticleSelection_cff import pfParticleSelectionSequence
process.pfParticleSelectionSequence = pfParticleSelectionSequence
process.pfIsolationSequence = cms.Sequence(
    process.pfParticleSelectionSequence*
    process.muIsoSequence* process.electronIsoSequence
    )
process.offlineSequence.replace(
    process.patDefaultSequence,
    process.pfIsolationSequence + process.patDefaultSequence)
        
#Custom cone size for Electron isolation
process.elPFIsoValueChargedAll04PFIdPFIso.deposits[0].vetos = cms.vstring(
    'EcalBarrel:ConeVeto(0.01)','EcalEndcaps:ConeVeto(0.015)',
    )
process.elPFIsoValueGamma04PFIdPFIso.deposits[0].vetos = cms.vstring(
    'EcalBarrel:ConeVeto(0.08)','EcalEndcaps:ConeVeto(0.08)',
    )
process.elPFIsoValuePU04PFIdPFIso.deposits[0].vetos = cms.vstring()
process.elPFIsoValueNeutral04PFIdPFIso.deposits[0].vetos = cms.vstring()

process.elPFIsoValueChargedAll04NoPFIdPFIso.deposits[0].vetos = cms.vstring(
    'EcalBarrel:ConeVeto(0.01)','EcalEndcaps:ConeVeto(0.015)',
    )
process.elPFIsoValueGamma04NoPFIdPFIso.deposits[0].vetos = cms.vstring(
    'EcalBarrel:ConeVeto(0.08)','EcalEndcaps:ConeVeto(0.08)',
    )
process.elPFIsoValuePU04NoPFIdPFIso.deposits[0].vetos = cms.vstring()
process.elPFIsoValueNeutral04PFIdPFIso.deposits[0].vetos = cms.vstring()

#Custom cone size for Muon isolation
process.muPFIsoValueChargedAll04PFIso.deposits[0].vetos = cms.vstring(
    '0.0001','Threshold(0.0)'
    )

process.patMuons.isoDeposits = cms.PSet(
    pfAllParticles   = cms.InputTag("muPFIsoDepositPUPFIso"),      # all PU   CH+MU+E
    pfChargedHadrons = cms.InputTag("muPFIsoDepositChargedPFIso"), # all noPU CH
    pfNeutralHadrons = cms.InputTag("muPFIsoDepositNeutralPFIso"), # all NH
    pfPhotons        = cms.InputTag("muPFIsoDepositGammaPFIso"),   # all PH
    user = cms.VInputTag(
        cms.InputTag("muPFIsoDepositChargedAllPFIso"),                 # all noPU CH+MU+E
        )
    )
process.patMuons.isolationValues = cms.PSet(
    pfAllParticles   = cms.InputTag("muPFIsoValuePU04PFIso"),
    pfChargedHadrons = cms.InputTag("muPFIsoValueCharged04PFIso"),
    pfNeutralHadrons = cms.InputTag("muPFIsoValueNeutral04PFIso"),
    pfPhotons        = cms.InputTag("muPFIsoValueGamma04PFIso"),
    user = cms.VInputTag(
        cms.InputTag("muPFIsoValueChargedAll04PFIso"),
        )
    )
process.patElectrons.addElectronID = False
process.patElectrons.electronIDSources = cms.PSet() #not used, potentiall problem
process.patElectrons.isoDeposits = cms.PSet(
    pfAllParticles   = cms.InputTag("elPFIsoDepositPUPFIso"),      # all PU   CH+MU+E
    pfChargedHadrons = cms.InputTag("elPFIsoDepositChargedPFIso"), # all noPU CH
    pfNeutralHadrons = cms.InputTag("elPFIsoDepositNeutralPFIso"), # all NH
    pfPhotons        = cms.InputTag("elPFIsoDepositGammaPFIso"),   # all PH
    user = cms.VInputTag(
        cms.InputTag("elPFIsoDepositChargedAllPFIso"),                 # all noPU CH+MU+E
        )
    )
process.patElectrons.isolationValues = cms.PSet(
    pfAllParticles   = cms.InputTag("elPFIsoValuePU04PFIdPFIso"),
    pfChargedHadrons = cms.InputTag("elPFIsoValueCharged04PFIdPFIso"),
    pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral04PFIdPFIso"),
    pfPhotons        = cms.InputTag("elPFIsoValueGamma04PFIdPFIso"),
    user = cms.VInputTag(
        cms.InputTag("elPFIsoValueChargedAll04PFIdPFIso"),
        )
    )
process.patElectrons.isolationValuesNoPFId = cms.PSet(
    pfAllParticles   = cms.InputTag("elPFIsoValuePU04NoPFIdPFIso"),
    pfChargedHadrons = cms.InputTag("elPFIsoValueCharged04NoPFIdPFIso"),
    pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral04NoPFIdPFIso"),
    pfPhotons        = cms.InputTag("elPFIsoValueGamma04NoPFIdPFIso"),
    user = cms.VInputTag(
        cms.InputTag("elPFIsoValueChargedAll04NoPFIdPFIso")
        )
    )

## PAT taus from HLT taus
#process.hltPatTaus = cms.EDProducer(
#    "PATTauProducer",
#    # input
#    tauSource = cms.InputTag("hltIsoMuPFTaus"),
#    # add user data
#    userData = cms.PSet(
#      # add custom classes here
#      userClasses = cms.PSet(
#        src = cms.VInputTag('')
#      ),
#      # add doubles here
#      userFloats = cms.PSet(
#        src = cms.VInputTag('')
#      ),
#      # add ints here
#      userInts = cms.PSet(
#        src = cms.VInputTag('')
#      ),
#      # add candidate ptrs here
#      userCands = cms.PSet(
#        src = cms.VInputTag('')
#      ),
#      # add "inline" functions here
#      userFunctions = cms.vstring(),
#      userFunctionLabels = cms.vstring()
#    ),
#    # jet energy corrections
#    addTauJetCorrFactors = cms.bool(False),
#    tauJetCorrFactorsSource = cms.VInputTag(cms.InputTag("patTauJetCorrFactors")),
#    # embedding objects (for Calo- and PFTaus)
#    embedLeadTrack = cms.bool(False), ## embed in AOD externally stored leading track
#    embedSignalTracks = cms.bool(False), ## embed in AOD externally stored signal tracks
#    embedIsolationTracks = cms.bool(False), ## embed in AOD externally stored isolation tracks
#    # embedding objects (for PFTaus only)
#    embedLeadPFCand = cms.bool(False), ## embed in AOD externally stored leading PFCandidate
#    embedLeadPFChargedHadrCand = cms.bool(False), ## embed in AOD externally stored leading PFChargedHadron candidate
#    embedLeadPFNeutralCand = cms.bool(False), ## embed in AOD externally stored leading PFNeutral Candidate
#    embedSignalPFCands = cms.bool(False), ## embed in AOD externally stored signal PFCandidates
#    embedSignalPFChargedHadrCands = cms.bool(False), ## embed in AOD externally stored signal PFChargedHadronCandidates
#    embedSignalPFNeutralHadrCands = cms.bool(False), ## embed in AOD externally stored signal PFNeutralHadronCandidates
#    embedSignalPFGammaCands = cms.bool(False), ## embed in AOD externally stored signal PFGammaCandidates
#    embedIsolationPFCands = cms.bool(False), ## embed in AOD externally stored isolation PFCandidates
#    embedIsolationPFChargedHadrCands = cms.bool(False), ## embed in AOD externally stored isolation PFChargedHadronCandidates
#    embedIsolationPFNeutralHadrCands = cms.bool(False), ## embed in AOD externally stored isolation PFNeutralHadronCandidates
#    embedIsolationPFGammaCands = cms.bool(False), ## embed in AOD externally stored isolation PFGammaCandidates
#
#    # embed IsoDeposits
#    isoDeposits = cms.PSet(),
#    # user defined isolation variables the variables defined here will be accessible
#    # via pat::Tau::userIsolation(IsolationKeys key) with the key as defined in
#    # DataFormats/PatCandidates/interface/Isolation.h
#    #
#    # (set Pt thresholds for PFChargedHadrons (PFGammas) to 1.0 (1.5) GeV,
#    # matching the thresholds used when computing the tau iso. discriminators
#    # in RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByIsolation_cfi.py)
#    userIsolation = cms.PSet(),
#    # tau ID (for efficiency studies)
#    addTauID     = cms.bool(True),
#    tauIDSources = cms.PSet(
#        # configure many IDs as InputTag <someName> = <someTag>
#        # you can comment out those you don't want to save some
#        # disk space
#        decayModeFinding = cms.InputTag("hltIsoMuPFTauTrackFindingDiscriminator"),
#        byIsolation = cms.InputTag("hltIsoMuPFTauLooseIsolationDiscriminatorNoFilters"),
#        byECalIsolation = cms.InputTag("hltIsoMuPFTauECalIsolationDiscriminatorNoFilters"),
#        byTrkIsolation = cms.InputTag("hltIsoMuPFTauTrkIsolationDiscriminatorNoFilters"),
#    ),
#    # mc matching configurables
#    addGenMatch      = cms.bool(False),
#    embedGenMatch    = cms.bool(False),
#    genParticleMatch = cms.InputTag(""),
#    addGenJetMatch   = cms.bool(False),
#    embedGenJetMatch = cms.bool(False),
#    genJetMatch      = cms.InputTag(""),
#    # efficiencies
#    addEfficiencies = cms.bool(False),
#    efficiencies    = cms.PSet(),
#    # resolution
#    addResolutions  = cms.bool(False),
#    resolutions     = cms.PSet()
#)
#process.hltPatTausStdVtx = process.hltPatTaus.clone(tauSource = 'hltIsoMuPFTausStdVtx')
#process.hltPatTausStdVtx.tauIDSources = cms.PSet(
#        decayModeFinding = cms.InputTag("hltIsoMuPFTauTrackFindingDiscriminatorStdVtx"),
#        byIsolation = cms.InputTag("hltIsoMuPFTauLooseIsolationDiscriminatorStdVtxNoFilters"),
#        byECalIsolation = cms.InputTag("hltIsoMuPFTauECalIsolationDiscriminatorStdVtxNoFilters"),
#        byTrkIsolation = cms.InputTag("hltIsoMuPFTauTrkIsolationDiscriminatorStdVtxNoFilters"),
#        )
#process.selectedHltPatTaus = cms.EDFilter(
#    "PATTauSelector",
#    src = cms.InputTag("hltPatTaus"),
#    cut = cms.string("pt>17"),
#    filter = cms.bool(False)
#    )
#process.selectedHltPatTausStdVtx = process.selectedHltPatTaus.clone(src='hltPatTausStdVtx')
#process.makeHltPatTaus = cms.Sequence(
#    process.hltPatTaus + process.selectedHltPatTaus +
#    process.hltPatTausStdVtx + process.selectedHltPatTausStdVtx 
#)
#process.offlineSequence += process.makeHltPatTaus

## cuts on selected pat-objects
## && offline event selection (global mu + some iso, isolated tau, mu+tau pair)

process.selectedPatJets.cut = "pt>10"
process.selectedPatMuons.cut = "pt>10 && abs(eta)<2.4 && isGlobalMuon"
process.selectedPatElectrons.cut = "pt>10 && abs(eta)<2.5"
process.selectedPatTaus.cut = "pt>15 && abs(eta)<2.3 && tauID('decayModeFinding')>0.5"
process.selectedPatTausFixedCone.cut = "pt>15 && abs(eta)<2.3 && tauID('byLeadingPion')>0.5"

process.selectedPrimaryVertices = cms.EDFilter(
    "VertexSelector",
    src = cms.InputTag('offlinePrimaryVertices'),
    cut = cms.string("isValid & ndof >= 4 & z > -24 & z < +24 & position.Rho < 2."),
    filter = cms.bool(False)                                          
)
process.primaryVertexCounter = cms.EDFilter(
    "VertexCountFilter",
    src = cms.InputTag('selectedPrimaryVertices'),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999),
    )
simpleCutsVeto = "(gsfTrack.trackerExpectedHitsInner.numberOfHits<=999"+ \
                 " && (" + \
                 " (isEB && sigmaIetaIeta<0.010 && abs(deltaPhiSuperClusterTrackAtVtx)<0.80 && "+ \
                 "          abs(deltaEtaSuperClusterTrackAtVtx)<0.007 && hadronicOverEm<0.15)"   + \
                 " || "  + \
                 " (isEE && sigmaIetaIeta<0.030 && abs(deltaPhiSuperClusterTrackAtVtx)<0.70 && "+ \
                 "          abs(deltaEtaSuperClusterTrackAtVtx)<0.010 && hadronicOverEm<999)"   + \
                 "     )"+ \
                 ")"
#it embeds only isolation
process.selectedPatElectronsUserIsoEmbedded  = cms.EDProducer(
    "ElectronsUserEmbeddedIso",
    electronTag = cms.InputTag("selectedPatElectrons"),
    )

elIsoFromReco = "(PflowIsolationVariables.sumChargedParticlePt+" \
                "max(0,PflowIsolationVariables.sumPhotonEt+" \
                "PflowIsolationVariables.sumNeutralHadronEt-" \
                "0.5*PflowIsolationVariables.sumPUPt) )/pt"
process.selectedElectrons = cms.EDFilter(
    "PATElectronSelector",
    #src = cms.InputTag("selectedPatElectronsUserEmbedded"),
    src = cms.InputTag("selectedPatElectronsUserIsoEmbedded"),
    #src = cms.InputTag("selectedPatElectrons"),
    #cut = cms.string("pt>15 && abs(eta)<2.5 && "+simpleCutsVeto),#iso??
    cut = cms.string("pt>15 && abs(eta)<2.5 && "+simpleCutsVeto+" && userFloat('PFRelIsoDB04v3')<0.50"),
    #cut = cms.string("pt>15 && abs(eta)<2.5 && "+simpleCutsVeto+" && "+elIsoFromReco+"+<0.50"),
    filter = cms.bool(False)
    )

process.selectedPatMuonsUserEmbedded = cms.EDProducer(
    "MuonsUserEmbedded",
    muonTag            = cms.InputTag("selectedPatMuons"),
    vertexTag          = cms.InputTag("offlinePrimaryVertices"),
    fitUnbiasedVertex  = cms.bool(False)
    )
process.selectedPatTausUserEmbedded = cms.EDProducer(
    "TausUserEmbedded",
    tauTag    = cms.InputTag("selectedPatTaus"),
    vertexTag = cms.InputTag("offlinePrimaryVertices"),
    )
process.selectedPatTausUserEmbeddedFixedCone = process.selectedPatTausUserEmbedded.clone(
    tauTag = cms.InputTag('selectedPatTausFixedCone')
)

muIsoFromReco = "(pfIsolationR04.sumChargedParticlePt+" \
                "max(0,pfIsolationR04.sumPhotonEt+" \
                "pfIsolationR04.sumNeutralHadronEt-" \
                "0.5*pfIsolationR04.sumPUPt) )/pt"
process.selectedMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("selectedPatMuonsUserEmbedded"),
    #src = cms.InputTag("selectedPatMuons"),
    cut = cms.string("pt>15 && abs(eta)<2.4 && isGlobalMuon && isPFMuon && isTrackerMuon && userFloat('PFRelIsoDB04v2')<0.50"),
    #cut = cms.string("pt>15 && abs(eta)<2.4 && isGlobalMuon && isPFMuon && isTrackerMuon && "+muIsoFromReco+"+<0.50"), 
    filter = cms.bool(False)
    )

process.selectedTaus  = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("selectedPatTausUserEmbedded"),
    cut = cms.string("pt>17 && abs(eta)<2.3 && tauID('decayModeFinding')>0.5"),
    filter = cms.bool(False)
    )
process.selectedTausFixedCone = process.selectedTaus.clone(
    src = cms.InputTag('selectedPatTausUserEmbeddedFixedCone'),
    cut = cms.string("pt>17 && abs(eta)<2.3 && tauID('byLeadingPion')>0.5")
)

process.isolatedElectrons = cms.EDFilter(
    "PATElectronSelector",
    src = cms.InputTag("selectedPatElectronsUserIsoEmbedded"),
    cut = cms.string("pt>15 && abs(eta)<2.5 && "+simpleCutsVeto+" && userFloat('PFRelIsoDB04v3')<0.50"),
    filter = cms.bool(False)
    )
process.isolatedElectronsCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("isolatedElectrons"),
    minNumber = cms.uint32(1)
    )
process.isolatedMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("selectedPatMuonsUserEmbedded"),
    cut = cms.string("pt>15 && abs(eta)<2.1 && isGlobalMuon && isPFMuon && isTrackerMuon && userFloat('PFRelIsoDB04v2')<0.15"),
    filter = cms.bool(False)
    )
process.isolatedMuonsCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("isolatedMuons"),
    minNumber = cms.uint32(1)
    )

process.isolatedTaus  = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("selectedPatTausUserEmbedded"),
    cut = cms.string("pt>17 && abs(eta)<2.3 && tauID('decayModeFinding')>0.5 && tauID('byLooseCombinedIsolationDeltaBetaCorr')>0.5"),
    filter = cms.bool(False)
    )
process.isolatedTausCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("isolatedTaus"),
    minNumber = cms.uint32(1)
    )

process.elTauPairs  = cms.EDProducer(
    "CandViewShallowCloneCombiner",
    decay = cms.string("isolatedElectrons isolatedTaus"),
    checkCharge = cms.bool(False),
    cut         = cms.string("sqrt((daughter(0).eta-daughter(1).eta)*(daughter(0).eta-daughter(1).eta)+  min( abs(daughter(0).phi-daughter(1).phi), 2*3.1415926 - abs(daughter(0).phi-daughter(1).phi)  ) *  min( abs(daughter(0).phi-daughter(1).phi), 2*3.1415926 - abs(daughter(0).phi-daughter(1).phi)  )  )>0.5")
    )
process.elTauPairsCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("elTauPairs"),
    minNumber = cms.uint32(1)
    )
process.muTauPairs  = cms.EDProducer(
    "CandViewShallowCloneCombiner",
    decay = cms.string("isolatedMuons isolatedTaus"),
    checkCharge = cms.bool(False),
    cut         = cms.string("sqrt((daughter(0).eta-daughter(1).eta)*(daughter(0).eta-daughter(1).eta)+  min( abs(daughter(0).phi-daughter(1).phi), 2*3.1415926 - abs(daughter(0).phi-daughter(1).phi)  ) *  min( abs(daughter(0).phi-daughter(1).phi), 2*3.1415926 - abs(daughter(0).phi-daughter(1).phi)  )  )>0.5")
    )
process.muTauPairsCounter = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("muTauPairs"),
    minNumber = cms.uint32(1)
    )

process.offlineObjectSelectionSequence = cms.Sequence(
    process.selectedPrimaryVertices+
    process.selectedPatElectronsUserIsoEmbedded+process.selectedElectrons+
    process.selectedPatMuonsUserEmbedded+process.selectedMuons+
    process.selectedPatTausUserEmbedded+process.selectedTaus+
    process.selectedPatTausUserEmbeddedFixedCone+process.selectedTausFixedCone
)
process.offlineSequence += process.offlineObjectSelectionSequence

process.offlineMuTauSelectionSequence = cms.Sequence(
    process.primaryVertexCounter+
    process.isolatedMuons+process.isolatedMuonsCounter+
    process.isolatedTaus+process.isolatedTausCounter+
    process.muTauPairs+process.muTauPairsCounter)

process.offlineElTauSelectionSequence = cms.Sequence(
    process.primaryVertexCounter+
    process.isolatedElectrons+process.isolatedElectronsCounter+
    process.isolatedTaus+process.isolatedTausCounter+
    process.elTauPairs+process.elTauPairsCounter)

process.offlineTauSelectionSequence = cms.Sequence(
    process.primaryVertexCounter+
    process.isolatedTaus+process.isolatedTausCounter)



## Customised output content
process.patOut.outputCommands = ['drop *']
process.patOut.outputCommands.append('keep *_patMETs*_*_*')
process.patOut.outputCommands.append('keep *_hltOnlineBeamSpot_*_*')
process.patOut.outputCommands.append('keep *_hltIsoMuonVertex_*_*')
process.patOut.outputCommands.append('keep *_hltIsoEleVertex_*_*')
process.patOut.outputCommands.append('keep *_hltPixelVertices_*_*')
process.patOut.outputCommands.append('keep *_hltOnlinePrimaryVertices_*_*')
process.patOut.outputCommands.append('keep *_offlinePrimaryVertices_*_*')
process.patOut.outputCommands.append('keep *_selectedPrimaryVertices_*_*')
process.patOut.outputCommands.append('keep *_hltParticleFlowForTaus_*_*')
process.patOut.outputCommands.append('keep *_particleFlow_*_*')
process.patOut.outputCommands.append('keep *_generalTracks_*_*')
process.patOut.outputCommands.append('keep *_hltIter4Merged_*_*')
process.patOut.outputCommands.append('keep *_hltPFMuonMerging_*_*')
process.patOut.outputCommands.append('keep *_hltLightPFTracks_*_*')
process.patOut.outputCommands.append('keep *_selectedHltPatTaus*_*_*')
process.patOut.outputCommands.append('keep *_selectedElectrons_*_*')
process.patOut.outputCommands.append('keep *_selectedMuons_*_*')
process.patOut.outputCommands.append('keep *_selectedTaus_*_*')
process.patOut.outputCommands.append('keep *_hltTriggerSummaryAOD_*_*')
process.patOut.outputCommands.append('keep *_TriggerResults_*_*')
process.patOut.outputCommands.append('keep *_patTrigger_*_*')
process.patOut.outputCommands.append('keep *_patTriggerEvent_*_*')
process.patOut.outputCommands.append('keep *_hltKT6PFJetsForTaus_rho_*')
process.patOut.outputCommands.append('keep *_kt6PFJets_rho_*')
process.patOut.outputCommands.append('keep *_UCT2015Producer_*_*')
process.patOut.outputCommands.append('keep *_uct2015L1ExtraParticles_*_*')
process.patOut.outputCommands.append('keep *_l1extraParticlesUCT*_*_*')
process.patOut.outputCommands.append('keep *_l1extraParticles_*_*')
process.patOut.outputCommands.append('keep *_genParticles_*_*')
process.patOut.outputCommands.append('keep *_hltMuons_*_*')
process.patOut.outputCommands.append('keep *_hltL2Muons_*_*')
process.patOut.outputCommands.append('keep *_hltL3crIsoL1sMu14erORMu16erL1f0L2f14QL3f17QL3crIsoRhoFiltered0p15_*_*')
process.patOut.outputCommands.append('keep *_hltL3MuonCandidates_*_*')
process.patOut.outputCommands.append('keep *_hltEle22WP90RhoTrackIsoFilter_*_*')
process.patOut.outputCommands.append('keep *_hltPixelMatchElectronsL1Seeded_*_*')
process.patOut.outputCommands.append('keep *_towerMaker_*_*')
process.patOut.outputCommands.append('keep *_hltTowerMakerForPF_*_*')
process.patOut.outputCommands.append('keep *_selectedTausFixedCone_*_*')
process.patOut.outputCommands.append('keep *_addPileupInfo_*_*')


## Pat trigger
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi')
process.load('PhysicsTools.PatAlgos.triggerLayer1.triggerEventProducer_cfi')
process.patTrigger.onlyStandAlone = False
process.patTriggerEvent.patTriggerMatches = cms.VInputTag()
#hltProcessName = '*'
#hltProcessName = 'TEST'
#hltProcessName = 'TauHLT'
hltProcessName = 'HLT' #keep info from oryginal triggers
process.patTrigger.processName = hltProcessName
process.patTriggerEvent.processName = hltProcessName
process.patTrgSequence = cms.Sequence(
    process.patTrigger +
    process.patTriggerEvent )

## EndPath
if not 'hltTriggerSummaryAOD' in process.__dict__:
    print "MB: Adding hltTriggerSummaryAOD"
    process.hltTriggerSummaryAOD = cms.EDProducer(
        "TriggerSummaryProducerAOD",
        processName = cms.string( "@" )
    )
    
process.endPath = cms.EndPath(
    process.hltTriggerSummaryAOD +
    process.patTrgSequence +
    process.patOut
    )
