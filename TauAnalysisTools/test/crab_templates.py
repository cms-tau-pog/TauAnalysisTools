from string import Template

crab_template_mc = Template('''
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '$ui_working_dir'
config.General.workArea = '$workarea'
config.General.transferLogs = True

config.section_("User")
config.User.voGroup = 'dcms'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '$pset'

config.section_("Data")
config.Data.inputDataset = '$datasetpath'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = $files_per_job
config.Data.totalUnits = $total_files
config.Data.outLFNDirBase = '$store_output_path'
config.Data.publication = False
config.Data.allowNonValidInputDataset = True

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
''')

crab_template_data = Template('''
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '$ui_working_dir'
config.General.workArea = 'TauIDMVATraining_v1'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '$pset'

config.section_("Data")
config.Data.inputDataset = '$datasetpath'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = $lumis_per_job
config.Data.totalUnits = $total_lumis
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions12/8TeV/Prompt/Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt'
#config.Data.runRange = '193093-193999' # '193093-194075'
config.Data.outLFNDirBase = '$store_output_path'
config.Data.publication = False

config.section_("Site")
config.Site.storageSite = 'T2_DE_DESY'
''')