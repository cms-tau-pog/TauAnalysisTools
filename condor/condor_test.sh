#!/bin/bash
# file name: sleep.sh

TIMETOWAIT="1"
echo "sleeping for $TIMETOWAIT seconds"
/bin/sleep $TIMETOWAIT

# return

# setmva10
echo 'setmva10'
cd /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src
export SCRAM_ARCH=slc6_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`
# set_cmssw slc6_amd64_gcc700

echo 'executing'
# touch delme.txt
# pwd
# ls -ltr
# echo $1

# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/train_test.py
/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/trainTauIdMVA $1 $2 $3

# echo 1
# echo $1
# echo 2
# echo $2
# echo 3
# echo $3
