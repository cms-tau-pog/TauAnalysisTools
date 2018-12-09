import json

class SamplesHandles(object):
    """docstring for SamplesHandles"""
    def __init__(self, era="2016"):
        super(SamplesHandles, self).__init__()
        self.era = era
        self.samples = {}
        self.samples_sg = {}
        self.samples_bg = {}
        self.setSamples()

    def setSamples(self):
        if self.era == "2016":
            self.samples = SamplesHandles.getSamples16()
            self.samples_sg = SamplesHandles.getSamplesSg16()
            self.samples_bg = SamplesHandles.getSamplesBg16()
        elif self.era == "2017":
            self.samples = SamplesHandles.getSamples17()
            self.samples_sg = SamplesHandles.getSamplesSg17()
            self.samples_bg = SamplesHandles.getSamplesBg17()
        elif self.era == "2016dR03":
            self.samples = SamplesHandles.getSamplesdR03_16()
            self.samples_sg = {}
            self.samples_bg = {}
        elif self.era == "2017PU":
            self.samples = SamplesHandles.getSamplesPU17()
            self.samples_sg = {} # this study has been stopped
            self.samples_bg = {}
        elif self.era == "2017MCv2":
            self.samples = SamplesHandles.getSamples17MCv2()
            self.samples_sg = SamplesHandles.getSamplesSg17MCv2()
            self.samples_bg = SamplesHandles.getSamplesBg17MCv2()
        elif self.era == "2017MCv2dR0p3":
            self.samples = SamplesHandles.getSamples17MCv2dR0p3()
            self.samples_sg = SamplesHandles.getSamplesSg17MCv2dR0p3()
            self.samples_bg = SamplesHandles.getSamplesBg17MCv2dR0p3()
        elif self.era == "2017MCv2RelVal":
            self.samples = SamplesHandles.getSamples17MCv2RelVal()
            self.samples_sg = SamplesHandles.getSamplesSg17MCv2RelVal()
            self.samples_bg = SamplesHandles.getSamplesBg17MCv2RelVal()
        else:
            self.samples = {}
            self.samples_sg = {}
            self.samples_bg = {}

    def updateSamplesJson(self):
        with open('samples.json', 'wb') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def getSamplesdR03_16():
        pass

    @staticmethod
    def getSamplesSg16():
        samples = {
            'ZplusJets_mcatnlo' : {
                'datasetpath'                        : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_HCALDebug_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }
        }

        smHiggsMassPoints2 = [ 120, 130 ]
        for massPoint in smHiggsMassPoints2:
            tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
            samples[tthSampleName] = {
                'datasetpath'                            : '/ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
                'files_per_job'                          : 1,
                'total_files'                            : -1,
                'type'                                   : 'SignalMC'
            }

        tthSampleName = "tthHiggs125toTauTau"
        samples[tthSampleName] = {
            'datasetpath'                            : '/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext4-v1/MINIAODSIM',
            'files_per_job'                          : 1,
            'total_files'                            : -1,
            'type'                                   : 'SignalMC'
        }

        ggSampleName = "ggHiggs125toTauTau"
        samples[ggSampleName] = {
            'datasetpath'                        : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'SignalMC'
        }

        ggSampleName = "ggHiggs130toTauTau"
        samples[ggSampleName] = {
            'datasetpath'                        : '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'SignalMC'
        }

        vbfSampleName = "vbfHiggs125toTauTau"
        samples[vbfSampleName] = {
            'datasetpath'                        : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'SignalMC'
        }

        # currently 29 mass points available
        mssmHiggsMassPoints1 = [ 80, 90, 100, 110, 120, 130, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
        for massPoint in mssmHiggsMassPoints1:
            ggSampleName = "ggA%1.0ftoTauTau" % massPoint
            samples[ggSampleName] = {
                'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        # currently 31 mass points available
        mssmHiggsMassPoints2 = [ 80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
        for massPoint in mssmHiggsMassPoints2:
            bbSampleName = "bbA%1.0ftoTauTau" % massPoint
            samples[bbSampleName] = {
                'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        # v1 of the mass point 300 is invalid
        bbSampleName = "bbA300toTauTau"
        samples[bbSampleName] = {
            'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-300_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'SignalMC'
        }

        # currently 11 mass points available
        ZprimeMassPoints = [ 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000 ]
        for massPoint in ZprimeMassPoints:
            sampleName = "Zprime%1.0ftoTauTau" % massPoint
            samples[sampleName] = {
                'datasetpath'                        : '/ZprimeToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        # currently 27 mass points available
        WprimeMassPoints = [ 400, 600, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800 ]
        for massPoint in WprimeMassPoints:
            sampleName = "Wprime%1.0ftoTauNu" % massPoint
            samples[sampleName] = {
                'datasetpath'                        : '/WprimeToTauNu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }


        return samples

    @staticmethod
    def getSamplesBg16():
        return {
            'TT_powheg': {
                'datasetpath'                        : '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'PPmuXptGt20Mu15' : {
                'datasetpath'                        : '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt30to50' : {
                'datasetpath'                        : '/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt50to80' : {
                'datasetpath'                        : '/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt80to120' : {
                'datasetpath'                        : '/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt120to170' : {
                'datasetpath'                        : '/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt170to300' : {
                'datasetpath'                        : '/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt300to470' : {
                'datasetpath'                        : '/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt470to600' : {
                'datasetpath'                        : '/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt600to800' : {
                'datasetpath'                        : '/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPt800to1000' : {
                'datasetpath'                        : '/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDmuEnrichedPtGt1000' : {
                'datasetpath'                        : '/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'WplusJets_mcatnlo' : {
                'datasetpath'                        : '/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsFlatPt15to7000' : {
                'datasetpath'                        : '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt30to50' : {
                'datasetpath'                        : '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt50to80' : {
                'datasetpath'                        : '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt80to120' : {
                'datasetpath'                        : '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt120to170' : {
                'datasetpath'                        : '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt170to300' : {
                'datasetpath'                        : '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt300to470' : {
                'datasetpath'                        : '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt470to600' : {
                'datasetpath'                        : '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt600to800' : {
                'datasetpath'                        : '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt800to1000' : {
                'datasetpath'                        : '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt1000to1400' : {
                'datasetpath'                        : '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt1400to1800' : {
                'datasetpath'                        : '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt1800to2400' : {
                'datasetpath'                        : '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt2400to3200' : {
                'datasetpath'                        : '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPtGt3200' : {
                'datasetpath'                        : '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPt20to30' : {
                'datasetpath'                        : '/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPt30to50' : {
                'datasetpath'                        : '/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPt50to80' : {
                'datasetpath'                        : '/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPt80to120' : {
                'datasetpath'                        : '/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPt120to170' : {
                'datasetpath'                        : '/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPt170to300' : {
                'datasetpath'                        : '/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDEmEnrichedPtGt300' : {
                'datasetpath'                        : '/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
        }

    @staticmethod
    def getSamples16():
        s = SamplesHandles.getSamplesSg16()
        s.update(SamplesHandles.getSamplesBg16())
        return s


    @staticmethod
    def getSamplesSg17():
        samples = {
        'ZplusJets_madgraph' : {
            'datasetpath'                        : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v2/MINIAODSIM',#same /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'SignalMC'
        }
        }

        #smHiggsMassPoints = [ 120, 125, 130 ]
        #for massPoint in smHiggsMassPoints:
        #    #ggSampleName = "ggHiggs%1.0ftoTauTau" % massPoint
        #    #samples[ggSampleName] = {
        #    #    'datasetpath'                        : '/GluGluHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
        #    #    'files_per_job'                      : 1,
        #    #    'total_files'                        : -1,
        #    #    'type'                               : 'SignalMC'
        #    #}
        #    #vbfSampleName = "vbfHiggs%1.0ftoTauTau" % massPoint
        #    #samples[vbfSampleName] = {
        #    #    'datasetpath'                        : '/VBFHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM' % massPoint,
        #    #    'files_per_job'                      : 1,
        #    #    'total_files'                        : -1,
        #    #    'type'                               : 'SignalMC'
        #    #}
        #    wPlusHSampleName = "WplusHHiggs%1.0ftoTauTau" % massPoint
        #    samples[wPlusHSampleName] = {
        #        'datasetpath'                        : '/WplusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        #        'files_per_job'                      : 1,
        #        'total_files'                        : -1,
        #        'type'                               : 'SignalMC'
        #    }
        #    wMinusHSampleName = "WminusHHiggs%1.0ftoTauTau" % massPoint
        #    samples[wMinusHSampleName] = {
        #        'datasetpath'                        : '/WminusHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        #        'files_per_job'                      : 1,
        #        'total_files'                        : -1,
        #        'type'                               : 'SignalMC'
        #    }
        #    zHSampleName = "ZHHiggs%1.0ftoTauTau" % massPoint
        #    samples[zHSampleName] = {
        #        'datasetpath'                        : '/ZHToTauTau_M%1.0f_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        #        'files_per_job'                      : 1,
        #        'total_files'                        : -1,
        #        'type'                               : 'SignalMC'
        #    }
        #smHiggsMassPoints2 = [ 120, 130 ]
        #for massPoint in smHiggsMassPoints2:
        #   tthSampleName = "tthHiggs%1.0ftoTauTau" % massPoint
        #   samples[tthSampleName] = {
        #       'datasetpath'                            : '/ttHJetToTT_M%1.0f_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        #       'files_per_job'                          : 1,
        #       'total_files'                            : -1,
        #       'type'                                   : 'SignalMC'
        #   }
        #tthSampleName = "tthHiggs125toTauTau"
        #samples[tthSampleName] = {
        #    'datasetpath'                            : '/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext4-v1/MINIAODSIM',
        #    'files_per_job'                          : 1,
        #    'total_files'                            : -1,
        #    'type'                                   : 'SignalMC'
        #}
        #ggSampleName = "ggHiggs130toTauTau"
        #samples[ggSampleName] = {
        #    'datasetpath'                        : '/GluGluHToTauTau_M130_13TeV_powheg_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM',
        #    'files_per_job'                      : 1,
        #    'total_files'                        : -1,
        #    'type'                               : 'SignalMC'
        #}

        ggSampleName = "ggHiggs125toTauTau"
        samples[ggSampleName] = {
           'datasetpath'                        : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
           'files_per_job'                      : 1,
           'total_files'                        : -1,
           'type'                               : 'SignalMC'
        }

        vbfSampleName = "vbfHiggs125toTauTau"
        samples[vbfSampleName] = {
           'datasetpath'                        : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
           'files_per_job'                      : 1,
           'total_files'                        : -1,
           'type'                               : 'SignalMC'
        }

        # currently 23 mass points available
        mssmHiggsMassPoints1 = [ 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
        for massPoint in mssmHiggsMassPoints1:
            ggSampleName = "ggA%1.0ftoTauTau" % massPoint
            samples[ggSampleName] = {
                'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        # currently 23 mass points available
        mssmHiggsMassPoints3 = [ 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, 2900, 3200 ]
        for massPoint in mssmHiggsMassPoints3:
            bbSampleName = "bbA%1.0ftoTauTau" % massPoint
            samples[bbSampleName] = {
                'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        # currently 9 mass points available
        #epsent ZprimeMassPoints = [ 750, 1000, 1250, 1750, 2000, 2500, 3000, 3500, 4000 ]
        # for massPoint in ZprimeMassPoints:
        #     sampleName = "Zprime%1.0ftoTauTau" % massPoint
        #     samples[sampleName] = {
        #         'datasetpath'                        : '/ZprimeToTauTau_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        #         'files_per_job'                      : 1,
        #         'total_files'                        : -1,
        #         'type'                               : 'SignalMC'
        #     }

        ## currently 27 mass points available
        #WprimeMassPoints = [ 400, 600, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800 ]
        #for massPoint in WprimeMassPoints:
        #    sampleName = "Wprime%1.0ftoTauNu" % massPoint
        #    samples[sampleName] = {
        #        'datasetpath'                        : '/WprimeToTauNu_M-%1.0f_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM' % massPoint,
        #        'files_per_job'                      : 1,
        #        'total_files'                        : -1,
        #        'type'                               : 'SignalMC'
        #    }
        return samples

    @staticmethod
    def getSamplesBg17():
        return {
            'TT_powheg': {
                'datasetpath'                        : '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            # was excluded because of too many TT bar events(~30%) in the signal after preselection
            # 'TTJets': {
            #     'datasetpath'                        : '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
            #     'files_per_job'                      : 1,
            #     'total_files'                        : -1,
            #     'type'                               : 'BackgroundMC'
            # },
           # 'PPmuXptGt20Mu15' : {
           #     'datasetpath'                        : '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-FlatPU0to70_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
           #     'files_per_job'                      : 1,
           #     'total_files'                        : -1,
           #     'type'                               : 'BackgroundMC'
           # },
           'QCDmuEnrichedPt15to20' : {
               'datasetpath'                        : '/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt20to30' : {
               'datasetpath'                        : '/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt30to50' : {
               'datasetpath'                        : '/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt50to80' : {
               'datasetpath'                        : '/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt80to120' : {
               'datasetpath'                        : '/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt120to170' : {
               'datasetpath'                        : '/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt170to300' : {
               'datasetpath'                        : '/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt300to470' : {
               'datasetpath'                        : '/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt470to600' : {
               'datasetpath'                        : '/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt600to800' : {
               'datasetpath'                        : '/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDmuEnrichedPt800to1000' : {
               'datasetpath'                        : '/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           #? 'QCDmuEnrichedPtGt1000' : {
           #     'datasetpath'                        : '/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v3/MINIAODSIM',
           #     'files_per_job'                      : 1,
           #     'total_files'                        : -1,
           #     'type'                               : 'BackgroundMC'
           # },

            'WplusJets_madgraph' : {
                'datasetpath'                        : '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'# /WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_SUS01_92X_upgrade2017_realistic_v10-v1/MINIAODSIM
            },
            #?    'QCDjetsFlatPt15to7000' : {
            #        'datasetpath'                        : '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM',
            #        'files_per_job'                      : 1,
            #        'total_files'                        : -1,
            #        'type'                               : 'BackgroundMC'
            #    },
            'QCDjetsPt30to50' : {
                'datasetpath'                        : '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v4/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            # 'QCDjetsPt50to80' : {
            #     'datasetpath'                        : '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16MiniAOD-PhaseIFall16PUFlat20to50_PhaseIFall16_81X_upgrade2017_realistic_v26-v1/MINIAODSIM',
            #     'files_per_job'                      : 1,
            #     'total_files'                        : -1,
            #     'type'                               : 'BackgroundMC'
            # },
            'QCDjetsPt80to120' : {
                'datasetpath'                        : '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt120to170' : {
                'datasetpath'                        : '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v4/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt170to300' : {
                'datasetpath'                        : '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v4/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt300to470' : {
                'datasetpath'                        : '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v4/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt470to600' : {
                'datasetpath'                        : '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v4/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt600to800' : {
                'datasetpath'                        : '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v5/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt800to1000' : {
                'datasetpath'                        : '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v5/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt1000to1400' : {
                'datasetpath'                        : '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v5/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPt1400to1800' : {
                'datasetpath'                        : '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v5/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
           'QCDjetsPt1800to2400' : {
               'datasetpath'                        : '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v5/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
            'QCDjetsPt2400to3200' : {
                'datasetpath'                        : '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v4/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'QCDjetsPtGt3200' : {
                'datasetpath'                        : '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v5/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
           'QCDEmEnrichedPt15to20' : {
               'datasetpath'                        : '/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPt20to30' : {
               'datasetpath'                        : '/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPt30to50' : {
               'datasetpath'                        : '/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPt50to80' : {
               'datasetpath'                        : '/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPt80to120' : {
               'datasetpath'                        : '/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPt120to170' : {
               'datasetpath'                        : '/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v3/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPt170to300' : {
               'datasetpath'                        : '/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           },
           'QCDEmEnrichedPtGt300' : {
               'datasetpath'                        : '/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
               'files_per_job'                      : 1,
               'total_files'                        : -1,
               'type'                               : 'BackgroundMC'
           }
        }

    @staticmethod
    def getSamples17():
        s = SamplesHandles.getSamplesSg17()
        s.update(SamplesHandles.getSamplesBg17())
        return s


    @staticmethod
    def getSamplesBg17MCv2():
        samples = {
            'TTJets_SingleLeptFromT' : {
                'datasetpath'                        : '/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },

            'TTTo2L2Nu' : {
                'datasetpath'                        : '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },

            'TTToHadronic' : {
                'datasetpath'                        : '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            }
        }

        QCD_Pt_ranges = ["1000to1400", "1400to1800", "15to30", "170to300", "1800to2400", "2400to3200", "300to470", "30to50", "3200toInf", "470to600", "50to80", "600to800", "80to120"]
        #missing:
        for massrange in QCD_Pt_ranges:
            sampleName = "QCDjetsPt" + massrange
            samples[sampleName] = {
                'datasetpath'                        : '/QCD_Pt_'+ massrange + '_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            }

        samples["QCDjetsPt2400to3200"] = {
            'datasetpath'                        : '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["QCDjetsPt2400to3200v1"] = {
            'datasetpath'                        : '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["QCDjetsPt800to1000"] = {
            'datasetpath'                        : '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["WplusJets_mcatnlo"] = {
            'datasetpath'                        : '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["Wplus1Jets_mcatnlo"] = {
            'datasetpath'                        : '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["Wplus2Jets_mcatnlo"] = {
            'datasetpath'                        : '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v3/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["Wplus3Jets_mcatnlo"] = {
            'datasetpath'                        : '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v3/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }

        samples["Wplus4Jets_mcatnlo"] = {
            'datasetpath'                        : '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
            'files_per_job'                      : 1,
            'total_files'                        : -1,
            'type'                               : 'BackgroundMC'
        }
        # I IGNORE FOR NOW /QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM
        return samples

    @staticmethod
    def getSamplesSg17MCv2():
        samples = {
            'ZplusJets_madgraph' : {
                'datasetpath'                        : '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM',#! LO
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'

            },

            'ZplusJets_madgraph_ext1' : {
                'datasetpath'                        : '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/MINIAODSIM',#! LO
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'

            },

            'tthHiggs125toTauTau' : {#in production
                'datasetpath'                        : '/ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'

            },
            # 'tthHiggs125toInclusiveNonbb' : {#in production
            #   'datasetpath'                        : '/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
            #   'files_per_job'                      : 1,
            #   'total_files'                        : -1,
            #   'type'                               : 'SignalMC'

            # },
            'vbfHiggs125toTauTau' : {#in production
                'datasetpath'                        : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'

            },
            'ggHiggs125toTauTau' : {#in production
                'datasetpath'                        : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'

            }
        }

        # currently 23 mass points available
        mssmHiggsMassPoints1 = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 600, 700, 800, 900, 1200, 1500, 1600, 1800, 2000, 2300, 2600, 2900, 3200]
        # new compared to v1: [80, 90, 100, 110, 120, 130, 1500]
        # missing compared to v1: [500, 1000, 1400]
        for massPoint in mssmHiggsMassPoints1:
            ggSampleName = "ggA%1.0ftoTauTau" % massPoint
            samples[ggSampleName] = {
                'datasetpath'                        : '/SUSYGluGluToHToTauTau_M-%1.0f_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        # currently 23 mass points available
        mssmHiggsMassPoints3 = [80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 600, 700, 800, 900, 1200, 1400, 1500, 1600, 1800, 2000, 2300, 2900, 3200]
        # missing: [500, 1000, 2600]
        # new: [80, 90, 100, 110, 120, 130, 1500]
        for massPoint in mssmHiggsMassPoints3:
            bbSampleName = "bbA%1.0ftoTauTau" % massPoint
            samples[bbSampleName] = {
                'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-%1.0f_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        samples["bbA2600toTauTau"] = {
                'datasetpath'                        : '/SUSYGluGluToBBHToTauTau_M-2600_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }


        ZprimeMassPoints = [1000, 1500, 2000, 2500, 3000, 3500, 4000]
        #missing: [ 500, 750, 1250, 1750]
        for massPoint in ZprimeMassPoints:
            sampleName = "Zprime%1.0ftoTauTau" % massPoint
            samples[sampleName] = {
                'datasetpath'                        : '/ZprimeToTauTau_M-%1.0f_TuneCP5_13TeV-pythia8-tauola/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM' % massPoint,
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'
            }

        return samples

    @staticmethod
    def getSamples17MCv2():
        s = SamplesHandles.getSamplesSg17MCv2()
        s.update(SamplesHandles.getSamplesBg17MCv2())
        return s


    @staticmethod
    def getSamplesSg17MCv2dR0p3():
        samples = {
            'tthHiggs125toTauTau' : {#in production
                'datasetpath'                        : '/ttHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'SignalMC'

            }
        }
        return samples

    @staticmethod
    def getSamplesBg17MCv2dR0p3():
        '''
        We don't use other Bg because we want to learn to descriminate against the bg events in very dense invironment.
        In other Bgs it's not the case.
        Fully leptonic TT events with jet->tau fakes are actually a relevant background in the ttH analysis and
        the generator level matching that is applied in the training should take care of splitting the events
        into genuine hadronic taus ("signal") and jet->tau fakes ("background").
        '''
        samples = {
            'TTJets_SingleLeptFromT' : {
                'datasetpath'                        : '/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },

            'TTTo2L2Nu' : {
                'datasetpath'                        : '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },

            'TTToHadronic' : {
                'datasetpath'                        : '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            }
        }

        return samples

    @staticmethod
    def getSamples17MCv2dR0p3():
        s = SamplesHandles.getSamplesSg17MCv2dR0p3()
        s.update(SamplesHandles.getSamplesBg17MCv2dR0p3())
        return s


    @staticmethod
    def getSamplesBg17MCv2RelVal():
        return {
            'RelValTTbar_13': {
                'datasetpath'                        : '/RelValTTbar_13/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'RelValQCD_FlatPt_15_3000HS_13': {
                'datasetpath'                        : '/RelValQCD_FlatPt_15_3000HS_13/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'RelValTTbarLepton_13': {
                'datasetpath'                        : '/RelValTTbarLepton_13/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            }
        }

    @staticmethod
    def getSamplesSg17MCv2RelVal():
        return {
            'RelValZpTT_1500_13': {
                'datasetpath'                        : '/RelValZpTT_1500_13/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'RelValZTT_13': {
                'datasetpath'                        : '/RelValZTT_13/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'RelValHiggs200ChargedTaus_13': {
                'datasetpath'                        : '/RelValHiggs200ChargedTaus_13/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            },
            'RelValTenTau_15_500': {
                'datasetpath'                        : '/RelValTenTau_15_500/CMSSW_9_4_0_pre3-PU25ns_94X_mc2017_realistic_v4-v1/MINIAODSIM',
                'files_per_job'                      : 1,
                'total_files'                        : -1,
                'type'                               : 'BackgroundMC'
            }
        }

    @staticmethod
    def getSamples17MCv2RelVal():
        s = SamplesHandles.getSamplesSg17MCv2RelVal()
        s.update(SamplesHandles.getSamplesBg17MCv2RelVal())
        return s


    @staticmethod
    def getSamplesPU17(key="all"):
        samplesPU = {
          "noPU": {
            'RelValZTT_14TeV_noPU': {
                            'datasetpath'                        : '/RelValZTT_14TeV/CMSSW_9_3_0_pre4-93X_upgrade2023_realistic_v0_2023D17noPU-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'SignalMC'
                        },
            'RelValQCD_Pt-15To7000_Flat_14TeV_noPU': {
                            'datasetpath'                        : '/RelValQCD_Pt-15To7000_Flat_14TeV/CMSSW_9_3_0_pre4-93X_upgrade2023_realistic_v0_2023D17noPU-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        },
            'RelValQCD_Pt-20toInf_MuEnrichedPt15_14TeV_noPU': {
                            'datasetpath'                        : '/RelValQCD_Pt-20toInf_MuEnrichedPt15_14TeV/CMSSW_9_3_0_pre4-93X_upgrade2023_realistic_v0_2023D17noPU-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        },
            'RelValTTbar_14TeV_noPU': {
                            'datasetpath'                        : '/RelValTTbar_14TeV/CMSSW_9_3_0_pre4-93X_upgrade2023_realistic_v0_2023D17noPU-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        }
          },
          "PU140": {
            'RelValZTT_14TeV_PU140': {
                            'datasetpath'                        : '/RelValZTT_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU140-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'SignalMC'
                        },
            'RelValQCD_Pt-15To7000_Flat_14TeV_PU140': {
                            'datasetpath'                        : '/RelValQCD_Pt-15To7000_Flat_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU140-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        },
            'RelValQCD_Pt-20toInf_MuEnrichedPt15_14TeV_PU140': {
                            'datasetpath'                        : '/RelValQCD_Pt-20toInf_MuEnrichedPt15_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU140-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        },
            'RelValTTbar_14TeV_PU140': {
                            'datasetpath'                        : '/RelValTTbar_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU140-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        }
          },
          "PU200": {
            'RelValZTT_14TeV_PU200': {
                            'datasetpath'                        : '/RelValZTT_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU200-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'SignalMC'
                        },
            'RelValQCD_Pt-15To7000_Flat_14TeV_PU200': {
                            'datasetpath'                        : '/RelValQCD_Pt-15To7000_Flat_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU200-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        },
            'RelValQCD_Pt-20toInf_MuEnrichedPt15_14TeV_PU200': {
                            'datasetpath'                        : '/RelValQCD_Pt-20toInf_MuEnrichedPt15_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU200-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        },
            'RelValTTbar_14TeV_PU200': {
                            'datasetpath'                        : '/RelValTTbar_14TeV/CMSSW_9_3_0_pre4-PU25ns_93X_upgrade2023_realistic_v0_D17PU200-v1/MINIAODSIM',
                            'files_per_job'                      : 1,
                            'total_files'                        : -1,
                            'type'                               : 'BackgroundMC'
                        }
            }
        }
        if key == "all":
            z = samplesPU["noPU"]
            z.update(samplesPU["PU140"])
            z.update(samplesPU["PU200"])
            return z
        elif key in samplesPU.keys(): return samplesPU[key]
        else: assert  "no such PU key: " + key

    def getDatabeseNames(self):
        datasetnames = []
        for sample in self.samples.values():
            datasetnames.append(sample['datasetpath'].split('/')[1])
        datasetnames.sort()
        return datasetnames

