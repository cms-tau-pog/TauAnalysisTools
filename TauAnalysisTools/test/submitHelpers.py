# def createFilePath(filePath):
#    import TauAnalysis.Configuration.tools.eos as eos
#    try:
#        eos.lsl(filePath)
#    except IOError:
#        print "filePath = %s does not yet exist, creating it." % filePath
#        eos.mkdir(filePath)
#        time.sleep(3)
#    eos.chmod(filePath, 777)

import subprocess
import json
from string import Template
from condorTemplates import presel_sub, presel_sh
import os

# Functions for skimming scripts creation
def runcommand(commandline):
    """Run and print a specific command."""
    print(commandline)
    subprocess.call(commandline, shell=True)


# Functions for training scripts creation
def replaceCommomns(commonName, commonList, singleList):
    if commonName in singleList:
        singleList[:] = [x for x in singleList if x != commonName]
        singleList[:] = commonList + singleList


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def getTrainingSets(trainingsets='trainingsets.json'):
    with open(trainingsets) as f:
        ff = json.load(f, object_hook=_decode_dict)

    preselections = ff['preselections']
    cutDiscriminatorsAll = ff['cutDiscriminators']
    trainings = ff['trainings']
    commonsDict = {
        'commonOtherVariables': ff['commonOtherVariables'],
        'commonSpectatorVariables': ff['commonSpectatorVariables'],
    }

    for cval in cutDiscriminatorsAll.values():
        cval["preselection"] = preselections[cval["preselection"]]

    for tval in trainings.values():
        tval["preselection"] = preselections[tval["preselection"]]
        replaceCommomns('commonOtherVariables', commonsDict['commonOtherVariables'], tval["otherVariables"])
        replaceCommomns('commonSpectatorVariables', commonsDict['commonSpectatorVariables'], tval["spectatorVariables"])

    return preselections, cutDiscriminatorsAll, trainings, commonsDict


reweighting_no_xml = Template('''

process.reweightTreeTauIdMVA.xmltraining = cms.string('')
# process.reweightTreeTauIdMVA.xmltraining_name = cms.string('background')
process.reweightTreeTauIdMVA.xmlinputVariables = cms.vstring([
    # "TMath::Log(TMath::Max(1., recTauPt))/F",
    # "TMath::Abs(recTauEta)/F",
    # "TMath::Log(TMath::Max(1.e-2, chargedIsoPtSum))/F",
    # "TMath::Log(TMath::Max(1.e-2, neutralIsoPtSum_ptGt1.0))/F",
    # "TMath::Log(TMath::Max(1.e-2, puCorrPtSum))/F",
    # "TMath::Log(TMath::Max(1.e-2, photonPtSumOutsideSignalCone_ptGt1.0))/F",
    # "recTauDecayMode/I",
    # "TMath::Min(30., recTauNphoton_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDetaStrip_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDphiStrip_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDrSignal_ptGt1.0)/F",
    # "TMath::Min(0.5, recTauPtWeightedDrIsolation_ptGt1.0)/F",
    # "TMath::Min(1., recTauEratio)/F",
    # "TMath::Sign(+1., recImpactParam)/F",
    # "TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam))))/F",
    # "TMath::Min(10., TMath::Abs(recImpactParamSign))/F",
    # "TMath::Sign(+1., recImpactParam3D)/F",
    # "TMath::Sqrt(TMath::Abs(TMath::Min(1., TMath::Abs(recImpactParam3D))))/F",
    # "TMath::Min(10., TMath::Abs(recImpactParamSign3D))/F",
    # "hasRecDecayVertex/I",
    # "TMath::Sqrt(recDecayDistMag)/F",
    # "TMath::Min(10., recDecayDistSign)/F",
    # "TMath::Max(-1.,recTauGJangleDiff)/F",
])
process.reweightTreeTauIdMVA.xmlspectatorVariables = cms.vstring([
    # "recTauPt",
    # "leadPFChargedHadrCandPt",
    # "numOfflinePrimaryVertices",
    # "genVisTauPt",
    # "genTauPt",
    # "byIsolationMVArun2v1DBdR03oldDMwLTraw",
    # "byIsolationMVArun2v1DBoldDMwLTraw",
    # "byIsolationMVArun2v1DBoldDMwLTraw2016",
    # "byIsolationMVArun2017v1DBoldDMwLTraw2017",
    # "byIsolationMVArun2v1DBnewDMwLTraw",
    # "byIsolationMVArun2v1DBnewDMwLTraw2016",
    # "byCombinedIsolationDeltaBetaCorrRaw3Hits",
    # "byLooseCombinedIsolationDeltaBetaCorr3Hits",
    # "byMediumCombinedIsolationDeltaBetaCorr3Hits",
    # "byTightCombinedIsolationDeltaBetaCorr3Hits",
    # "byIsolationMVArun2v1DBoldDMwLTraw",
    # "byIsolationMVArun2v1DBoldDMwLTraw2016",
    # "byIsolationMVArun2017v1DBoldDMwLTraw2017",
    # "recTauNphoton",
    # "recTauNphoton_ptGt1.0",
    # "recTauNphoton_ptGt1.5",
    # "photonPtSumOutsideSignalCone_ptGt1.0",
    # "photonPtSumOutsideSignalCone_ptGt1.5",
    # "photonPtSumOutsideSignalConedRgt0p1_ptGt1.0",
    # "photonPtSumOutsideSignalConedRgt0p1_ptGt1.5",
    # "neutralIsoPtSum_ptGt1.0",
    # "neutralIsoPtSum_ptGt1.5",
    # "recTauPtWeightedDetaStrip_ptGt1.0",
    # "recTauPtWeightedDetaStrip_ptGt1.5",
    # "recTauPtWeightedDphiStrip_ptGt1.0",
    # "recTauPtWeightedDphiStrip_ptGt1.5",
    # "recTauPtWeightedDrSignal_ptGt1.0",
    # "recTauPtWeightedDrSignal_ptGt1.5",
    # "recTauPtWeightedDrIsolation_ptGt1.0",
    # "recTauPtWeightedDrIsolation_ptGt1.5",
    #     "chargedIsoPtSumdR03",
    # "neutralIsoPtSumdR03",
    # "neutralIsoPtSum_IsoConeR0p3_ptGt1.0",
    # "neutralIsoPtSum_IsoConeR0p3_ptGt1.5",
    # "photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.0",
    # "photonPtSumOutsideSignalCone_IsoConeR0p3_ptGt1.5",
])
process.reweightTreeTauIdMVA.gbrForestName = cms.string('')  # "BDT::BDTG"
process.reweightTreeTauIdMVA.createClassId = cms.bool(False)  # "BDT::BDTG"
process.reweightTreeTauIdMVA.classId = cms.int32(1)  # "BDT::BDTG"
''')



# def addCondorToMake(makeFile, sh_name, py_name, log_name):
#     presel_sh_file = open(sh_name, "w")
#     print 'sh_name:', sh_name
#     print 'py_name:', py_name

#     presel_sub_name = sh_name.replace('.sh', '.sub')
#     presel_sub_file = open(presel_sub_name, "w")
#     presel_sub_file.write(presel_sub.safe_substitute({
#         "preselsh": sh_name,
#         'preselid': sh_name.split('/')[-1].split('.')[0],  #'_'.join([DM, '0p5', discriminator, sample, version]),
#     }))
#     presel_sub_file.close()

#     presel_sh_file.write(presel_sh.safe_substitute({
#         'execDir': execDir,
#         'preselcommand': ' '.join([executable_preselectTreeTauIdMVA, py_name, '&>', log_name]),
#     }))
#     presel_sh_file.close()
#     makeFile.write('\tcd ' + os.path.join(outputFilePath, 'preselection') +
#         "; chmod +x *.sh" +
#         "; condor_submit " + sh_name.replace('.sh', '.sub') + '\n')
def addCondorToMake(makeFile, sh_name, py_name, log_name, execDir, executable_preselectTreeTauIdMVA, outputFilePath):
    presel_sh_file = open(sh_name, "w")
    print 'sh_name:', sh_name
    print 'py_name:', py_name
    presel_sub_name = sh_name.replace('.sh', '.sub')
    presel_sub_file = open(presel_sub_name, "w")
    presel_sub_file.write(presel_sub.safe_substitute({
        "preselsh": sh_name,
        'preselid': sh_name.split('/')[-1].split('.')[0],  #'_'.join([DM, '0p5', discriminator, sample, version]),
    }))
    presel_sub_file.close()

    presel_sh_file.write(presel_sh.safe_substitute({
        'execDir': execDir,
        'preselcommand': ' '.join([executable_preselectTreeTauIdMVA, py_name, '&>', log_name]),
    }))
    presel_sh_file.close()
    makeFile.write('\tcd ' + os.path.join(outputFilePath, 'preselection') +
        "; chmod +x *.sh" +
        "; condor_submit " + sh_name.replace('.sh', '.sub') + '\n')
