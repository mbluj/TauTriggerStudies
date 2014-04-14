## DA vertices at online
process.hltOnlinePrimaryVertices = cms.EDProducer( "PrimaryVertexProducer",
    vertexCollections = cms.VPSet( 
      cms.PSet(  maxDistanceToBeam = cms.double( 1.0 ),
        useBeamConstraint = cms.bool( False ),
        minNdof = cms.double( 0.0 ),
        algorithm = cms.string( "AdaptiveVertexFitter" ),
        label = cms.string( "" )
      )#,
      #MB do not reproduce "WithBS" collection which is not used by tau
      #cms.PSet(  maxDistanceToBeam = cms.double( 1.0 ),
      #  useBeamConstraint = cms.bool( True ),
      #  minNdof = cms.double( 2.0 ),
      #  algorithm = cms.string( "AdaptiveVertexFitter" ),
      #  label = cms.string( "WithBS" )
      #)
    ),
    verbose = cms.untracked.bool( False ),
    TkFilterParameters = cms.PSet( 
      maxNormalizedChi2 = cms.double( 20.0 ),
      minPt = cms.double( 0.0 ),
      algorithm = cms.string( "filter" ),
      maxD0Significance = cms.double( 5.0 ),
      trackQuality = cms.string( "any" ),
      minPixelLayersWithHits = cms.int32( 2 ),
      minSiliconLayersWithHits = cms.int32( 5 )
    ),
    beamSpotLabel = cms.InputTag( "hltOnlineBeamSpot" ),
    TrackLabel = cms.InputTag( "hltPFMuonMerging" ),
    TkClusParameters = cms.PSet( 
      TkDAClusParameters = cms.PSet( 
        d0CutOff = cms.double( 3.0 ),
        Tmin = cms.double( 4.0 ),
        dzCutOff = cms.double( 4.0 ),
        coolingFactor = cms.double( 0.6 ),
        use_vdt = cms.untracked.bool( True ),
        vertexSize = cms.double( 0.01 )
      ),
      algorithm = cms.string( "DA_vect" ) #MB DA->DA_vec (faster algorithm)
    )
)

# Jets for rho
process.hltKT6PFJetsForTaus = cms.EDProducer( "FastjetJetProducer",
    Active_Area_Repeats = cms.int32( 1 ),
    doAreaFastjet = cms.bool( False ),
    voronoiRfact = cms.double( 0.9 ),
    maxBadHcalCells = cms.uint32( 9999999 ),
    doAreaDiskApprox = cms.bool( True ),
    maxRecoveredEcalCells = cms.uint32( 9999999 ),
    jetType = cms.string( "PFJet" ),
    minSeed = cms.uint32( 14327 ),
    Ghost_EtaMax = cms.double( 5.0 ),
    doRhoFastjet = cms.bool( True ),
    jetAlgorithm = cms.string( "Kt" ),
    nSigmaPU = cms.double( 1.0 ),
    GhostArea = cms.double( 0.01 ),
    Rho_EtaMax = cms.double( 2.5 ),
    maxBadEcalCells = cms.uint32( 9999999 ),
    useDeterministicSeed = cms.bool( True ),
    doPVCorrection = cms.bool( False ),
    maxRecoveredHcalCells = cms.uint32( 9999999 ),
    rParam = cms.double( 0.6 ),
    maxProblematicHcalCells = cms.uint32( 9999999 ),
    doOutputJets = cms.bool( True ),
    src = cms.InputTag( "hltParticleFlowForTaus" ),
    inputEtMin = cms.double( 0.0 ),
    puPtMin = cms.double( 10.0 ),
    srcPVs = cms.InputTag( "NotUsed" ),
    jetPtMin = cms.double( 1.0 ),
    radiusPU = cms.double( 0.5 ),
    maxProblematicEcalCells = cms.uint32( 9999999 ),
    doPUOffsetCorr = cms.bool( False ),
    inputEMin = cms.double( 0.0 ),
    subtractorName = cms.string( "" ),
    MinVtxNdof = cms.int32( 0 ),
    MaxVtxZ = cms.double( 15.0 ),
    UseOnlyVertexTracks = cms.bool( False ),
    UseOnlyOnePV = cms.bool( False ),
    DzTrVtxMax = cms.double( 0.0 ),
    sumRecHits = cms.bool( False ),
    DxyTrVtxMax = cms.double( 0.0 )
)

## PFTaus
####
# Discriminators for cloning
process.hltPFTauTrackFindingDiscriminatorOffVtx = cms.EDProducer(
    "PFRecoTauDiscriminationByLeadingObjectPtCut",
    MinPtLeadingObject = cms.double( 0.0 ),
    Prediscriminants = cms.PSet(  BooleanOperator = cms.string( "and" ) ),
    UseOnlyChargedHadrons = cms.bool( True ),
    PFTauProducer = cms.InputTag( "hltPFTausOffVtx" )
    )
process.hltPFTauLooseIsolationDiscriminatorOffVtx = cms.EDProducer(
    "PFRecoTauDiscriminationByIsolation",
    PFTauProducer = cms.InputTag( "hltPFTausOffVtx" ),
    qualityCuts = cms.PSet(
       isolationQualityCuts = cms.PSet(
          minTrackHits = cms.uint32( 8 ),
          minTrackPt = cms.double( 1.5 ),
          maxTrackChi2 = cms.double( 100.0 ),
          minTrackPixelHits = cms.uint32( 3 ),
          minGammaEt = cms.double( 1.5 ),
          useTracksInsteadOfPFHadrons = cms.bool( False ),
          maxDeltaZ = cms.double( 0.2 ),
          maxTransverseImpactParameter = cms.double( 0.05 )
          ),
       signalQualityCuts = cms.PSet(
          minTrackPt = cms.double( 0.0 ),
          maxTrackChi2 = cms.double( 1000.0 ),
          useTracksInsteadOfPFHadrons = cms.bool( False ),
          minGammaEt = cms.double( 0.5 ),
          minTrackPixelHits = cms.uint32( 0 ),
          minTrackHits = cms.uint32( 3 ),
          maxDeltaZ = cms.double( 0.4 ),
          maxTransverseImpactParameter = cms.double( 0.2 )
          ),
       primaryVertexSrc = cms.InputTag( "offlinePrimaryVertices" ),
       pvFindingAlgo = cms.string( "highestPtInEvent" ),
       leadingTrkOrPFCandOption = cms.string( "leadPFCand" )
       ),
    maximumSumPtCut = cms.double( 6.0 ),
    deltaBetaPUTrackPtCutOverride = cms.double( 0.5 ),
    isoConeSizeForDeltaBeta = cms.double( 0.3 ),
    vertexSrc = cms.InputTag( "NotUsed" ),
    applySumPtCut = cms.bool( False ),
    rhoConeSize = cms.double( 0.5 ),
    ApplyDiscriminationByTrackerIsolation = cms.bool( True ),
    rhoProducer = cms.InputTag( 'hltKT6PFJetsForTaus','rho' ),
    deltaBetaFactor = cms.string( "0.38" ),
    relativeSumPtCut = cms.double( 0.0 ),
    Prediscriminants = cms.PSet(
    BooleanOperator = cms.string( "and" ),
    leadTrack = cms.PSet(
       Producer = cms.InputTag( "hltPFTauTrackFindingDiscriminatorOffVtx" ),
       cut = cms.double( 0.5 )
       )
    ),
    applyOccupancyCut = cms.bool( True ),
    applyDeltaBetaCorrection = cms.bool( False ),
    applyRelativeSumPtCut = cms.bool( False ),
    maximumOccupancy = cms.uint32( 0 ),
    rhoUEOffsetCorrection = cms.double( 1.0 ),
    ApplyDiscriminationByECALIsolation = cms.bool( False ),
    storeRawSumPt = cms.bool( False ),
    applyRhoCorrection = cms.bool( False ),
    customOuterCone = cms.double( -1.0 ),
    particleFlowSrc = cms.InputTag( "hltParticleFlowForTaus" )
    )

process.hltPFTauECalIsolationDiscriminatorOffVtx = cms.EDProducer(
    "PFRecoTauDiscriminationByIsolation",
    PFTauProducer = cms.InputTag( "hltPFTausOffVtx" ),
    qualityCuts = cms.PSet(
       isolationQualityCuts = cms.PSet(
          minTrackHits = cms.uint32( 8 ),
          minTrackPt = cms.double( 1.5 ),
          maxTrackChi2 = cms.double( 100.0 ),
          minTrackPixelHits = cms.uint32( 3 ),
          minGammaEt = cms.double( 1.5 ),
          useTracksInsteadOfPFHadrons = cms.bool( False ),
          maxDeltaZ = cms.double( 0.2 ),
          maxTransverseImpactParameter = cms.double( 0.05 )
          ),
       signalQualityCuts = cms.PSet(
          minTrackPt = cms.double( 0.0 ),
          maxTrackChi2 = cms.double( 1000.0 ),
          useTracksInsteadOfPFHadrons = cms.bool( False ),
          minGammaEt = cms.double( 0.5 ),
          minTrackPixelHits = cms.uint32( 0 ),
          minTrackHits = cms.uint32( 3 ),
          maxDeltaZ = cms.double( 0.4 ),
          maxTransverseImpactParameter = cms.double( 0.2 )
          ),
       primaryVertexSrc = cms.InputTag( "offlinePrimaryVertices" ),
       pvFindingAlgo = cms.string( "highestPtInEvent" ),
       leadingTrkOrPFCandOption = cms.string( "leadPFCand" )
       ),
    maximumSumPtCut = cms.double( 6.0 ),
    deltaBetaPUTrackPtCutOverride = cms.double( 0.5 ),
    isoConeSizeForDeltaBeta = cms.double( 0.3 ),
    vertexSrc = cms.InputTag( "NotUsed" ),
    applySumPtCut = cms.bool( False ),
    rhoConeSize = cms.double( 0.5 ),
    ApplyDiscriminationByTrackerIsolation = cms.bool( False ),
    rhoProducer = cms.InputTag( 'hltKT6PFJetsForTaus','rho' ),
    deltaBetaFactor = cms.string( "0.38" ),
    relativeSumPtCut = cms.double( 0.0 ),
    Prediscriminants = cms.PSet(
    BooleanOperator = cms.string( "and" ),
    leadTrack = cms.PSet(
       Producer = cms.InputTag( "hltPFTauTrackFindingDiscriminatorOffVtx" ),
       cut = cms.double( 0.5 )
       )
    ),
    applyOccupancyCut = cms.bool( False ),
    applyDeltaBetaCorrection = cms.bool( False ),
    applyRelativeSumPtCut = cms.bool( False ),
    maximumOccupancy = cms.uint32( 0 ),
    rhoUEOffsetCorrection = cms.double( 1.0 ),
    ApplyDiscriminationByECALIsolation = cms.bool( True ),
    storeRawSumPt = cms.bool( True ),
    applyRhoCorrection = cms.bool( False ),
    customOuterCone = cms.double( -1.0 ),
    particleFlowSrc = cms.InputTag( "hltParticleFlowForTaus" )
    )
process.hltPFTauTrkIsolationDiscriminatorOffVtx = cms.EDProducer(
    "PFRecoTauDiscriminationByIsolation",
    PFTauProducer = cms.InputTag( "hltPFTausOffVtx" ),
    qualityCuts = cms.PSet(
       isolationQualityCuts = cms.PSet(
          minTrackHits = cms.uint32( 8 ),
          minTrackPt = cms.double( 0.5 ),
          maxTrackChi2 = cms.double( 100.0 ),
          minTrackPixelHits = cms.uint32( 3 ),
          minGammaEt = cms.double( 1.5 ),
          useTracksInsteadOfPFHadrons = cms.bool( False ),
          maxDeltaZ = cms.double( 0.2 ),
          maxTransverseImpactParameter = cms.double( 0.05 )
          ),
       signalQualityCuts = cms.PSet(
          minTrackPt = cms.double( 0.0 ),
          maxTrackChi2 = cms.double( 1000.0 ),
          useTracksInsteadOfPFHadrons = cms.bool( False ),
          minGammaEt = cms.double( 0.5 ),
          minTrackPixelHits = cms.uint32( 0 ),
          minTrackHits = cms.uint32( 3 ),
          maxDeltaZ = cms.double( 0.4 ),
          maxTransverseImpactParameter = cms.double( 0.2 )
          ),
       primaryVertexSrc = cms.InputTag( "offlinePrimaryVertices" ),
       pvFindingAlgo = cms.string( "highestPtInEvent" ),
       leadingTrkOrPFCandOption = cms.string( "leadPFCand" )
       ),
    maximumSumPtCut = cms.double( 6.0 ),
    deltaBetaPUTrackPtCutOverride = cms.double( 0.5 ),
    isoConeSizeForDeltaBeta = cms.double( 0.3 ),
    vertexSrc = cms.InputTag( "NotUsed" ),
    applySumPtCut = cms.bool( False ),
    rhoConeSize = cms.double( 0.5 ),
    ApplyDiscriminationByTrackerIsolation = cms.bool( True ),
    rhoProducer = cms.InputTag( 'hltKT6PFJetsForTaus','rho' ),
    deltaBetaFactor = cms.string( "0.38" ),
    relativeSumPtCut = cms.double( 0.0 ),
    Prediscriminants = cms.PSet(
    BooleanOperator = cms.string( "and" ),
    leadTrack = cms.PSet(
       Producer = cms.InputTag( "hltPFTauTrackFindingDiscriminatorOffVtx" ),
       cut = cms.double( 0.5 )
       )
    ),
    applyOccupancyCut = cms.bool( False ),
    applyDeltaBetaCorrection = cms.bool( False ),
    applyRelativeSumPtCut = cms.bool( False ),
    maximumOccupancy = cms.uint32( 0 ),
    rhoUEOffsetCorrection = cms.double( 1.0 ),
    ApplyDiscriminationByECALIsolation = cms.bool( False ),
    storeRawSumPt = cms.bool( True ),
    applyRhoCorrection = cms.bool( False ),
    customOuterCone = cms.double( -1.0 ),
    particleFlowSrc = cms.InputTag( "hltParticleFlowForTaus" )
    )
process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx = process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackHits = 5
process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackPixelHits = 2
process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackHits = 5
process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackPixelHits = 2
process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx = process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackHits = 3
process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackPixelHits = 1
process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackHits = 3
process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.qualityCuts.isolationQualityCuts.minTrackPixelHits = 1

#anti-mu discr
process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx = cms.EDProducer(
    "PFRecoTauDiscriminationAgainstMuon2",
    PFTauProducer = cms.InputTag('hltPFTausOffVtx'),
    Prediscriminants = cms.PSet(
      BooleanOperator = cms.string("and"),
    ),
    discriminatorOption = cms.string('custom'),
    HoPMin = cms.double(-1),
    maxNumberOfMatches = cms.int32(1),
    doCaloMuonVeto = cms.bool(False),
    maxNumberOfHitsLast2Stations = cms.int32(-1),
    # optional collection of muons to check for overlap with taus
    srcMuons = cms.InputTag(''), #cms.InputTag('hltMuons')
    dRmuonMatch = cms.double(0.3),
    dRmuonMatchLimitedToJetArea = cms.bool(False),
    minPtMatchedMuon = cms.double(5.),
    maskMatchesDT = cms.vint32(0,0,0,0),
    maskMatchesCSC = cms.vint32(1,0,0,0),
    maskMatchesRPC = cms.vint32(0,0,0,0),
    maskHitsDT = cms.vint32(0,0,0,0),
    maskHitsCSC = cms.vint32(0,0,0,0),
    maskHitsRPC = cms.vint32(0,0,0,0),
    verbosity = cms.int32(0)
    )
process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.maxNumberOfMatches = -1
process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.doCaloMuonVeto = True
process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.HoPMin = 0.2

## New producer
process.hltTauPFJets08Region = cms.EDProducer("RecoTauJetRegionProducer",
    src = cms.InputTag( "hltAntiKT5PFJetsForTaus" ),
    deltaR = cms.double(0.8),
    pfSrc = cms.InputTag( "hltParticleFlowForTaus" ), #MB not needed?
    pfCandSrc = cms.InputTag('hltParticleFlowForTaus'), #added CV
    pfCandAssocMapSrc = cms.InputTag('') #added CV
)
process.hltPFTauPiZeros = cms.EDProducer( "RecoTauPiZeroProducer",
    massHypothesis = cms.double( 0.136 ),
    ranking = cms.VPSet( 
      cms.PSet(  selectionPassFunction = cms.string( "abs(mass() - 0.13579)" ),
        selectionFailValue = cms.double( 1000.0 ),
        selection = cms.string( "algoIs(\"kStrips\")" ),
        name = cms.string( "InStrip" ),
        plugin = cms.string( "RecoTauPiZeroStringQuality" )
      )
    ),
    jetRegionSrc = cms.InputTag( "hltTauPFJets08Region" ),
    outputSelection = cms.string( "pt > 0" ),
    jetSrc = cms.InputTag( "hltAntiKT5PFJetsForTaus" ),
    builders = cms.VPSet( 
      cms.PSet(  name = cms.string( "s" ),
        stripPhiAssociationDistance = cms.double( 0.2 ),
        plugin = cms.string( "RecoTauPiZeroStripPlugin2" ),
        minGammaEtStripAdd = cms.double( 0.0 ),
        minGammaEtStripSeed = cms.double( 0.5 ),
        qualityCuts = cms.PSet(
          pvFindingAlgo = cms.string( "highestPtInEvent" ),
          primaryVertexSrc = cms.InputTag( "hltIsoMuonVertex" ),
          leadingTrkOrPFCandOption = cms.string( "leadPFCand" ),
          signalQualityCuts = cms.PSet(
            maxDeltaZ = cms.double( 0.4 ),
            minTrackPt = cms.double( 0.0 ),
            useTracksInsteadOfPFHadrons = cms.bool( False ),
            maxTrackChi2 = cms.double( 1000.0 ),
            minTrackPixelHits = cms.uint32( 0 ),
            minGammaEt = cms.double( 0.5 ),
            minTrackHits = cms.uint32( 3 ),
            maxTransverseImpactParameter = cms.double( 0.2 )
          )
        ),
        maxStripBuildIterations = cms.int32( -1 ),
        updateStripAfterEachDaughter = cms.bool( False ),
        makeCombinatoricStrips = cms.bool(False),
        applyElecTrackQcuts = cms.bool(False),
        stripCandidatesParticleIds = cms.vint32(2, 4),
        minStripEt = cms.double(1.0),
        stripEtaAssociationDistance = cms.double(0.05)
      ) 
    )
)
# added for boosted tau CV
process.hltTauPFJetsRecoTauChargedHadrons = cms.EDProducer(
    "PFRecoTauChargedHadronProducer",
    outputSelection = cms.string('pt > 0.5'),
    ranking = cms.VPSet(cms.PSet(
       selectionPassFunction = cms.string('-pt'),
       selection = cms.string("algoIs(\'kChargedPFCandidate\')"),
       name = cms.string('ChargedPFCandidate'),
       plugin = cms.string('PFRecoTauChargedHadronStringQuality'),
       selectionFailValue = cms.double(1000.0)
    )),
    builders = cms.VPSet(cms.PSet(
       minMergeChargedHadronPt = cms.double(100.0),
       name = cms.string('chargedPFCandidates'),
       dRmergeNeutralHadronWrtOther = cms.double(0.005),
       plugin = cms.string('PFRecoTauChargedHadronFromPFCandidatePlugin'),
       minBlockElementMatchesPhoton = cms.int32(2),
       dRmergeNeutralHadronWrtNeutralHadron = cms.double(0.01),
       maxUnmatchedBlockElementsPhoton = cms.int32(1),
       qualityCuts = cms.PSet(
          signalQualityCuts = cms.PSet(
             minTrackHits = cms.uint32(3),
             minTrackVertexWeight = cms.double(-1),
             minTrackPt = cms.double(0.5),
             maxTrackChi2 = cms.double(1000.0), #MB 100.0->1000.0
             minTrackPixelHits = cms.uint32(0),
             minGammaEt = cms.double(0.5),
             maxDeltaZ = cms.double(0.4),
             minNeutralHadronEt = cms.double(30.0),
             maxTransverseImpactParameter = cms.double(0.2) #MB: 0.03->0.2
          ),
          vxAssocQualityCuts = cms.PSet(
             minTrackVertexWeight = cms.double(-1),
             minTrackPt = cms.double(0.5),
             maxTrackChi2 = cms.double(1000.0), #MB 100.0->1000.0
             minTrackPixelHits = cms.uint32(0),
             minGammaEt = cms.double(0.5),
             minTrackHits = cms.uint32(3),
             maxTransverseImpactParameter = cms.double(0.2) #MB: 0.03->0.2
          ),
          isolationQualityCuts = cms.PSet(
             minTrackHits = cms.uint32(5), #MB 8->5
             minTrackVertexWeight = cms.double(-1),
             minTrackPt = cms.double(0.5), #MB 1.5->0.5
             maxTrackChi2 = cms.double(100.0),
             minTrackPixelHits = cms.uint32(2), #MB 0->2
             minGammaEt = cms.double(0.5), #MB 1.5->0.5
             maxDeltaZ = cms.double(0.2),
             maxTransverseImpactParameter = cms.double(0.05) #MB: 0.03->0.05
          ),
          #pvFindingAlgo = cms.string('highestWeightForLeadTrack'), #MB FIXME correct?
          pvFindingAlgo = cms.string('highestPtInEvent'),
          recoverLeadingTrk = cms.bool(False),
          vertexTrackFiltering = cms.bool(False),
          #primaryVertexSrc = cms.InputTag("offlinePrimaryVertices") #MB FIXME correct?
          primaryVertexSrc = cms.InputTag("hltIsoMuonVertex"),
          leadingTrkOrPFCandOption = cms.string( "leadPFCand" )
       ),
       dRmergeNeutralHadronWrtElectron = cms.double(0.05),
       minBlockElementMatchesNeutralHadron = cms.int32(2),
       dRmergePhotonWrtOther = cms.double(0.005),
       chargedHadronCandidatesParticleIds = cms.vint32(1, 2, 3),
       minMergeNeutralHadronEt = cms.double(0.0),
       minMergeGammaEt = cms.double(0.0),
       dRmergeNeutralHadronWrtChargedHadron = cms.double(0.005),
       dRmergePhotonWrtChargedHadron = cms.double(0.005),
       dRmergePhotonWrtNeutralHadron = cms.double(0.01),
       maxUnmatchedBlockElementsNeutralHadron = cms.int32(1),
       dRmergePhotonWrtElectron = cms.double(0.005)
    )),
    jetRegionSrc = cms.InputTag("hltTauPFJets08Region"),
    jetSrc = cms.InputTag("hltAntiKT5PFJetsForTaus")
)
    
process.hltPFTausNPSansRef = cms.EDProducer( "RecoTauProducer",
    piZeroSrc = cms.InputTag( "hltPFTauPiZeros" ),
    chargedHadronSrc = cms.InputTag('hltTauPFJetsRecoTauChargedHadrons'),
    modifiers = cms.VPSet( 
      cms.PSet(  ElectronPreIDProducer = cms.InputTag( "elecpreid" ),
        name = cms.string( "fixedConeElectronRej" ),
        plugin = cms.string( "RecoTauElectronRejectionPlugin" ),
        DataType = cms.string( "AOD" ),
        maximumForElectrionPreIDOutput = cms.double( -0.1 ),
        EcalStripSumE_deltaPhiOverQ_minValue = cms.double( -0.1 ),
        ElecPreIDLeadTkMatch_maxDR = cms.double( 0.01 ),
        EcalStripSumE_minClusEnergy = cms.double( 0.1 ),
        EcalStripSumE_deltaPhiOverQ_maxValue = cms.double( 0.5 ),
        EcalStripSumE_deltaEta = cms.double( 0.03 )
      )
    ),
    jetRegionSrc = cms.InputTag( "hltTauPFJets08Region" ),
    jetSrc = cms.InputTag( "hltAntiKT5PFJetsForTaus" ),
    builders = cms.VPSet( 
      cms.PSet(  usePFLeptons = cms.bool( True ),
        name = cms.string( "fixedCone" ),
        pfCandSrc = cms.InputTag( "hltParticleFlowForTaus" ),
        plugin = cms.string( "RecoTauBuilderConePlugin" ),
        signalConeNeutralHadrons = cms.string( "0.1" ), #MB
        isoConeNeutralHadrons = cms.string( "0.4" ),
        isoConeChargedHadrons = cms.string( "0.4" ),
        isoConePiZeros = cms.string( "0.4" ),
        matchingCone = cms.string( "0.4" ),
        signalConeChargedHadrons = cms.string( "0.12" ),
        leadObjectPt = cms.double( 0.5 ),
        signalConePiZeros = cms.string( "0.12" ), #MB
        maxSignalConeChargedHadrons = cms.int32(3),
        qualityCuts = cms.PSet( 
          pvFindingAlgo = cms.string( "highestPtInEvent" ),
          primaryVertexSrc = cms.InputTag( "hltIsoMuonVertex" ),
          recoverLeadingTrk = cms.bool(False),
          vertexTrackFiltering = cms.bool(False),
          leadingTrkOrPFCandOption = cms.string( "leadPFCand" ),
          signalQualityCuts = cms.PSet( 
            minTrackPt = cms.double( 0.5 ),
            maxTrackChi2 = cms.double( 1000.0 ),
            useTracksInsteadOfPFHadrons = cms.bool( False ),
            minGammaEt = cms.double( 0.5 ),
            minTrackPixelHits = cms.uint32( 0 ),
            minTrackHits = cms.uint32( 3 ),
            maxDeltaZ = cms.double( 0.4 ),
            maxTransverseImpactParameter = cms.double( 0.2 )
          ),
          isolationQualityCuts = cms.PSet( 
            minTrackHits = cms.uint32( 5 ),
            minTrackPt = cms.double( 1.0 ),
            maxTrackChi2 = cms.double( 100.0 ),
            minTrackPixelHits = cms.uint32( 2 ),
            useTracksInsteadOfPFHadrons = cms.bool( False ),
            maxDeltaZ = cms.double( 0.2 ),
            maxTransverseImpactParameter = cms.double( 0.05 ),
            minGammaEt = cms.double( 0.5 )
          ),
          vxAssocQualityCuts = cms.PSet(
             minTrackVertexWeight = cms.double(-1),
             minTrackPt = cms.double(0.5),
             maxTrackChi2 = cms.double(1000.0),
             minTrackPixelHits = cms.uint32(0),
             minGammaEt = cms.double(0.5),
             minTrackHits = cms.uint32(3),
             maxTransverseImpactParameter = cms.double(0.2)
          )
        )
      )
    ),
    buildNullTaus = cms.bool( True ) #MB ->False??
)
process.hltPFTausNP = cms.EDProducer( "RecoTauPiZeroUnembedder",
    src = cms.InputTag( "hltPFTausNPSansRef" ),
    tauTransverseImpactParameterSource = cms.InputTag('')
)
process.hltPFTauTrackFindingDiscriminatorNP = process.hltPFTauTrackFindingDiscriminatorOffVtx.clone()
process.hltPFTauTrackFindingDiscriminatorNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauLooseIsolationDiscriminatorNP =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauLooseIsolationDiscriminatorNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauLooseIsolationDiscriminatorNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauLooseIsolationDiscriminator5hitsNP = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauLooseIsolationDiscriminator5hitsNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauLooseIsolationDiscriminator5hitsNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauLooseIsolationDiscriminator3hitsNP = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauLooseIsolationDiscriminator3hitsNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauLooseIsolationDiscriminator3hitsNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauECalIsolationDiscriminatorNP = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauECalIsolationDiscriminatorNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauECalIsolationDiscriminatorNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauTrkIsolationDiscriminatorNP = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauTrkIsolationDiscriminatorNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauTrkIsolationDiscriminatorNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauTrkIsolationDiscriminator5hitsNP = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauTrkIsolationDiscriminator5hitsNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauTrkIsolationDiscriminator5hitsNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauTrkIsolationDiscriminator3hitsNP = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauTrkIsolationDiscriminator3hitsNP.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauTrkIsolationDiscriminator3hitsNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorNP"
process.hltPFTauAgainstMuonDiscriminatorLooseNP = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseNP.PFTauProducer = "hltPFTausNP"
process.hltPFTauAgainstMuonDiscriminatorHoPNP = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPNP.PFTauProducer = "hltPFTausNP"

process.hltPFTauSequnceNP = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZeros +
    process.hltTauPFJetsRecoTauChargedHadrons +
    process.hltPFTausNPSansRef +
    process.hltPFTausNP +
    process.hltPFTauTrackFindingDiscriminatorNP +
    process.hltPFTauLooseIsolationDiscriminatorNP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsNP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsNP + 
    process.hltPFTauECalIsolationDiscriminatorNP +
    process.hltPFTauTrkIsolationDiscriminatorNP +
    process.hltPFTauTrkIsolationDiscriminator5hitsNP +
    process.hltPFTauTrkIsolationDiscriminator3hitsNP
    + process.hltPFTauAgainstMuonDiscriminatorLooseNP
    + process.hltPFTauAgainstMuonDiscriminatorHoPNP
    )

#####
## New producer with online vertices
process.hltPFTauPiZerosOnl = process.hltPFTauPiZeros.clone()
process.hltPFTauPiZerosOnl.builders[0].qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltTauPFJetsRecoTauChargedHadronsOnl = process.hltTauPFJetsRecoTauChargedHadrons.clone()
process.hltTauPFJetsRecoTauChargedHadronsOnl.builders[0].qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTausOnlNPSansRef = process.hltPFTausNPSansRef.clone()
process.hltPFTausOnlNPSansRef.piZeroSrc = "hltPFTauPiZerosOnl"
process.hltPFTausOnlNPSansRef.chargedHadronSrc = 'hltTauPFJetsRecoTauChargedHadronsOnl'
process.hltPFTausOnlNPSansRef.builders[0].qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTausOnlNP = process.hltPFTausNP.clone()
process.hltPFTausOnlNP.src = "hltPFTausOnlNPSansRef"
process.hltPFTauTrackFindingDiscriminatorOnlNP = process.hltPFTauTrackFindingDiscriminatorOffVtx.clone()
process.hltPFTauTrackFindingDiscriminatorOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauLooseIsolationDiscriminatorOnlNP =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauLooseIsolationDiscriminatorOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminatorOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauLooseIsolationDiscriminator5hitsOnlNP = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauLooseIsolationDiscriminator5hitsOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminator5hitsOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauLooseIsolationDiscriminator3hitsOnlNP = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauLooseIsolationDiscriminator3hitsOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminator3hitsOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauECalIsolationDiscriminatorOnlNP = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauECalIsolationDiscriminatorOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauECalIsolationDiscriminatorOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauTrkIsolationDiscriminatorOnlNP = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauTrkIsolationDiscriminatorOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminatorOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauTrkIsolationDiscriminator5hitsOnlNP = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauTrkIsolationDiscriminator5hitsOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminator5hitsOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauTrkIsolationDiscriminator3hitsOnlNP = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauTrkIsolationDiscriminator3hitsOnlNP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminator3hitsOnlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnlNP"
process.hltPFTauAgainstMuonDiscriminatorLooseOnlNP = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseOnlNP.PFTauProducer = "hltPFTausOnlNP"
process.hltPFTauAgainstMuonDiscriminatorHoPOnlNP = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPOnlNP.PFTauProducer = "hltPFTausOnlNP"

process.hltPFTauSequnceOnlNP = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZerosOnl +
    process.hltTauPFJetsRecoTauChargedHadronsOnl +
    process.hltPFTausOnlNPSansRef +
    process.hltPFTausOnlNP +
    process.hltPFTauTrackFindingDiscriminatorOnlNP +
    process.hltPFTauLooseIsolationDiscriminatorOnlNP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsOnlNP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsOnlNP + 
    process.hltPFTauECalIsolationDiscriminatorOnlNP +
    process.hltPFTauTrkIsolationDiscriminatorOnlNP +
    process.hltPFTauTrkIsolationDiscriminator5hitsOnlNP +
    process.hltPFTauTrkIsolationDiscriminator3hitsOnlNP
    +process.hltPFTauAgainstMuonDiscriminatorLooseOnlNP
    +process.hltPFTauAgainstMuonDiscriminatorHoPOnlNP
    )
#####
## New producer with online vertices comb sorting
process.hltPFTauPiZerosOnl2 = process.hltPFTauPiZeros.clone()
process.hltPFTauPiZerosOnl2.builders[0].qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauPiZerosOnl2.builders[0].qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltTauPFJetsRecoTauChargedHadronsOnl2 = process.hltTauPFJetsRecoTauChargedHadrons.clone()
process.hltTauPFJetsRecoTauChargedHadronsOnl2.builders[0].qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltTauPFJetsRecoTauChargedHadronsOnl2.builders[0].qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTausOnl2NPSansRef = process.hltPFTausNPSansRef.clone()
process.hltPFTausOnl2NPSansRef.piZeroSrc = "hltPFTauPiZerosOnl2"
process.hltPFTausOnl2NPSansRef.chargedHadronSrc = "hltTauPFJetsRecoTauChargedHadronsOnl2"
process.hltPFTausOnl2NPSansRef.builders[0].qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTausOnl2NPSansRef.builders[0].qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTausOnl2NP = process.hltPFTausNP.clone()
process.hltPFTausOnl2NP.src = "hltPFTausOnl2NPSansRef"
process.hltPFTauTrackFindingDiscriminatorOnl2NP = process.hltPFTauTrackFindingDiscriminatorOffVtx.clone()
process.hltPFTauTrackFindingDiscriminatorOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauLooseIsolationDiscriminatorOnl2NP =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauLooseIsolationDiscriminatorOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminatorOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauLooseIsolationDiscriminatorOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauLooseIsolationDiscriminator5hitsOnl2NP = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauLooseIsolationDiscriminator5hitsOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminator5hitsOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauLooseIsolationDiscriminator5hitsOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauLooseIsolationDiscriminator3hitsOnl2NP = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauLooseIsolationDiscriminator3hitsOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminator3hitsOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauLooseIsolationDiscriminator3hitsOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauECalIsolationDiscriminatorOnl2NP = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauECalIsolationDiscriminatorOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauECalIsolationDiscriminatorOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauECalIsolationDiscriminatorOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauTrkIsolationDiscriminatorOnl2NP = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauTrkIsolationDiscriminatorOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminatorOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauTrkIsolationDiscriminatorOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauTrkIsolationDiscriminator5hitsOnl2NP = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauTrkIsolationDiscriminator5hitsOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminator5hitsOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauTrkIsolationDiscriminator5hitsOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauTrkIsolationDiscriminator3hitsOnl2NP = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauTrkIsolationDiscriminator3hitsOnl2NP.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminator3hitsOnl2NP.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauTrkIsolationDiscriminator3hitsOnl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorOnl2NP"
process.hltPFTauAgainstMuonDiscriminatorLooseOnl2NP = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseOnl2NP.PFTauProducer = "hltPFTausOnl2NP"
process.hltPFTauAgainstMuonDiscriminatorHoPOnl2NP = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPOnl2NP.PFTauProducer = "hltPFTausOnl2NP"

process.hltPFTauSequnceOnl2NP = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZerosOnl2 +
    process.hltTauPFJetsRecoTauChargedHadronsOnl2 +
    process.hltPFTausOnl2NPSansRef +
    process.hltPFTausOnl2NP +
    process.hltPFTauTrackFindingDiscriminatorOnl2NP +
    process.hltPFTauLooseIsolationDiscriminatorOnl2NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsOnl2NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsOnl2NP + 
    process.hltPFTauECalIsolationDiscriminatorOnl2NP +
    process.hltPFTauTrkIsolationDiscriminatorOnl2NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsOnl2NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsOnl2NP
    + process.hltPFTauAgainstMuonDiscriminatorLooseOnl2NP
    + process.hltPFTauAgainstMuonDiscriminatorHoPOnl2NP
    )
#####
## New producer with pixel vertices
process.hltPFTauPiZerosPxl = process.hltPFTauPiZeros.clone()
process.hltPFTauPiZerosPxl.builders[0].qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltTauPFJetsRecoTauChargedHadronsPxl = process.hltTauPFJetsRecoTauChargedHadrons.clone()
process.hltTauPFJetsRecoTauChargedHadronsPxl.builders[0].qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTausPxlNPSansRef = process.hltPFTausNPSansRef.clone()
process.hltPFTausPxlNPSansRef.piZeroSrc = "hltPFTauPiZerosPxl"
process.hltPFTausPxlNPSansRef.chargedHadronSrc = "hltTauPFJetsRecoTauChargedHadronsPxl"
process.hltPFTausPxlNPSansRef.builders[0].qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTausPxlNP = process.hltPFTausNP.clone()
process.hltPFTausPxlNP.src = "hltPFTausPxlNPSansRef"
process.hltPFTauTrackFindingDiscriminatorPxlNP = process.hltPFTauTrackFindingDiscriminatorOffVtx.clone()
process.hltPFTauTrackFindingDiscriminatorPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauLooseIsolationDiscriminatorPxlNP =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauLooseIsolationDiscriminatorPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminatorPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxlNP = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminator5hitsPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxlNP = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminator3hitsPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauECalIsolationDiscriminatorPxlNP = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauECalIsolationDiscriminatorPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauECalIsolationDiscriminatorPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauTrkIsolationDiscriminatorPxlNP = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauTrkIsolationDiscriminatorPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminatorPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxlNP = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminator5hitsPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxlNP = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsPxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxlNP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminator3hitsPxlNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxlNP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxlNP = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLoosePxlNP.PFTauProducer = "hltPFTausPxlNP"
process.hltPFTauAgainstMuonDiscriminatorHoPPxlNP = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPPxlNP.PFTauProducer = "hltPFTausPxlNP"


process.hltPFTauSequncePxlNP = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZerosPxl +
    process.hltTauPFJetsRecoTauChargedHadronsPxl +
    process.hltPFTausPxlNPSansRef +
    process.hltPFTausPxlNP +
    process.hltPFTauTrackFindingDiscriminatorPxlNP +
    process.hltPFTauLooseIsolationDiscriminatorPxlNP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxlNP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxlNP + 
    process.hltPFTauECalIsolationDiscriminatorPxlNP +
    process.hltPFTauTrkIsolationDiscriminatorPxlNP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxlNP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxlNP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxlNP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxlNP
    )

####### New producer with pixel vertices
process.hltPFTauPiZerosPxl2 = process.hltPFTauPiZeros.clone()
process.hltPFTauPiZerosPxl2.builders[0].qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauPiZerosPxl2.builders[0].qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltTauPFJetsRecoTauChargedHadronsPxl2 = process.hltTauPFJetsRecoTauChargedHadrons.clone()
process.hltTauPFJetsRecoTauChargedHadronsPxl2.builders[0].qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltTauPFJetsRecoTauChargedHadronsPxl2.builders[0].qualityCuts.pvFindingAlgo = "closestInDeltaZ" 
process.hltPFTausPxl2NPSansRef = process.hltPFTausNPSansRef.clone()
process.hltPFTausPxl2NPSansRef.piZeroSrc = "hltPFTauPiZerosPxl2"
process.hltPFTausPxl2NPSansRef.builders[0].qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTausPxl2NPSansRef.builders[0].qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTausPxl2NPSansRef.chargedHadronSrc = 'hltTauPFJetsRecoTauChargedHadronsPxl2'
process.hltPFTausPxl2NP = process.hltPFTausNP.clone()
process.hltPFTausPxl2NP.src = "hltPFTausPxl2NPSansRef"
process.hltPFTauTrackFindingDiscriminatorPxl2NP = process.hltPFTauTrackFindingDiscriminatorOffVtx.clone()
process.hltPFTauTrackFindingDiscriminatorPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauLooseIsolationDiscriminatorPxl2NP =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauLooseIsolationDiscriminatorPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminatorPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauLooseIsolationDiscriminatorPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauECalIsolationDiscriminatorPxl2NP = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauECalIsolationDiscriminatorPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauECalIsolationDiscriminatorPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauECalIsolationDiscriminatorPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2NP = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminatorPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauTrkIsolationDiscriminatorPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.qualityCuts.pvFindingAlgo = "closestInDeltaZ" #MB: "combined" does not exist with tags in the release, replaxed by pixelVtx un-friendly one. To be rechecked with "closestInDeltaZ". Also quality cuts for track for vtx finding to be reconsidered
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2NP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.PFTauProducer = "hltPFTausPxl2NP"
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.PFTauProducer = "hltPFTausPxl2NP"

process.hltPFTauSequncePxl2NP = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZerosPxl2 +
    process.hltTauPFJetsRecoTauChargedHadronsPxl2 +
    process.hltPFTausPxl2NPSansRef +
    process.hltPFTausPxl2NP +
    process.hltPFTauTrackFindingDiscriminatorPxl2NP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2NP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP
    )

## pxl2 with different signal area definitions
process.hltPFTausPxl2R15N3NPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R15N3NPSansRef.builders[0].signalConeChargedHadrons = "0.15"
process.hltPFTausPxl2R15N3NPSansRef.builders[0].signalConePiZeros = "0.15"
process.hltPFTausPxl2R15N3NPSansRef.builders[0].maxSignalConeChargedHadrons = 3

process.hltPFTausPxl2R18N3NPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R18N3NPSansRef.builders[0].signalConeChargedHadrons = "0.18"
process.hltPFTausPxl2R18N3NPSansRef.builders[0].signalConePiZeros = "0.18"
process.hltPFTausPxl2R18N3NPSansRef.builders[0].maxSignalConeChargedHadrons = 3

process.hltPFTausPxl2R12N5NPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R12N5NPSansRef.builders[0].signalConeChargedHadrons = "0.12"
process.hltPFTausPxl2R12N5NPSansRef.builders[0].signalConePiZeros = "0.15"
process.hltPFTausPxl2R12N5NPSansRef.builders[0].maxSignalConeChargedHadrons = 5

process.hltPFTausPxl2R15N5NPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R15N5NPSansRef.builders[0].signalConeChargedHadrons = "0.15"
process.hltPFTausPxl2R15N5NPSansRef.builders[0].signalConePiZeros = "0.15"
process.hltPFTausPxl2R15N5NPSansRef.builders[0].maxSignalConeChargedHadrons = 5

process.hltPFTausPxl2R18N5NPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R18N5NPSansRef.builders[0].signalConeChargedHadrons = "0.18"
process.hltPFTausPxl2R18N5NPSansRef.builders[0].signalConePiZeros = "0.18"
process.hltPFTausPxl2R18N5NPSansRef.builders[0].maxSignalConeChargedHadrons = 5

process.hltPFTausPxl2R12NInfNPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R12NInfNPSansRef.builders[0].signalConeChargedHadrons = "0.12"
process.hltPFTausPxl2R12NInfNPSansRef.builders[0].signalConePiZeros = "0.15"
process.hltPFTausPxl2R12NInfNPSansRef.builders[0].maxSignalConeChargedHadrons = 999

process.hltPFTausPxl2R15NInfNPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R15NInfNPSansRef.builders[0].signalConeChargedHadrons = "0.15"
process.hltPFTausPxl2R15NInfNPSansRef.builders[0].signalConePiZeros = "0.15"
process.hltPFTausPxl2R15NInfNPSansRef.builders[0].maxSignalConeChargedHadrons = 999
    
process.hltPFTausPxl2R18NInfNPSansRef = process.hltPFTausPxl2NPSansRef.clone()
process.hltPFTausPxl2R18NInfNPSansRef.builders[0].signalConeChargedHadrons = "0.18"
process.hltPFTausPxl2R18NInfNPSansRef.builders[0].signalConePiZeros = "0.18"
process.hltPFTausPxl2R18NInfNPSansRef.builders[0].maxSignalConeChargedHadrons = 999

process.hltPFTausPxl2R15N3NP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R15N3NPSansRef")
process.hltPFTausPxl2R18N3NP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R18N3NPSansRef")
process.hltPFTausPxl2R12N5NP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R12N5NPSansRef")
process.hltPFTausPxl2R15N5NP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R15N5NPSansRef")
process.hltPFTausPxl2R18N5NP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R18N5NPSansRef")
process.hltPFTausPxl2R12NInfNP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R12NInfNPSansRef")
process.hltPFTausPxl2R15NInfNP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R15NInfNPSansRef")
process.hltPFTausPxl2R18NInfNP = process.hltPFTausPxl2NP.clone(
    src = "hltPFTausPxl2R18NInfNPSansRef")

#R15N3
process.hltPFTauTrackFindingDiscriminatorPxl2R15N3NP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R15N3NP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N3NP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N3NP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauECalIsolationDiscriminatorPxl2R15N3NP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R15N3NP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N3NP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N3NP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauECalIsolationDiscriminatorPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R15N3NP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R15N3NP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N3NP")

#R18N3
process.hltPFTauTrackFindingDiscriminatorPxl2R18N3NP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R18N3NP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N3NP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N3NP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauECalIsolationDiscriminatorPxl2R18N3NP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R18N3NP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N3NP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N3NP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauECalIsolationDiscriminatorPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N3NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R18N3NP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R18N3NP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N3NP")

#R12N5
process.hltPFTauTrackFindingDiscriminatorPxl2R12N5NP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R12N5NP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R12N5NP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R12N5NP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauECalIsolationDiscriminatorPxl2R12N5NP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R12N5NP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R12N5NP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R12N5NP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauECalIsolationDiscriminatorPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R12N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R12N5NP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R12N5NP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12N5NP")

#R15N5
process.hltPFTauTrackFindingDiscriminatorPxl2R15N5NP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R15N5NP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N5NP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N5NP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauECalIsolationDiscriminatorPxl2R15N5NP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R15N5NP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N5NP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N5NP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauECalIsolationDiscriminatorPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R15N5NP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R15N5NP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15N5NP")

#R18N5
process.hltPFTauTrackFindingDiscriminatorPxl2R18N5NP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R18N5NP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N5NP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N5NP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauECalIsolationDiscriminatorPxl2R18N5NP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R18N5NP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N5NP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N5NP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauECalIsolationDiscriminatorPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N5NP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R18N5NP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R18N5NP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18N5NP")

#R12NInf
process.hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R12NInfNP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R12NInfNP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R12NInfNP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauECalIsolationDiscriminatorPxl2R12NInfNP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R12NInfNP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R12NInfNP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R12NInfNP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauECalIsolationDiscriminatorPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R12NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R12NInfNP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R12NInfNP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R12NInfNP")

#R15NInf
process.hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R15NInfNP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15NInfNP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15NInfNP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauECalIsolationDiscriminatorPxl2R15NInfNP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R15NInfNP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15NInfNP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15NInfNP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauECalIsolationDiscriminatorPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R15NInfNP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R15NInfNP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R15NInfNP")

#R18NInf
process.hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP = process.hltPFTauTrackFindingDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R18NInfNP = process.hltPFTauLooseIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18NInfNP = process.hltPFTauLooseIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18NInfNP = process.hltPFTauLooseIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauECalIsolationDiscriminatorPxl2R18NInfNP = process.hltPFTauECalIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauTrkIsolationDiscriminatorPxl2R18NInfNP = process.hltPFTauTrkIsolationDiscriminatorPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18NInfNP = process.hltPFTauTrkIsolationDiscriminator5hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18NInfNP = process.hltPFTauTrkIsolationDiscriminator3hitsPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauLooseIsolationDiscriminatorPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauECalIsolationDiscriminatorPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauTrkIsolationDiscriminatorPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18NInfNP.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"
process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R18NInfNP = process.hltPFTauAgainstMuonDiscriminatorLoosePxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")
process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R18NInfNP = process.hltPFTauAgainstMuonDiscriminatorHoPPxl2NP.clone(
    PFTauProducer = "hltPFTausPxl2R18NInfNP")

process.hltPFTauSequncePxl2NPTuning = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZerosPxl2 +
    process.hltTauPFJetsRecoTauChargedHadronsPxl2 +

    process.hltPFTausPxl2R15N3NPSansRef +
    process.hltPFTausPxl2R18N3NPSansRef +
    process.hltPFTausPxl2R12N5NPSansRef +
    process.hltPFTausPxl2R15N5NPSansRef +
    process.hltPFTausPxl2R18N5NPSansRef +
    process.hltPFTausPxl2R12NInfNPSansRef +
    process.hltPFTausPxl2R15NInfNPSansRef +
    process.hltPFTausPxl2R18NInfNPSansRef +

    process.hltPFTausPxl2R15N3NP +
    process.hltPFTausPxl2R18N3NP +
    process.hltPFTausPxl2R12N5NP +
    process.hltPFTausPxl2R15N5NP +
    process.hltPFTausPxl2R18N5NP +
    process.hltPFTausPxl2R12NInfNP +
    process.hltPFTausPxl2R15NInfNP +
    process.hltPFTausPxl2R18NInfNP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R15N3NP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R15N3NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N3NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N3NP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R15N3NP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R15N3NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N3NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N3NP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R15N3NP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R15N3NP+

    process.hltPFTauTrackFindingDiscriminatorPxl2R18N3NP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R18N3NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N3NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N3NP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R18N3NP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R18N3NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N3NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N3NP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R18N3NP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R18N3NP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R12N5NP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R12N5NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R12N5NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R12N5NP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R12N5NP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R12N5NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R12N5NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R12N5NP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R12N5NP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R12N5NP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R15N5NP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R15N5NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N5NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N5NP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R15N5NP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R15N5NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N5NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N5NP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R15N5NP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R15N5NP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R18N5NP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R18N5NP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N5NP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N5NP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R18N5NP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R18N5NP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N5NP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N5NP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R18N5NP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R18N5NP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R12NInfNP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R12NInfNP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R12NInfNP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R12NInfNP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R12NInfNP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R12NInfNP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R12NInfNP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R12NInfNP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R12NInfNP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R15NInfNP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R15NInfNP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R15NInfNP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R15NInfNP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R15NInfNP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R15NInfNP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R15NInfNP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R15NInfNP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R15NInfNP +

    process.hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP +
    process.hltPFTauLooseIsolationDiscriminatorPxl2R18NInfNP + 
    process.hltPFTauLooseIsolationDiscriminator5hitsPxl2R18NInfNP + 
    process.hltPFTauLooseIsolationDiscriminator3hitsPxl2R18NInfNP + 
    process.hltPFTauECalIsolationDiscriminatorPxl2R18NInfNP +
    process.hltPFTauTrkIsolationDiscriminatorPxl2R18NInfNP +
    process.hltPFTauTrkIsolationDiscriminator5hitsPxl2R18NInfNP +
    process.hltPFTauTrkIsolationDiscriminator3hitsPxl2R18NInfNP
    +process.hltPFTauAgainstMuonDiscriminatorLoosePxl2R18NInfNP
    +process.hltPFTauAgainstMuonDiscriminatorHoPPxl2R18NInfNP

    )

#####
## New producer with online vertices, HPS
process.hltCombinatoricRecoTaus = cms.EDProducer(
    "RecoTauProducer",
    piZeroSrc = cms.InputTag("hltPFTauPiZerosOnl2"),
    chargedHadronSrc = cms.InputTag('hltTauPFJetsRecoTauChargedHadronsOnl2'),
    modifiers = cms.VPSet(
       cms.PSet(
          plugin = cms.string('RecoTauImpactParameterSignificancePlugin'),
          name = cms.string('sipt'),
          qualityCuts = process.hltPFTauPiZerosOnl2.builders[0].qualityCuts
       ),
       cms.PSet(
          ElectronPreIDProducer = cms.InputTag("elecpreid"),
          name = cms.string('elec_rej'),
          plugin = cms.string('RecoTauElectronRejectionPlugin'),
          DataType = cms.string('AOD'),
          maximumForElectrionPreIDOutput = cms.double(-0.1),
          EcalStripSumE_deltaPhiOverQ_minValue = cms.double(-0.1),
          EcalStripSumE_deltaPhiOverQ_maxValue = cms.double(0.5),
          EcalStripSumE_minClusEnergy = cms.double(0.1),
          ElecPreIDLeadTkMatch_maxDR = cms.double(0.01),
          EcalStripSumE_deltaEta = cms.double(0.03)
       ),
       cms.PSet(
          dRcone = cms.double(0.12),
          name = cms.string('tau_en_recovery'),
          plugin = cms.string('RecoTauEnergyRecoveryPlugin2')
          ),
       #cms.PSet( #MB assume that TauTagInfo not mandatory for HPS
       #   pfTauTagInfoSrc = cms.InputTag("pfRecoTauTagInfoProducer"),
       #   name = cms.string('TTIworkaround'),
       #   plugin = cms.string('RecoTauTagInfoWorkaroundModifer')
       #)
    ),
    jetRegionSrc = cms.InputTag("hltTauPFJets08Region"),
    jetSrc = cms.InputTag("hltAntiKT5PFJetsForTaus"),
    builders = cms.VPSet(
       cms.PSet(
           usePFLeptons = cms.bool(True),
           name = cms.string('combinatoric'),
           plugin = cms.string('RecoTauBuilderCombinatoricPlugin'),
           qualityCuts = process.hltPFTauPiZerosOnl2.builders[0].qualityCuts,
           decayModes = cms.VPSet(
              cms.PSet(
                 nPiZeros = cms.uint32(0),
                 nCharged = cms.uint32(1),
                 maxPiZeros = cms.uint32(0),
                 maxTracks = cms.uint32(6)
              ),
              cms.PSet(
                 nPiZeros = cms.uint32(1),
                 nCharged = cms.uint32(1),
                 maxPiZeros = cms.uint32(6),
                 maxTracks = cms.uint32(6)
              ),
              cms.PSet(
                 nPiZeros = cms.uint32(2),
                 nCharged = cms.uint32(1),
                 maxPiZeros = cms.uint32(5),
                 maxTracks = cms.uint32(6)
              ),
              cms.PSet(
                 nPiZeros = cms.uint32(0),
                 nCharged = cms.uint32(3),
                 maxPiZeros = cms.uint32(0),
                 maxTracks = cms.uint32(6)
              )
           ),
           isolationConeSize = cms.double(0.5),
           pfCandSrc = cms.InputTag("hltParticleFlowForTaus")
       )
    ),
    buildNullTaus = cms.bool(True)
)
process.hltHpsSelectionDiscriminator = cms.EDProducer(
    "PFRecoTauDiscriminationByHPSSelection",
    PFTauProducer = cms.InputTag("hltCombinatoricRecoTaus"),
    Prediscriminants = cms.PSet(
      BooleanOperator = cms.string('and')
    ),
    minTauPt = cms.double(0.0),
    requireTauChargedHadronsToBeChargedPFCands = cms.bool(True),
    coneSizeFormula = cms.string('max(min(0.12, 3.5/pt()),0.07)'),
    matchingCone = cms.double(0.3),
    decayModes = cms.VPSet(
       cms.PSet(
          nPiZeros = cms.uint32(0),
          minMass = cms.double(-1000.0),
          maxMass = cms.string('1.'),
          nCharged = cms.uint32(1)
       ),
       cms.PSet(
          nPiZeros = cms.uint32(1),
          assumeStripMass = cms.double(0.1349),
          minMass = cms.double(0.3),
          maxMass = cms.string('max(1.3, min(1.3*sqrt(pt/200.), 2.1))'),
          nCharged = cms.uint32(1)
       ),
       cms.PSet(
          minPi0Mass = cms.double(0.05),
          maxMass = cms.string('max(1.2, min(1.2*sqrt(pt/200.), 2.0))'),
          maxPi0Mass = cms.double(0.2),
          nPiZeros = cms.uint32(2),
          minMass = cms.double(0.4),
          nCharged = cms.uint32(1),
          assumeStripMass = cms.double(0.0)
       ),
       cms.PSet(
          nPiZeros = cms.uint32(0),
          minMass = cms.double(0.8),
          maxMass = cms.string('1.5'),
          nCharged = cms.uint32(3)
       )
    )
)                              
process.hltPFTausHPSSansRef = cms.EDProducer(
    "RecoTauCleaner",
    cleaners = cms.VPSet(
       cms.PSet(
          selectionPassFunction = cms.string('abs(charge())-1'),
          selection = cms.string('signalPFChargedHadrCands().size() = 3'),
          name = cms.string('UnitCharge'),
          plugin = cms.string('RecoTauStringCleanerPlugin'),
          selectionFailValue = cms.double(0)
       ),
       cms.PSet(
          selectionPassFunction = cms.string('0'),
          selection = cms.string('signalPiZeroCandidates().size() = 0 | signalPiZeroCandidates()[0].pt > 2.5'),
          name = cms.string('leadStripPtLt2_5'),
          plugin = cms.string('RecoTauStringCleanerPlugin'),
          selectionFailValue = cms.double(1000.0)
       ),
       cms.PSet(
          src = cms.InputTag("hltHpsSelectionDiscriminator"),
          name = cms.string('HPS_Select'),
          plugin = cms.string('RecoTauDiscriminantCleanerPlugin')
          ),
       cms.PSet(
          selectionPassFunction = cms.string('isolationPFChargedHadrCandsPtSum()+isolationPFGammaCandsEtSum()'),
          selection = cms.string('leadPFCand().isNonnull()'),
          name = cms.string('CombinedIsolation'),
          plugin = cms.string('RecoTauStringCleanerPlugin'),
          selectionFailValue = cms.double(1000.0)
       )
    ),
    src = cms.InputTag("hltCombinatoricRecoTaus")
)
process.hltPFTausHPS = cms.EDProducer(
    "RecoTauPiZeroUnembedder",
    src = cms.InputTag("hltPFTausHPSSansRef"),
    tauTransverseImpactParameterSource = cms.InputTag('')
)
process.hltPFTauTrackFindingDiscriminatorHPS = cms.EDProducer(
    "PFRecoTauDiscriminationByHPSSelection",
    PFTauProducer = cms.InputTag("hltPFTausHPS"),
    Prediscriminants = cms.PSet(
       BooleanOperator = cms.string('and')
    ),
    minTauPt = cms.double(0.0),
    requireTauChargedHadronsToBeChargedPFCands = cms.bool(True),
    coneSizeFormula = cms.string('max(min(0.12, 3.5/pt()),0.07)'),
    decayModes = cms.VPSet(
       cms.PSet(
          nPiZeros = cms.uint32(0),
          minMass = cms.double(-1000.0),
          maxMass = cms.string('1.'),
          nCharged = cms.uint32(1)
       ),
       cms.PSet(
          nPiZeros = cms.uint32(1),
          assumeStripMass = cms.double(0.1349),
          minMass = cms.double(0.3),
          maxMass = cms.string('max(1.3, min(1.3*sqrt(pt/200.), 2.1))'),
          nCharged = cms.uint32(1)
       ),
       cms.PSet(
          minPi0Mass = cms.double(0.05),
          maxMass = cms.string('max(1.2, min(1.2*sqrt(pt/200.), 2.0))'),
          maxPi0Mass = cms.double(0.2),
          nPiZeros = cms.uint32(2),
          minMass = cms.double(0.4),
          nCharged = cms.uint32(1),
          assumeStripMass = cms.double(0.0)
          ),
       cms.PSet(
          nPiZeros = cms.uint32(0),
          minMass = cms.double(0.8),
          maxMass = cms.string('1.5'),
          nCharged = cms.uint32(3)
       )
    ),
    matchingCone = cms.double(0.3)
)
process.hltPFTauLooseIsolationDiscriminatorHPS =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauLooseIsolationDiscriminatorHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminatorHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauLooseIsolationDiscriminatorHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauLooseIsolationDiscriminator5hitsHPS = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauLooseIsolationDiscriminator5hitsHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminator5hitsHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauLooseIsolationDiscriminator5hitsHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauLooseIsolationDiscriminator3hitsHPS = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauLooseIsolationDiscriminator3hitsHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauLooseIsolationDiscriminator3hitsHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauLooseIsolationDiscriminator3hitsHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauECalIsolationDiscriminatorHPS = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauECalIsolationDiscriminatorHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauECalIsolationDiscriminatorHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauECalIsolationDiscriminatorHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauTrkIsolationDiscriminatorHPS = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauTrkIsolationDiscriminatorHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminatorHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauTrkIsolationDiscriminatorHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauTrkIsolationDiscriminator5hitsHPS = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauTrkIsolationDiscriminator5hitsHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminator5hitsHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauTrkIsolationDiscriminator5hitsHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauTrkIsolationDiscriminator3hitsHPS = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauTrkIsolationDiscriminator3hitsHPS.qualityCuts.primaryVertexSrc = "hltOnlinePrimaryVertices"
process.hltPFTauTrkIsolationDiscriminator3hitsHPS.qualityCuts.pvFindingAlgo = "highestWeightForLeadTrack"
process.hltPFTauTrkIsolationDiscriminator3hitsHPS.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminatorHPS"
process.hltPFTauAgainstMuonDiscriminatorLooseHPS = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseHPS.PFTauProducer = "hltPFTausHPS"
process.hltPFTauAgainstMuonDiscriminatorHoPHPS = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPHPS.PFTauProducer = "hltPFTausHPS"

process.hltPFTauSequnceHPS = cms.Sequence(
    process.hltTauPFJets08Region +
    process.hltPFTauPiZerosOnl2 +
    process.hltTauPFJetsRecoTauChargedHadronsOnl2 +
    process.hltCombinatoricRecoTaus +
    process.hltHpsSelectionDiscriminator +
    process.hltPFTausHPSSansRef +
    process.hltPFTausHPS +
    process.hltPFTauTrackFindingDiscriminatorHPS +
    process.hltPFTauLooseIsolationDiscriminatorHPS + 
    process.hltPFTauLooseIsolationDiscriminator5hitsHPS + 
    process.hltPFTauLooseIsolationDiscriminator3hitsHPS + 
    process.hltPFTauECalIsolationDiscriminatorHPS +
    process.hltPFTauTrkIsolationDiscriminatorHPS +
    process.hltPFTauTrkIsolationDiscriminator5hitsHPS +
    process.hltPFTauTrkIsolationDiscriminator3hitsHPS
    +process.hltPFTauAgainstMuonDiscriminatorLooseHPS
    +process.hltPFTauAgainstMuonDiscriminatorHoPHPS
    )

#########################
## PAT taus from HLT taus

#generic configuration for tauId
tauIdGeneric = cms.PSet(
        # configure many IDs as InputTag <someName> = <someTag>
        # you can comment out those you don't want to save some
        # disk space
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorGeneric"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorGeneric"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorGeneric"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorGeneric"),
)

hltPatTausGeneric = cms.EDProducer(
    "PATTauProducer",
    # input
    tauSource = cms.InputTag("hltPFTausGeneric"),
    # add user data
    userData = cms.PSet(
      # add custom classes here
      userClasses = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add doubles here
      userFloats = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add ints here
      userInts = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add candidate ptrs here
      userCands = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add "inline" functions here
      userFunctions = cms.vstring(),
      userFunctionLabels = cms.vstring()
    ),
    # jet energy corrections
    addTauJetCorrFactors = cms.bool(False),
    tauJetCorrFactorsSource = cms.VInputTag(cms.InputTag("patTauJetCorrFactors")),
    # embedding objects (for Calo- and PFTaus)
    embedLeadTrack = cms.bool(False), ## embed in AOD externally stored leading track
    embedSignalTracks = cms.bool(False), ## embed in AOD externally stored signal tracks
    embedIsolationTracks = cms.bool(False), ## embed in AOD externally stored isolation tracks
    # embedding objects (for PFTaus only)
    embedLeadPFCand = cms.bool(False), ## embed in AOD externally stored leading PFCandidate
    embedLeadPFChargedHadrCand = cms.bool(False), ## embed in AOD externally stored leading PFChargedHadron candidate
    embedLeadPFNeutralCand = cms.bool(False), ## embed in AOD externally stored leading PFNeutral Candidate
    embedSignalPFCands = cms.bool(False), ## embed in AOD externally stored signal PFCandidates
    embedSignalPFChargedHadrCands = cms.bool(False), ## embed in AOD externally stored signal PFChargedHadronCandidates
    embedSignalPFNeutralHadrCands = cms.bool(False), ## embed in AOD externally stored signal PFNeutralHadronCandidates
    embedSignalPFGammaCands = cms.bool(False), ## embed in AOD externally stored signal PFGammaCandidates
    embedIsolationPFCands = cms.bool(False), ## embed in AOD externally stored isolation PFCandidates
    embedIsolationPFChargedHadrCands = cms.bool(False), ## embed in AOD externally stored isolation PFChargedHadronCandidates
    embedIsolationPFNeutralHadrCands = cms.bool(False), ## embed in AOD externally stored isolation PFNeutralHadronCandidates
    embedIsolationPFGammaCands = cms.bool(False), ## embed in AOD externally stored isolation PFGammaCandidates

    # embed IsoDeposits
    isoDeposits = cms.PSet(),
    # user defined isolation variables the variables defined here will be accessible
    # via pat::Tau::userIsolation(IsolationKeys key) with the key as defined in
    # DataFormats/PatCandidates/interface/Isolation.h
    #
    # (set Pt thresholds for PFChargedHadrons (PFGammas) to 1.0 (1.5) GeV,
    # matching the thresholds used when computing the tau iso. discriminators
    # in RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByIsolation_cfi.py)
    userIsolation = cms.PSet(),
    # tau ID (for efficiency studies)
    addTauID     = cms.bool(True),
    tauIDSources = tauIdGeneric,
    # mc matching configurables
    addGenMatch      = cms.bool(False),
    embedGenMatch    = cms.bool(False),
    genParticleMatch = cms.InputTag(""),
    addGenJetMatch   = cms.bool(False),
    embedGenJetMatch = cms.bool(False),
    genJetMatch      = cms.InputTag(""),
    # efficiencies
    addEfficiencies = cms.bool(False),
    efficiencies    = cms.PSet(),
    # resolution
    addResolutions  = cms.bool(False),
    resolutions     = cms.PSet(),
    #
    tauTransverseImpactParameterSource = cms.InputTag("")
)
###
process.selectedHltPatTaus = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("hltPatTaus"),
    #cut = cms.string("pt>17"),
    cut = cms.string("pt>0"),
    filter = cms.bool(False)
    )
###
process.hltPatTausNP = hltPatTausGeneric.clone(tauSource = 'hltPFTausNP')
process.hltPatTausNP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorNP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorNP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsNP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsNP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorNP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorNP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsNP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsNP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseNP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPNP"),
        )
process.selectedHltPatTausNP = process.selectedHltPatTaus.clone(src='hltPatTausNP')

###
process.hltPatTausOnlNP = hltPatTausGeneric.clone(tauSource = 'hltPFTausOnlNP')
process.hltPatTausOnlNP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorOnlNP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorOnlNP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsOnlNP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsOnlNP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorOnlNP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorOnlNP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsOnlNP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsOnlNP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseOnlNP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPOnlNP"),
        )
process.selectedHltPatTausOnlNP = process.selectedHltPatTaus.clone(src='hltPatTausOnlNP')

######
process.hltPatTausOnl2NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausOnl2NP')
process.hltPatTausOnl2NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorOnl2NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorOnl2NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsOnl2NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsOnl2NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorOnl2NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorOnl2NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsOnl2NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsOnl2NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseOnl2NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPOnl2NP"),
        )
process.selectedHltPatTausOnl2NP = process.selectedHltPatTaus.clone(src='hltPatTausOnl2NP')

###
process.hltPatTausPxlNP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxlNP')
process.hltPatTausPxlNP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxlNP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxlNP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxlNP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxlNP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxlNP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxlNP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxlNP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxlNP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxlNP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxlNP"),
        )
process.selectedHltPatTausPxlNP = process.selectedHltPatTaus.clone(src='hltPatTausPxlNP')

###
process.hltPatTausPxl2NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2NP')
process.hltPatTausPxl2NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2NP"),
        )
process.selectedHltPatTausPxl2NP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2NP')

###
process.hltPatTausPxl2R15N3NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R15N3NP')
process.hltPatTausPxl2R15N3NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R15N3NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R15N3NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N3NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N3NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R15N3NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R15N3NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N3NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N3NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R15N3NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R15N3NP"),
        )
process.selectedHltPatTausPxl2R15N3NP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R15N3NP')
process.hltPatTausPxl2R18N3NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R18N3NP')
process.hltPatTausPxl2R18N3NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R18N3NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R18N3NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N3NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N3NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R18N3NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R18N3NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N3NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N3NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R18N3NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R18N3NP"),
        )
process.selectedHltPatTausPxl2R18N3NP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R18N3NP')
process.hltPatTausPxl2R12N5NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R12N5NP')
process.hltPatTausPxl2R12N5NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R12N5NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R12N5NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R12N5NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R12N5NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R12N5NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R12N5NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R12N5NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R12N5NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R12N5NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R12N5NP"),
        )
process.selectedHltPatTausPxl2R12N5NP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R12N5NP')
process.hltPatTausPxl2R15N5NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R15N5NP')
process.hltPatTausPxl2R15N5NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R15N5NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R15N5NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R15N5NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R15N5NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R15N5NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R15N5NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R15N5NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R15N5NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R15N5NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R15N5NP"),
        )
process.selectedHltPatTausPxl2R15N5NP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R15N5NP')
process.hltPatTausPxl2R18N5NP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R18N5NP')
process.hltPatTausPxl2R18N5NP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R18N5NP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R18N5NP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R18N5NP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R18N5NP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R18N5NP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R18N5NP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R18N5NP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R18N5NP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R18N5NP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R18N5NP"),
        )
process.selectedHltPatTausPxl2R18N5NP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R18N5NP')
process.hltPatTausPxl2R12NInfNP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R12NInfNP')
process.hltPatTausPxl2R12NInfNP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R12NInfNP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R12NInfNP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R12NInfNP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R12NInfNP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R12NInfNP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R12NInfNP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R12NInfNP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R12NInfNP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R12NInfNP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R12NInfNP"),
        )
process.selectedHltPatTausPxl2R12NInfNP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R12NInfNP')
process.hltPatTausPxl2R15NInfNP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R15NInfNP')
process.hltPatTausPxl2R15NInfNP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R15NInfNP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R15NInfNP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R15NInfNP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R15NInfNP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R15NInfNP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R15NInfNP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R15NInfNP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R15NInfNP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R15NInfNP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R15NInfNP"),
        )
process.selectedHltPatTausPxl2R15NInfNP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R15NInfNP')
process.hltPatTausPxl2R18NInfNP = hltPatTausGeneric.clone(tauSource = 'hltPFTausPxl2R18NInfNP')
process.hltPatTausPxl2R18NInfNP.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorPxl2R18NInfNP"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorPxl2R18NInfNP"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsPxl2R18NInfNP"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsPxl2R18NInfNP"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorPxl2R18NInfNP"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorPxl2R18NInfNP"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsPxl2R18NInfNP"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsPxl2R18NInfNP"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLoosePxl2R18NInfNP"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPPxl2R18NInfNP"),
        )
process.selectedHltPatTausPxl2R18NInfNP = process.selectedHltPatTaus.clone(src='hltPatTausPxl2R18NInfNP')

###
process.hltPatTausHPS = hltPatTausGeneric.clone(tauSource = 'hltPFTausHPS')
process.hltPatTausHPS.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminatorHPS"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorHPS"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsHPS"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsHPS"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorHPS"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorHPS"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsHPS"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsHPS"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseHPS"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPHPS"),
        )
process.selectedHltPatTausHPS = process.selectedHltPatTaus.clone(src='hltPatTausHPS')


process.hltTauSequence = cms.Sequence(
    process.hltKT6PFJetsForTaus + process.hltOnlinePrimaryVertices +

    process.hltPFTauSequnceOnlNP +
    process.hltPatTausOnlNP + process.selectedHltPatTausOnlNP +
    process.hltPFTauSequnceOnl2NP +
    process.hltPatTausOnl2NP + process.selectedHltPatTausOnl2NP +
    process.hltPFTauSequncePxlNP +
    process.hltPatTausPxlNP + process.selectedHltPatTausPxlNP +
    process.hltPFTauSequncePxl2NP +
    process.hltPatTausPxl2NP + process.selectedHltPatTausPxl2NP +

    process.hltPFTauSequncePxl2NPTuning +
    process.hltPatTausPxl2R15N3NP + process.selectedHltPatTausPxl2R15N3NP +
    process.hltPatTausPxl2R18N3NP + process.selectedHltPatTausPxl2R18N3NP +
    process.hltPatTausPxl2R12N5NP + process.selectedHltPatTausPxl2R12N5NP +
    process.hltPatTausPxl2R15N5NP + process.selectedHltPatTausPxl2R15N5NP +
    process.hltPatTausPxl2R18N5NP + process.selectedHltPatTausPxl2R18N5NP +
    process.hltPatTausPxl2R12NInfNP + process.selectedHltPatTausPxl2R12NInfNP +
    process.hltPatTausPxl2R15NInfNP + process.selectedHltPatTausPxl2R15NInfNP +
    process.hltPatTausPxl2R18NInfNP + process.selectedHltPatTausPxl2R18NInfNP

    + process.hltPFTauSequnceHPS +
    process.hltPatTausHPS + process.selectedHltPatTausHPS
    )

process.hltTauMuVtxSequence = cms.Sequence(
    process.hltKT6PFJetsForTaus + process.hltIsoMuonVertex +
    process.hltPFTauSequnceNP +
    process.hltPatTausNP + process.selectedHltPatTausNP
    )


## Legacy HLT taus for reference
# MuTau
# Most of stuff already in master, add isolation anti-mu and pat
process.hltPFTauLooseIsolationDiscriminatorIsoMuTauLegacy =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauLooseIsolationDiscriminatorIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauLooseIsolationDiscriminatorIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauLooseIsolationDiscriminator5hitsIsoMuTauLegacy = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauLooseIsolationDiscriminator5hitsIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauLooseIsolationDiscriminator5hitsIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauLooseIsolationDiscriminator3hitsIsoMuTauLegacy = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauLooseIsolationDiscriminator3hitsIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauLooseIsolationDiscriminator3hitsIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauECalIsolationDiscriminatorIsoMuTauLegacy = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauECalIsolationDiscriminatorIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauECalIsolationDiscriminatorIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminatorIsoMuTauLegacy = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauTrkIsolationDiscriminatorIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauTrkIsolationDiscriminatorIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminator5hitsIsoMuTauLegacy = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauTrkIsolationDiscriminator5hitsIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauTrkIsolationDiscriminator5hitsIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminator3hitsIsoMuTauLegacy = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauTrkIsolationDiscriminator3hitsIsoMuTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoMuonVertex"
process.hltPFTauTrkIsolationDiscriminator3hitsIsoMuTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoMuPFTauTrackFindingDiscriminator"
process.hltPFTauAgainstMuonDiscriminatorLooseIsoMuTauLegacy = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
process.hltPFTauAgainstMuonDiscriminatorHoPIsoMuTauLegacy = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPIsoMuTauLegacy.PFTauProducer = "hltIsoMuPFTaus"
#
process.hltPatTausIsoMuLegacy = hltPatTausGeneric.clone(tauSource = 'hltIsoMuPFTaus')
process.hltPatTausIsoMuLegacy.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltIsoMuPFTauTrackFindingDiscriminator"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorIsoMuTauLegacy"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsIsoMuTauLegacy"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsIsoMuTauLegacy"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorIsoMuTauLegacy"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorIsoMuTauLegacy"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsIsoMuTauLegacy"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsIsoMuTauLegacy"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseIsoMuTauLegacy"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPIsoMuTauLegacy"),
        )
process.selectedHltPatTausIsoMuLegacy = process.selectedHltPatTaus.clone(src='hltPatTausIsoMuLegacy')
# 
process.hltIsoMuTauLegacySequence = cms.Sequence(
    # from master
    process.hltPFTauJetTracksAssociator + 
    process.hltIsoMuonVertex + 
    process.hltIsoMuPFTauTagInfo + 
    process.hltIsoMuPFTaus +
    process.hltIsoMuPFTauTrackFindingDiscriminator +
    # defined in this config
    process.hltPFTauLooseIsolationDiscriminatorIsoMuTauLegacy + 
    process.hltPFTauLooseIsolationDiscriminator5hitsIsoMuTauLegacy + 
    process.hltPFTauLooseIsolationDiscriminator3hitsIsoMuTauLegacy + 
    process.hltPFTauECalIsolationDiscriminatorIsoMuTauLegacy +
    process.hltPFTauTrkIsolationDiscriminatorIsoMuTauLegacy +
    process.hltPFTauTrkIsolationDiscriminator5hitsIsoMuTauLegacy +
    process.hltPFTauTrkIsolationDiscriminator3hitsIsoMuTauLegacy
    + process.hltPFTauAgainstMuonDiscriminatorLooseIsoMuTauLegacy
    + process.hltPFTauAgainstMuonDiscriminatorHoPIsoMuTauLegacy
    # pat
    + process.hltPatTausIsoMuLegacy + process.selectedHltPatTausIsoMuLegacy
)
# EleTau
# Most of stuff already in master, add isolation anti-mu and pat
process.hltPFTauLooseIsolationDiscriminatorIsoEleTauLegacy =  process.hltPFTauLooseIsolationDiscriminatorOffVtx.clone()
process.hltPFTauLooseIsolationDiscriminatorIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauLooseIsolationDiscriminatorIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauLooseIsolationDiscriminatorIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauLooseIsolationDiscriminator5hitsIsoEleTauLegacy = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauLooseIsolationDiscriminator5hitsIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauLooseIsolationDiscriminator5hitsIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauLooseIsolationDiscriminator3hitsIsoEleTauLegacy = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauLooseIsolationDiscriminator3hitsIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauLooseIsolationDiscriminator3hitsIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauECalIsolationDiscriminatorIsoEleTauLegacy = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauECalIsolationDiscriminatorIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauECalIsolationDiscriminatorIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminatorIsoEleTauLegacy = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauTrkIsolationDiscriminatorIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauTrkIsolationDiscriminatorIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminator5hitsIsoEleTauLegacy = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauTrkIsolationDiscriminator5hitsIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauTrkIsolationDiscriminator5hitsIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminator3hitsIsoEleTauLegacy = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauTrkIsolationDiscriminator3hitsIsoEleTauLegacy.qualityCuts.primaryVertexSrc = "hltIsoEleVertex"
process.hltPFTauTrkIsolationDiscriminator3hitsIsoEleTauLegacy.Prediscriminants.leadTrack.Producer = "hltIsoElePFTauTrackFindingDiscriminator"
process.hltPFTauAgainstMuonDiscriminatorLooseIsoEleTauLegacy = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
process.hltPFTauAgainstMuonDiscriminatorHoPIsoEleTauLegacy = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPIsoEleTauLegacy.PFTauProducer = "hltIsoElePFTaus"
#
process.hltPatTausIsoEleLegacy = hltPatTausGeneric.clone(tauSource = 'hltIsoElePFTaus')
process.hltPatTausIsoEleLegacy.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltIsoElePFTauTrackFindingDiscriminator"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminatorIsoEleTauLegacy"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsIsoEleTauLegacy"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsIsoEleTauLegacy"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorIsoEleTauLegacy"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorIsoEleTauLegacy"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsIsoEleTauLegacy"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsIsoEleTauLegacy"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseIsoEleTauLegacy"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPIsoEleTauLegacy"),
        )
process.selectedHltPatTausIsoEleLegacy = process.selectedHltPatTaus.clone(src='hltPatTausIsoEleLegacy')
#
process.hltIsoEleTauLegacySequence = cms.Sequence(
    # from master
    process.hltPFTauJetTracksAssociator + 
    process.hltIsoEleVertex + 
    process.hltIsoElePFTauTagInfo + 
    process.hltIsoElePFTaus + 
    process.hltIsoElePFTau20 + 
    process.hltIsoElePFTauTrackFindingDiscriminator +
    # defined in this config
    process.hltPFTauLooseIsolationDiscriminatorIsoEleTauLegacy + 
    process.hltPFTauLooseIsolationDiscriminator5hitsIsoEleTauLegacy + 
    process.hltPFTauLooseIsolationDiscriminator3hitsIsoEleTauLegacy + 
    process.hltPFTauECalIsolationDiscriminatorIsoEleTauLegacy +
    process.hltPFTauTrkIsolationDiscriminatorIsoEleTauLegacy +
    process.hltPFTauTrkIsolationDiscriminator5hitsIsoEleTauLegacy +
    process.hltPFTauTrkIsolationDiscriminator3hitsIsoEleTauLegacy
    + process.hltPFTauAgainstMuonDiscriminatorLooseIsoEleTauLegacy
    + process.hltPFTauAgainstMuonDiscriminatorHoPIsoEleTauLegacy
    # pat
    + process.hltPatTausIsoEleLegacy + process.selectedHltPatTausIsoEleLegacy
)

# singleTau
# Most of stuff already in master, add isolation anti-mu and pat
process.hltPFTauLooseIsolationDiscriminator5hitsTauLegacy = process.hltPFTauLooseIsolationDiscriminator5hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator5hitsTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauLooseIsolationDiscriminator5hitsTauLegacy.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminator5hitsTauLegacy.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminator"
process.hltPFTauLooseIsolationDiscriminator3hitsTauLegacy = process.hltPFTauLooseIsolationDiscriminator3hitsOffVtx.clone() 
process.hltPFTauLooseIsolationDiscriminator3hitsTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauLooseIsolationDiscriminator3hitsTauLegacy.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauLooseIsolationDiscriminator3hitsTauLegacy.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminator"
process.hltPFTauECalIsolationDiscriminatorTauLegacy = process.hltPFTauECalIsolationDiscriminatorOffVtx.clone()
process.hltPFTauECalIsolationDiscriminatorTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauECalIsolationDiscriminatorTauLegacy.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauECalIsolationDiscriminatorTauLegacy.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminatorTauLegacy = process.hltPFTauTrkIsolationDiscriminatorOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminatorTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauTrkIsolationDiscriminatorTauLegacy.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminatorTauLegacy.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminator5hitsTauLegacy = process.hltPFTauTrkIsolationDiscriminator5hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator5hitsTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauTrkIsolationDiscriminator5hitsTauLegacy.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminator5hitsTauLegacy.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminator"
process.hltPFTauTrkIsolationDiscriminator3hitsTauLegacy = process.hltPFTauTrkIsolationDiscriminator3hitsOffVtx.clone()
process.hltPFTauTrkIsolationDiscriminator3hitsTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauTrkIsolationDiscriminator3hitsTauLegacy.qualityCuts.primaryVertexSrc = "hltPixelVertices"
process.hltPFTauTrkIsolationDiscriminator3hitsTauLegacy.Prediscriminants.leadTrack.Producer = "hltPFTauTrackFindingDiscriminator"
process.hltPFTauAgainstMuonDiscriminatorLooseTauLegacy = process.hltPFTauAgainstMuonDiscriminatorLooseOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorLooseTauLegacy.PFTauProducer = "hltPFTaus"
process.hltPFTauAgainstMuonDiscriminatorHoPTauLegacy = process.hltPFTauAgainstMuonDiscriminatorHoPOffVtx.clone()
process.hltPFTauAgainstMuonDiscriminatorHoPTauLegacy.PFTauProducer = "hltPFTaus"
#
process.hltPatTausLegacy = hltPatTausGeneric.clone(tauSource = 'hltPFTaus')
process.hltPatTausLegacy.tauIDSources = cms.PSet(
        decayModeFinding = cms.InputTag("hltPFTauTrackFindingDiscriminator"),
        byIsolation = cms.InputTag("hltPFTauLooseIsolationDiscriminator"),
        byIsolation5hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator5hitsTauLegacy"),
        byIsolation3hits = cms.InputTag("hltPFTauLooseIsolationDiscriminator3hitsTauLegacy"),
        byECalIsolation = cms.InputTag("hltPFTauECalIsolationDiscriminatorTauLegacy"),
        byTrkIsolation = cms.InputTag("hltPFTauTrkIsolationDiscriminatorTauLegacy"),
        byTrkIsolation5hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator5hitsTauLegacy"),
        byTrkIsolation3hits = cms.InputTag("hltPFTauTrkIsolationDiscriminator3hitsTauLegacy"),
        againstMuonLoose = cms.InputTag("hltPFTauAgainstMuonDiscriminatorLooseTauLegacy"),
        againstMuonHoP = cms.InputTag("hltPFTauAgainstMuonDiscriminatorHoPTauLegacy"),
        )
process.selectedHltPatTausLegacy = process.selectedHltPatTaus.clone(src='hltPatTausLegacy')
#
process.hltTauLegacySequence = cms.Sequence( 
    # from master
    process.hltPFTauJetTracksAssociator + 
    process.hltPFTauTagInfo + 
    process.hltPFTaus + 
    process.hltPFTauTrackFindingDiscriminator + 
    process.hltPFTauLooseIsolationDiscriminator +
    # defined in this config
    process.hltPFTauLooseIsolationDiscriminator5hitsTauLegacy + 
    process.hltPFTauLooseIsolationDiscriminator3hitsTauLegacy + 
    process.hltPFTauECalIsolationDiscriminatorTauLegacy +
    process.hltPFTauTrkIsolationDiscriminatorTauLegacy +
    process.hltPFTauTrkIsolationDiscriminator5hitsTauLegacy +
    process.hltPFTauTrkIsolationDiscriminator3hitsTauLegacy
    + process.hltPFTauAgainstMuonDiscriminatorLooseTauLegacy
    + process.hltPFTauAgainstMuonDiscriminatorHoPTauLegacy
    # pat
    + process.hltPatTausLegacy + process.selectedHltPatTausLegacy
)
