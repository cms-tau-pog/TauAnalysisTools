import os
import ROOT

from ROOT import TFile, TCanvas, TGraph, TLegend, gROOT, gStyle

def rocPlotMacro():
	
	# load TDR-style plotting macro
	gROOT.LoadMacro("$CMSSW_BASE/src/TauAnalysisTools/TauAnalysisTools/macros/tdrstyle.C")
	ROOT.setTDRStyle()
	gStyle.SetFrameLineWidth(3)
	gStyle.SetLineWidth(3)
	gStyle.SetPadGridX(True)
	gStyle.SetPadGridY(True)
	gStyle.SetPadTopMargin(0.08)
	gStyle.SetPadBottomMargin(0.15)
	gStyle.SetPadLeftMargin(0.18)
	gStyle.SetPadRightMargin(0.05)
	gStyle.SetTitleFontSize(0.055)
	gStyle.SetTitleSize(0.055, "XYZ")
	gStyle.SetTitleXOffset(1.25)
	gStyle.SetTitleYOffset(1.60)
	gStyle.SetLabelSize(0.04, "XYZ")
	gStyle.SetLabelOffset(0.013, "XYZ")

	# list of trainings
	reference53X = {
		'folder' : 'forFabio',
		'color'  : ROOT.kGreen,
		'text'   : '53X'
	}
	oldTraining72X = {
		'folder' : 'oldTraining_fixTauGSF',
		'color'  : ROOT.kRed,
		'text'   : '72X old training'
	}	
	newTraining72X_noTauMVA_MvaInput_lessVars = {
		'folder' : 'fixTauGSF_scenario3_v2_lessVars',
		'color'  : ROOT.kCyan,
		'text'   : '72X new train w/ ele MVA input w/o Tau_HadrMVA'
	}

	inputFilePath = '/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining'

	trainingList = []
	trainingList.append(reference53X)
	trainingList.append(oldTraining72X)
	trainingList.append(newTraining72X_noTauMVA_MvaInput_lessVars)

	# list of plots to produce
	roc_linear = {
		'file' : 'showROCcurvesAntiElectronDiscrMVA_all_linear.root',
		'name' : 'roc_all_linear',
		'y_range' : [0.7, 1.],
		'y_log' : False,
		'leg_loc' : [0.2, 0.2, 0.8, 0.35]
	}
	roc_log = {
		'file' : 'showROCcurvesAntiElectronDiscrMVA_all_log.root',
		'name' : 'roc_all_log',
		'y_range' : [0.001, 1.],
		'y_log' : True,
		'leg_loc' : [0.2, 0.75, 0.8, 0.9]
	}

	plotList = []
	plotList.append(roc_linear)
	plotList.append(roc_log)

	for iPlot, plotDict in enumerate(plotList):

		c1 = TCanvas()
		c1.SetTitle(plotDict['name'])

		legend = TLegend(plotDict['leg_loc'][0], plotDict['leg_loc'][1], plotDict['leg_loc'][2], plotDict['leg_loc'][3])
		legend.SetShadowColor(0)
		legend.SetFillColor(0)

		for iTrain, trainDict in enumerate(trainingList):

			file = TFile.Open(os.path.join(inputFilePath, trainDict['folder'], plotDict['file']))
			canvas = file.Get("canvas")
			histo = canvas.GetPrimitive("dummyHistogram")
			graph = canvas.GetPrimitive("mvaAntiElectronDiscr5_TestTree_cloned")

			legend.AddEntry(graph, trainDict['text'], 'l')
			c1.cd()
			if (iTrain == 0):
				histo.GetYaxis().SetRangeUser(plotDict['y_range'][0], plotDict['y_range'][1])
				histo.GetYaxis().SetTitleOffset(1.6)
				histo.Draw()

			graph.SetMarkerColor(trainDict['color'])
			graph.SetLineColor(trainDict['color'])
			graph.SetLineWidth(2)
			graph.Draw("LP SAME")

		if (plotDict['y_log'] == True):
			c1.SetLogy()

		legend.Draw()

		if 'plots' not in os.listdir(inputFilePath):
			os.mkdir(os.path.join(inputFilePath, 'plots'))

		c1.SaveAs(os.path.join(inputFilePath, 'plots', plotDict['name']+'.png'))


if __name__ == "__main__":
	rocPlotMacro()

