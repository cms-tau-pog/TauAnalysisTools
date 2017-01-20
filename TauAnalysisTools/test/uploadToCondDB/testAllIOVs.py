#!/usr/bin/env python

import subprocess

version = '2015Oct21'

payloads = [
    "RecoTauTag_tauIdMVADBoldDMwLTv1",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff90",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff80",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff70",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff60",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff50",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff40",
    "RecoTauTag_tauIdMVADBoldDMwLTv1_mvaOutput_normalization",
    "RecoTauTag_tauIdMVADBnewDMwLTv1",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff90",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff80",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff70",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff60",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff50",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff40",
    "RecoTauTag_tauIdMVADBnewDMwLTv1_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff90",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff80",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff70",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff60",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff50",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff40",
    "RecoTauTag_tauIdMVAPWoldDMwLTv1_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff90",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff80",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff70",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff60",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff50",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff40",
    "RecoTauTag_tauIdMVAPWnewDMwLTv1_mvaOutput_normalization",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff90",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff80",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff70",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff60",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff50",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff40",
    "RecoTauTag_tauIdMVADBdR03oldDMwLTv1_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff90",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff80",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff70",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff60",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff50",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff40",
    "RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_mvaOutput_normalization"
    ]

for payload in payloads :
    s = 'conddb --db RecoTauTag_MVAs_'+version+'.db list ' + payload
    subprocess.call( [s, ""], shell=True )   
