# import os
# import copy
# import ROOT
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# import functools


# TFile *f = new TFile("treeparent.root");
# TTree *T = (TTree*)f->Get("T");
# TFile *ff = new TFile("treefriend.root","recreate");
# TTree *TF = T->CopyTree("z<10");
# TF->SetName("TF");
# TF->BuildIndex("Run","Event");
# TF->Write();
# TF->Print();

import argparse
import ROOT
import random
import os.path
from array import array

# void upd()
#{
# TFile *f = new TFile("hs.root","update")
# TTree *T = (TTree*)f->Get("ntuple");
# float px, py
# float pt
# TBranch *bpt = T->Branch("pt", &pt, "pt/F")
# for (Long64_t i = 0; i < nentries; i++)
# {
#  T->GetEntry(i)
#  pt = TMath::Sqrt(px*px+py*py)
#  bpt->Fill()
# }
# T->Print()
# T->Write()
# delete f


def normalizeHistogram(histogram):
    if histogram.Integral() > 0.:
        if not histogram.GetSumw2N():
            histogram.Sumw2()
        histogram.Scale(1. / histogram.Integral())


def fillHistogramsForPtVsEtaReweighting(inputTree,
       branchNamePt, branchNameEta, branchNameEvtWeight,
       histogramLogPt, histogramAbsEta, histogramLogPtVsAbsEta,
       reportEvery, maxnevents=-1, ptmax=-1):
    print "fillHistogramsForPtVsEtaReweighting<>: begin"
    pt = array('f', [0])
    inputTree.SetBranchAddress(branchNamePt, pt)
    eta = array('f', [0])
    inputTree.SetBranchAddress(branchNameEta, eta)

    evtWeight = array('f', [1.0])
    if branchNameEvtWeight != "":
        inputTree.SetBranchAddress(branchNameEvtWeight, evtWeight)

    numEntries = inputTree.GetEntries()
    # numEntries = maxnevents if maxnevents != -1 and maxnevents < numEntries else numEntries
    for iEntry in range(0, numEntries):
        inputTree.GetEntry(iEntry)
        if ptmax > -1 and pt[0] > ptmax: continue

        if iEntry > 0 and (iEntry % reportEvery) == 0:
            if maxnevents == -1:
                print "processing Entry", iEntry, "out", numEntries
            else:
                print "processing Entry", iEntry, "left", maxnevents, "more"
        absEta = ROOT.TFormula("f1", "TMath::Abs(eta)".replace('eta', str(eta[0]))).Eval(0)
        logPt = ROOT.TFormula("f2", "TMath::Log(TMath::Max(1., pt));".replace('pt', str(pt[0]))).Eval(0)

        histogramLogPt.Fill(logPt, evtWeight[0])
        histogramAbsEta.Fill(absEta, evtWeight[0])
        histogramLogPtVsAbsEta.Fill(absEta, logPt, evtWeight[0])

        if maxnevents > -1:
            maxnevents -= 1
            if maxnevents == 0: break


    normalizeHistogram(histogramLogPt)
    normalizeHistogram(histogramAbsEta)
    normalizeHistogram(histogramLogPtVsAbsEta)
    print"fillHistogramsForPtVsEtaReweighting<>: end"


def divideHistograms(numerator, denominator):
    histogramName_ratio = numerator.GetName() + "_div_" + denominator.GetName()
    histogram_ratio = numerator.Clone(histogramName_ratio)
    histogram_ratio.Divide(denominator)
    return histogram_ratio


def ReweightFriend(rew_x=["TMath::Log(TMath::Max(1., recTauPt))", "TMath::Abs(recTauEta)"], weight_name="newWeight"):
    input_file_name_sg = '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauIdv2/tauId_dR05_new_v2/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_background.root'
    input_file_name_bg = '/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/presel_2018_bg.root'
    input_tree_name_sg = 'reweightedTauIdMVATrainingNtuple'
    input_tree_name_bg = 'preselectedTauIdMVATrainingNtuple'

    rfile_sg = ROOT.TFile(input_file_name_sg, "READ")  ## "UPDATE" "READ"
    rfile_bg = ROOT.TFile(input_file_name_bg, "READ")  ## "UPDATE" "READ"

    tree_sg = rfile_sg.Get(input_tree_name_sg)
    tree_bg = rfile_bg.Get(input_tree_name_bg)
    # nentrie = tree.GetEntries()
    # Deactivate all branches
    tree_sg.SetBranchStatus("*", 0)
    tree_bg.SetBranchStatus("*", 0)
    # Activate only four of them
    activeBranchNames = []
    for r in rew_x:
        activeBranchName = r.replace("(", "")
        activeBranchName = activeBranchName.replace(")", "")
        activeBranchName = activeBranchName.replace(" ", "")
        activeBranchName = activeBranchName.replace("TMath::Log", "")
        activeBranchName = activeBranchName.replace("TMath::Max", "")
        activeBranchName = activeBranchName.replace("TMath::Abs", "")
        print "activeBranchName split:", activeBranchName
        activeBranchName = activeBranchName.split(',')
        activeBranchName = [i for i in activeBranchName if not i.isdigit() and not i[:-1].isdigit()][0]
        activeBranchNames.append(activeBranchName)
        tree_sg.SetBranchStatus(activeBranchName, 1)
        tree_bg.SetBranchStatus(activeBranchName, 1)

    histogramLogPt_signal = ROOT.TH1D("histogramLogPt_signal", "log(tauPt) signal", 400, 0., 10.)
    histogramLogPt_background = ROOT.TH1D("histogramLogPt_background", "log(tauPt) background", 400, 0., 10.)
    histogramAbsEta_signal = ROOT.TH1D("histogramAbsEta_signal", "abs(tauEta) signal", 100, 0., 5.)
    histogramAbsEta_background= ROOT.TH1D("histogramAbsEta_background","abs(tauEta) background", 100, 0.,  5.);
    histogramLogPtVsAbsEta_signal = ROOT.TH2D("histogramLogPtVsAbsEta_signal", "log(tauPt) vs. abs(tauEta) signal",100, 0.,  5., 400, 0., 10.)
    histogramLogPtVsAbsEta_background = ROOT.TH2D("histogramLogPtVsAbsEta_background", "log(tauPt) vs. abs(tauEta) background", 100, 0.,  5., 400, 0., 10.)

    fillHistogramsForPtVsEtaReweighting(
      tree_sg,
      'recTauPt', 'recTauEta', 'evtWeight',
      histogramLogPt_signal, histogramAbsEta_signal, histogramLogPtVsAbsEta_signal,
      1000, maxnevents=25000, ptmax=300)
    fillHistogramsForPtVsEtaReweighting(
      tree_bg,
      'recTauPt', 'recTauEta', 'evtWeight',
      histogramLogPt_background, histogramAbsEta_background, histogramLogPtVsAbsEta_background,
      1000, maxnevents=-1)

    histogramLogPt_reweight_background = divideHistograms(histogramLogPt_signal, histogramLogPt_background)
    histogramAbsEta_reweight_background = divideHistograms(histogramAbsEta_signal, histogramAbsEta_background)
    histogramLogPtVsAbsEta_reweight_background = divideHistograms(histogramLogPtVsAbsEta_signal, histogramLogPtVsAbsEta_background)

    output_file_name = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/outputFileName_histograms.root"
    outputFile_histograms = ROOT.TFile(output_file_name, "RECREATE")
    histogramLogPt_signal.Write()
    histogramAbsEta_signal.Write()
    histogramLogPtVsAbsEta_signal.Write()
    # if ( histogramLogPt_reweight_signal             ) histogramLogPt_reweight_signal->Write();
    # if ( histogramAbsEta_reweight_signal            ) histogramAbsEta_reweight_signal->Write();
    # if ( histogramLogPtVsAbsEta_reweight_signal     ) histogramLogPtVsAbsEta_reweight_signal->Write();
    histogramLogPt_background.Write()
    histogramAbsEta_background.Write()
    histogramLogPtVsAbsEta_background.Write()
    histogramLogPt_reweight_background.Write()
    histogramAbsEta_reweight_background.Write()
    histogramLogPtVsAbsEta_reweight_background.Write()

    # newfile.Write()
    print 'done:', output_file_name
    return 0

'''
python ~/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/TauAnalysisTools/TauAnalysisTools/python/reweightfriend.py \
            -i $BG \
            -o /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/friend_presel_2018_bg.root \
            -t $TREEBG \
            -m websync/mva/weights2/weights_normalised.root  \
            -n rat_B_over_A \
            -x "TMath::Log(TMath::Max(1., recTauPt))" "TMath::Abs(recTauEta)"
'''
if __name__ == '__main__':
    ReweightFriend()
    exit(1)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='ReweightFriend parser'
    )
    parser.add_argument('-i', type=str, help='input file')
    parser.add_argument('-o', type=str, help='output file')
    parser.add_argument('-t', type=str, help='input tree')
    parser.add_argument('-m', type=str, help='input reweighting histogram file')
    parser.add_argument('-n', type=str, help='input reweighting histogram name')
    parser.add_argument('-w', type=str, default="newWeight", help='output branch waight name')
    parser.add_argument('-x', type=str, default=[''], nargs="*", help='x,y,z.. for reweighting')
    args = parser.parse_args()

    ReweightFriend(input_file_name=args.i, output_file_name=args.o, tree_name=args.t, reweighting_hist=args.m, reweighting_name=args.n, rew_x=args.x, weight_name=args.w)
