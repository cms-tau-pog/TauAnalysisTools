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


def addNormalizingWeight(fileNames, treeNames, frac=None):
    if type(fileNames) != type(treeNames):
        raise Exception('Give fileNames, treeNames of a same type')
    if isinstance(fileNames, basestring):
        if frac in None:
            raise Exception('Give the weight next to a single file')
        fileNames = [fileNames]
        treeNames = [treeNames]
    if not isinstance(fileNames, (list, tuple)):
        raise Exception('fileNames should be (list) or (tuple) or (a string next to float)')
    elif frac is not None:
        raise Exception('no frac in multyfile mode')

    files = []
    trees = []
    nentries = []
    for fileName, treeName in zip(fileNames, treeNames):
        print 'file:', fileName
        print 'tree', treeName
        if not os.path.isfile(fileName):
            raise Exception('Not a file: ' + fileName)
        files.append(ROOT.TFile(fileName, "UPDATE"))  ## "UPDATE" "READ"
        trees.append(files[-1].Get(treeName))
        nentries.append(trees[-1].GetEntries())
        print 'nentries', nentries[-1]

    val, idx = min((float(val), idx) for (idx, val) in enumerate(nentries))
    print '\n minimum entries:', val, idx, '\n'

    for file, tree, nentrie in zip(files, trees, nentries):
        file.cd()
        print 'file:', file.GetName()
        # print 'gFile', ROOT.gFile.GetName()
        normalizingWeight = array('f', [val / nentrie])
        print ' normalizing weight:', normalizingWeight[0]
        print 'create branch'
        newBranch = tree.Branch("normalizingWeight", normalizingWeight, "normalizingWeight/F")

        print 'fill branch'
        for i in range(0, nentrie):
            # normalizingWeight[0] = ...
            newBranch.Fill()
        print 'Write branch'
        tree.Write("", ROOT.TObject.kOverwrite)

        print [i.GetName() for i in tree.GetListOfBranches()], '\n\n'
        # tree.Print()

        file.Close()

    # newtree.Print()
    # newtree.AutoSave()
    # oldfile.Close()
    # newfile.Close()
    print 'done'
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='addNormalizingWeight parser'
    )
    parser.add_argument('-i', type=str, default=[''], nargs="*", help='input file')
    parser.add_argument('-t', type=str, default=[''], nargs="*", help='input tree')
    parser.add_argument('-f', type=float, default=None, help='weight for output events')
    args = parser.parse_args()

    addNormalizingWeight(fileNames=args.i, treeNames=args.t, frac=args.f)
