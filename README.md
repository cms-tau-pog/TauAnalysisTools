# TauAnalysisTools

## Anti-e discriminator
The following section explains briefly the codes and macros used for the training of the antiElectron MVA discriminator. This includes skimming of the ntuples, preselection, training, evaluation of the cut working points and plotting.

### Skimming
The ntuples for the training are created by the following codes:
- [CMSSW Analyzer](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/plugins/AntiElectronDiscrMVATrainingNtupleProducer.cc) (and the corresponding header file): produces a TTree containing a large number of tau/electron-related variables, used for the subsequent preselection and as input variables for the training.
- [CMSSW python config](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/test/produceAntiElectronDiscrMVATrainingNtuple_cfg.py): here some configuration parameters (e.g., the GlobalTag or the names of the tau/electron input collections) are set. The variable "type" (SignalMC or BackgroundMC) is automatically replaced via hooks during the submission of the skimming jobs on the Grid, as explained later.

For a simple local test skim, insert a valid sample path in *process.source()* and set the desired number of events to skim in *process.maxEvents()*. Then run with:

	cmsRun produceAntiElectronDiscrMVATrainingNtuple_cfg.py

**IMPORTANT**: the *maxEvents* setting is **not** overwritten later, so remember to set it back to "-1" (i.e., skim all the available events) before submitting real skimming jobs on the Grid.

The signal and background samples to be skimmed are defined in the first part of a python script called [submitAntiElectronDiscrMVATrainingNtupleProduction_grid](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/test/submitAntiElectronDiscrMVATrainingNtupleProduction_grid.py). For each sample, it is required to specify a valid DAS path, a name (e.g., ZplusJets_madgraph_signal) and a type (SignalMC or BackgroundMC).
When executed, the script runs on all the defined samples, creates copies of the CMSSW python config, substitutes the "type" variable of the config in the appropriate way, creates a Crab3 submission config and finally submits the jobs on the Grid.
A config file for the submission of jobs using the [Grid-Control](https://ekptrac.physik.uni-karlsruhe.de/trac/grid-control/) tool is also created.

The output path where the jobs are landing is set in *crabConfig.Data.outLFNDirBase* and the SE in *crabConfig.Site.storageSite*.

To skim all the signal and background samples needed for a training, you need first of all to source a valid Crab3 environment, doing for example:

	source /cvmfs/cms.cern.ch/crab3/crab.sh
	voms-proxy-init --voms cms:/cms/dcms --valid 192:00

then, simply run the script with:

	python submitAntiElectronDiscrMVATrainingNtupleProduction_grid.py

**IMPORTANT**: in the current version of the script, jobs will be automatically submitted using Crab3 as soon as the script is executed and without asking for confirmation. To avoid this, search and comment out the following lines:

	p = Process(target=submitWithCrab, args=(crabConfig,))
	p.start()
	p.join()

### Running the training
One single script called [runAntiElectronDiscrMVATraining](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/test/runAntiElectronDiscrMVATraining.py) takes care of the whole training from front to end. A training consists of the following steps, ordered according to their execution:
- [extendTreeAntiElectronDiscrMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/extendTreeAntiElectronDiscrMVA.cc): creates two large ntuples (one for signals and one for backgrounds), merging together the entries of all the samples skimmed in the previous step. Additional branches (e.g., the MVA output of a previous training, if available) are added to the TTree.
- [preselectTreeTauIdMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/preselectTreeTauIdMVA.cc): applies a preselection and separates the events in the training categories. The preselection cuts and the categories are defined in the first part of runAntiElectronDiscrMVATraining.
- [trainTauIdMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/trainTauIdMVA.cc): runs the training and testing of one Boosted Decision Tree (BDT) for each category.
- [computeWPcutsAntiElectronDiscrMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/computeWPcutsAntiElectronDiscrMVA.cc): runs an algorithm to compute the best cut working point on the BDT output (for a given target signal efficiency), for each one of the categories. This recursive cut optimization is done splitting the events in different tau pT-bins. The current pT-binning default is [0 - 60, 60 - 100, 100 - 200, 200 - inf] GeV. 
- [computeBDTGmappedAntiElectronDiscrMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/computeBDTGmappedAntiElectronDiscrMVA.cc)
- [makeROCcurveTauIdMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/makeROCcurveTauIdMVA.cc) and [showROCcurvesTauIdMVA](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/bin/showROCcurvesTauIdMVA.cc): create a set of ROC curves (background rejection vs. signal efficiency and background efficiency vs. signal efficiency) based on the cut points defined in the previous steps and display them as ROOT plots.

When calling:

	python runAntiElectronDiscrMVATraining.py

the script creates a set of config files for each one of the steps above, based on some templates located in *TauAnalysisTools/TauAnalysisTools/test*. The commands and the configs are dumped in a bash file, which can be sourced (at best from a detached screen session) on a local or remote machine:

	source Makefile_runAntiElectronDiscrMVATraining_<version>

The above command start the whole training procedure, from the ntuple creation and preselection to the plotting.
The output of all the codes which are executed is saved in logfiles for debugging and future reference. The preselection and training steps are splitted on different cores, such that the training of the different BDTs is executed in parallel.
Indicatively, a complete training takes approximately 8-9 hours, depending from the number of signal and background samples which are available.

### Additional codes and macros
- [plotAntiElectronDiscrROCs](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/macros/plotAntiElectronDiscrROCs.py): simple pyROOT macro which displays different ROC curves on the same plot. Useful for comparing the performance of different trainings.
- [dumpWPsAntiElectronDiscr](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/macros/dumpWPsAntiElectronDiscr.C): dumps the output of computeWPcutsAntiElectronDiscrMVA (cut working points as a function of the tau pT for each one of the training categories) in the form of TGraphs.

### Saving the training outputs
After the complete training step has successfully run, the structure of the newly created boosted decision trees is saved into .xml files (one file for each BDT/category) which are located in a "weights" folder, inside your training output folder.

The working points for each one of the categories, as a function of the tau pT, can be saved in the form of TGraphs using the [dumpWPsAntiElectronDiscr](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/macros/dumpWPsAntiElectronDiscr.C) macro:

	root dumpWPsAntiElectronDiscr.C

The output is saved into *../data/wpDiscriminationAgainstElectronMVA6.root*. The target signal efficiencies of the working points can be modified acting on the macro code (current values: VLoose 99%, Loose 96%, Medium 91%, Tight 85%, VTight 79%).

The .xml files can be converted into a ROOT file containing GBRForest objects using the [writeGBRForests_antiElectronDiscrMVA_cfg](https://github.com/cms-tau-pog/TauAnalysisTools/blob/master/TauAnalysisTools/test/writeGBRForests_antiElectronDiscrMVA_cfg.py) config file:

	cmsRun writeGBRForests_antiElectronDiscrMVA_cfg.py

The output is saved into *gbrDiscriminationAgainstElectronMVA6.root*, in the current folder (but it can be moved manually to *../data/*). Before running, change all the *inputFileName* in the config to point to the correct location of the .xml files.
