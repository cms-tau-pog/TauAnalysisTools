import argparse
import ROOT
import random


def pruneToNEvents(fileName, treeName, m=None, frac=None):
    import os.path
    if not os.path.isfile(fileName):
        raise Exception('Not a file: ' + fileName)

    # Get old file, old tree and set top branch address
    oldfile = ROOT.TFile(fileName, 'read')
    oldtree = oldfile.Get(treeName)

    nentries = oldtree.GetEntries()
    if m is None and frac is None:
        raise Exception('neither M nor fraction given')
    if frac is not None:
        if frac >= 0 and frac < 1:
            m = int(nentries * frac)
        else:
            raise Exception('bad frac')
    else:
        frac = (nentries - m) / nentries
        frac = float(m) / nentries
        if frac < 0:
            raise Exception('too few events in the input file')

    # Create a new file + a clone of old tree in new file
    output_filename = fileName.split('.root')[0] + '_' + str(frac) + 'fr_' + str(m) + 'ev.root'
    print 'output:', output_filename, '\n ', nentries, '->', m, '\n fraction to keep:', frac, float(m / nentries)
    newfile = ROOT.TFile(output_filename, "recreate")
    newtree = oldtree.CloneTree(0)

    # for event in tree:
    nout = 0
    skipped = 0
    accepted = 0
    r = random
    r.seed(a=1)
    for event in range(0, nentries):
        if event == nentries - 2:
            print 'by the end ', event, 'nout:', nout,
        if r.random() > frac:
            skipped += 1
            continue
        accepted += 1
        oldtree.GetEntry(event)
        newtree.Fill()
        nout += 1
        if nout == m:
            print 'all ev are gathered:', newtree.GetEntries()
            break
    print 'before safe:', newtree.GetEntries()
    print 'skipped:', skipped, 'accepted:', accepted,'sum:', skipped+accepted

    newfile.cd()
    # newtree.Print()
    newtree.Write()
    newfile.Close()
    oldfile.Close()
    print 'done'
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='pruneToNEvents parser'
    )
    parser.add_argument('-i', type=str, help='input file')
    parser.add_argument('-t', type=str, default="preselectedTauIdMVATrainingNtuple", help='input tree')
    parser.add_argument('-m', type=int, default=None, help='number of output events')
    parser.add_argument('-f', type=float, default=None, help='fruction for output events to keep')
    args = parser.parse_args()

    pruneToNEvents(fileName=args.i, treeName=args.t, m=args.m, frac=args.f)
