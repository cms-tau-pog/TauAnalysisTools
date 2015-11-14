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
	reference74X = {
		'folder' : 'antiElectronDiscr74X_onlyZWTTjetsHiggsWZprimeSUSY_FullSkim',
		'color'  : ROOT.kMagenta,
		'text'   : '74X (Complete skim)'
	}

	inputFilePath = '/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining'

	trainingList = []
	trainingList.append(reference53X)
	trainingList.append(reference74X)

	# list of plots to produce
	roc_linear = {
		'file' : 'showROCcurvesAntiElectronDiscrMVA_all_linear.root',
		'name' : 'roc_linear',
		'y_range' : [0.4, 1.],
		'y_log' : False,
		'leg_loc' : [0.2, 0.2, 0.8, 0.35]
	}
	roc_log = {
		'file' : 'showROCcurvesAntiElectronDiscrMVA_all_log.root',
		'name' : 'roc_log',
		'y_range' : [0.001, 1.],
		'y_log' : True,
		'leg_loc' : [0.2, 0.75, 0.8, 0.9]
	}

	plotList = []
	plotList.append(roc_linear)
	plotList.append(roc_log)

	pTbinsList = ['','tauPtLt50_','tauPt50to100_','tauPt100to200_','tauPt200to400_','tauPt400to600_','tauPt600to900_','tauPt900to1200_','tauPtGt1200_']

	for iPlot, plotDict in enumerate(plotList):
		for ptBin in pTbinsList:

			filename = 'showROCcurvesAntiElectronDiscrMVA_all_'+ptBin+('log' if plotDict['y_log'] else 'linear')

			c1 = TCanvas()
			c1.SetTitle(plotDict['name'])

			legend = TLegend(plotDict['leg_loc'][0], plotDict['leg_loc'][1], plotDict['leg_loc'][2], plotDict['leg_loc'][3])
			legend.SetShadowColor(0)
			legend.SetFillColor(0)

			for iTrain, trainDict in enumerate(trainingList):

				file = TFile.Open(os.path.join(inputFilePath, trainDict['folder'], filename+'.root'))
				canvas = file.Get("canvas")
				histo = canvas.GetPrimitive("dummyHistogram")
				graph = canvas.GetPrimitive("mvaAntiElectronDiscr5_TestTree_"+ptBin+"cloned")

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

			c1.SaveAs(os.path.join(inputFilePath, 'plots', plotDict['name']+'_'+(ptBin[:-1] if ptBin != '' else 'all')+'.png'))


if __name__ == "__main__":
	rocPlotMacro()
