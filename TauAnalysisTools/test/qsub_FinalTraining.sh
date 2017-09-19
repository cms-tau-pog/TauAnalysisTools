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
#(the maximum memory usage of this job)
#$ -l h_vmem=32G
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
#$ -o $1.out
#
#$ -e $1.err
make -f /nfs/dust/cms/user/anehrkor/TauIDMVATraining2016/Summer16_25ns_V1/tauId_v3_0/trainfilesfinal_v1/$1

EOF

rm $1.out
rm $1.err
chmod u+x $1.zsh
qsub $1.zsh
