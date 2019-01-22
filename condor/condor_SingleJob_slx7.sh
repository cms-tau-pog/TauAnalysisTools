#!/bin/bash
# file name: sleep.sh

# setmva10
echo 'setmva10 SL7'
cd /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/test/CMSSW_10_4_0_pre3/src
export SCRAM_ARCH=slc7_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`
# set_cmssw slc6_amd64_gcc700

echo 'Executing'

# job: 2575465
# Example resources:
/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/test/CMSSW_10_4_0_pre3/bin/slc7_amd64_gcc700/trainTauIdMVA \
/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_SL7_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_SL7.log
tail /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_SL7.log
