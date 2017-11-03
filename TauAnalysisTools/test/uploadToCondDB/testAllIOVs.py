#!/usr/bin/env python

import subprocess

version = '2017Oct25'

payloads = [
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff95",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff95",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_mvaOutput_normalization"
    ]

for payload in payloads :
    s = 'conddb --db RecoTauTag_MVAs_'+version+'.db list ' + payload
    subprocess.call( [s, ""], shell=True )   
