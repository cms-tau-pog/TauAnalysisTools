#!/usr/bin/env python
'''
script to fast remove the SUBMITFAILED jobs

Example:
cd <to the dir with crab wds>
for i in *; do   ~/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/TauAnalysisTools/TauAnalysisTools/python/del_crab3_wd.py $i ; done ; cd ..; for i in *; do  crab submit $i; done

for i in *; do   ~/RWTH/MVAtraining/CMSSW_10_4_0_pre3/src/TauAnalysisTools/TauAnalysisTools/python/del_crab3_wd.py $i ; done ; cd ..; for i in *; do  crab submit $i; done
'''

# https://github.com/PerilousApricot/CRABAPI/tree/master/CRABAPI
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
from CRABClient.UserUtilities import config
import shutil
import os
import argparse


parser = argparse.ArgumentParser(description='jobind.py parser')
parser.add_argument('crab_wd', default=None, nargs='+', help='crab workdir')
parser.add_argument('--crab-configs-dir', default=None, type=str, help='crab workdir')
# parser.add_argument('--dry', action='store_true', default=False, help='dry run')
# parser.add_argument('--debug', action='store_true', default=False, help='debug')
args = parser.parse_args()


l = [os.path.abspath(i) for i in args.crab_wd]
were_deletions = False
deleted = []
for d in l:
    if not os.path.isdir(d): continue
    print d
    if crabCommand('status', dir=d)['dbStatus'] in ['SUBMITFAILED']:
        print '*' * 30, '\n\t Deletting:'
        were_deletions = True
        deleted.append(d.split('/')[-1])
        # shutil.rmtree(d)

if were_deletions and args.crab_configs_dir is not None:
    conf_d = os.path.abspath(args.crab_configs_dir)
    onlyfiles = [f for f in os.listdir(conf_d) if os.path.isfile(os.path.join(conf_d, f)) and f.startswith('crab_tauId_ntuplizer_') and f.split('.')[-1] == 'py']
    for i in onlyfiles:
        key = i.strip('crab_tauId_ntuplizer_').strip('_cfg.py')
        print key, conf_d, 'crab_crabdir_' + key
        if 'crab_crabdir_' + key in deleted:
            print 'subm:', os.path.join(conf_d, config)
            crabCommand('submit', config=os.path.join(conf_d, 'crab_tauId_ntuplizer_' + key + '_cfg.py'))
        else:
            print 'conf not found:', i
    # print 'onlyfiles:', onlyfiles


if d is not None:
    # crab job state to delete
    if crabCommand('status', dir=d)['dbStatus'] in ['SUBMITFAILED']:
        print '*' * 30, '\n\t Deletting:'
        shutil.rmtree(d)
