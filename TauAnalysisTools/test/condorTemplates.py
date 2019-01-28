
from string import Template

# preselsh
# preselid
# execDir
# preselcommand

presel_sub = Template('''
# Unix submit description file
# Default Universe for normal jobs
universe                = vanilla
executable              = $preselsh

log                     = pres_$preselid.$(Cluster).$(DOLLAR).$$(Name).$(DOLLAR).clog
output                  = pres_$preselid.$(Cluster).$(DOLLAR).$$(Name).$(DOLLAR).cout
error                   = pres_$preselid.$(Cluster).$(DOLLAR).$$(Name).$(DOLLAR).cerr


should_transfer_files   = No
requirements   = OpSysAndVer == "SL6"

# request_cpus = Cpus
# rank = Cpus

# choose the machine with max RAM possible
rank = Memory

# (the cpu time for this job) -l h_cpu=72:00:00
# Defaults to 1 day:
# RequestRuntime = 72 * 60 * 60

# Mailing requests:
# notification = $<$Always | Complete | Error | Never$>$
notification  = Complete
notify_user   = olena.hlushchenko@desy.de

queue
''')

presel_sh = Template('''
#!/bin/bash
# file name: sleep.sh

# setmva10
echo 'setmva10'
cd $execDir
export SCRAM_ARCH=slc6_amd64_gcc700
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $VO_CMS_SW_DIR/cmsset_default.sh
eval `scramv1 runtime -sh`
# set_cmssw slc6_amd64_gcc700

echo 'Executing'

$preselcommand

''')
