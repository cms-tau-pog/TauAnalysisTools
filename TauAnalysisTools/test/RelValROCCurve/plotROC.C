#include <TFile.h>
#include <TTree.h>
#include <TTreeFormula.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TMath.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TCut.h>
#include <vector>

std::string sample = "ZTT";
bool debug = true;
bool standartConeSize = false;
//NO std::string sample = "H";
//NO std::string sample = "DY";
//NO std::string sample = "Zp2";

void dout() 
{
    if (debug) std::cout << std::endl; 
}
template <typename Head, typename... Tail>
void dout(Head H, Tail... T) 
{
  if (debug) std::cout << H << ' ';
  dout(T...);
}

void LegendSettings(TLegend *leg, int ncolumn)
{
	leg->SetNColumns(ncolumn);
	leg->SetBorderSize(0);
	leg->SetFillColor(10);
	leg->SetLineColor(0);
	leg->SetFillStyle(0);
	leg->SetTextSize(0.035);
	leg->SetTextFont(42);
}

double getEff(TTree* tree, TCut denominator, TCut numerator, TString variable)
{
	// dout("\t\tgetEff", "\n\t\t\tnumerator", numerator, "\n\t\t\tdenominator", denominator, "\n\t\t\tvariable", variable);
	TH1F* h_denom = new TH1F("denom", "", 10, -5., 5.);
	TH1F* h_num = new TH1F("num", "", 10, -5., 5.);

	TString var_denom(variable + ">>denom");
	tree->Draw(var_denom.Data(), denominator, "SAME");
	double denom_value = h_denom->Integral(); // h_denom->Print();
	delete h_denom;

	TString var_num(variable + ">>num");
	tree->Draw(var_num.Data(), numerator, "SAME");
	double num_value = h_num->Integral();
	delete h_num;

	// dout("\n\t\t\tdenom_value ",  denom_value, " num_value ", num_value, "\n\t\tgetEff end");
	if (denom_value != 0)
		return num_value / denom_value;
	return 0;
}

TGraph * getROC(std::vector<TString>discriminators, float xmin = -1, float xmax = -1)
{
	std::cout << "getROC" << std::endl;
	dout("discriminators len", discriminators.size());
	gROOT->SetBatch(true);
	std::vector<double> eff_value, fr_value;
	TString fileTauname = "";

	// Access the files
		// TString pathToFile = "/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_0_pre3/src/";// /nfs/dust/cms/user/anehrkor/TauIDMVATraining2016/TauPaper/
		TString pathToFile = "/afs/cern.ch/user/o/ohlushch/workspace/CMSSW_9_4_0_pre3/src/TauAnalysisTools/TauAnalysisTools/";
		TString treeName = "tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD";
		
		if (sample == "DY") fileTauname = "";
		else if (sample == "QCD") fileTauname = "RelValQCD_FlatPt_15_3000HS_13.root";
		else if (sample == "ZTT") fileTauname = "RelValZTT_13.root";
		else if (sample == "H") fileTauname = ""; //ggHiggs125toTauTau.root
		else if (sample == "Zp2") fileTauname = ""; //Zprime2000toTauTau.root

		TFile *file_tau = new TFile(pathToFile + fileTauname);
		TTree *tree_tau = (TTree*)file_tau->Get(treeName.Data());

		TFile *file_jet = new TFile(pathToFile + "RelValQCD_FlatPt_15_3000HS_13.root");
		TTree *tree_jet = (TTree*)file_jet->Get(treeName.Data());
	
	// Cuts For the efficiency
		dout("\ttree_tau entries", tree_tau->GetEntries());
		TString variable_tau("genTauEta");
		TCut denom_tau("genTauPt > 20. && TMath::Abs(genTauEta) < 2.3 && (genTauDecayMode == 0 || genTauDecayMode == 1 || genTauDecayMode == 2 || genTauDecayMode == 10) && genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 18.");//  TCut denom_tau("genTauPt > 20. && TMath::Abs(genTauEta) < 2.3 && (genTauDecayMode ==  0 || genTauDecayMode ==  1 || genTauDecayMode ==  2 || genTauDecayMode == 10) && (genTauNDaPhotons == 0 || genTauNDaPhotons == 2 || genTauNDaPhotons == 4 || genTauNDaPhotons == 6 || genTauNDaPhotons == 8) && genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 18.");
		TCut num_tau = denom_tau && TCut("recTauPt > 20. && TMath::Abs(recTauEta) < 2.3 ");
	
	// Cuts For the fakerate
		dout("\ttree_jet entries", tree_jet->GetEntries());
		TString variable_jet("recJetEta");
		TCut denom_jet("TMath::Abs(recTauEta) < 2.3 && recTauPt > 18.");//denom_jet = TCut("recJetPt > 20. && TMath::Abs(recJetEta) < 2.3 && recTauPt > 18.");
		if (sample == "Zp2")
			denom_jet = denom_jet && TCut("recTauPt < 1000."); 
		else
			denom_jet = denom_jet &&  TCut("recTauPt < 100."); 
		TCut num_jet = denom_jet && TCut("recTauPt > 20. && TMath::Abs(recTauEta) < 2.3");//TCut denom_jet("recJetPt > 20. && recJetPt < 1000. && TMath::Abs(recJetEta) < 2.3 && recJetMatch > 0.5 && recJetDeltaR < 0.3 && recTauPt > 18.");


	if (discriminators.size() > 1) // not raw isolation but WP
	{
		dout("WP handle");
		for (size_t i = 0; i < discriminators.size(); i++)
		{
			TCut num_tau_d = num_tau && TCut(discriminators[i] + " > 0.5");
			TCut num_jet_d = num_jet && TCut(discriminators[i] + " > 0.5");
			// dout("discriminators[i]:", discriminators[i]);
			// cout << "denom tau " << denom_tau << std::endl << "num tau " << num_tau << std::endl << "denom jet "<< denom_jet << std::endl << "num jet " << num_jet << std::endl;
			// TH1F* h_denom = new TH1F("denom", "", 1000, -5000., 5000.);
			// tree_jet->Draw("recJetEta>>denom");
			// h_denom->Print();
			// exit(1);
			double eff_i = getEff(tree_tau, denom_tau, num_tau_d, variable_tau);
			dout("\t\teff:", eff_i);
			double fr_i = getEff(tree_jet, denom_jet, num_jet_d, variable_jet);
			// dout("\t\tfr:", fr_i);
			
			eff_value.push_back(eff_i);
			fr_value.push_back(fr_i);
		}
	}
	else // For the drawing of the line from the raw-branch
	{
		dout("raw isolation handle");
		/*
			//first find the maximum point
			double max_eff = 1.0;
			double cut = 10.;
			while(max_eff > xmax)
			{
				TCut num_tau_d = num_tau && TCut("photonPtSumOutsideSignalCone < 0.1*recTauPt") && TCut(Form(discriminators[0]+" < %f", cut));
				std::cout<<" num_tau_d "<<num_tau_d<<std::endl;
				max_eff = getEff(tree_tau, denom_tau, num_tau_d, variable_tau);
				std::cout<<" max_eff "<<max_eff<<std::endl;
				cut -= 0.2;
			}
			double max_cut = cut;
			//find the minimum point
			double min_eff = 0.;
			cut = 0.;
			while(min_eff < xmin)
			{
				TCut num_tau_d = num_tau && TCut("photonPtSumOutsideSignalCone < 0.1*recTauPt") && TCut(Form(discriminators[0]+" < %f", cut));
				std::cout<<" num_tau_d "<<num_tau_d<<std::endl;
				min_eff = getEff(tree_tau, denom_tau, num_tau_d, variable_tau);
				std::cout<<" min_eff "<<min_eff<<std::endl;
				cut += 0.1;
			}
			double min_cut = cut - 0.5;
			if (min_cut < 0) min_cut = 0.;

			double itr = (max_cut - min_cut)/100;

			cut = max_cut;
		*/

		double cut = 50.;
		while (cut > 0.0)
		{
			
			TCut num_tau_d = num_tau && TCut("photonPtSumOutsideSignalCone_ptGt1.0 < 0.1*recTauPt") && TCut(Form(discriminators[0] + " < %f", cut));
			TCut num_jet_d = num_jet && TCut("photonPtSumOutsideSignalCone_ptGt1.0 < 0.1*recTauPt") && TCut(Form(discriminators[0] + " < %f", cut));
			double eff_i = getEff(tree_tau, denom_tau, num_tau_d, variable_tau);
			double fr_i = getEff(tree_jet, denom_jet, num_jet_d, variable_jet);

			eff_value.push_back(eff_i);
			fr_value.push_back(fr_i);
			
			if (cut > 1.0) cut = cut - cut * 0.1;
			else cut = cut - 0.1;

			dout("\t\teff vs fr:", eff_i, fr_i);
		}
	}

	std::cout << "Num. of points " << eff_value.size() << std::endl;
	double efficiency[eff_value.size()];
	double fake_rate[eff_value.size()];
	for(int i = 0; i < eff_value.size(); i++)
	{
		if (discriminators.size() > 1)
			dout(eff_value[i], "vs",fr_value[i], discriminators[i]);
		else
			dout(eff_value[i], "vs",fr_value[i]);

		efficiency[i] = eff_value[i];
		fake_rate[i] = fr_value[i];
	}

	TGraph *g = new TGraph(eff_value.size(), efficiency, fake_rate);
	std::cout << "getROC end" << std::endl;
	return g;
}

void ConstructRocCurves(std::vector<TString> mva, TGraph** gr_mva, TString mvaname, std::vector<TString> mva_raw = std::vector<TString>(), TGraph** gr_mva_raw = NULL)
{
	dout("\n\n+++++++++++++++++++++", mvaname, "+++++++++++++++++++++");
	*gr_mva = (TGraph*)getROC(mva);//(TGraph*)getROC(mva);

	double x1(0.), y1(0.), x2(0.), y2(0.);
	(*gr_mva)->GetPoint(0, x1, y1);
	(*gr_mva)->GetPoint(mva.size() - 1, x2, y2);
	float xmax(x1), xmin(x2);

	if (gr_mva_raw != NULL)
	{
		dout("\n\n+++++++++++++++++++++", mvaname, "_raw mva_raw, xmin, xmax:,", xmin, ",", xmax, "+++++++++++++++++++++");
		*gr_mva_raw = (TGraph*)getROC(mva_raw, xmin, xmax);//(TGraph*)getROC(mva_raw, xmin, xmax);
		std::cout << " xmin " << xmin << " xmax " << xmax << std::endl;	
	}
}

void plotROC()
{
	// Init
		std::vector<TString> cutbased_db, cutbased_db_raw,
			mva_db,
			mva_db_2017_explicit, mva_db_2017_explicit_raw,
			mva_db_2017v2_explicit, mva_db_2017v2_explicit_raw,
			mva_db_2016, mva_db_2016_raw,
			mva_db_2016newDM, mva_db_2016newDM_raw,
			mva_db_2015dR0p3_explicit, mva_db_2015dR0p3_explicit_raw,
			mva_db_2017v2dR0p3_explicit, mva_db_2017v2dR0p3_explicit_raw;
		double x1(0.), y1(0.), x2(0.), y2(0.);
		float xmax = x1, xmin = x2;
		int colors[] = {6, 2, 1, 10};//, 6};
		int markerStyles[] = {23, 21, 22, 25};//, 22};
		TGraph *gr_mva_2017v2dR0p3_explicit, *gr_mva_db_2017v2dR0p3_explicit_raw,
			*gr_mva_2015dR0p3_explicit, *gr_mva_db_2015dR0p3_explicit_raw,
			*gr_mva_2016, *gr_mva_db_2016_raw,
			*gr_mva,
			*gr_mva_2017_explicit, *gr_mva_db_2017_explicit_raw,
			*gr_mva_2017v2_explicit, *gr_mva_db_2017v2_explicit_raw;

	// List the isolation variables
		cutbased_db.clear();
		cutbased_db.push_back("byLooseCombinedIsolationDeltaBetaCorr3Hits");
		cutbased_db.push_back("byMediumCombinedIsolationDeltaBetaCorr3Hits");
		cutbased_db.push_back("byTightCombinedIsolationDeltaBetaCorr3Hits");
		//
		cutbased_db_raw.clear();
		cutbased_db_raw.push_back("byCombinedIsolationDeltaBetaCorrRaw3Hits");

		if (standartConeSize)
		{
			mva_db.clear();
			// mva_db.push_back("byVVLooseIsolationMVArun2v1DBoldDMwLT"); why not there?
			mva_db.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
			mva_db.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
			mva_db.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
			mva_db.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
			mva_db.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
			mva_db.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");

			// 2016v1
			mva_db_2016.clear();
			mva_db_2016.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT2016");
			mva_db_2016.push_back("byLooseIsolationMVArun2v1DBoldDMwLT2016");
			mva_db_2016.push_back("byMediumIsolationMVArun2v1DBoldDMwLT2016");
			mva_db_2016.push_back("byTightIsolationMVArun2v1DBoldDMwLT2016");
			mva_db_2016.push_back("byVTightIsolationMVArun2v1DBoldDMwLT2016");
			mva_db_2016.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT2016");
			//
			mva_db_2016_raw.clear();
			mva_db_2016_raw.push_back("byIsolationMVArun2v1DBoldDMwLTraw2016");

			// 2016 new DM
			mva_db_2016newDM.clear();
			mva_db_2016newDM.push_back("byVLooseIsolationMVArun2v1DBnewDMwLT2016");
			mva_db_2016newDM.push_back("byLooseIsolationMVArun2v1DBnewDMwLT2016");
			mva_db_2016newDM.push_back("byMediumIsolationMVArun2v1DBnewDMwLT2016");
			mva_db_2016newDM.push_back("byTightIsolationMVArun2v1DBnewDMwLT2016");
			mva_db_2016newDM.push_back("byVTightIsolationMVArun2v1DBnewDMwLT2016");
			mva_db_2016newDM.push_back("byVVTightIsolationMVArun2v1DBnewDMwLT2016");
			//
			mva_db_2016newDM_raw.clear();
			mva_db_2016newDM_raw.push_back("byIsolationMVArun2v1DBnewDMwLTraw2016");
				
			// 2017 v1
			mva_db_2017_explicit.clear();
			mva_db_2017_explicit.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
			mva_db_2017_explicit.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
			mva_db_2017_explicit.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
			mva_db_2017_explicit.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
			mva_db_2017_explicit.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
			mva_db_2017_explicit.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
			mva_db_2017_explicit.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
			//
			mva_db_2017_explicit_raw.clear();
			mva_db_2017_explicit_raw.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");

			// 2017 v2
			mva_db_2017v2_explicit.clear();
			mva_db_2017v2_explicit.push_back("byVVLooseIsolationMVArun2017v2DBoldDMwLT2017");
			mva_db_2017v2_explicit.push_back("byVLooseIsolationMVArun2017v2DBoldDMwLT2017");
			mva_db_2017v2_explicit.push_back("byLooseIsolationMVArun2017v2DBoldDMwLT2017");
			mva_db_2017v2_explicit.push_back("byMediumIsolationMVArun2017v2DBoldDMwLT2017");
			mva_db_2017v2_explicit.push_back("byTightIsolationMVArun2017v2DBoldDMwLT2017");
			mva_db_2017v2_explicit.push_back("byVTightIsolationMVArun2017v2DBoldDMwLT2017");
			mva_db_2017v2_explicit.push_back("byVVTightIsolationMVArun2017v2DBoldDMwLT2017");
			//
			mva_db_2017v2_explicit_raw.clear();
			mva_db_2017v2_explicit_raw.push_back("byIsolationMVArun2017v2DBoldDMwLTraw2017");
		}
		else
		{
			// 2017 dr=0.3
			mva_db_2017v2dR0p3_explicit.clear();
			mva_db_2017v2dR0p3_explicit.push_back("byVVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			mva_db_2017v2dR0p3_explicit.push_back("byVLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			mva_db_2017v2dR0p3_explicit.push_back("byLooseIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			mva_db_2017v2dR0p3_explicit.push_back("byMediumIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			mva_db_2017v2dR0p3_explicit.push_back("byTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			mva_db_2017v2dR0p3_explicit.push_back("byVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			mva_db_2017v2dR0p3_explicit.push_back("byVVTightIsolationMVArun2017v2DBoldDMdR0p3wLT2017");
			//
			mva_db_2017v2dR0p3_explicit_raw.clear();
			mva_db_2017v2dR0p3_explicit_raw.push_back("byIsolationMVArun2017v2DBoldDMdR0p3wLTraw2017");

			// 2015 dR=0.3
			mva_db_2015dR0p3_explicit.clear();
			mva_db_2015dR0p3_explicit.push_back("byVLooseIsolationMVArun2v1DBdR03oldDMwLT");
			mva_db_2015dR0p3_explicit.push_back("byLooseIsolationMVArun2v1DBdR03oldDMwLT");
			mva_db_2015dR0p3_explicit.push_back("byMediumIsolationMVArun2v1DBdR03oldDMwLT");
			mva_db_2015dR0p3_explicit.push_back("byTightIsolationMVArun2v1DBdR03oldDMwLT");
			mva_db_2015dR0p3_explicit.push_back("byVTightIsolationMVArun2v1DBdR03oldDMwLT");
			mva_db_2015dR0p3_explicit.push_back("byVVTightIsolationMVArun2v1DBdR03oldDMwLT");
			//
			mva_db_2015dR0p3_explicit_raw.clear();
			mva_db_2015dR0p3_explicit_raw.push_back("byIsolationMVArun2v1DBdR03oldDMwLTraw");
		}

	// Construct ROC curves from root-files
		dout("\n\n+++++++++++++++++++++cutbased_db+++++++++++++++++++++");
		TGraph *gr_cut = (TGraph*)getROC(cutbased_db);
		dout("\n\n+++++++++++++++++++++cutbased_db_raw, xmin, xmax:,", xmin, ",", xmax, "+++++++++++++++++++++");
		TGraph *gr_cut_raw = (TGraph*)getROC(cutbased_db_raw, xmin, xmax);
		std::cout << " xmin " << xmin << " xmax " << xmax << std::endl;

		if (standartConeSize)
		{
			dout("\n\n+++++++++++++++++++++mva_db+++++++++++++++++++++");
			ConstructRocCurves(mva_db, &gr_mva, "mva_db_2016");
			gr_mva = (TGraph*)getROC(mva_db);
			x1 = 0., y1 = 0., x2 = 0., y2 = 0.;
			gr_mva->GetPoint(0, x1, y1);
			gr_mva->GetPoint(mva_db.size() - 1, x2, y2);
			xmax = x1, xmin = x2;

			ConstructRocCurves(mva_db_2016, &gr_mva_2016, "mva_db_2016", mva_db_2016_raw, &gr_mva_db_2016_raw);
			ConstructRocCurves(mva_db_2017_explicit, &gr_mva_2017_explicit, "mva_db_2017_explicit", mva_db_2017_explicit_raw, &gr_mva_db_2017_explicit_raw);
			ConstructRocCurves(mva_db_2017v2_explicit, &gr_mva_2017v2_explicit, "mva_db_2017v2_explicit", mva_db_2017v2_explicit_raw, &gr_mva_db_2017v2_explicit_raw);
		}
		else
		{
			ConstructRocCurves(mva_db_2017v2dR0p3_explicit, &gr_mva_2017v2dR0p3_explicit, "mva_db_2017v2dR0p3_explicit", mva_db_2017v2dR0p3_explicit_raw, &gr_mva_db_2017v2dR0p3_explicit_raw);
			ConstructRocCurves(mva_db_2015dR0p3_explicit, &gr_mva_2015dR0p3_explicit, "mva_db_2015dR0p3_explicit", mva_db_2015dR0p3_explicit_raw, &gr_mva_db_2015dR0p3_explicit_raw);
		}
		
	// Plot styling & legend
		TCanvas* canvas = new TCanvas();
		canvas->SetLogy();
		canvas->cd();
		//canvas->SetFillColor(10);
		//canvas->SetBorderSize(2);
		//canvas->SetLeftMargin(0.12);
		//canvas->SetBottomMargin(0.12);
		//canvas->SetRightMargin(0.05);

		double legendX0 = 0.20;
		double legendY0 = 0.7;
		TLegend* legend = new TLegend(legendX0, legendY0, legendX0 + 0.30, legendY0 + 0.15, "", "brNDC"); 
		legend->SetBorderSize(0);
		legend->SetFillColor(0);
		//legend->SetTextSize(1.5);

		//double yAxisOffset = 1.1;
		//double xAxisOffset = 1.1;
		double yMin = 0.0005;
		double yMax = 0.05;

		TH1F* histogram_base = new TH1F("histogram_base", "", 60, 0.25, 1.0);//
		histogram_base->SetTitle("");
		histogram_base->SetStats(false);
		histogram_base->SetMinimum(yMin);
		histogram_base->SetMaximum(yMax);
		histogram_base->GetXaxis()->SetRangeUser(0.36, 0.78 );// 0.36, 0.78 //(xmin-0.02, xmax+0.02);
		histogram_base->Draw("hist");

		const std::string xAxisTitle("#tau_{h} identification efficiency");
		TAxis* xAxis_top = histogram_base->GetXaxis();
		xAxis_top->SetTitle(xAxisTitle.data());
		//xAxis_top->SetTitleOffset(xAxisOffset);
		//xAxis_top->SetTitleSize(0.05);
		const std::string yAxisTitle("Misidentification rate");
		TAxis* yAxis_top = histogram_base->GetYaxis();
		yAxis_top->SetTitle(yAxisTitle.data());
		//yAxis_top->SetTitleOffset(yAxisOffset);
		//yAxis_top->SetTitleSize(0.05);


		gr_cut->SetLineColor(6); // PINK
		gr_cut->SetLineWidth(2);
		gr_cut->SetMarkerColor(6);
		gr_cut->SetMarkerStyle(markerStyles[0]);
		gr_cut->SetMarkerSize(2.0);
		gr_cut_raw->SetLineColor(6);
		gr_cut_raw->SetLineWidth(2);

		if (standartConeSize)
		{
			gr_mva->SetLineColor(2); // Red
			gr_mva->SetLineWidth(2);
			gr_mva->SetMarkerColor(2);
			gr_mva->SetMarkerStyle(markerStyles[1]);
			gr_mva->SetMarkerSize(2.0);

			gr_mva_2017_explicit->SetLineColor(3); // Green
			gr_mva_2017_explicit->SetLineWidth(2);
			gr_mva_2017_explicit->SetMarkerColor(3);
			gr_mva_2017_explicit->SetMarkerStyle(markerStyles[3]);
			gr_mva_2017_explicit->SetMarkerSize(2.0);
			gr_mva_db_2017_explicit_raw->SetLineColor(3);
			gr_mva_db_2017_explicit_raw->SetLineWidth(4);

			gr_mva_2017v2_explicit->SetLineColor(4); // Blue
			gr_mva_2017v2_explicit->SetLineWidth(2);
			gr_mva_2017v2_explicit->SetMarkerColor(4);
			gr_mva_2017v2_explicit->SetMarkerStyle(markerStyles[3]);
			gr_mva_2017v2_explicit->SetMarkerSize(2.0);
			gr_mva_db_2017v2_explicit_raw->SetLineColor(4);
			gr_mva_db_2017v2_explicit_raw->SetLineWidth(4);

			gr_mva_2016->SetLineColor(1); // Black
			gr_mva_2016->SetLineWidth(2);
			gr_mva_2016->SetMarkerColor(1);
			gr_mva_2016->SetMarkerStyle(markerStyles[3]);
			gr_mva_2016->SetMarkerSize(2.0);
			gr_mva_db_2016_raw->SetLineColor(2);
			gr_mva_db_2016_raw->SetLineWidth(4);
		}
		else
		{
			gr_mva_2015dR0p3_explicit->SetLineColor(1); // Black
			gr_mva_2015dR0p3_explicit->SetLineWidth(2);
			gr_mva_2015dR0p3_explicit->SetMarkerColor(1);
			gr_mva_2015dR0p3_explicit->SetMarkerStyle(markerStyles[3]);
			gr_mva_2015dR0p3_explicit->SetMarkerSize(2.0);
			gr_mva_db_2015dR0p3_explicit_raw->SetLineColor(2);
			gr_mva_db_2015dR0p3_explicit_raw->SetLineWidth(4);

			gr_mva_2017v2dR0p3_explicit->SetLineColor(4); // Blue
			gr_mva_2017v2dR0p3_explicit->SetLineWidth(2);
			gr_mva_2017v2dR0p3_explicit->SetMarkerColor(4);
			gr_mva_2017v2dR0p3_explicit->SetMarkerStyle(markerStyles[3]);
			gr_mva_2017v2dR0p3_explicit->SetMarkerSize(2.0);
			gr_mva_db_2017v2dR0p3_explicit_raw->SetLineColor(4);
			gr_mva_db_2017v2dR0p3_explicit_raw->SetLineWidth(4);
		}

	// Draw
		gr_cut_raw->Draw("Lsame");
		gr_cut->Draw("Psame");	legend->AddEntry(gr_cut, "cut-based", "pl");
		if (standartConeSize)
		{
			gr_mva->Draw("PLsame");	legend->AddEntry(gr_mva, "MVA-based, in-file", "pl");
			gr_mva_2016->Draw("PLsame"); legend->AddEntry(gr_mva_2016, "MVA-based, re-run, 2016", "pl"); // re-run
			gr_mva_2017_explicit->Draw("PLsame"); legend->AddEntry(gr_mva_2017_explicit, "MVA-based, re-run, 2017v1", "pl");
			gr_mva_2017v2_explicit->Draw("PLsame"); legend->AddEntry(gr_mva_2017v2_explicit, "MVA-based, re-run, 2017v2", "pl");
			// gr_mva_db_2017_explicit_raw->Draw("PLsame"); legend->AddEntry(gr_mva_db_2017_explicit_raw, "MVA-based, re-run, 2017v1, raw", "pl");
			// gr_mva_db_2016_raw->Draw("PLsame"); legend->AddEntry(gr_mva_db_2016_raw, "MVA-based, re-run 2016, raw", "pl");
		}
		else
		{
			gr_mva_2015dR0p3_explicit->Draw("PLsame"); legend->AddEntry(gr_mva_2015dR0p3_explicit, "MVA-based, re-run, 2015, dR=0.3", "pl");
			gr_mva_db_2015dR0p3_explicit_raw->Draw("PLsame"); legend->AddEntry(gr_mva_db_2015dR0p3_explicit_raw, "MVA-based, re-run, 2015, dR=0.3, raw", "pl");
			gr_mva_2017v2dR0p3_explicit->Draw("PLsame"); legend->AddEntry(gr_mva_2017v2dR0p3_explicit, "MVA-based, re-run, 2017v2, dR=0.3", "pl");
		}
		
		legend->Draw();

	// More style & text
		//TPaveText* label_cms = new TPaveText(0.14, 0.905, 0.88, 0.965, "brNDC");
		TPaveText* label_cms = new TPaveText(0.14, 0.96, 0.55, 0.995, "brNDC");
		label_cms->AddText("#bf{CMS} #it{RelVal MCv2} 2017");
		label_cms->SetFillColor(10);
		label_cms->SetBorderSize(0);
		label_cms->SetTextColor(1);
		label_cms->SetTextAlign(12);
		label_cms->SetTextSize(0.045);
		label_cms->SetTextFont(42);
		label_cms->Draw();

		TLegend *leg4 = new TLegend(0.58,0.96,0.9,0.99);
		LegendSettings(leg4, 1);
		
		leg4->AddEntry(histogram_base, "13 TeV, 27 pileup at 25ns","");
		leg4->SetTextSize(0.03);
		leg4->Draw();
		/*
			TPaveText *pt1 = new TPaveText(0.5,0.3,0.9,0.35,"brNDC");
			pt1->SetBorderSize(0);
			pt1->SetFillColor(10);
			pt1->SetTextAlign(12);
			pt1->SetTextSize(0.038);
			TText *AText1 = pt1->AddText("p_{T}^{#tau} > 20 GeV, |#eta_{#tau}| < 2.3");
			pt1->Draw();

			TPaveText *pt2 = new TPaveText(0.2,0.15,0.9,0.22,"brNDC");
			pt2->SetBorderSize(0);
			pt2->SetFillColor(10);
			pt2->SetTextAlign(12);
			pt2->SetTextSize(0.03);
			if (sample == "DY")
				TText *AText2 = pt2->AddText("Efficiency : Z #rightarrow #tau#tau MC");
			else if (sample == "H")
				TText *AText2 = pt2->AddText("Efficiency : H #rightarrow #tau#tau MC");
			else if (sample == "Zp1")
				TText *AText2 = pt2->AddText("Efficiency : Z' (1 TeV) #rightarrow #tau#tau MC"); 
			else if (sample == "Zp2")
				TText *AText2 = pt2->AddText("Efficiency : Z' (2 TeV) #rightarrow #tau#tau MC");
			else if (sample == "Zp4.5")
				TText *AText2 = pt2->AddText("Efficiency : Z' (4.5 TeV) #rightarrow #tau#tau MC");
			TText *AText3 = pt2->AddText("Fake rate : QCD multi-jet MC (15 < #hat{p}_{T} < 3000 GeV flat)");
			pt2->Draw();
		*/

		TLegend *leg2 = new TLegend(0.45,0.3,0.9,0.4);
		LegendSettings(leg2, 1);
		leg2->AddEntry(histogram_base, "#bf{p_{T}^{#tau} > 20 GeV, |#eta_{#tau}| < 2.3}","");
		leg2->Draw();

		TLegend *leg3 = new TLegend(0.0,0.2,0.9,0.3);
		LegendSettings(leg3, 1);
		leg3->SetTextSize(0.03);
		if (sample == "DY")          leg3->AddEntry(histogram_base, "Efficiency : Z #rightarrow #tau#tau MC","");
		else if (sample == "H")      leg3->AddEntry(histogram_base, "Efficiency : H #rightarrow #tau#tau MC","");
		else if (sample == "Zp1")    leg3->AddEntry(histogram_base, "Efficiency : Z' (1TeV) #rightarrow #tau#tau MC","");
		else if (sample == "Zp2")    leg3->AddEntry(histogram_base, "Efficiency : Z' (2TeV) #rightarrow #tau#tau MC","");
		else if (sample == "Zp4p5")  leg3->AddEntry(histogram_base, "Efficiency : Z' (4.5TeV) #rightarrow #tau#tau MC","");
		leg3->AddEntry(histogram_base, "Fake rate : QCD multi-jet MC (15 < #hat{p_{T}} < 3000 GeV flat)","");
		// leg3->AddEntry(histogram_base, "Fake rate : QCD multi-jet MC (20 < #hat{p_{T}} < 1000 GeV)","");
		leg3->Draw();

	// Save picture
		canvas->cd();
		canvas->Update();
		TString st = "plots/roc_cut_vs_run2mva_";
		if (!standartConeSize) st +=  "_dR=0.3";
		// Save the ROC-curves
		canvas->Print(st + sample + "_RelValQCD_FlatPt_15_3000HS_13_pt18.png");
		canvas->Print(st + sample + "_RelValQCD_FlatPt_15_3000HS_13_pt18.pdf");
		canvas->Print(st + sample + "_RelValQCD_FlatPt_15_3000HS_13_pt18.C");
}