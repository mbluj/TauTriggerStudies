
#process.load("L1Trigger.UCT2015.emulation_cfi")
process.load("L1Trigger.UCT2015.emulationMC_cfi") #MB wrong config for 53X MC, use standard one with reruning hcal digis, should be fine for 62X/70X?

#to re-emulate HCal digis
#process.load("SimCalorimetry.HcalSimProducers.hcalUnsuppressedDigis_cfi")
#process.load("SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff")

#process.hcalReEmulDigis = process.simHcalTriggerPrimitiveDigis.clone()
#process.hcalReEmulDigis.inputLabel = cms.VInputTag(cms.InputTag('hcalDigis'), cms.InputTag('hcalDigis'))
#process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
#process.hackHCALMIPs.src = cms.InputTag("hcalReEmulDigis")
#
#process.emulationSequence.replace(process.hcalDigis,
#                                  process.hcalDigis+process.hcalReEmulDigis) #Reproduce HCal digis 


# Determine which calibration to use
from L1Trigger.UCT2015.emulation_cfi import \
        eg_calib_v1, eg_calib_v3, eg_calib_v4

ecal_calibration = eg_calib_v4 #eg_calib_v1 eg_calib_v3
process.RCTConfigProducers.eGammaECalScaleFactors = ecal_calibration
process.RCTConfigProducers.jetMETECalScaleFactors = ecal_calibration
process.UCT2015EClusterProducer.ecalCalibration = ecal_calibration

process.RCTConfigProducers.eicIsolationThreshold = 3
process.RCTConfigProducers.hActivityCut = 0.5

#process.load("L1Trigger.UCT2015.uct2015L1ExtraParticles_cfi")
process.load("L1Trigger.UCT2015.uctl1extraparticles_cfi.py")
#clone UCT gt stuff to have isoTau version in parallel
process.gctUCTDigis2 = process.gctUCTDigis.clone(
    tauIsolated  = cms.InputTag("UCT2015Producer","IsolatedTauUnpacked")
)
process.l1extraParticlesUCT2 = process.l1extraParticlesUCT.clone(
    etTotalSource = cms.InputTag("gctUCTDigis2"),
    nonIsolatedEmSource = cms.InputTag("gctUCTDigis2","nonIsoEm"),
    etMissSource = cms.InputTag("gctUCTDigis2"),
    htMissSource = cms.InputTag("gctUCTDigis2"),
    forwardJetSource = cms.InputTag("gctUCTDigis2","forJets"),
    centralJetSource = cms.InputTag("gctUCTDigis2","cenJets"),
    tauJetSource = cms.InputTag("gctUCTDigis2","tauJets"),
    isolatedEmSource = cms.InputTag("gctUCTDigis2","isoEm"),
    etHadSource = cms.InputTag("gctUCTDigis2"),
    hfRingEtSumsSource = cms.InputTag("gctUCTDigis2"),
    hfRingBitCountsSource = cms.InputTag("gctUCTDigis2")
)
process.gtUCTDigis2 = process.gtUCTDigis.clone(
    GctInputTag  = cms.InputTag("gctUCTDigis2")
)
process.uct2015L1Extra.replace(process.gctUCTDigis,
                               process.gctUCTDigis*process.gctUCTDigis2)
process.uct2015L1Extra.replace(process.gtUCTDigis,
                               process.gtUCTDigis*process.gtUCTDigis2)
process.uct2015L1Extra.replace(process.l1extraParticlesUCT,
                               process.l1extraParticlesUCT*process.l1extraParticlesUCT2)


process.uct2015Sequence = cms.Sequence(
   process.emulationSequence +
   #process.uct2015L1ExtraParticles
   process.uct2015L1Extra
)

#to keep
# *_uct2015L1ExtraParticles_*_*
# *_l1extraParticlesUCT*_*_*
# *_UCT2015Producer_*_*
