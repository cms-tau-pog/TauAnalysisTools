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

from submitHelpers import getTrainingSets, reweighting_no_xml, addCondorToMake
from condorTemplates import presel_sub, presel_sh

config = yaml.load(open("config.yaml", 'r'))
preselections, cutDiscriminatorsAll, trainings, commonsDict = getTrainingSets(trainingsets='trainingsets.json')

inputFilePath = os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], 'ntuples')
outputFilePath = Template(os.path.join(config['nfs_base'], config['workarea_base'] + config['version'], "$trainingtype"))
# ---------- Settings to touch ----------------
DM = "new"
disable_xml_inclusion = True
use_condor = True

traintingVariables = ['recTauPt', 'recTauEta', 'chargedIsoPtSum', 'neutralIsoPtSum_ptGt1.0', 'puCorrPtSum', 'photonPtSumOutsideSignalCone_ptGt1.0', 'recTauDecayMode', 'recTauNphoton_ptGt1.0', 'recTauPtWeightedDetaStrip_ptGt1.0', 'recTauPtWeightedDphiStrip_ptGt1.0', 'recTauPtWeightedDrSignal_ptGt1.0', 'recTauPtWeightedDrIsolation_ptGt1.0', 'recTauEratio', 'recImpactParam', 'recImpactParam', 'recImpactParamSign', 'recImpactParam3D', 'recImpactParam3D', 'recImpactParamSign3D', 'hasRecDecayVertex', 'recDecayDistMag', 'recDecayDistSign', 'recTauGJangleDiff']
#TODO:
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
        },
        "plots": {
            'mvaIsolation_optDeltaR05BDeltaBeta_oldDM': {
                'graphs': [
                    'mvaIsolation3HitsDeltaR05opt2aLTDB_1p0',
                    # 'mvaIsolation3HitsDeltaR05opt2aLTDB_1p5',
                    'rawMVAoldDMwLT',
                    'rawMVAoldDMwLT2016',
                    'rawMVAoldDMwLT2017v2'
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
    inputFilePath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_PU/ntuples/" + subfolder + (len(subfolder) > 0 ) * "/"
    outputFilePath = "/nfs/dust/cms/user/glusheno/TauIDMVATraining2017/Summer17_25ns_PU/%s/trainfilesfinal_newDM" % version + (len(subfolder) > 0 ) * "_" + subfolder+ "/"


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

#==================================================== NO SETTINGS BELOW THIS LINE

execDir = "%s/bin/%s/" % (os.environ['CMSSW_BASE'], os.environ['SCRAM_ARCH'])

executable_preselectTreeTauIdMVA = execDir + 'preselectTreeTauIdMVA'
executable_reweightTreeTauIdMVA  = execDir + 'reweightTreeTauIdMVA'
executable_trainTauIdMVA         = execDir + 'trainTauIdMVA'
executable_makeROCcurveTauIdMVA  = execDir + 'makeROCcurveTauIdMVA'
executable_showROCcurvesTauIdMVA = execDir + 'showROCcurvesTauIdMVA'
executable_hadd                  = 'hadd'
executable_rm                    = 'rm -f'

nice = 'nice '

configFile_preselectTreeTauIdMVA = 'preselectTreeTauIdMVA_cfg.py'
configFile_reweightTreeTauIdMVA  = 'reweightTreeTauIdMVA_cfg.py'
configFile_trainTauIdMVA         = 'trainTauIdMVA_cfg.py'
configFile_makeROCcurveTauIdMVA  = 'makeROCcurveTauIdMVA_cfg.py'
configFile_showROCcurvesTauIdMVA = 'showROCcurvesTauIdMVA_cfg.py'

def getInputFileNames(inputFilePath, samples):
    inputFileNames = []
    for sample in samples:
        try:
            inputFileNames_sample = [ os.path.join(inputFilePath, sample, file) for file in os.listdir(os.path.join(inputFilePath, sample)) ]
            print "sample = %s: #inputFiles = %i" % (sample, len(inputFileNames_sample))
            inputFileNames.extend(inputFileNames_sample)
        except OSError:
            print "inputFilePath = %s does not exist --> skipping !!" % os.path.join(inputFilePath, sample)
            continue
    return inputFileNames

inputFileNames_signal     = getInputFileNames(inputFilePath, signalSamples)
if not len(inputFileNames_signal) > 0:
    raise ValueError("Failed to find signal samples !!")
inputFileNames_background = getInputFileNames(inputFilePath, backgroundSamples)
if not len(inputFileNames_background) > 0:
    raise ValueError("Failed to find background samples !!")

inputFileNames = []
inputFileNames.extend(inputFileNames_signal)
inputFileNames.extend(inputFileNames_background)

# create outputFilePath in case it does not yet exist
def createFilePath_recursively(filePath):
    filePath_items = filePath.split('/')
    currentFilePath = "/"
    for filePath_item in filePath_items:
        currentFilePath = os.path.join(currentFilePath, filePath_item)
        if len(currentFilePath) <= 1:
            continue
        if not os.path.exists(currentFilePath):
            os.mkdir(currentFilePath)

if not os.path.isdir(outputFilePath):
    print "outputFilePath does not yet exist, creating it."
    createFilePath_recursively(outputFilePath)
# else:
#     print 'first delete dir:', outputFilePath
#     exit(1)

if not os.path.exists(os.path.join(outputFilePath, 'preselection')):
    os.mkdir(os.path.join(outputFilePath, 'preselection'))

def getStringRep_bool(flag):
    retVal = None
    if flag:
        retVal = "True"
    else:
        retVal = "False"
    return retVal

print "Info: building config files for MVA training"
preselectTreeTauIdMVA_configFileNames     = {} # key = discriminator, "signal" or "background"
preselectTreeTauIdMVA_outputFileNames     = {} # key = discriminator, "signal" or "background"
preselectTreeTauIdMVA_logFileNames        = {} # key = discriminator, "signal" or "background"
reweightTreeTauIdMVA_configFileNames      = {} # key = discriminator, "signal" or "background"
reweightTreeTauIdMVA_outputFileNames      = {} # key = discriminator, "signal" or "background"
reweightTreeTauIdMVA_logFileNames         = {} # key = discriminator, "signal" or "background"
trainTauIdMVA_configFileNames             = {} # key = discriminator
trainTauIdMVA_outputFileNames             = {} # key = discriminator
trainTauIdMVA_logFileNames                = {} # key = discriminator
merged_preselected_root                   = {} # key = discriminator
preselected_roots                   = {} # key = discriminator


for discriminator in mvaDiscriminators.keys():

    print "processing discriminator = %s" % discriminator

    #----------------------------------------------------------------------------
    # build config file for preselecting training trees for signal and background
    preselectTreeTauIdMVA_configFileNames[discriminator] = {}
    preselectTreeTauIdMVA_outputFileNames[discriminator] = {}
    preselectTreeTauIdMVA_logFileNames[discriminator]    = {}
    for sample in ["signal"]:
        outputFileName = os.path.join(outputFilePath, "preselectTreeTauIdMVA_%s_%s.root" % (discriminator, sample))
        print " outputFileName = '%s'" % outputFileName
        preselectTreeTauIdMVA_outputFileNames[discriminator][sample] = outputFileName

        cfgFileName_original = configFile_preselectTreeTauIdMVA
        cfgFile_original = open(cfgFileName_original, "r")
        cfg_original = cfgFile_original.read()
        cfgFile_original.close()
        cfg_modified  = cfg_original
        cfg_modified += "\n"
        cfg_modified += "process.fwliteInput.fileNames = cms.vstring()\n"
        for inputFileName in inputFileNames:
            cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % inputFileName
        cfg_modified += "\n"
        eventPruningLevel = None
        ptDependentPruning = None
        if sample == 'signal':
            cfg_modified += "process.preselectTreeTauIdMVA.samples = cms.vstring(%s)\n" % signalSamples
            eventPruningLevel = mvaDiscriminators[discriminator]['applyEventPruningSignal']
            ptDependentPruning = mvaDiscriminators[discriminator]['applyPtDependentPruningSignal']
        else:
            cfg_modified += "process.preselectTreeTauIdMVA.samples = cms.vstring(%s)\n" % backgroundSamples
            eventPruningLevel = mvaDiscriminators[discriminator]['applyEventPruningBackground']
            ptDependentPruning = mvaDiscriminators[discriminator]['applyPtDependentPruningBackground']
        cfg_modified += "process.preselectTreeTauIdMVA.inputTreeName = cms.string('%s')\n" % "tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD"
        cfg_modified += "process.preselectTreeTauIdMVA.preselection = cms.string('%s')\n" % mvaDiscriminators[discriminator]['preselection']
        cfg_modified += "process.preselectTreeTauIdMVA.applyEventPruning = cms.int32(%i)\n" % eventPruningLevel
        cfg_modified += "process.preselectTreeTauIdMVA.applyPtDependentPruning = cms.bool(%s)\n" % ptDependentPruning
        cfg_modified += "process.preselectTreeTauIdMVA.inputVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['inputVariables']
        cfg_modified += "process.preselectTreeTauIdMVA.spectatorVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['spectatorVariables']
        cfg_modified += "process.preselectTreeTauIdMVA.otherVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['otherVariables']
        cfg_modified += "process.preselectTreeTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
        cfgFileName_modified = os.path.join(outputFilePath, 'preselection', cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (discriminator, sample)))

        print " cfgFileName_modified = '%s'" % cfgFileName_modified
        cfgFile_modified = open(cfgFileName_modified, "w")
        cfgFile_modified.write(cfg_modified)
        cfgFile_modified.close()
        preselectTreeTauIdMVA_configFileNames[discriminator][sample] = cfgFileName_modified

        logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
        preselectTreeTauIdMVA_logFileNames[discriminator][sample] = logFileName

    # Background preselections
    preselectTreeTauIdMVA_outputFileNames[discriminator]["background"] = []
    preselectTreeTauIdMVA_configFileNames[discriminator]["background"] = []
    preselectTreeTauIdMVA_logFileNames[discriminator]["background"] = []
    merged_preselected_root[discriminator] = os.path.join(outputFilePath, "preselectTreeTauIdMVA_%s_%s.root" % (discriminator, "background"))
    preselected_roots[discriminator] = []
    for proc in backgroundSamples:
        sample = "background"
        outputFileName = os.path.join(outputFilePath, "preselectTreeTauIdMVA_%s_%s_%s.root" % (discriminator, sample, proc))
        preselected_roots[discriminator].append(outputFileName)
        print " outputFileName = '%s'" % outputFileName
        preselectTreeTauIdMVA_outputFileNames[discriminator][sample].append(outputFileName)

        cfgFileName_original = configFile_preselectTreeTauIdMVA
        cfgFile_original = open(cfgFileName_original, "r")
        cfg_original = cfgFile_original.read()
        cfgFile_original.close()
        cfg_modified  = cfg_original
        cfg_modified += "\n"
        cfg_modified += "process.fwliteInput.fileNames = cms.vstring()\n"
        for inputFileName in inputFileNames:
            cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % inputFileName
        cfg_modified += "\n"
        eventPruningLevel = None
        ptDependentPruning = None
        cfg_modified += "process.preselectTreeTauIdMVA.samples = cms.vstring(%s)\n" % [proc]
        eventPruningLevel = mvaDiscriminators[discriminator]['applyEventPruningBackground']
        ptDependentPruning = mvaDiscriminators[discriminator]['applyPtDependentPruningBackground']
        cfg_modified += "process.preselectTreeTauIdMVA.inputTreeName = cms.string('%s')\n" % "tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD"
        cfg_modified += "process.preselectTreeTauIdMVA.preselection = cms.string('%s')\n" % mvaDiscriminators[discriminator]['preselection']
        cfg_modified += "process.preselectTreeTauIdMVA.applyEventPruning = cms.int32(%i)\n" % eventPruningLevel
        cfg_modified += "process.preselectTreeTauIdMVA.applyPtDependentPruning = cms.bool(%s)\n" % ptDependentPruning
        cfg_modified += "process.preselectTreeTauIdMVA.inputVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['inputVariables']
        cfg_modified += "process.preselectTreeTauIdMVA.spectatorVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['spectatorVariables']
        cfg_modified += "process.preselectTreeTauIdMVA.otherVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['otherVariables']
        cfg_modified += "process.preselectTreeTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
        cfgFileName_modified = os.path.join(outputFilePath, 'preselection', cfgFileName_original.replace("_cfg.py", "_%s_%s_%s_cfg.py" % (discriminator, sample, proc)))
        print " cfgFileName_modified = '%s'" % cfgFileName_modified
        cfgFile_modified = open(cfgFileName_modified, "w")
        cfgFile_modified.write(cfg_modified)
        cfgFile_modified.close()
        preselectTreeTauIdMVA_configFileNames[discriminator][sample].append(cfgFileName_modified)

        # presel_sub_name = cfgFileName_modified.replace('.py', '.sub')
        # presel_sub_file = open(presel_sub_name, "w")
        # presel_sub_file.write(presel_sub.safe_substitute({
        #     "preselsh": presel_sub_name,
        #     'preselid': '_'.join([DM, '0p5', discriminator, sample, version]),
        # }))
        # presel_sub_file.close()

        logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
        preselectTreeTauIdMVA_logFileNames[discriminator][sample].append(logFileName)
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # CV: build config file for Pt, eta reweighting
    reweightTreeTauIdMVA_configFileNames[discriminator] = {}
    reweightTreeTauIdMVA_outputFileNames[discriminator] = {}
    reweightTreeTauIdMVA_logFileNames[discriminator]    = {}
    for sample in [ "signal", "background" ]:
        outputFileName = os.path.join(outputFilePath, "reweightTreeTauIdMVA_%s_%s.root" % (discriminator, sample))
        print " outputFileName = '%s'" % outputFileName
        reweightTreeTauIdMVA_outputFileNames[discriminator][sample] = outputFileName

        cfgFileName_original = configFile_reweightTreeTauIdMVA
        cfgFile_original = open(cfgFileName_original, "r")
        cfg_original = cfgFile_original.read()
        cfgFile_original.close()
        cfg_modified  = cfg_original
        cfg_modified += "\n"
        cfg_modified += "process.fwliteInput.fileNames = cms.vstring()\n"
        cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % preselectTreeTauIdMVA_outputFileNames[discriminator]['signal']
        cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % merged_preselected_root[discriminator]
        cfg_modified += "\n"
        cfg_modified += "process.reweightTreeTauIdMVA.signalSamples = cms.vstring('signal')\n"
        cfg_modified += "process.reweightTreeTauIdMVA.backgroundSamples = cms.vstring('background')\n"
        cfg_modified += "process.reweightTreeTauIdMVA.applyPtReweighting = cms.bool(%s)\n" % getStringRep_bool(mvaDiscriminators[discriminator]['applyPtReweighting'])
        cfg_modified += "process.reweightTreeTauIdMVA.applyEtaReweighting = cms.bool(%s)\n" % getStringRep_bool(mvaDiscriminators[discriminator]['applyEtaReweighting'])
        cfg_modified += "process.reweightTreeTauIdMVA.reweight = cms.string('%s')\n" % mvaDiscriminators[discriminator]['reweight']
        cfg_modified += "process.reweightTreeTauIdMVA.inputVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['inputVariables']
        cfg_modified += "process.reweightTreeTauIdMVA.spectatorVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['spectatorVariables']
        cfg_modified += "process.reweightTreeTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
        cfg_modified += "process.reweightTreeTauIdMVA.save = cms.string('%s')\n" % sample

        if disable_xml_inclusion:
            cfg_modified += reweighting_no_xml.safe_substitute()

        cfgFileName_modified = os.path.join(outputFilePath, cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (discriminator, sample)))
        print " cfgFileName_modified = '%s'" % cfgFileName_modified
        cfgFile_modified = open(cfgFileName_modified, "w")
        cfgFile_modified.write(cfg_modified)
        cfgFile_modified.close()
        reweightTreeTauIdMVA_configFileNames[discriminator][sample] = cfgFileName_modified

        logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
        reweightTreeTauIdMVA_logFileNames[discriminator][sample] = logFileName
    #----------------------------------------------------------------------------

    #----------------------------------------------------------------------------
    # CV: build config file for actual MVA training

    outputFileName = os.path.join(outputFilePath, "trainTauIdMVA_%s.root" % discriminator)
    print " outputFileName = '%s'" % outputFileName
    trainTauIdMVA_outputFileNames[discriminator] = outputFileName

    cfgFileName_original = configFile_trainTauIdMVA
    cfgFile_original = open(cfgFileName_original, "r")
    cfg_original = cfgFile_original.read()
    cfgFile_original.close()
    cfg_modified  = cfg_original
    cfg_modified += "\n"
    cfg_modified += "process.fwliteInput.fileNames = cms.vstring()\n"
    cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % reweightTreeTauIdMVA_outputFileNames[discriminator]['signal']
    cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % reweightTreeTauIdMVA_outputFileNames[discriminator]['background']
    cfg_modified += "\n"
    cfg_modified += "process.trainTauIdMVA.signalSamples = cms.vstring('signal')\n"
    cfg_modified += "process.trainTauIdMVA.backgroundSamples = cms.vstring('background')\n"
    cfg_modified += "process.trainTauIdMVA.applyPtReweighting = cms.bool(%s)\n" % getStringRep_bool(mvaDiscriminators[discriminator]['applyPtReweighting'])
    cfg_modified += "process.trainTauIdMVA.applyEtaReweighting = cms.bool(%s)\n" % getStringRep_bool(mvaDiscriminators[discriminator]['applyEtaReweighting'])
    cfg_modified += "process.trainTauIdMVA.reweight = cms.string('%s')\n" % mvaDiscriminators[discriminator]['reweight']
    cfg_modified += "process.trainTauIdMVA.mvaName = cms.string('%s')\n" % discriminator
    cfg_modified += "process.trainTauIdMVA.mvaTrainingOptions = cms.string('%s')\n" % mvaDiscriminators[discriminator]['mvaTrainingOptions']
    cfg_modified += "process.trainTauIdMVA.inputVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['inputVariables']
    cfg_modified += "process.trainTauIdMVA.traintingVariables = cms.vstring(%s)\n" % traintingVariables  # mvaDiscriminators[discriminator]['traintingVariables']
    cfg_modified += "process.trainTauIdMVA.spectatorVariables = cms.vstring(%s)\n" % mvaDiscriminators[discriminator]['spectatorVariables']
    cfg_modified += "process.trainTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
    cfg_modified += "process.trainTauIdMVA.datasetDirName = cms.string('%s')\n" % datasetDirName
    cfgFileName_modified = os.path.join(outputFilePath, cfgFileName_original.replace("_cfg.py", "_%s_cfg.py" % discriminator))
    print " cfgFileName_modified = '%s'" % cfgFileName_modified
    cfgFile_modified = open(cfgFileName_modified, "w")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()
    trainTauIdMVA_configFileNames[discriminator] = cfgFileName_modified

    logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
    trainTauIdMVA_logFileNames[discriminator] = logFileName

print "\n", "=" * 50, "Info: building config files for evaluating MVA performance"
makeROCcurveTauIdMVA_configFileNames = {} # key = discriminator, "TestTree" or "TrainTree"
makeROCcurveTauIdMVA_outputFileNames = {} # key = discriminator, "TestTree" or "TrainTree"
makeROCcurveTauIdMVA_logFileNames    = {} # key = discriminator, "TestTree" or "TrainTree"
for discriminator in mvaDiscriminators.keys():

    print "processing discriminator = %s" % discriminator

    makeROCcurveTauIdMVA_configFileNames[discriminator] = {}
    makeROCcurveTauIdMVA_outputFileNames[discriminator] = {}
    makeROCcurveTauIdMVA_logFileNames[discriminator]    = {}

    for tree in [ "TestTree", "TrainTree" ]:
        outputFileName = os.path.join(outputFilePath, "makeROCcurveTauIdMVA_%s_%s.root" % (discriminator, tree))
        print " outputFileName = '%s'" % outputFileName
        makeROCcurveTauIdMVA_outputFileNames[discriminator][tree] = outputFileName

        cfgFileName_original = configFile_makeROCcurveTauIdMVA
        cfgFile_original = open(cfgFileName_original, "r")
        cfg_original = cfgFile_original.read()
        cfgFile_original.close()
        cfg_modified  = cfg_original
        cfg_modified += "\n"
        cfg_modified += "process.fwliteInput.fileNames = cms.vstring('%s')\n" % trainTauIdMVA_outputFileNames[discriminator]
        cfg_modified += "\n"
        cfg_modified += "delattr(process.makeROCcurveTauIdMVA, 'signalSamples')\n"
        cfg_modified += "delattr(process.makeROCcurveTauIdMVA, 'backgroundSamples')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.treeName = cms.string('%s/%s')\n" % (datasetDirName, tree)
        ##cfg_modified += "process.makeROCcurveTauIdMVA.preselection = cms.string('%s')\n" % mvaDiscriminators[discriminator]['preselection']
        cfg_modified += "process.makeROCcurveTauIdMVA.preselection = cms.string('')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.classId_signal = cms.int32(0)\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.classId_background = cms.int32(1)\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.branchNameClassId = cms.string('classID')\n"
        if 'recTauPt/F' in mvaDiscriminators[discriminator]['spectatorVariables']:
            cfg_modified += "process.makeROCcurveTauIdMVA.branchNameLogTauPt = cms.string('')\n"
            cfg_modified += "process.makeROCcurveTauIdMVA.branchNameTauPt = cms.string('recTauPt')\n"
        else:
            cfg_modified += "process.makeROCcurveTauIdMVA.branchNameLogTauPt = cms.string('TMath_Log_TMath_Max_1.,recTauPt__')\n"
            cfg_modified += "process.makeROCcurveTauIdMVA.branchNameTauPt = cms.string('')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.discriminator = cms.string('BDTG')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.branchNameEvtWeight = cms.string('weight')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.graphName = cms.string('%s_%s')\n" % (discriminator, tree)
        cfg_modified += "process.makeROCcurveTauIdMVA.binning.numBins = cms.int32(%i)\n" % 30000
        cfg_modified += "process.makeROCcurveTauIdMVA.binning.min = cms.double(%1.2f)\n" % -1.5
        cfg_modified += "process.makeROCcurveTauIdMVA.binning.max = cms.double(%1.2f)\n" % +1.5
        cfg_modified += "process.makeROCcurveTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
        cfgFileName_modified = os.path.join(outputFilePath, cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (discriminator, tree)))
        print " cfgFileName_modified = '%s'" % cfgFileName_modified
        cfgFile_modified = open(cfgFileName_modified, "w")
        cfgFile_modified.write(cfg_modified)
        cfgFile_modified.close()
        makeROCcurveTauIdMVA_configFileNames[discriminator][tree] = cfgFileName_modified

        logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
        makeROCcurveTauIdMVA_logFileNames[discriminator][tree] = logFileName

    plotName = "mvaIsolation_%s_overtraining" % discriminator
    plots[plotName] = {
        'graphs' : [
            '%s:TestTree' % discriminator,
            '%s:TrainTree' % discriminator
        ]
    }

if computeROConAllEvents:
    for discriminator in cutDiscriminators.keys():

        print "processing discriminator = %s" % discriminator

        makeROCcurveTauIdMVA_configFileNames[discriminator] = {}
        makeROCcurveTauIdMVA_outputFileNames[discriminator] = {}
        makeROCcurveTauIdMVA_logFileNames[discriminator]    = {}

        outputFileName = os.path.join(outputFilePath, "makeROCcurveTauIdMVA_%s.root" % discriminator)
        print " outputFileName = '%s'" % outputFileName
        makeROCcurveTauIdMVA_outputFileNames[discriminator]['TestTree'] = outputFileName

        cfgFileName_original = configFile_makeROCcurveTauIdMVA
        cfgFile_original = open(cfgFileName_original, "r")
        cfg_original = cfgFile_original.read()
        cfgFile_original.close()
        cfg_modified  = cfg_original
        cfg_modified += "\n"
        cfg_modified += "process.fwliteInput.fileNames = cms.vstring()\n"
        for inputFileName in inputFileNames:
            cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % inputFileName
        cfg_modified += "\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.signalSamples = cms.vstring(%s)\n" % signalSamples
        cfg_modified += "process.makeROCcurveTauIdMVA.backgroundSamples = cms.vstring(%s)\n" % backgroundSamples
        cfg_modified += "process.makeROCcurveTauIdMVA.treeName = cms.string('tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.preselection = cms.string('%s')\n" % cutDiscriminators[discriminator]['preselection']
        cfg_modified += "process.makeROCcurveTauIdMVA.branchNameLogTauPt = cms.string('')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.branchNameTauPt = cms.string('recTauPt')\n"
        cfg_modified += "process.makeROCcurveTauIdMVA.discriminator = cms.string('%s')\n" % cutDiscriminators[discriminator]['discriminator']
        cfg_modified += "process.makeROCcurveTauIdMVA.graphName = cms.string('%s_%s')\n" % (discriminator, "TestTree")
        cfg_modified += "process.makeROCcurveTauIdMVA.binning.numBins = cms.int32(%i)\n" % cutDiscriminators[discriminator]['numBins']
        cfg_modified += "process.makeROCcurveTauIdMVA.binning.min = cms.double(%1.2f)\n" % cutDiscriminators[discriminator]['min']
        cfg_modified += "process.makeROCcurveTauIdMVA.binning.max = cms.double(%1.2f)\n" % cutDiscriminators[discriminator]['max']
        cfg_modified += "process.makeROCcurveTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
        cfgFileName_modified = os.path.join(outputFilePath, cfgFileName_original.replace("_cfg.py", "_%s_cfg.py" % discriminator))
        print " cfgFileName_modified = '%s'" % cfgFileName_modified
        cfgFile_modified = open(cfgFileName_modified, "w")
        cfgFile_modified.write(cfg_modified)
        cfgFile_modified.close()
        makeROCcurveTauIdMVA_configFileNames[discriminator]['TestTree'] = cfgFileName_modified

        logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
        makeROCcurveTauIdMVA_logFileNames[discriminator]['TestTree'] = logFileName
else:
    for mvaDiscriminator in mvaDiscriminators.keys():
        for cutDiscriminator in cutDiscriminators.keys():

            print "processing discriminator = %s" % cutDiscriminator

            makeROCcurveTauIdMVA_configFileNames[cutDiscriminator] = {}
            makeROCcurveTauIdMVA_outputFileNames[cutDiscriminator] = {}
            makeROCcurveTauIdMVA_logFileNames[cutDiscriminator]    = {}

            for tree in [ "TestTree" ]:
                outputFileName = os.path.join(outputFilePath, "makeROCcurveTauIdMVA_%s_%s.root" % (cutDiscriminator, tree))
                print " outputFileName = '%s'" % outputFileName
                makeROCcurveTauIdMVA_outputFileNames[cutDiscriminator][tree] = outputFileName

                cfgFileName_original = configFile_makeROCcurveTauIdMVA
                cfgFile_original = open(cfgFileName_original, "r")
                cfg_original = cfgFile_original.read()
                cfgFile_original.close()
                cfg_modified  = cfg_original
                cfg_modified += "\n"
                cfg_modified += "process.fwliteInput.fileNames = cms.vstring('%s')\n" % trainTauIdMVA_outputFileNames[mvaDiscriminator]
                cfg_modified += "\n"
                cfg_modified += "delattr(process.makeROCcurveTauIdMVA, 'signalSamples')\n"
                cfg_modified += "delattr(process.makeROCcurveTauIdMVA, 'backgroundSamples')\n"
                cfg_modified += "process.makeROCcurveTauIdMVA.treeName = cms.string('%s/%s')\n" % (datasetDirName, tree)
                cfg_modified += "process.makeROCcurveTauIdMVA.preselection = cms.string('')\n"
                cfg_modified += "process.makeROCcurveTauIdMVA.classId_signal = cms.int32(0)\n"
                cfg_modified += "process.makeROCcurveTauIdMVA.classId_background = cms.int32(1)\n"
                cfg_modified += "process.makeROCcurveTauIdMVA.branchNameClassId = cms.string('classID')\n"
                if 'recTauPt/F' in mvaDiscriminators[mvaDiscriminator]['spectatorVariables']:
                    cfg_modified += "process.makeROCcurveTauIdMVA.branchNameLogTauPt = cms.string('')\n"
                    cfg_modified += "process.makeROCcurveTauIdMVA.branchNameTauPt = cms.string('recTauPt')\n"
                else:
                    cfg_modified += "process.makeROCcurveTauIdMVA.branchNameLogTauPt = cms.string('TMath_Log_TMath_Max_1.,recTauPt__')\n"
                    cfg_modified += "process.makeROCcurveTauIdMVA.branchNameTauPt = cms.string('')\n"
                cfg_modified += "process.makeROCcurveTauIdMVA.discriminator = cms.string('%s')\n" % cutDiscriminators[cutDiscriminator]['discriminator']
                cfg_modified += "process.makeROCcurveTauIdMVA.branchNameEvtWeight = cms.string('weight')\n"
                cfg_modified += "process.makeROCcurveTauIdMVA.graphName = cms.string('%s_%s')\n" % (cutDiscriminator, tree)
                cfg_modified += "process.makeROCcurveTauIdMVA.binning.numBins = cms.int32(%i)\n" % cutDiscriminators[cutDiscriminator]['numBins']
                cfg_modified += "process.makeROCcurveTauIdMVA.binning.min = cms.double(%1.2f)\n" % cutDiscriminators[cutDiscriminator]['min']
                cfg_modified += "process.makeROCcurveTauIdMVA.binning.max = cms.double(%1.2f)\n" % cutDiscriminators[cutDiscriminator]['max']
                cfg_modified += "process.makeROCcurveTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
                cfgFileName_modified = os.path.join(outputFilePath, cfgFileName_original.replace("_cfg.py", "_%s_%s_cfg.py" % (cutDiscriminator, tree)))
                print " cfgFileName_modified = '%s'" % cfgFileName_modified
                cfgFile_modified = open(cfgFileName_modified, "w")
                cfgFile_modified.write(cfg_modified)
                cfgFile_modified.close()
                makeROCcurveTauIdMVA_configFileNames[cutDiscriminator][tree] = cfgFileName_modified

                logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
                makeROCcurveTauIdMVA_logFileNames[cutDiscriminator][tree] = logFileName

hadd_inputFileNames = []
for discriminator in makeROCcurveTauIdMVA_outputFileNames.keys():
    for tree in [ "TestTree", "TrainTree" ]:
        if tree in makeROCcurveTauIdMVA_outputFileNames[discriminator].keys():
            hadd_inputFileNames.append(makeROCcurveTauIdMVA_outputFileNames[discriminator][tree])
hadd_outputFileName = os.path.join(outputFilePath, "makeROCcurveTauIdMVA_all.root")

print "Info: building config files for displaying results"
showROCcurvesTauIdMVA_configFileNames = {} # key = plot
showROCcurvesTauIdMVA_outputFileNames = {} # key = plot
showROCcurvesTauIdMVA_logFileNames    = {} # key = plot
for plot in plots.keys():

    print "processing plot = %s" % plot

    outputFileName = os.path.join(outputFilePath, "showROCcurvesTauIdMVA_%s.png" % plot)
    print " outputFileName = '%s'" % outputFileName
    showROCcurvesTauIdMVA_outputFileNames[plot] = outputFileName

    cfgFileName_original = configFile_showROCcurvesTauIdMVA
    cfgFile_original = open(cfgFileName_original, "r")
    cfg_original = cfgFile_original.read()
    cfgFile_original.close()
    cfg_modified  = cfg_original
    cfg_modified += "\n"
    cfg_modified += "process.fwliteInput.fileNames = cms.vstring('%s')\n" % hadd_outputFileName
    cfg_modified += "\n"
    cfg_modified += "process.showROCcurvesTauIdMVA.graphs = cms.VPSet(\n"
    for graph in plots[plot]['graphs']:
        discriminator = None
        tree = None
        legendEntry = None
        markerStyle = None
        markerSize  = None
        markerColor = None
        if graph.find(":") != -1:
            discriminator = graph[:graph.find(":")]
            tree = graph[graph.find(":") + 1:]
            legendEntry = tree
            if tree == "TestTree":
                markerStyle = 20
                markerColor = 1
                markerSize  = 1
            elif tree == "TrainTree":
                markerStyle = 24
                markerColor = 2
                markerSize  = 1
            else:
                raise ValueError("Invalid Parameter 'tree' = %s !!" % tree)
        else:
            discriminator = graph
            tree = "TestTree"
            legendEntry = allDiscriminators[graph]['legendEntry']
            if 'markerStyle' in allDiscriminators[graph].keys():
                markerStyle = allDiscriminators[graph]['markerStyle']
            if 'markerSize' in allDiscriminators[graph].keys():
                markerSize = allDiscriminators[graph]['markerSize']
            markerColor = allDiscriminators[graph]['color']
        cfg_modified += "    cms.PSet(\n"
        cfg_modified += "        graphName = cms.string('%s_%s'),\n" % (discriminator, tree)
        cfg_modified += "        legendEntry = cms.string('%s'),\n" % legendEntry
        if markerStyle:
            cfg_modified += "        markerStyle = cms.int32(%i),\n" % markerStyle
        if markerSize:
            cfg_modified += "        markerSize = cms.int32(%i),\n" % markerSize
        cfg_modified += "        color = cms.int32(%i)\n" % markerColor
        cfg_modified += "    ),\n"
    cfg_modified += ")\n"
    cfg_modified += "process.showROCcurvesTauIdMVA.outputFileName = cms.string('%s')\n" % outputFileName
    cfgFileName_modified = os.path.join(outputFilePath, cfgFileName_original.replace("_cfg.py", "_%s_cfg.py" % plot))
    print " cfgFileName_modified = '%s'" % cfgFileName_modified
    cfgFile_modified = open(cfgFileName_modified, "w")
    cfgFile_modified.write(cfg_modified)
    cfgFile_modified.close()
    showROCcurvesTauIdMVA_configFileNames[plot] = cfgFileName_modified

    logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
    showROCcurvesTauIdMVA_logFileNames[plot] = logFileName

def make_MakeFile_vstring(list_of_strings):
    retVal = ""
    for i, string_i in enumerate(list_of_strings):
        if i > 0:
            retVal += " "
        retVal += string_i
    return retVal

# done building config files, now build Makefile...
makeFileName = os.path.join(outputFilePath, "Makefile_runTauIdMVATraining_%s_%s.make" % (decaymodes[DM]["version"], train_option))
makeFile = open(makeFileName, "w")
makeFile.write("\n")
outputFileNames = []
for discriminator in trainTauIdMVA_outputFileNames.keys():
    for sample in [ "signal", "background" ]:
        if sample == "signal":
            outputFileNames.append(preselectTreeTauIdMVA_outputFileNames[discriminator][sample])
        else:
            outputFileNames += preselectTreeTauIdMVA_outputFileNames[discriminator][sample]
        outputFileNames.append(reweightTreeTauIdMVA_outputFileNames[discriminator][sample])
    outputFileNames.append(trainTauIdMVA_outputFileNames[discriminator])
for discriminator in makeROCcurveTauIdMVA_outputFileNames.keys():
    for tree in makeROCcurveTauIdMVA_outputFileNames[discriminator]:
        outputFileNames.append(makeROCcurveTauIdMVA_outputFileNames[discriminator][tree])
outputFileNames.append(hadd_outputFileName)
for plot in showROCcurvesTauIdMVA_outputFileNames.keys():
    outputFileNames.append(showROCcurvesTauIdMVA_outputFileNames[plot])

print '\n Expected output filenames:'
pp.pprint(outputFileNames)
print '\n'


makeFile.write("all: %s\n" % make_MakeFile_vstring(outputFileNames))
makeFile.write("\techo 'Finished tau ID MVA training.'\n")
makeFile.write("\n")
for discriminator in trainTauIdMVA_outputFileNames.keys():
    for sample in ["signal", "background"]:
        if sample == "signal":
            makeFile.write("%s:\n" % (preselectTreeTauIdMVA_outputFileNames[discriminator][sample]))
            makeFile.write("\t%s%s %s &> %s\n" %
              (nice, executable_preselectTreeTauIdMVA,
               preselectTreeTauIdMVA_configFileNames[discriminator][sample],
               preselectTreeTauIdMVA_logFileNames[discriminator][sample]))

            if use_condor:
                addCondorToMake(makeFile,
                    sh_name=''.join(os.path.join(outputFilePath, 'preselection', preselectTreeTauIdMVA_configFileNames[discriminator][sample].replace("_cfg.py", ".sh"))),
                    py_name=preselectTreeTauIdMVA_configFileNames[discriminator][sample],
                    log_name=preselectTreeTauIdMVA_logFileNames[discriminator][sample],
                    execDir=execDir,
                    executable_preselectTreeTauIdMVA=executable_preselectTreeTauIdMVA,
                    outputFilePath=outputFilePath,
                )

        else:
            hadd_command = "hadd " + merged_preselected_root[discriminator] + " "

            for proc_i in range(0, len(preselectTreeTauIdMVA_outputFileNames[discriminator][sample])):
                makeFile.write("%s:\n" % (preselectTreeTauIdMVA_outputFileNames[discriminator][sample][proc_i]))
                makeFile.write("\t%s%s %s &> %s\n" %
                  (nice, executable_preselectTreeTauIdMVA,
                   preselectTreeTauIdMVA_configFileNames[discriminator][sample][proc_i],
                   preselectTreeTauIdMVA_logFileNames[discriminator][sample][proc_i]))

                if use_condor:
                    addCondorToMake(makeFile,
                        sh_name=''.join(os.path.join(outputFilePath, 'preselection', preselectTreeTauIdMVA_configFileNames[discriminator][sample][proc_i].replace("_cfg.py", ".sh"))),
                        py_name=preselectTreeTauIdMVA_configFileNames[discriminator][sample][proc_i],
                        log_name=preselectTreeTauIdMVA_logFileNames[discriminator][sample][proc_i],
                        execDir=execDir,
                        executable_preselectTreeTauIdMVA=executable_preselectTreeTauIdMVA,
                        outputFilePath=outputFilePath,
                    )

                hadd_command += ' ' + preselected_roots[discriminator][proc_i]

            hadd_command += '\n'
            pp.pprint(hadd_command)
            makeFile.write(hadd_command)

        makeFile.write("%s: %s\n" %
          (reweightTreeTauIdMVA_outputFileNames[discriminator][sample],
           make_MakeFile_vstring([ preselectTreeTauIdMVA_outputFileNames[discriminator]['signal']] + preselectTreeTauIdMVA_outputFileNames[discriminator]['background'])))
        makeFile.write("\t%s%s %s &> %s\n" %
          (nice, executable_reweightTreeTauIdMVA,
           reweightTreeTauIdMVA_configFileNames[discriminator][sample],
           reweightTreeTauIdMVA_logFileNames[discriminator][sample]))
    makeFile.write("%s: %s\n" %
      (trainTauIdMVA_outputFileNames[discriminator],
       make_MakeFile_vstring([ reweightTreeTauIdMVA_outputFileNames[discriminator]['signal'], reweightTreeTauIdMVA_outputFileNames[discriminator]['background'] ])))
    makeFile.write("\tcd %s; %s%s %s &> %s\n" %
      (execDir, nice, executable_trainTauIdMVA,
       trainTauIdMVA_configFileNames[discriminator],
       trainTauIdMVA_logFileNames[discriminator]))
makeFile.write("\n")
for discriminator in makeROCcurveTauIdMVA_outputFileNames.keys():
    for tree in [ "TestTree", "TrainTree" ]:
        if tree in makeROCcurveTauIdMVA_outputFileNames[discriminator].keys():
            if discriminator in trainTauIdMVA_outputFileNames.keys():
                makeFile.write("%s: %s %s\n" %
                  (makeROCcurveTauIdMVA_outputFileNames[discriminator][tree],
                   trainTauIdMVA_outputFileNames[discriminator],
                   #executable_makeROCcurveTauIdMVA,
                   ""))
            else:
                makeFile.write("%s:\n" %
                  (makeROCcurveTauIdMVA_outputFileNames[discriminator][tree]))
            makeFile.write("\t%s%s %s &> %s\n" %
              (nice, executable_makeROCcurveTauIdMVA,
               makeROCcurveTauIdMVA_configFileNames[discriminator][tree],
               makeROCcurveTauIdMVA_logFileNames[discriminator][tree]))
makeFile.write("\n")
makeFile.write("%s: %s\n" %
  (hadd_outputFileName,
   make_MakeFile_vstring(hadd_inputFileNames)))
makeFile.write("\t%s%s %s\n" %
  (nice, executable_rm,
   hadd_outputFileName))
makeFile.write("\t%s%s %s %s\n" %
  (nice, executable_hadd,
   hadd_outputFileName, make_MakeFile_vstring(hadd_inputFileNames)))
makeFile.write("\n")
for plot in showROCcurvesTauIdMVA_outputFileNames.keys():
    makeFile.write("%s: %s %s\n" %
      (showROCcurvesTauIdMVA_outputFileNames[plot],
       hadd_outputFileName,
       executable_showROCcurvesTauIdMVA))
    makeFile.write("\t%s%s %s &> %s\n" %
      (nice, executable_showROCcurvesTauIdMVA,
       showROCcurvesTauIdMVA_configFileNames[plot],
       showROCcurvesTauIdMVA_logFileNames[plot]))
makeFile.write("\n")
makeFile.write(".PHONY: clean\n")
makeFile.write("clean:\n")
makeFile.write("\t%s %s\n" % (executable_rm, make_MakeFile_vstring(outputFileNames)))
makeFile.write("\techo 'Finished deleting old files.'\n")
makeFile.write("\n")
makeFile.close()

print("\n Finished building Makefile. Now execute 'make -f %s'." % makeFileName)
