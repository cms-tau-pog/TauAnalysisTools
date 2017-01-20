#!/usr/bin/env python

import subprocess

version = '2015Nov03'

payloads = [
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL",
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff99",
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff96",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff91",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff85",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff79",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL",
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff99",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff96",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff91",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff85",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff79",       
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL",
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff99",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff96",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff91",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff85",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff79",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL",
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff99",
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff96",          
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff91",          
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff85",          
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff79",          
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC",
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff99",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff96",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff91",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff85",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff79",      
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC",
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff99",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff96",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff91",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff85",       
    "RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff79", 
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC",
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff99",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff96",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff91",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff85",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff79",                  
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC",
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff99",                   
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff96",                   
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff91",                   
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff85",                   
    "RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff79",             
    ]

for payload in payloads :
    s = 'conddb --db RecoTauTag_AntiEMVAs_'+version+'.db list ' + payload
    subprocess.call( [s, ""], shell=True )   
