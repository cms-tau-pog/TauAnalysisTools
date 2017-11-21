from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import patDiscriminationByIsolationMVArun2v1raw, patDiscriminationByIsolationMVArun2v1VLoose
import os

class TauIDEmbedder(object):
	"""class to rerun the tau seq and acces trainings from the database"""

	def __init__(self, process, cms, debug = True, 
		tauIdDiscrMVA_trainings_run2_2017 = {
			'tauIdMVAIsoDBoldDMwLT2017' : "tauIdMVAIsoDBoldDMwLT2017",
		},
		tauIdDiscrMVA_WPs_run2_2017 = {
			'tauIdMVAIsoDBoldDMwLT2017' : {
				'Eff95' : "DBoldDMwLTEff95",
				'Eff90' : "DBoldDMwLTEff90",
				'Eff80' : "DBoldDMwLTEff80",
				'Eff70' : "DBoldDMwLTEff70",
				'Eff60' : "DBoldDMwLTEff60",
				'Eff50' : "DBoldDMwLTEff50",
				'Eff40' : "DBoldDMwLTEff40"
			}
		},
		tauIdDiscrMVA_2017_version = "v1"
		):
		super(TauIDEmbedder, self).__init__()
		self.process = process
		self.cms = cms
		self.debug = debug
		self.process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
		self.tauIdDiscrMVA_trainings_run2_2017 = tauIdDiscrMVA_trainings_run2_2017
		self.tauIdDiscrMVA_WPs_run2_2017 = tauIdDiscrMVA_WPs_run2_2017
		self.tauIdDiscrMVA_2017_version = tauIdDiscrMVA_2017_version

	@staticmethod
	def get_cmssw_version(debug = False):
		"""returns 'CMSSW_X_Y_Z'"""
		if debug: print "get_cmssw_version:", os.environ["CMSSW_RELEASE_BASE"].split('/')[-1]
		return os.environ["CMSSW_RELEASE_BASE"].split('/')[-1]

	@classmethod
	def get_cmssw_version_number(klass, debug = False):
		"""returns 'X_Y_Z' (without 'CMSSW_')"""
		if debug: print "get_cmssw_version_number:", map(int, klass.get_cmssw_version().split("CMSSW_")[1].split("_")[0:3])
		return map(int, klass.get_cmssw_version().split("CMSSW_")[1].split("_")[0:3])

	@staticmethod
	def versionToInt(release=9, subversion=4, patch=0, debug = False):
		if debug: print "versionToInt:", release * 10000 + subversion * 100 + patch
		return release * 10000 + subversion * 100 + patch

	@classmethod
	def is_above_cmssw_version(klass, release=9, subversion=4, patch=0, debug = False):
		split_cmssw_version = klass.get_cmssw_version_number()
		if klass.versionToInt(release, subversion, patch) > klass.versionToInt(split_cmssw_version[0], split_cmssw_version[1], split_cmssw_version[2]):
			if debug: print "is_above_cmssw_version:", False
			return False
		else:
			if debug: print "is_above_cmssw_version:", True
			return True

	def loadMVA_WPs_run2_2017(self):
		if self.debug: print "loadMVA_WPs_run2_2017: performed"
		global cms
		for training, gbrForestName in self.tauIdDiscrMVA_trainings_run2_2017.items():

			self.process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
				self.cms.PSet(
					record = self.cms.string('GBRWrapperRcd'),
					tag = self.cms.string("RecoTauTag_%s%s" % (gbrForestName, self.tauIdDiscrMVA_2017_version)),
					label = self.cms.untracked.string("RecoTauTag_%s%s" % (gbrForestName, self.tauIdDiscrMVA_2017_version))
				)
			)

			for WP in self.tauIdDiscrMVA_WPs_run2_2017[training].keys():
				self.process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
					self.cms.PSet(
						record = self.cms.string('PhysicsTGraphPayloadRcd'),
						tag = self.cms.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, self.tauIdDiscrMVA_2017_version, WP)),
						label = self.cms.untracked.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, self.tauIdDiscrMVA_2017_version, WP))
					)
				)

			self.process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
				self.cms.PSet(
					record = self.cms.string('PhysicsTFormulaPayloadRcd'),
					tag = self.cms.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, self.tauIdDiscrMVA_2017_version)),
					label = self.cms.untracked.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, self.tauIdDiscrMVA_2017_version))
				)
			)
	
	def runTauID(self, name='NewTauIDsEmbedded'):
		# update the available in DB samples
		if not self.is_above_cmssw_version(10, 0, 0, self.debug):
			if self.debug: print "runTauID: not is_above_cmssw_version(10, 0, 0)"
			self.loadMVA_WPs_run2_2017()

		# rerun the seq to obtain the 2017 nom training with 0.5 iso cone, old DM, ptph>1, trained on 2017MCv1
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
			PATTauProducer = self.cms.InputTag('slimmedTaus'),
			Prediscriminants = noPrediscriminants,
			loadMVAfromDB = self.cms.bool(True),
			mvaName = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1"),#RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1 writeTauIdDiscrMVAs
			mvaOpt = self.cms.string("DBoldDMwLTwGJ"),
			requireDecayMode = self.cms.bool(True),
			verbosity = self.cms.int32(0)
		)
		#
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
			PATTauProducer = self.cms.InputTag('slimmedTaus'),
			Prediscriminants = noPrediscriminants,
			toMultiplex = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1raw'),
			key = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1raw:category'),#?
			loadMVAfromDB = self.cms.bool(True),
			mvaOutput_normalization = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_mvaOutput_normalization"), #writeTauIdDiscrMVAoutputNormalizations
			mapping = self.cms.VPSet(
				self.cms.PSet(
					category = self.cms.uint32(0),
					cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff90"), #writeTauIdDiscrWPs
					variable = self.cms.string("pt"),
				)
			)
		)
		#
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VVLoose = self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VVLoose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff95")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Loose = self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Loose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff80")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Medium = self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Medium.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff70")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Tight = self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Tight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff60")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VTight = self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff50")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VVTight = self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VVTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff40")


		# 2016 training strategy(v2), trained on 2017MCv2, old DM - currently not implemented in the tau sequence of any release
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2raw = patDiscriminationByIsolationMVArun2v1raw.clone(
		#     PATTauProducer = self.cms.InputTag('slimmedTaus'),
		#     Prediscriminants = noPrediscriminants,
		#     loadMVAfromDB = self.cms.bool(True),
		#     mvaName = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2"),#RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1 writeTauIdDiscrMVAs
		#     mvaOpt = self.cms.string("DBoldDMwLTwGJ"),
		#     requireDecayMode = self.cms.bool(True),
		#     verbosity = self.cms.int32(0)
		# )
		# #
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
		#     PATTauProducer = self.cms.InputTag('slimmedTaus'),
		#     Prediscriminants = noPrediscriminants,
		#     toMultiplex = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2raw'),
		#     key = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2raw:category'),#?
		#     loadMVAfromDB = self.cms.bool(True),
		#     mvaOutput_normalization = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_mvaOutput_normalization"), #writeTauIdDiscrMVAoutputNormalizations
		#     mapping = self.cms.VPSet(
		#         self.cms.PSet(
		#             category = self.cms.uint32(0),
		#             cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff90"), #writeTauIdDiscrWPs
		#             variable = self.cms.string("pt"),
		#         )
		#     )
		# )
		# #
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VVLoose = self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose.clone()
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VVLoose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff95")
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Loose = self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose.clone()
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Loose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff80")
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Medium = self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose.clone()
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Medium.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff70")
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Tight = self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose.clone()
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Tight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff60")
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VTight = self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose.clone()
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff50")
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VVTight = self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose.clone()
		# self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VVTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v2_WPEff40")

		# 2016 training strategy(v1), trained on 2016MC, old DM
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
			PATTauProducer = self.cms.InputTag('slimmedTaus'),
			Prediscriminants = noPrediscriminants,
			loadMVAfromDB = self.cms.bool(True),
			mvaName = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1"),
			mvaOpt = self.cms.string("DBoldDMwLT"),
			requireDecayMode = self.cms.bool(True),
			verbosity = self.cms.int32(0)
		)
		#
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
				PATTauProducer = self.cms.InputTag('slimmedTaus'),
				Prediscriminants = noPrediscriminants,
				toMultiplex = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1raw'),
				key = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1raw:category'),
				loadMVAfromDB = self.cms.bool(True),
				mvaOutput_normalization = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_mvaOutput_normalization"),
				mapping = self.cms.VPSet(
					self.cms.PSet(
						category = self.cms.uint32(0),
						cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff90"),
						variable = self.cms.string("pt"),
					)
				)
			)
		#
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Loose = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Loose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff80")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Medium = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Medium.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff70")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Tight = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Tight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff60")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VTight = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff50")
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VVTight = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VVTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2016v1_WPEff40")

		# 2016 training strategy(v1), trained on 2016MC, new DM
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1raw = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1raw.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1raw.mvaName = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1")
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1raw.mvaOpt = self.cms.string("DBnewDMwLT")
		#
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose = self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.toMultiplex = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1raw')
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.key = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1raw:category')
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.mvaOutput_normalization = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_mvaOutput_normalization")
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff90")
		#
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Loose = self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Loose.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff80")
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Medium = self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Medium.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff70")
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Tight = self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Tight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff60")
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VTight = self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff50")
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VVTight = self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose.clone()
		self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VVTight.mapping[0].cut = self.cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2016v1_WPEff40")


		self.process.rerunMvaIsolationSequence = self.cms.Sequence(
			# 2017 training strategy (v1), trained on 2017MCv1, old DM
				self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1raw
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VVLoose
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Loose
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Medium
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1Tight
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VTight
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2017v1VVTight
			# 2016 training strategy(v2) - essentially the same as 2017 training strategy (v1), trained on 2016MC, old DM - currently not implemented in the tau sequence of any release
			#     *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2raw
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VLoose
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VVLoose
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Loose
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Medium
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2Tight
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VTight
			# *self.process.rerunDiscriminationByIsolationOldDMMVArun2v2VVTight
			# 2016 training strategy(v1), trained on 2016MC, old DM
			   *self.process.rerunDiscriminationByIsolationOldDMMVArun2v1raw
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VLoose
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Loose
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Medium
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2v1Tight
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VTight
			*self.process.rerunDiscriminationByIsolationOldDMMVArun2v1VVTight
			# 2016 training strategy(v1), trained on 2016MC, new DM
			   *self.process.rerunDiscriminationByIsolationNewDMMVArun2v1raw
			*self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VLoose
			*self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Loose
			*self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Medium
			*self.process.rerunDiscriminationByIsolationNewDMMVArun2v1Tight
			*self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VTight
			*self.process.rerunDiscriminationByIsolationNewDMMVArun2v1VVTight
		)

		embedID = self.cms.EDProducer("PATTauIDEmbedder",
			src = self.cms.InputTag('slimmedTaus'),
			tauIDSources = self.cms.PSet(
					byIsolationMVArun2017v1DBoldDMwLTraw2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1raw'),
				byVVLooseIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1VVLoose'),
				byVLooseIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1VLoose'),
				byLooseIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1Loose'),
				byMediumIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1Medium'),
				byTightIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1Tight'),
				byVTightIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1VTight'),
				byVVTightIsolationMVArun2017v1DBoldDMwLT2017 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2017v1VVTight'),
				# currently not implemented in the tau sequence of any release
				#     byIsolationMVArun2v2DBoldDMwLTraw2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2raw'),
				# byVVLooseIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2VVLoose'),
				# byVLooseIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2VLoose'),
				# byLooseIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2Loose'),
				# byMediumIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2Medium'),
				# byTightIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2Tight'),
				# byVTightIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2VTight'),
				# byVVTightIsolationMVArun2v2DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v2VVTight'),
				  byIsolationMVArun2v1DBoldDMwLTraw2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1raw'),
				byVLooseIsolationMVArun2v1DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1VLoose'),
				byLooseIsolationMVArun2v1DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1Loose'),
				byMediumIsolationMVArun2v1DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1Medium'),
				byTightIsolationMVArun2v1DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1Tight'),
				byVTightIsolationMVArun2v1DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1VTight'),
				byVVTightIsolationMVArun2v1DBoldDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationOldDMMVArun2v1VVTight'),
				  byIsolationMVArun2v1DBnewDMwLTraw2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1raw'),
				byVLooseIsolationMVArun2v1DBnewDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1VLoose'),
				byLooseIsolationMVArun2v1DBnewDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1Loose'),
				byMediumIsolationMVArun2v1DBnewDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1Medium'),
				byTightIsolationMVArun2v1DBnewDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1Tight'),
				byVTightIsolationMVArun2v1DBnewDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1VTight'),
				byVVTightIsolationMVArun2v1DBnewDMwLT2016 = self.cms.InputTag('rerunDiscriminationByIsolationNewDMMVArun2v1VVTight')
			),
		)
		self.process.NewTauIDsEmbedded = embedID
		#setattr(process, "NewTauIDsEmbedded", embedID)
