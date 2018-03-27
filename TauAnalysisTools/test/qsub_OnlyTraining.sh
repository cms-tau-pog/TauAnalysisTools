#!/bin/sh 
# $1 : Makefile_runTauIdMVATraining_tauId_v3_0_optaDBAll
cat > $1.zsh <<EOF
#!/bin/zsh
#
#(make sure the right shell will be used)
#$ -S /bin/zsh
#
#(the cpu time for this job)
#$ -l h_cpu=72:00:00
#
#(the maximum memory usage of this job) - 32G; 48G - for the NEW DM; 64G
#$ -l h_vmem=48G
#
#(the maximum Available_Disk_Space	Amount of memory). 10G for all, 20G for new DM
#$ -l h_fsize=20G
#
#(use hh site)
#$ -l site=hh 
#(stderr and stdout are merged together to stdout)
#$ -j y
#
# use SL6
#$ -l os=sld6
#
# use current dir and current environment
#$ -cwd
#$ -V
#
#
#
#
#
#$ -o $1.out
#
#$ -e $1.err
#
#example: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_2_4/bin/slc6_amd64_gcc530/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_V1_allPhotonsCut/tauId_v3_0/trainfilesfinal_v1/$1.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_V1_allPhotonsCut/tauId_v3_0/trainfilesfinal_v1/$1.log
#Old
# 1)   trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_cfg ; #trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p5_cfg
# DONE partial Bg: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_attempt2/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_attempt2/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_cfg.log
# bad run: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_newDM/$1.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_newDM/$1.log
# DONE full bg: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_multiple_presel_bg_files/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_multiple_presel_bg_files/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0.log
# KILLED without duplication: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_multiple_presel_bg_files/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_old_v2/trainfilesfinal_multiple_presel_bg_files/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_1p0.log
#
# New
# 2) trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_cfg; # trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p5_cfg
# bad run: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_newDM/$1.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_newDM/$1.log
# partial Bg: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_attempt2/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_attempt2/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_cfg.log
# RUNNING full bg: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_multiple_presel_bg_files/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_multiple_presel_bg_files/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0.log
# DONE prunning 3 Bg:  nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_multiple_presel_bg_files_Prunning3/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR05_new_v2/trainfilesfinal_multiple_presel_bg_files_Prunning3/trainTauIdMVA_mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0.log
#
# 0.3
# 3)  trainTauIdMVA_mvaIsolation3HitsDeltaR03opt2aLTDB_cfg; # trainTauIdMVA_mvaIsolation3HitsDeltaR03opt2aLTDB_1p0_cfg trainTauIdMVA_mvaIsolation3HitsDeltaR03opt1aLTDB_cfg
# bad run: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR03_old_v2/trainfilesfinal_WIP1/$1.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR03_old_v2/trainfilesfinal_WIP1/$1.log
# DONE full Bg: nice /afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_2/bin/slc6_amd64_gcc630/trainTauIdMVA /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR03_old_v2/trainfilesfinal_WIP1_attempt2/trainTauIdMVA_mvaIsolation3HitsDeltaR03opt2aLTDB_cfg.py &> /nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_2017MCv2_partial/tauId_dR03_old_v2/trainfilesfinal_WIP1_attempt2/trainTauIdMVA_mvaIsolation3HitsDeltaR03opt2aLTDB_cfg.log


EOF

rm $1.out
rm $1.err
chmod u+x $1.zsh
# Send an email for the  job notifications. -m sets whether the mail should be sent after the end(s), begin(b), abort(a) or suspend(s) of the batch jobs
qsub $1.zsh -M olena.hlushchenko@desy.de -m bea
