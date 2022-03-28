import os
import ROOT
from optparse import OptionParser


parser=OptionParser()
parser.add_option("-p","--path",dest="Path",type="str",default="di-tau",help="HLT path")

opts, args = parser.parse_args()

rootfiles = str(args[0]).split(',')


dir_relval = "DQMData/Run 1/HLT/Run summary/TAU/RelVal/MC/"

physics_path = {
                "di-tau":[
                           "HLT_DoubleMediumDeepTauIsoPFTauHPS35_L2NN_eta2p1",
                           ["L3TrigTauEtEff","L3TrigTauEtaEff"]
                         ],
                "mu-tau":[
                           "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                           ["L3TrigTauEtEff","L3TrigTauEtaEff","L3TrigMuonEtEff","L3TrigMuonEtaEff"]
                         ],
                "e-tau" :[
                           "HLT_Ele24_eta2p1_WPTight_Gsf_LooseDeepTauPFTauHPS30_eta2p1_CrossL1",
                          ["L3TrigTauEtEff","L3TrigTauEtaEff","L3TrigElectronEtEff","L3TrigElectronEtaEff"]
                         ],
                "single-tau":[
                               "HLT_LooseDeepTauPFTauHPS180_L2NN_eta2p1",
                              ["L3TrigTauHighEtEff","L3TrigTauEtaEff"]
                         ]
                }

class TObject:
    def __init__(self,rootfile,ch):
        self.file = ROOT.TFile(rootfile)
        self.dirtoprofile = dir_relval+physics_path[ch][0]

    def getProfile(self,profilename):
        return self.file.Get(self.dirtoprofile+'/'+profilename)

ProfileCollection = dict()
for rootfile in rootfiles:
    obj = TObject(rootfile,str(opts.Path))
    ProfileCollection[rootfile] = obj

histnames = physics_path[opts.Path][1]


try:
    os.mkdir(opts.Path)
except:
    print('Directory is already created')
    
for histname in histnames:
    ic = 2
    c1 = ROOT.TCanvas()
    leg = ROOT.TLegend(0.4,0.4,0.6,0.6)
    for rootfile in rootfiles:
        profile = ProfileCollection[rootfile].getProfile(histname)
        profile.SetStats(0)
        profile.SetLineWidth(3)
        profile.SetLineColor(ic)
        profile.Draw("same")
        leg.AddEntry(profile,rootfile.split('.root')[0],'l')
        ic = ic +1
    leg.Draw()
    c1.SaveAs('./'+opts.Path+'/'+histname+'_'+opts.Path+'.png')
        
    
        
