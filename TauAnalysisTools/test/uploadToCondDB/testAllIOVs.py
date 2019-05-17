#!/usr/bin/env python

import subprocess

version = 'RecoTauTag_MVAs_2019Feb18.db' #RecoTauTag_MVAs_

payloads = [
    #"RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff95",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff90",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff80",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff70",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff60",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff50",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff40",
    #
    #   2017v1
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff95",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff90",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff80",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff70",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff60",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff50",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff40",
    #
    #   2017v2
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff95",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff90",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff80",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff70",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff60",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff50",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff40",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff95",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff90",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff80",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff70",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff60",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff50",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff40",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff95",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff90",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff80",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff70",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff60",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff50",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff40",
    # "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_mvaOutput_normalization",
    # "RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_mvaOutput_normalization",
    # "RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_mvaOutput_normalization",
    #2018
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff95",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff95",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff95",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff90",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff80",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff70",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff60",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff50",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_WPEff40",
    "RecoTauTag_tauIdMVAIsoDBoldDMwLT2018_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2018_mvaOutput_normalization",
    "RecoTauTag_tauIdMVAIsoDBnewDMwLT2018_mvaOutput_normalization",
    ]

for payload in payloads :
    s = 'conddb --db ' + version + ' list ' + payload
    subprocess.call([s, ""], shell=True )
