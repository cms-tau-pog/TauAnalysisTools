#! /usr/bin/env python
import os
import re
import sys
import subprocess

from optparse import OptionParser

parser = OptionParser()

parser.add_option('--sqlite_file', metavar='F', type='string', action='store',
                  dest='sqlite_file',
                  help='Input sqlite file')

parser.add_option('--version', metavar='F', type='string', action='store',
                  dest='version',
                  help='Version')

parser.add_option('--prep', metavar='F', action='store_true',
                  dest='prep',
                  help='Upload to prep area')

(options, args) = parser.parse_args()

#******************   template file  **********************************
if options.prep :
	templateFile = open('templateForDropbox_PREP.txt', 'r')
else :
	templateFile = open('templateForDropbox_PRODUCTION.txt', 'r')
fileContents = templateFile.read(-1)
print '--------------- TEMPLATE :  -----------------'
print fileContents
p1 = re.compile(r'TAGNAME')
p2 = re.compile(r'PRODNAME')

#******************   definitions  **********************************

##version = '2014Apr29'
version = options.version

payloads = [
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL",
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff99",
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff96",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff91",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff85",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_BL_WPEff79",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL",
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff99",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff96",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff91",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff85",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_BL_WPEff79",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL",
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff99",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff96",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff91",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff85",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_BL_WPEff79",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL",
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff99",
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff96",          
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff91",          
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff85",          
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_BL_WPEff79",	
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC",
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff99",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff96",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff91",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff85",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_woGwoGSF_EC_WPEff79",      
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC",
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff99",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff96",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff91",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff85",       
    #"RecoTauTag_antiElectronMVA6v1_gbr_NoEleMatch_wGwoGSF_EC_WPEff79", 
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC",
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff99",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff96",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff91",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff85",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_woGwGSF_EC_WPEff79",                  
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC",
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff99",                   
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff96",                   
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff91",                   
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff85",                   
    #"RecoTauTag_antiElectronMVA6v1_gbr_wGwGSF_EC_WPEff79"
    #"RecoTauTag_tauIdMVADBoldDMwLTv1",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff90",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff80",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff70",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff60",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff50",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff40",
    #"RecoTauTag_tauIdMVADBoldDMwLTv1_mvaOutput_normalization",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff90",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff80",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff70",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff60",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff50",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_WPEff40",
    #"RecoTauTag_tauIdMVADBnewDMwLTv1_mvaOutput_normalization",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff90",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff80",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff70",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff60",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff50",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_WPEff40",
    #"RecoTauTag_tauIdMVAPWoldDMwLTv1_mvaOutput_normalization",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff90",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff80",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff70",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff60",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff50",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_WPEff40",
    #"RecoTauTag_tauIdMVAPWnewDMwLTv1_mvaOutput_normalization",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff90",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff80",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff70",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff60",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff50",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_WPEff40",
    #"RecoTauTag_tauIdMVADBdR03oldDMwLTv1_mvaOutput_normalization",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff90",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff80",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff70",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff60",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff50",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_WPEff40",
    #"RecoTauTag_tauIdMVAPWdR03oldDMwLTv1_mvaOutput_normalization"	
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
        "RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_mvaOutput_normalization",	
]

#*********************************************************************

files = []

# add all MVA configs plus WPs
for payload in payloads:

    s1 = payload
    s2 = payload
    k1 = p1.sub( s1, fileContents )
    k2 = p2.sub( s2, k1 )
    k2outfile = s2 + '.txt'
    print '--------------------------------------'
    print 'ORCOFF File for payload : ' + s2
    print 'Written to ' + k2outfile
    FILE = open(k2outfile,"w")
    FILE.write(k2)       
    files.append( k2outfile )
    
for ifile in files :
    if options.prep :
        append = '_test'
    else :
         append = ''
    s = "./dropBoxOffline" + append + ".sh "+options.sqlite_file+" " + ifile
    print s
    subprocess.call([ "./dropBoxOffline" + append + ".sh", options.sqlite_file, ifile ])
  
