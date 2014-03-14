# Dump from ConfDB a setup with common trigger modules and sequences
#echo -n Dumping setup from ConfDB... 
#edmConfigFromDB --cff --configName /online/collisions/2012/8e33/v2.3/HLT/V28 --nopaths > ../python/setup_cff.py
#echo Done!

# Dump from ConfDB configuration with reference Ele+Tau paths and a Ele+Tau path w/o tau filters
echo -n Dumping	Tau paths to hlt.py from ConfDB... 
hltGetConfiguration /users/mbluj/CMSSW_7_0_0/Tau2015/V3 --full --offline --data --unprescale --process TauHLT --globaltag auto:hltonline > hlt_Tau2015_v3.py
echo Done!

# Add setup to configuration,
# i.e. put process.load("TriggerStudies.Tau.setup_cff") after process=cms.Process...:
echo -n Adding setup to hlt.py... 
sed -i -e 's/\(cms\.Process.*\)/\1 \nprocess.load("TriggerStudies\.Tau\.setup_cff")/' hlt_Tau2015_v3.py
echo Done!

# Add isMC switch
echo -n Adding isMC to hlt.py...
sed -i '3i\#\ User\ switches\nisMC\ =\ False\n' hlt_Tau2015_v3.py

n=`sed -n '/Enable\ HF\ Noise\ filters\ in\ GRun\ menu/=' hlt_Tau2015_v3.py`
n=$(( $n + 4 )) 
sed -i "${n}i\#\ customise\ the\ HLT\ menu\ for\ running\ on\ MC\nif\ isMC\:\n\tfrom\ HLTrigger\.Configuration\.customizeHLTforMC\ import\ customizeHLTforMC\n\tprocess\ =\ customizeHLTforMC(process)\n" hlt_Tau2015_v3.py

sed -i "$ a\if\ isMC\:\n\tprocess\.GlobalTag\ =\ customiseGlobalTag\(process\.GlobalTag\,\ globaltag\ =\ \'auto\:startup\'\)\n" hlt_Tau2015_v3.py
echo Done!

## Add offline stuff and output module
sed -i '$ a\#\#\#\#\#\#\#\#\#\n\#\#\#\ Final customisation\n' hlt_Tau2015_v3.py  
echo -n Adding offline stuff and output module to hlt.py...
sed -i '$ a\#\ Add output module and offline+PAT\nif not isMC:\n\texecfile\(\"pat-and-out\.py\"\)\nelse:\n\texecfile\(\"pat-and-out_MC\.py\"\)\n' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTEndSequence,\n\tprocess\.offlineSequence+process\.HLTEndSequence\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTEndSequence,\n\tprocess\.offlineSequence+process\.HLTEndSequence\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_SingleLooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTEndSequence,\n\tprocess\.offlineSequence+process\.HLTEndSequence\n\)' hlt_Tau2015_v3.py
# Add isFake switch
sed -i '5iisFake\ =\ False\n' hlt_Tau2015_v3.py
sed -i "$ a\# Add\ offline\ filters\nif not isFake:" hlt_Tau2015_v3.py
sed -i '$ a\\tprocess\.HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v8\.replace\(\n\t\tprocess\.HLTEndSequence,\n\t\tprocess\.offlineMuTauSelectionSequence+process\.HLTEndSequence\n\t\)' hlt_Tau2015_v3.py
sed -i '$ a\\tprocess\.HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20_v8\.replace\(\n\t\tprocess\.HLTEndSequence,\n\t\tprocess\.offlineElTauSelectionSequence+process\.HLTEndSequence\n\t\)' hlt_Tau2015_v3.py
sed -i '$ a\\tprocess\.HLT_SingleLooseIsoPFTau20_v8\.replace\(\n\t\tprocess\.HLTEndSequence,\n\t\tprocess\.offlineTauSelectionSequence+process\.HLTEndSequence\n\t\)' hlt_Tau2015_v3.py
echo Done!

# Add online taus
echo -n Adding new online taus...
sed -i '$ a\#\ Add new online taus\nexecfile\(\"online-tau-rereco_v3\.1\.py\"\)\n' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTIsoMuLooseIsoPFTauSequence,\n\tprocess\.hltTauSequence+process\.hltTauMuVtxSequence\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTIsoEleLooseIsoPFTauSequence,\n\tprocess\.hltTauSequence+process\.hltIsoEleVertex\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_SingleLooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTLooseIsoPFTauSequence,\n\tprocess\.hltTauSequence\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_SingleLooseIsoPFTau20_v8\.remove\(process\.hltPFTau20\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_SingleLooseIsoPFTau20_v8\.remove\(process\.hltPFTau20Track\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_SingleLooseIsoPFTau20_v8\.remove\(process\.hltPFTau20TrackLooseIso\)' hlt_Tau2015_v3.py
echo Done!

# Add UCT2015 stuff
echo -n Adding UCT2015 stuff... 
sed -i '$ a\#\ Add UCT2015 stuff\nif not isMC:\n\texecfile\(\"uct2015\.py\"\)\nelse:\n\texecfile\(\"uct2015_MC\.py\"\)\n' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTEndSequence,\n\tprocess\.uct2015Sequence+process\.HLTEndSequence\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTEndSequence,\n\tprocess\.uct2015Sequence+process\.HLTEndSequence\n\)' hlt_Tau2015_v3.py
sed -i '$ aprocess\.HLT_SingleLooseIsoPFTau20_v8\.replace\(\n\tprocess\.HLTEndSequence,\n\tprocess\.uct2015Sequence+process\.HLTEndSequence\n\)' hlt_Tau2015_v3.py

echo Done

# Tune output and pat and uct2015
sed -i '$ a\#\ Tune\ output' hlt_Tau2015_v3.py
sed -i '$ aprocess\.patOut\.SelectEvents\.SelectEvents\ =\ []' hlt_Tau2015_v3.py
sed -i '$ aprocess\.patOut\.SelectEvents\.SelectEvents\.append(\"HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v8\")' hlt_Tau2015_v3.py
sed -i '$ aprocess\.patOut\.SelectEvents\.SelectEvents\.append(\"HLT_Ele22_eta2p1_WP90Rho_LooseIsoPFTau20_v8\")' hlt_Tau2015_v3.py
sed -i '$ aprocess\.patOut\.SelectEvents\.SelectEvents\.append(\"HLT_SingleLooseIsoPFTau20_v8\")' hlt_Tau2015_v3.py
#sed -i '$ aprocess\.patOut\.outputCommands\.append(\"keep *_UCT2015Producer_*_*\")' hlt_Tau2015_v3.py


# Customise source (for tests)
echo -n Customise source... 
echo >> hlt_Tau2015_v3.py
sed -i '$ a\# Customise source \(for tests\)\nif not isMC:\n\texecfile\(\"source\.py\"\)\nelse:\n\texecfile\(\"source_MC\.py\"\)\n' hlt_Tau2015_v3.py
sed -i "$ aprocess.maxEvents.input\ =\ -1\n" hlt_Tau2015_v3.py
echo Done!

echo Done!

echo >> hlt_Tau2015_v3.py

echo
echo 'Do not forget complie all pythons (cd $CMSSW_BASE/src; scram b)'
echo
