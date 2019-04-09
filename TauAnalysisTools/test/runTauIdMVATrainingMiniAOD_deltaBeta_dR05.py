#!/usr/bin/env python
'''
In this file as for the dR0p5 cone you can make a choice of training with new or old DM
as well as the choice of the campaighn
'''
from samplesHandles import SamplesHandles
import os
import yaml
from string import Template
import pprint
pp = pprint.PrettyPrinter(indent=4)

from submitHelpers import getTrainingSets

config = yaml.load(open(os.path.join(os.environ['CMSSW_BASE'], "src/TauAnalysisTools/TauAnalysisTools/test/config.yaml"), 'r'))
preselections, cutDiscriminatorsAll, trainings, commonsDict = getTrainingSets(
    trainingsets=os.path.join(os.environ['CMSSW_BASE'], 'src/TauAnalysisTools/TauAnalysisTools/test/trainingsets.json'))

inputFilePath = os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], 'ntuples')
outputFilePath = Template(os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], "$trainingtype"))
# ---------- Settings to touch ----------------
DM = "new"
disable_xml_inclusion = True
use_condor = True

# TODO:
traintingVariables = ['recTauPt', 'recTauEta', 'chargedIsoPtSum', 'neutralIsoPtSum_ptGt1.0', 'puCorrPtSum', 'photonPtSumOutsideSignalCone_ptGt1.0', 'recTauDecayMode', 'recTauNphoton_ptGt1.0', 'recTauPtWeightedDetaStrip_ptGt1.0', 'recTauPtWeightedDphiStrip_ptGt1.0', 'recTauPtWeightedDrSignal_ptGt1.0', 'recTauPtWeightedDrIsolation_ptGt1.0', 'recTauEratio', 'recImpactParam', 'recImpactParam', 'recImpactParamSign', 'recImpactParam3D', 'recImpactParam3D', 'recImpactParamSign3D', 'hasRecDecayVertex', 'recDecayDistMag', 'recDecayDistSign', 'recTauGJangleDiff']
# TODO:
prepareTreeOptions = "nTrain_Signal=0:nTrain_Background=0:nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V"

# v = config['version']
decaymodes = {
    "new": {
        "mvaDiscriminators": {
            'mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0'],
            # 'mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p5': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p5']
        },
        "cutDiscriminators": {
            'rawMVAnewDMwLT': cutDiscriminatorsAll['rawMVAnewDMwLT'],
            'rawMVAnewDMwLT2016': cutDiscriminatorsAll['rawMVAnewDMwLT2016'],
            'rawMVAnewDMwLT2017v2': cutDiscriminatorsAll['rawMVAnewDMwLT2017v2'],
        },
        "plots": {
            'mvaIsolation_optDeltaR05BDeltaBeta_newDM': {
                'graphs': [
                    'mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p0',
                    # 'mvaIsolation3HitsDeltaR05opt2aLTDB_newDM_1p5',
                    'rawMVAnewDMwLT',
                    'rawMVAnewDMwLT2016',
                    'rawMVAnewDMwLT2017v2',
                ]
            }
        },
        "version": 'tauId_dR05_new_' + config['version'],
    },
    "old": {
        "mvaDiscriminators": {
            'mvaIsolation3HitsDeltaR05opt2aLTDB_1p0': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_1p0'],  # Standart training.
            # 'mvaIsolation3HitsDeltaR05opt2aLTDB_1p0': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_1p0'], # this one should have different presel input file
            # 'mvaIsolation3HitsDeltaR05opt1aLTDB': trainings['mvaIsolation3HitsDeltaR05opt1aLTDB'], # only untill will be possible to lead the trainings
            # 'mvaIsolation3HitsDeltaR05opt2aLTDB_1p5': trainings['mvaIsolation3HitsDeltaR05opt2aLTDB_1p5']
        },
        "cutDiscriminators": {
            'rawMVAoldDMwLT': cutDiscriminatorsAll['rawMVAoldDMwLT'],
            'rawMVAoldDMwLT2016': cutDiscriminatorsAll['rawMVAoldDMwLT2016'],
            'rawMVAoldDMwLT2017v2': cutDiscriminatorsAll['rawMVAoldDMwLT2017v2'],
            # 'rawMVAoldDMwLT2018': cutDiscriminatorsAll['rawMVAoldDMwLT2018'],
        },
        "plots": {
            'mvaIsolation_optDeltaR05BDeltaBeta_oldDM': {
                'graphs': [
                    'mvaIsolation3HitsDeltaR05opt2aLTDB_1p0',
                    # 'mvaIsolation3HitsDeltaR05opt2aLTDB_1p5',
                    'rawMVAoldDMwLT',
                    'rawMVAoldDMwLT2016',
                    'rawMVAoldDMwLT2017v2'
                    # 'rawMVAoldDMwLT2018',
                ]
            }
        },
        "version": 'tauId_dR05_old_' + config['version'],
    }
}

datasetDirName = 'dataset_' + DM + "DM_" + decaymodes[DM]["version"]

# OPTIONAL!!!!
# for val in decaymodes[DM]['mvaDiscriminators'].values():
#     val['applyPtDependentPruningSignal'] = False

# Set this to true if you want to compute ROC curves for additional
# discriminators for comparisons on ALL events available in the ntuples
# NB: if pt-dependent pruning is used, this will not result in an
# apples-to-apples comparison!
computeROConAllEvents = False

# ---------- end Settings to touch ----------------

train_option = 'optaDBAll'

outputFilePath = outputFilePath.substitute(trainingtype=decaymodes[DM]["version"])

samples_key = config['samples_key']['dR0p5']
sh = SamplesHandles(samples_key)
signalSamples = sh.samples_sg.keys()
backgroundSamples = sh.samples_bg.keys()

# Setting for very specific test
if samples_key == "2017PU":
    # Rewrite to analyse PU samples
    subfolder = "noPU"  # for regular runs use empty string
    samples = sh.getSamplesPU17(subfolder)
    for key in samples.keys():
        if samples[key]['type'] == 'BackgroundMC':
            backgroundSamples = [key]
        elif samples[key]['type'] == 'SignalMC':
            signalSamples = [key]

    pp.pprint(signalSamples)

    version = subfolder
    inputFilePath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_PU/ntuples/" + subfolder + (len(subfolder) > 0) * "/"
    outputFilePath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_PU/%s/trainfilesfinal_newDM" % version + (len(subfolder) > 0) * "_" + subfolder + "/"


# DO NOT process isodR03 and isodR05 together! - different input variables
# preselection root-files can be shared only if thew follow the same preselection choice (1 of 4)
mvaDiscriminators = decaymodes[DM]["mvaDiscriminators"]

# to ensure the final reweighting root files will be suitable for larger spectra of trainings
for value in mvaDiscriminators.values():
    value["spectatorVariables"] += commonsDict['commonOtherVariables']

cutDiscriminators = decaymodes[DM]["cutDiscriminators"]
plots = decaymodes[DM]["plots"]
allDiscriminators = {}
allDiscriminators.update(mvaDiscriminators)
allDiscriminators.update(cutDiscriminators)

from runTauIdMVATrainingMiniAOD_common import produceRunScripts
produceRunScripts(
    inputFilePath=inputFilePath,
    signalSamples=signalSamples,
    backgroundSamples=backgroundSamples,
    decaymodes=decaymodes,
    DM=DM,
    train_option=train_option,
    mvaDiscriminators=mvaDiscriminators,
    outputFilePath=outputFilePath,
    disable_xml_inclusion=disable_xml_inclusion,
    computeROConAllEvents=computeROConAllEvents,
    datasetDirName=datasetDirName,
    cutDiscriminators=cutDiscriminators,
    plots=plots,
    traintingVariables=traintingVariables,
    allDiscriminators=allDiscriminators,
    use_condor=use_condor,
)
