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


def MakeWeightFriend(input_file_name, output_file_name, tree_name, reweighting_hist, reweighting_name, rew_x, weight_name="newWeight"):
    if isinstance(rew_x, basestring):
        rew_x = [rew_x]
    print 'input_file_name:', input_file_name
    print 'tree_name:', tree_name
    for i in [reweighting_hist, input_file_name]:
        if not os.path.isfile(i):
                raise Exception('Not a file: ' + i)
    # if os.path.isfile(output_file_name):
    #         raise Exception('Exists: ' + output_file_name)

    rfile = ROOT.TFile(reweighting_hist, "READ")  ## "UPDATE" "READ"
    print 'rfile:', rfile.GetName()
    hist = rfile.Get(reweighting_name)
    print 'type(hist):', type(hist)
    maxh = hist.GetBinContent(hist.GetMaximumBin())
    print "maximum bin:", maxh
    # hist.Print("all")

    file = ROOT.TFile(input_file_name, "READ")  ## "UPDATE" "READ" ROOT.TFile(fileName, "UPDATE")
    # file.Open()
    print 'file:', file.GetName()
    tree = file.Get(tree_name)
    # nentrie = tree.GetEntries()
    # Deactivate all branches
    tree.SetBranchStatus("*", 0)
    # Activate only four of them
    activeBranchNames = []
    for r in rew_x:
        activeBranchName = r.replace("(", "")
        activeBranchName = activeBranchName.replace(")", "")
        activeBranchName = activeBranchName.replace(" ", "")
        activeBranchName = activeBranchName.replace("TMath::Log", "")
        activeBranchName = activeBranchName.replace("TMath::Max", "")
        activeBranchName = activeBranchName.replace("TMath::Abs", "")  # ((1.,recTauPt))", '') "TMath::(recTauEta)"
        print "activeBranchName split:", activeBranchName
        # import re
        # activeBranchName = re.split(';|,|\*|\n',activeBranchName)
        activeBranchName = activeBranchName.split(',')
        print "activeBranchName:", activeBranchName, [i for i in activeBranchName if not i.isdigit() and not i[:-1].isdigit()]
        activeBranchName = [i for i in activeBranchName if not i.isdigit() and not i[:-1].isdigit()][0]
        print " true activeBranchName:", activeBranchName
        activeBranchNames.append(activeBranchName)
        tree.SetBranchStatus(activeBranchName, 1)

    # Create a new file + a clone of old tree in new file
    newfile = ROOT.TFile(output_file_name, "recreate")  ## "UPDATE" "READ" ROOT.TFile(fileName, "UPDATE"
    newtree = tree.CloneTree()
    # otree.SetName(tree_name)
    # newtree.BuildIndex("Event")
    print "After clonning:"
    newtree.Print()
    # newtree.SetBranchStatus("*", 0)
    # newtree.Write()
    # tree.delete()
    # file.Close()
    newWeight = array('f', [0])
    br=newtree.Branch(weight_name, newWeight, weight_name+"/F")
    newtree.SetBranchAddress(weight_name, newWeight)
    nentrie = newtree.GetEntries()
    vars = [newtree.GetLeaf(x) for x in activeBranchNames]
    print 'fill branch'
    for i in range(0, nentrie):
        newtree.GetEntry(i)
        values = map(lambda x: x.GetValue(), vars)
        binvalues = []
        binvalues.append(ROOT.TFormula("f1", rew_x[0].replace(activeBranchNames[0], str(values[0]))).Eval(0))
        # binn = [hist.GetXaxis().FindBin(values[0])]
        binn = [hist.GetXaxis().FindBin(binvalues[-1])]
        if len(values) > 1:
            binvalues.append(ROOT.TFormula('f2', rew_x[1].replace(activeBranchNames[1], str(values[1]))).Eval(0))
            # binn.append(hist.GetYaxis().FindBin(values[1]))
            binn.append(hist.GetYaxis().FindBin(binvalues[-1]))
        if len(values) > 2:
            binvalues.append(ROOT.TFormula('f3', rew_x[2].replace(activeBranchNames[2], str(values[2]))).Eval(0))
            # binn.append(hist.GetZaxis().FindBin(values[2]))
            binn.append(hist.GetYaxis().FindBin(binvalues[-1]))

        if hist.GetBinContent(*binn) < 0.0001: print values, '->', binvalues, hist.GetBinContent(*binn)

        newWeight[0] = hist.GetBinContent(*binn)
        br.Fill()

    print 'Write branch'
    # newfile.cd()
    newtree.Write("", ROOT.TObject.kOverwrite)
    print "After adding weight branch:"
    newtree.Print()

    newfile.Close()
    # newfile.Write()
    print 'done:', output_file_name
    return 0

'''
python ~/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/TauAnalysisTools/TauAnalysisTools/python/makeWeightfriend.py \
            -i $BG \
            -o /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/outputs_afs/friend_presel_2018_bg.root \
            -t $TREEBG \
            -m websync/mva/weights2/weights_normalised.root  \
            -n rat_B_over_A \
            -x "TMath::Log(TMath::Max(1., recTauPt))" "TMath::Abs(recTauEta)"
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='MakeWeightFriend parser'
    )
    parser.add_argument('-i', type=str, help='input file')
    parser.add_argument('-o', type=str, help='output file')
    parser.add_argument('-t', type=str, help='input tree')
    parser.add_argument('-m', type=str, help='input reweighting histogram file')
    parser.add_argument('-n', type=str, help='input reweighting histogram name')
    parser.add_argument('-w', type=str, default="newWeight", help='output branch waight name')
    parser.add_argument('-x', type=str, default=[''], nargs="*", help='x,y,z.. for reweighting')
    args = parser.parse_args()

    MakeWeightFriend(input_file_name=args.i, output_file_name=args.o, tree_name=args.t, reweighting_hist=args.m, reweighting_name=args.n, rew_x=args.x, weight_name=args.w)
