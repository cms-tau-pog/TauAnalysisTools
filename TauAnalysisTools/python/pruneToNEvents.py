import argparse
import ROOT
import random


def pruneToNEvents(fileName, m=8000000):
    import os.path
    if not os.path.isfile(fileName):
        raise Exception('Not a file: ' + fileName)

    # Get old file, old tree and set top branch address
    oldfile = ROOT.TFile(fileName, 'read')
    oldtree = oldfile.Get("preselectedTauIdMVATrainingNtuple")

    nentries = oldtree.GetEntries()
    frac = (nentries - m) / nentries
    if frac < 0:
        raise Exception('too few events')

    # Create a new file + a clone of old tree in new file
    output_filename = fileName.split('.root')[0] + '_' + str(m) + 'ev.root'
    print 'output:', output_filename, '\n ', nentries, '->', m
    newfile = ROOT.TFile(output_filename, "recreate")
    newtree = oldtree.CloneTree(0)

    # for event in tree:
    nout = 0
    r = random
    r.seed(a=1)
    for event in range(0, nentries):
        if r.random() < frac:
            continue
        oldtree.GetEntry(event)
        newtree.Fill()
        nout += 1
        if nout == m:
            break

    newtree.Print()
    newtree.AutoSave()
    oldfile.Close()
    newfile.Close()
    print 'done'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='pruneToNEvents parser'
    )
    parser.add_argument('-i', type=str, help='input file')
    parser.add_argument('-m', type=int, default=2000000, help='number of output events')
    args = parser.parse_args()

    pruneToNEvents(fileName=args.i, m=args.m)
