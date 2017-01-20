#!/usr/bin/env python

import subprocess

version = '2017Jan20'

payloads = [
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_mvaOutput_normalization"
    ]

for payload in payloads :
    s = 'conddb --db RecoTauTag_MVAs_'+version+'.db list ' + payload
    subprocess.call( [s, ""], shell=True )   
