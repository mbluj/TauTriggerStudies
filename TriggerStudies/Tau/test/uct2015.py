
process.load("L1Trigger.UCT2015.emulation_cfi")
#process.load("L1Trigger.UCT2015.emulationMC_cfi")

# Determine which calibration to use
from L1Trigger.UCT2015.emulation_cfi import \
        eg_calib_v1, eg_calib_v3, eg_calib_v4

ecal_calibration = eg_calib_v4 #eg_calib_v1 eg_calib_v3
process.RCTConfigProducers.eGammaECalScaleFactors = ecal_calibration
process.RCTConfigProducers.jetMETECalScaleFactors = ecal_calibration
process.UCT2015EClusterProducer.ecalCalibration = ecal_calibration

process.RCTConfigProducers.eicIsolationThreshold = 3
process.RCTConfigProducers.hActivityCut = 0.5

process.load("L1Trigger.UCT2015.uct2015L1ExtraParticles_cfi")

process.uct2015Sequence = cms.Sequence(
   process.emulationSequence +
   process.uct2015L1ExtraParticles
)

#to keep
# *_uct2015L1ExtraParticles_*_*
# *_UCT2015Producer_*_*
