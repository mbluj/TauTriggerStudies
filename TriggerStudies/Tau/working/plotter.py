import ROOT

from copy import deepcopy as dc

### style parameters
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetLegendFillColor(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetStatBorderSize(0)
ROOT.gStyle.SetTitleBorderSize(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetTitleSize(0.040,'t')
# ROOT.gStyle.SetTitleOffset(1.200,"X")
# ROOT.gStyle.SetTitleX(-0.038) ## to be changed to 0.15
ROOT.gStyle.SetTitleY(0.96)
ROOT.gStyle.SetTitleW(0.8)
ROOT.gStyle.SetTextFont(42)
ROOT.gStyle.SetLegendFont(42)	
# ROOT.gStyle.SetLabelSize(0.040,'xy')
ROOT.gStyle.SetLabelFont(42, 'xy')
# ROOT.gStyle.SetTitleFont(42, 'xy')
# ROOT.gStyle.SetTitleSize(0.105,'xy')

def doRatio( num, den ) :
  num1 = dc(num)
  den1 = dc(den)
  ratio = dc(num1)
  ratio.Divide(num1,den1,1.,1.,'b')
  ratio.SetMinimum(0.7)
  ratio.SetMaximum(1.1)
  return ratio  

def plot( basehisto, basehistolegend, name, xaxis, yaxis, title='CMS Simulation, #sqrt{s} = 8 TeV', morehistos = {}, color = ROOT.kRed, drawoptions = 'E', log = False , setRangeX = []) :
  '''
  Plots an histogram, eventually more histos to be drawn with Draw(SAME).
  morehistos should be a dict like {histo:[ROOT.kBlue,'legend entry']}
  '''
  c1 = ROOT.TCanvas('','',700,700)
  
  ROOT.gPad.SetLeftMargin(0.18)
  ROOT.gPad.SetBottomMargin(0.18)
  ROOT.gPad.SetFrameLineWidth(3)
  ROOT.gPad.SetGridx(1)
  ROOT.gPad.SetGridy(1)
  ROOT.gPad.SetLogy(log)

  l1 = ROOT.TLegend(0.5,0.3,0.8,0.5)
  l1.AddEntry(basehisto,basehistolegend)
  l1.SetFillColor(0)

  basehisto.SetLineWidth(2)  
  basehisto.SetLineColor(color)
  basehisto.SetMarkerStyle(9)
  basehisto.SetTitle('{TITLE};{XAXIS};{YAXIS}'.format(TITLE=title, XAXIS=xaxis, YAXIS=yaxis))
  basehisto.GetXaxis().SetTitle(xaxis)
  basehisto.GetYaxis().SetTitle(yaxis)
  basehisto.GetYaxis().SetTitleOffset(1.5)
  basehisto.GetXaxis().SetTitleOffset(1.5)
  if setRangeX != [] : basehisto.GetXaxis().SetRangeUser(setRangeX[0],setRangeX[1])  
  #basehisto.DrawNormalized(drawoptions)
  basehisto.Draw(drawoptions)
  
  for key in morehistos.keys() :
    l1.AddEntry(key,morehistos[key][1])
    key.SetLineWidth(2)  
    key.SetLineColor(morehistos[key][0])
    key.SetMarkerStyle(9)
    key.Draw('SAME'+drawoptions)

  if len(basehistolegend) > 0 : l1.Draw('sameAEPZ')
  
  c1.SaveAs(name+'.pdf')

# suffix = '_offlineVtx'    
# suffix = '_firstPixelVtx' 
# suffix = '_first2PixelVtx'
# suffix = '_first4PixelVtx'
# suffix = '_dummy2'
# suffix = '_newTauIDs'
suffix = '_first4PixVtx_sorted4power_threshold25gev'

# file = ROOT.TFile.Open('out_offlineVtx.root','read')
# file = ROOT.TFile.Open('out_firstPixelVtx.root','read')
# file = ROOT.TFile.Open('out_first2PixelVtx.root','read')
file = ROOT.TFile.Open('out{SUF}.root'.format(SUF=suffix),'read')

file.cd()

variable = '_gen_pt'
# variable = '_pt'


offTaus              = ROOT.gDirectory.FindObjectAny('offTaus'                + variable)
onlTauPix            = ROOT.gDirectory.FindObjectAny('onlTausPixVtx_recoHLT'  + variable)
onlTauPixPassingDM   = ROOT.gDirectory.FindObjectAny('onlTausPixVtx_passDM'   + variable)
onlTauPixPassingIso  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx_passIso'  + variable)
onlTauPix2           = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12NN_recoHLT' + variable)
onlTauPixPassingDM2  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12NN_passDM'  + variable)
onlTauPixPassingIso2 = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12NN_passIso' + variable)
# onlTauPix2           = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2_recoHLT' + variable)
# onlTauPixPassingDM2  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2_passDM'  + variable)
# onlTauPixPassingIso2 = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2_passIso' + variable)
onlTauMu             = ROOT.gDirectory.FindObjectAny('onlTausMuVtx_recoHLT'   + variable)
onlTauMuPassingDM    = ROOT.gDirectory.FindObjectAny('onlTausMuVtx_passDM'    + variable)
onlTauMuPassingIso   = ROOT.gDirectory.FindObjectAny('onlTausMuVtx_passIso'   + variable)
position             = ROOT.gDirectory.FindObjectAny('position')


vert = ROOT.gDirectory.FindObjectAny('pixVtx_failDMonl_noOnlTrk_dz(offlineVtx)')

pixRatio1 = doRatio( onlTauPix          , offTaus )
pixRatio2 = doRatio( onlTauPixPassingDM , offTaus )
pixRatio3 = doRatio( onlTauPixPassingIso, offTaus )

pix2Ratio1 = doRatio( onlTauPix2          , offTaus )
pix2Ratio2 = doRatio( onlTauPixPassingDM2 , offTaus )
pix2Ratio3 = doRatio( onlTauPixPassingIso2, offTaus )

muRatio1 = doRatio( onlTauMu          , offTaus )
muRatio2 = doRatio( onlTauMuPassingDM , offTaus )
muRatio3 = doRatio( onlTauMuPassingIso, offTaus )

# plot( pixRatio1, 'p_{T}>20 GeV', 'pixefficiency', 'offline #tau p_{T} [GeV]', 'efficiency', morehistos = {pixRatio2:[ROOT.kGreen+3,'pass DecayMode'],pixRatio3:[ROOT.kBlue,'pass Isolation']} )
# plot( muRatio1 , 'p_{T}>20 GeV', 'muefficiency' , 'offline #tau p_{T} [GeV]', 'efficiency', morehistos = {muRatio2 :[ROOT.kGreen+3,'pass DecayMode'],muRatio3 :[ROOT.kBlue,'pass Isoaltion']} )

# plot( pixRatio1, 'p_{T}>20 GeV', 'pixefficiency', 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {pixRatio2:[ROOT.kGreen+3,'pass DecayMode'],pixRatio3:[ROOT.kBlue,'pass Isolation']} )
# plot( muRatio1 , 'p_{T}>20 GeV', 'muefficiency' , 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {muRatio2 :[ROOT.kGreen+3,'pass DecayMode'],muRatio3 :[ROOT.kBlue,'pass Isoaltion']} )

plot( pixRatio1 , 'p_{T}>20 GeV', 'pixefficiency'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {pixRatio2 :[ROOT.kGreen+3,'pass DecayMode']}, setRangeX = [0.,510.] )
plot( pix2Ratio1, 'p_{T}>20 GeV', 'pix2efficiency' + suffix, 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {pix2Ratio2:[ROOT.kGreen+3,'pass DecayMode']}, setRangeX = [0.,510.] )
plot( muRatio1  , 'p_{T}>20 GeV', 'muefficiency'   + suffix, 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {muRatio2  :[ROOT.kGreen+3,'pass DecayMode']}, setRangeX = [0.,510.] )
# plot( position   , ''            , 'position'       + suffix, 'position of offline PV in online PixVtx collection', 'fraction', drawoptions = '', log = True, setRangeX = [0.,20.] )

# plot( vert , '', 'dzPix_Off' , 'dz [cm]', 'events' )











onlTausPixVtx2S12N3_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12N3_recoHLT' + variable)
onlTausPixVtx2S12N3_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12N3_passDM'  + variable)
onlTausPixVtx2S12N3_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12N3_passIso' + variable)

onlTausPixVtx2S12N5_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12N5_recoHLT' + variable)
onlTausPixVtx2S12N5_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12N5_passDM'  + variable)
onlTausPixVtx2S12N5_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12N5_passIso' + variable)

onlTausPixVtx2S12NN_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12NN_recoHLT' + variable)
onlTausPixVtx2S12NN_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12NN_passDM'  + variable)
onlTausPixVtx2S12NN_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S12NN_passIso' + variable)

onlTausPixVtx2S15N3_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15N3_recoHLT' + variable)
onlTausPixVtx2S15N3_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15N3_passDM'  + variable)
onlTausPixVtx2S15N3_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15N3_passIso' + variable)

onlTausPixVtx2S15N5_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15N5_recoHLT' + variable)
onlTausPixVtx2S15N5_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15N5_passDM'  + variable)
onlTausPixVtx2S15N5_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15N5_passIso' + variable)

onlTausPixVtx2S15NN_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15NN_recoHLT' + variable)
onlTausPixVtx2S15NN_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15NN_passDM'  + variable)
onlTausPixVtx2S15NN_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S15NN_passIso' + variable)

onlTausPixVtx2S18N3_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18N3_recoHLT' + variable)
onlTausPixVtx2S18N3_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18N3_passDM'  + variable)
onlTausPixVtx2S18N3_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18N3_passIso' + variable)

onlTausPixVtx2S18N5_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18N5_recoHLT' + variable)
onlTausPixVtx2S18N5_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18N5_passDM'  + variable)
onlTausPixVtx2S18N5_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18N5_passIso' + variable)

onlTausPixVtx2S18NN_recoHLT = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18NN_recoHLT' + variable)
onlTausPixVtx2S18NN_passDM  = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18NN_passDM'  + variable)
onlTausPixVtx2S18NN_passIso = ROOT.gDirectory.FindObjectAny('onlTausPixVtx2S18NN_passIso' + variable)

onlTausPixVtx2S12N3_ratioHLT = doRatio( onlTausPixVtx2S12N3_recoHLT , offTaus )
onlTausPixVtx2S12N3_ratioDM  = doRatio( onlTausPixVtx2S12N3_passDM  , offTaus )
onlTausPixVtx2S12N3_ratioIso = doRatio( onlTausPixVtx2S12N3_passIso , offTaus )

onlTausPixVtx2S12N5_ratioHLT = doRatio( onlTausPixVtx2S12N5_recoHLT , offTaus )
onlTausPixVtx2S12N5_ratioDM  = doRatio( onlTausPixVtx2S12N5_passDM  , offTaus )
onlTausPixVtx2S12N5_ratioIso = doRatio( onlTausPixVtx2S12N5_passIso , offTaus )

onlTausPixVtx2S12NN_ratioHLT = doRatio( onlTausPixVtx2S12NN_recoHLT , offTaus )
onlTausPixVtx2S12NN_ratioDM  = doRatio( onlTausPixVtx2S12NN_passDM  , offTaus )
onlTausPixVtx2S12NN_ratioIso = doRatio( onlTausPixVtx2S12NN_passIso , offTaus )

onlTausPixVtx2S15N3_ratioHLT = doRatio( onlTausPixVtx2S15N3_recoHLT , offTaus )
onlTausPixVtx2S15N3_ratioDM  = doRatio( onlTausPixVtx2S15N3_passDM  , offTaus )
onlTausPixVtx2S15N3_ratioIso = doRatio( onlTausPixVtx2S15N3_passIso , offTaus )

onlTausPixVtx2S15N5_ratioHLT = doRatio( onlTausPixVtx2S15N5_recoHLT , offTaus )
onlTausPixVtx2S15N5_ratioDM  = doRatio( onlTausPixVtx2S15N5_passDM  , offTaus )
onlTausPixVtx2S15N5_ratioIso = doRatio( onlTausPixVtx2S15N5_passIso , offTaus )

onlTausPixVtx2S15NN_ratioHLT = doRatio( onlTausPixVtx2S15NN_recoHLT , offTaus )
onlTausPixVtx2S15NN_ratioDM  = doRatio( onlTausPixVtx2S15NN_passDM  , offTaus )
onlTausPixVtx2S15NN_ratioIso = doRatio( onlTausPixVtx2S15NN_passIso , offTaus )

onlTausPixVtx2S18N3_ratioHLT = doRatio( onlTausPixVtx2S18N3_recoHLT , offTaus )
onlTausPixVtx2S18N3_ratioDM  = doRatio( onlTausPixVtx2S18N3_passDM  , offTaus )
onlTausPixVtx2S18N3_ratioIso = doRatio( onlTausPixVtx2S18N3_passIso , offTaus )

onlTausPixVtx2S18N5_ratioHLT = doRatio( onlTausPixVtx2S18N5_recoHLT , offTaus )
onlTausPixVtx2S18N5_ratioDM  = doRatio( onlTausPixVtx2S18N5_passDM  , offTaus )
onlTausPixVtx2S18N5_ratioIso = doRatio( onlTausPixVtx2S18N5_passIso , offTaus )

onlTausPixVtx2S18NN_ratioHLT = doRatio( onlTausPixVtx2S18NN_recoHLT , offTaus )
onlTausPixVtx2S18NN_ratioDM  = doRatio( onlTausPixVtx2S18NN_passDM  , offTaus )
onlTausPixVtx2S18NN_ratioIso = doRatio( onlTausPixVtx2S18NN_passIso , offTaus )



# plot( onlTausPixVtx2S12N3_ratioHLT , 'onlTausPixVtx2S12N3_ratioHLT', 'onlTausPixVtx2S12N3_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S12N5_ratioHLT , 'onlTausPixVtx2S12N5_ratioHLT', 'onlTausPixVtx2S12N5_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S12NN_ratioHLT , 'onlTausPixVtx2S12NN_ratioHLT', 'onlTausPixVtx2S12NN_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S15N3_ratioHLT , 'onlTausPixVtx2S15N3_ratioHLT', 'onlTausPixVtx2S15N3_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S15N5_ratioHLT , 'onlTausPixVtx2S15N5_ratioHLT', 'onlTausPixVtx2S15N5_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S15NN_ratioHLT , 'onlTausPixVtx2S15NN_ratioHLT', 'onlTausPixVtx2S15NN_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S18N3_ratioHLT , 'onlTausPixVtx2S18N3_ratioHLT', 'onlTausPixVtx2S18N3_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S18N5_ratioHLT , 'onlTausPixVtx2S18N5_ratioHLT', 'onlTausPixVtx2S18N5_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )
# plot( onlTausPixVtx2S18NN_ratioHLT , 'onlTausPixVtx2S18NN_ratioHLT', 'onlTausPixVtx2S18NN_ratioHLT'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency' )





plot( onlTausPixVtx2S12N3_ratioHLT , 'onlTausPixVtx2S12N3', 'newTauIds'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {onlTausPixVtx2S12N5_ratioHLT :[ROOT.kRed  +2,'onlTausPixVtx2S12N5'],\
                                                                                                                                       onlTausPixVtx2S12NN_ratioHLT :[ROOT.kRed  +3,'onlTausPixVtx2S12NN'],\
                                                                                                                                       onlTausPixVtx2S15N3_ratioHLT :[ROOT.kGreen  ,'onlTausPixVtx2S15N3'],\
                                                                                                                                       onlTausPixVtx2S15N5_ratioHLT :[ROOT.kGreen+2,'onlTausPixVtx2S15N5'],\
                                                                                                                                       onlTausPixVtx2S15NN_ratioHLT :[ROOT.kGreen+3,'onlTausPixVtx2S15NN'],\
                                                                                                                                       onlTausPixVtx2S18N3_ratioHLT :[ROOT.kBlue   ,'onlTausPixVtx2S18N3'],\
                                                                                                                                       onlTausPixVtx2S18N5_ratioHLT :[ROOT.kBlue +2,'onlTausPixVtx2S18N5'],\
                                                                                                                                       onlTausPixVtx2S18NN_ratioHLT :[ROOT.kBlue +3,'onlTausPixVtx2S18NN'] } )


plot( onlTausPixVtx2S12N3_ratioDM , 'onlTausPixVtx2S12N3', 'newTauIdsDM'  + suffix, 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {onlTausPixVtx2S12N5_ratioDM :[ROOT.kRed  +2,'onlTausPixVtx2S12N5'],\
                                                                                                                                        onlTausPixVtx2S12NN_ratioDM :[ROOT.kRed  +3,'onlTausPixVtx2S12NN'],\
                                                                                                                                        onlTausPixVtx2S15N3_ratioDM :[ROOT.kGreen  ,'onlTausPixVtx2S15N3'],\
                                                                                                                                        onlTausPixVtx2S15N5_ratioDM :[ROOT.kGreen+2,'onlTausPixVtx2S15N5'],\
                                                                                                                                        onlTausPixVtx2S15NN_ratioDM :[ROOT.kGreen+3,'onlTausPixVtx2S15NN'],\
                                                                                                                                        muRatio2                    :[ROOT.kOrange ,'muVtx'] ,\
                                                                                                                                        onlTausPixVtx2S18N3_ratioDM :[ROOT.kBlue   ,'onlTausPixVtx2S18N3'],\
                                                                                                                                        onlTausPixVtx2S18N5_ratioDM :[ROOT.kBlue +2,'onlTausPixVtx2S18N5'],\
                                                                                                                                        onlTausPixVtx2S18NN_ratioDM :[ROOT.kBlue +3,'onlTausPixVtx2S18NN'] } )












