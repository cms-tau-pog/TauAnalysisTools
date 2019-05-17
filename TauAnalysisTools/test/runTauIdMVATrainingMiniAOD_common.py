from samplesHandles import SamplesHandles
import os
import yaml
from string import Template
import pprint
pp = pprint.PrettyPrinter(indent=4)

from submitHelpers import getTrainingSets, reweighting_no_xml, addCondorToMake
from condorTemplates import presel_sub, presel_sh


def produceRunScripts(
    inputFilePath,
    signalSamples,
    backgroundSamples,
    decaymodes,
    DM,
    train_option,
    mvaDiscriminators,
    outputFilePath,
    disable_xml_inclusion,
    computeROConAllEvents,
    datasetDirName,
    cutDiscriminators,
    plots,
    traintingVariables,
    prepareTreeOptions,
    allDiscriminators,
    use_condor,
    ):

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

    configsDir = os.path.join(os.environ['CMSSW_BASE'], "src/TauAnalysisTools/TauAnalysisTools/test/")
    configFile_preselectTreeTauIdMVA = configsDir + 'preselectTreeTauIdMVA_cfg.py'
    configFile_reweightTreeTauIdMVA  = configsDir + 'reweightTreeTauIdMVA_cfg.py'
    configFile_trainTauIdMVA         = configsDir + 'trainTauIdMVA_cfg.py'
    configFile_makeROCcurveTauIdMVA  = configsDir + 'makeROCcurveTauIdMVA_cfg.py'
    configFile_showROCcurvesTauIdMVA = configsDir + 'showROCcurvesTauIdMVA_cfg.py'

    def getInputFileNames(inputFilePath, samples):
        inputFileNames = []
        for sample in samples:
            try:
                print 'in:', os.path.join(inputFilePath, sample)
                inputFileNames_sample = [os.path.join(inputFilePath, sample, file) for file in os.listdir(os.path.join(inputFilePath, sample))]
                print "sample = %s: #inputFiles = %i" % (sample, len(inputFileNames_sample))
                inputFileNames.extend(inputFileNames_sample)
            except OSError:
                print "inputFilePath = %s does not exist --> skipping !!" % os.path.join(inputFilePath, sample)
                continue
        return inputFileNames

    inputFileNames_signal     = getInputFileNames(inputFilePath, signalSamples)
    if not len(inputFileNames_signal) > 0:
        print 'inputFilePath:', inputFilePath
        print 'signalSamples:', signalSamples
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
    preselectTreeTauIdMVA_configFileNames     = {}  # key = discriminator, "signal" or "background"
    preselectTreeTauIdMVA_outputFileNames     = {}  # key = discriminator, "signal" or "background"
    preselectTreeTauIdMVA_logFileNames        = {}  # key = discriminator, "signal" or "background"
    reweightTreeTauIdMVA_configFileNames      = {}  # key = discriminator, "signal" or "background"
    reweightTreeTauIdMVA_outputFileNames      = {}  # key = discriminator, "signal" or "background"
    reweightTreeTauIdMVA_logFileNames         = {}  # key = discriminator, "signal" or "background"
    trainTauIdMVA_configFileNames             = {}  # key = discriminator
    trainTauIdMVA_outputFileNames             = {}  # key = discriminator
    trainTauIdMVA_logFileNames                = {}  # key = discriminator
    merged_preselected_root                   = {}  # key = discriminator
    preselected_roots                         = {} # key = discriminator

    # Prepare all the commands till ROC
    for discriminator in mvaDiscriminators.keys():

        print "processing discriminator = %s" % discriminator

        #---------------------------------------------------------------------------- Preselection
        # build config file for preselecting training trees for signal and background
        preselectTreeTauIdMVA_configFileNames[discriminator] = {}
        preselectTreeTauIdMVA_outputFileNames[discriminator] = {}
        preselectTreeTauIdMVA_logFileNames[discriminator]    = {}
        merged_preselected_root[discriminator] = {}
        preselected_roots[discriminator] = {}

        preselectTreeTauIdMVA_outputFileNames[discriminator]["signal"] = []
        preselectTreeTauIdMVA_configFileNames[discriminator]["signal"] = []
        preselectTreeTauIdMVA_logFileNames[discriminator]["signal"] = []
        merged_preselected_root[discriminator]["signal"] = os.path.join(outputFilePath, "preselectTreeTauIdMVA_%s_%s.root" % (discriminator, "signal"))
        preselected_roots[discriminator]["signal"] = []
        preselectTreeTauIdMVA_outputFileNames[discriminator]["background"] = []
        preselectTreeTauIdMVA_configFileNames[discriminator]["background"] = []
        preselectTreeTauIdMVA_logFileNames[discriminator]["background"] = []
        merged_preselected_root[discriminator]["background"] = os.path.join(outputFilePath, "preselectTreeTauIdMVA_%s_%s.root" % (discriminator, "background"))
        preselected_roots[discriminator]['background'] = []

        preselHandles = {
            'signal': {
                'samples': signalSamples,
                'eventPruningLevel': 'applyEventPruningSignal',
                'ptDependentPruning': 'applyPtDependentPruningSignal',
            },
            'background': {
                'samples': backgroundSamples,
                'eventPruningLevel': 'applyEventPruningBackground',
                'ptDependentPruning': 'applyPtDependentPruningBackground',
            }
        }

        for sample in preselHandles.keys():
            for proc in preselHandles[sample]['samples']:  # signalSamples:
                outputFileName = os.path.join(outputFilePath, "preselectTreeTauIdMVA_%s_%s_%s.root" % (discriminator, sample, proc))
                preselected_roots[discriminator][sample].append(outputFileName)
                print " preselection outputFileName = '%s'" % outputFileName
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
                eventPruningLevel = mvaDiscriminators[discriminator][preselHandles[sample]['eventPruningLevel']]
                ptDependentPruning = mvaDiscriminators[discriminator][preselHandles[sample]['ptDependentPruning']]
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

                logFileName = cfgFileName_modified.replace("_cfg.py", ".log")
                preselectTreeTauIdMVA_logFileNames[discriminator][sample].append(logFileName)
        #----------------------------------------------------------------------------

        #---------------------------------------------------------------------------- Reweighting
        # CV: build config file for Pt, eta reweighting
        reweightTreeTauIdMVA_configFileNames[discriminator] = {}
        reweightTreeTauIdMVA_outputFileNames[discriminator] = {}
        reweightTreeTauIdMVA_logFileNames[discriminator]    = {}
        for sample in ["signal", "background"]:
            outputFileName = os.path.join(outputFilePath, "reweightTreeTauIdMVA_%s_%s.root" % (discriminator, sample))
            print " reweighted outputFileName = '%s'" % outputFileName
            reweightTreeTauIdMVA_outputFileNames[discriminator][sample] = outputFileName

            cfgFileName_original = configFile_reweightTreeTauIdMVA
            cfgFile_original = open(cfgFileName_original, "r")
            cfg_original = cfgFile_original.read()
            cfgFile_original.close()
            cfg_modified  = cfg_original
            cfg_modified += "\n"
            cfg_modified += "process.fwliteInput.fileNames = cms.vstring()\n"
            cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % merged_preselected_root[discriminator]['signal']
            cfg_modified += "process.fwliteInput.fileNames.append('%s')\n" % merged_preselected_root[discriminator]['background']
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

        #---------------------------------------------------------------------------- Training
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
        cfg_modified += "process.trainTauIdMVA.prepareTreeOptions = cms.string('%s')\n" % prepareTreeOptions
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
    makeROCcurveTauIdMVA_configFileNames = {}  # key = discriminator, "TestTree" or "TrainTree"
    makeROCcurveTauIdMVA_outputFileNames = {}  # key = discriminator, "TestTree" or "TrainTree"
    makeROCcurveTauIdMVA_logFileNames    = {}  # key = discriminator, "TestTree" or "TrainTree"
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
        for tree in ["TestTree", "TrainTree"]:
            if tree in makeROCcurveTauIdMVA_outputFileNames[discriminator].keys():
                hadd_inputFileNames.append(makeROCcurveTauIdMVA_outputFileNames[discriminator][tree])
    hadd_outputFileName = os.path.join(outputFilePath, "makeROCcurveTauIdMVA_all.root")

    print "Info: building config files for displaying results"
    showROCcurvesTauIdMVA_configFileNames = {}  # key = plot
    showROCcurvesTauIdMVA_outputFileNames = {}  # key = plot
    showROCcurvesTauIdMVA_logFileNames    = {}  # key = plot
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
        for sample in ["signal", "background"]:
            # if sample == "signal":
            #     outputFileNames.append(preselectTreeTauIdMVA_outputFileNames[discriminator][sample])
            # else:
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

    # Creating the Makefile
    makeFile.write("all: %s\n" % make_MakeFile_vstring(outputFileNames))
    makeFile.write("\techo 'Finished tau ID MVA training.'\n")
    makeFile.write("\n")
    for discriminator in trainTauIdMVA_outputFileNames.keys():
        # Preselection
        for sample in ["signal", "background"]:
            makeFile.write("# Preselecting %s \n" % (sample))
            hadd_command = "\n\thadd " + merged_preselected_root[discriminator][sample] + " "

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
                        outputFilePath=outputFilePath)

                hadd_command += ' ' + preselected_roots[discriminator][sample][proc_i]

            hadd_command += '\n\n'
            pp.pprint(hadd_command)
            makeFile.write(hadd_command)

            # Reweighting
            makeFile.write("# Run the reweighting\n")
            makeFile.write("%s: %s\n" %
                           (reweightTreeTauIdMVA_outputFileNames[discriminator][sample],
                            make_MakeFile_vstring(
                                preselectTreeTauIdMVA_outputFileNames[discriminator]['signal'] +
                                preselectTreeTauIdMVA_outputFileNames[discriminator]['background'])))
            makeFile.write("\t%s%s %s &> %s\n" %
                           (nice, executable_reweightTreeTauIdMVA,
                            reweightTreeTauIdMVA_configFileNames[discriminator][sample],
                            reweightTreeTauIdMVA_logFileNames[discriminator][sample]))

        # Training
        # - requirements
        makeFile.write("# Run the training\n")
        makeFile.write("%s: %s\n" %
                       (trainTauIdMVA_outputFileNames[discriminator],
                        make_MakeFile_vstring(
                            [reweightTreeTauIdMVA_outputFileNames[discriminator]['signal'],
                             reweightTreeTauIdMVA_outputFileNames[discriminator]['background']])))
        # - cd the src and run training
        makeFile.write("\tcd %s; %s%s %s &> %s\n" %
                       (os.path.join('/'.join(execDir.split('/')[:-3]), 'str'),
                        nice,
                        executable_trainTauIdMVA,
                        trainTauIdMVA_configFileNames[discriminator],
                        trainTauIdMVA_logFileNames[discriminator]))
    makeFile.write("\n")

    for discriminator in makeROCcurveTauIdMVA_outputFileNames.keys():
        for tree in ["TestTree", "TrainTree"]:
            if tree in makeROCcurveTauIdMVA_outputFileNames[discriminator].keys():
                if discriminator in trainTauIdMVA_outputFileNames.keys():
                    makeFile.write("%s: %s %s\n" %
                                   (makeROCcurveTauIdMVA_outputFileNames[discriminator][tree],
                                    trainTauIdMVA_outputFileNames[discriminator],
                                    # executable_makeROCcurveTauIdMVA,
                                    ""))
                else:
                    makeFile.write("%s:\n" % (makeROCcurveTauIdMVA_outputFileNames[discriminator][tree]))
                makeFile.write("\t%s%s %s &> %s\n" %
                               (nice,
                                executable_makeROCcurveTauIdMVA,
                                makeROCcurveTauIdMVA_configFileNames[discriminator][tree],
                                makeROCcurveTauIdMVA_logFileNames[discriminator][tree]))

    makeFile.write("\n")
    makeFile.write("%s: %s\n" % (hadd_outputFileName, make_MakeFile_vstring(hadd_inputFileNames)))
    makeFile.write("\t%s%s %s\n" % (nice, executable_rm, hadd_outputFileName))
    makeFile.write("\t%s%s %s %s\n" % (nice, executable_hadd, hadd_outputFileName, make_MakeFile_vstring(hadd_inputFileNames)))
    makeFile.write("\n")

    # ROC
    for plot in showROCcurvesTauIdMVA_outputFileNames.keys():
        makeFile.write("%s: %s %s\n" % (showROCcurvesTauIdMVA_outputFileNames[plot], hadd_outputFileName, executable_showROCcurvesTauIdMVA))
        makeFile.write("\t%s%s %s &> %s\n" % (nice, executable_showROCcurvesTauIdMVA, showROCcurvesTauIdMVA_configFileNames[plot], showROCcurvesTauIdMVA_logFileNames[plot]))

    makeFile.write("\n")
    makeFile.write(".PHONY: clean\n")
    makeFile.write("clean:\n")
    makeFile.write("\t%s %s\n" % (executable_rm, make_MakeFile_vstring(outputFileNames)))
    makeFile.write("\techo 'Finished deleting old files.'\n")
    makeFile.write("\n")
    makeFile.close()

    print("\n Finished building Makefile. Now execute 'make -f %s'." % makeFileName)
