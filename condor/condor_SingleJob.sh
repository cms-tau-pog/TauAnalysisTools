#!/bin/bash
# file name: sleep.sh

# setmva10
echo 'setmva10'
cd /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src
export SCRAM_ARCH=slc6_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`
# set_cmssw slc6_amd64_gcc700

echo 'Executing'

# old
# hadd -f /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/hadd_test.root  \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt1400to1800.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt120to170.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt600to800.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_TTToHadronic.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_Wplus2Jets_mcatnlo.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt1800to2400.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt50to80.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt1000to1400.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_Wplus3Jets_mcatnlo.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt30to50.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt80to120.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt300to470.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt470to600.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_Wplus4Jets_mcatnlo.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt170to300.root \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/preselectTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_QCDjetsPt2400to3200.root

#/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/reweightTreeTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_signal_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_signal.log
# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/reweightTreeTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_background.log

# job: 2570164 - killed by 3h short que limit while used 17438 Mb;
# job: 2574670 - bus error on the last iteration
# job 2623516 - failed machine req; submitted to machine: rank = Memory ; +RequestRuntime = 129600 ; request_memory = 10 GB ; requirements= Name == "bird821.desy.de"
# 2623517 - file not found
# 2623763 - long in the cue
# Example resources:
/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/trainTauIdMVA \
/nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0.log
tail /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0.log

# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/trainTauIdMVA \
# /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/train_test.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0.log
# tail /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_old_v1/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0.log



# new
# job: 2565715.000
# Example resources:
# Partitionable Resources :    Usage  Request Allocated
#        Cpus                 :     0.80        1         1
#        Disk (KB)            :     7      512000    809783
#        Memory (MB)          :   169        1536      1536
# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/reweightTreeTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_new_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_signal_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_new_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_signal.log
# tail /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_new_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_signal.log

# job: 2568887
# Example resources:
# Partitionable Resources :    Usage  Request Allocated
#    Cpus                 :     0.78        1         1
#    Disk (KB)            :     7      512000    795096
#    Memory (MB)          :   165        1536      1536
# /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_10_4_0_pre3/bin/slc6_amd64_gcc700/reweightTreeTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_new_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_background_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_new_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_background.log
# tail /nfs/dust/cms/user/glusheno/TauIDMVATraining2018/Autum2018tauId_v1/tauId_dR05_new_v1/reweightTreeTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_background.log
