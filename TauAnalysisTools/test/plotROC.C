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
	dout("\t\tgetEff");
	dout("\t\t\tnumerator", numerator);
	dout("\t\t\tdenominator", denominator);
	dout("\t\t\tvariable", variable);
	TH1F* h_denom = new TH1F("denom", "", 10, -5., 5.);
	TH1F* h_num = new TH1F("num", "", 10, -5., 5.);

	TString var_denom(variable + ">>denom");
	tree->Draw(var_denom.Data(), denominator);
	// h_denom->Print();
	double denom_value = h_denom->Integral();

	TString var_num(variable + ">>num");
	tree->Draw(var_num.Data(), numerator);
	double num_value = h_num->Integral();

	dout("\n\t\t\tdenom_value ",  denom_value, " num_value ", num_value);
	dout("\t\tgetEff end");
	
	delete h_num, h_denom;
	if (denom_value != 0)
		return num_value / denom_value;
	else return 0;
}

TGraph * getROC(std::vector<TString>discriminators, float xmin = -1, float xmax = -1)
{
	std::cout << "getROC" << std::endl;
	dout("discriminators len", discriminators.size());
	gROOT->SetBatch(true);

	TString pathToFile = "/afs/desy.de/user/g/glusheno/RWTH/MVAtraining/CMSSW_9_4_0_pre3/src/";// /nfs/dust/cms/user/anehrkor/TauIDMVATraining2016/TauPaper/
	TString treeName = "tauIdMVATrainingNtupleProducerMiniAOD/tauIdMVATrainingNtupleMiniAOD";

	TString filename = "";
	if (sample == "DY") filename = "";
	else if (sample == "QCD") filename = "RelValQCD_FlatPt_15_3000HS_13_OLD.root";
	else if (sample == "ZTT") filename = "RelValZTT_13_OLD_WORKING.root";
	else if (sample == "H") filename = ""; //ggHiggs125toTauTau.root
	else if (sample == "Zp2") filename = ""; //Zprime2000toTauTau.root
	TFile *file_tau = new TFile(pathToFile + filename);
	TTree *tree_tau = (TTree*)file_tau->Get(treeName.Data());
	TFile *file_jet = new TFile(pathToFile + "RelValQCD_FlatPt_15_3000HS_13_OLD.root"); //QCDjetsFlatPt15to7000
	TTree *tree_jet = (TTree*)file_jet->Get(treeName.Data());
	dout("\ttree_tau entries", tree_tau->GetEntries());
	dout("\ttree_jet entries", tree_jet->GetEntries());

	//int size = discriminators.size();
	//if (discriminators.size() <= 1)size = 100;
	//double efficiency[size];
	//double fake_rate[size];

	TString variable_tau("genTauEta");
	TString variable_jet("recJetEta");

	//  TCut denom_tau("genTauPt > 20. && TMath::Abs(genTauEta) < 2.3 && (genTauDecayMode ==  0 || genTauDecayMode ==  1 || genTauDecayMode ==  2 || genTauDecayMode == 10) && (genTauNDaPhotons == 0 || genTauNDaPhotons == 2 || genTauNDaPhotons == 4 || genTauNDaPhotons == 6 || genTauNDaPhotons == 8) && genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 18.");
	// TCut denom_tau("genTauPt > 20. && TMath::Abs(genTauEta) < 2.3 && (genTauDecayMode ==  0 || genTauDecayMode ==  1 || genTauDecayMode ==  2 || genTauDecayMode == 10) && genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 18.");
	TCut denom_tau("genTauPt > 20. &&  TMath::Abs(genTauEta) < 2.3 &&  (genTauDecayMode ==  0 || genTauDecayMode ==  1 || genTauDecayMode ==  2 || genTauDecayMode == 10) &&  genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 18."
		);
	/*
	"genTauPt > 20. && \
		TMath::Abs(genTauEta) < 2.3 && \
		(genTauDecayMode ==  0 || genTauDecayMode ==  1 || genTauDecayMode ==  2 || genTauDecayMode == 10) && \
		genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 18."
	*/
	TCut num_tau = denom_tau && TCut("genTauMatch > 0.5 && genTauDeltaR < 0.3 && recTauPt > 20. && TMath::Abs(recTauEta) < 2.3 ");
	
	TCut denom_jet;
	if (sample == "Zp2") denom_jet = TCut("recTauPt < 1000. && TMath::Abs(recTauEta) < 2.3 && recTauPt > 18."); //denom_jet = TCut("recJetPt > 20. && recJetPt < 1000. && TMath::Abs(recJetEta) < 2.3 && recTauPt > 18.");
	else denom_jet = TCut("recTauPt < 100. && TMath::Abs(recTauEta) < 2.3 && recTauPt > 18."); //denom_jet = TCut("recJetPt > 20. && recJetPt < 100. && TMath::Abs(recJetEta) < 2.3 && recTauPt > 18.");
	TCut num_jet = denom_jet && TCut("recTauPt > 20. && TMath::Abs(recTauEta) < 2.3");//TCut denom_jet("recJetPt > 20. && recJetPt < 1000. && TMath::Abs(recJetEta) < 2.3 && recJetMatch > 0.5 && recJetDeltaR < 0.3 && recTauPt > 18.");


	std::vector<double>eff_value; eff_value.clear();
	std::vector<double>fr_value; fr_value.clear();

	if (discriminators.size() > 1)
	{
		for (size_t i = 0; i < discriminators.size(); i++)
		{
			dout("discriminators[i]:", discriminators[i]);
			TCut num_tau_d = num_tau && TCut(discriminators[i] + " > 0.5");
			TCut num_jet_d = num_jet && TCut(discriminators[i] + " > 0.5");
			//cout << "denom tau " << denom_tau << std::endl << "num tau " << num_tau << std::endl << "denom jet "<< denom_jet << std::endl << "num jet " << num_jet << std::endl;
			// TH1F* h_denom = new TH1F("denom", "", 1000, -5000., 5000.);
			// tree_tau->Draw("genTauEta>>denom", denom_tau);
			// h_denom->Print();

			double eff_i = getEff(tree_tau, denom_tau, num_tau_d, variable_tau);
			double fr_i  = getEff(tree_jet, denom_jet, num_jet_d, variable_jet);
			
			eff_value.push_back(eff_i);
			fr_value.push_back(fr_i);

			dout("\t\teff vs fr:", eff_i, fr_i);
			
		}
	}
	else // For the drawing of the line from the raw-branch
	{
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
		dout(eff_value[i], "vs",fr_value[i]);
		efficiency[i] = eff_value[i];
		fake_rate[i] = fr_value[i];
	}

	TGraph *g = new TGraph(eff_value.size(), efficiency, fake_rate);
	std::cout << "getROC end" << std::endl;
	return g;
}
	
void plotROC()
{

	std::vector<TString>cutbased_db;
	std::vector<TString>mva_db;
	std::vector<TString>mva_db_2017_explicit;
	std::vector<TString>mva_db_2017_explicit_raw;
	std::vector<TString>mva_db_2016;
	std::vector<TString>mva_db_2016_raw;
	// List the isolation variables
		cutbased_db.clear();
		cutbased_db.push_back("byLooseCombinedIsolationDeltaBetaCorr3Hits");
		cutbased_db.push_back("byMediumCombinedIsolationDeltaBetaCorr3Hits");
		cutbased_db.push_back("byTightCombinedIsolationDeltaBetaCorr3Hits");

		mva_db.clear();
		// mva_db.push_back("byVVLooseIsolationMVArun2v1DBoldDMwLT"); why not there?
		mva_db.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT");
		mva_db.push_back("byLooseIsolationMVArun2v1DBoldDMwLT");
		mva_db.push_back("byMediumIsolationMVArun2v1DBoldDMwLT");
		mva_db.push_back("byTightIsolationMVArun2v1DBoldDMwLT");
		mva_db.push_back("byVTightIsolationMVArun2v1DBoldDMwLT");
		mva_db.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT");

		mva_db_2017_explicit.clear();
		mva_db_2017_explicit.push_back("byVVLooseIsolationMVArun2017v1DBoldDMwLT2017");
		mva_db_2017_explicit.push_back("byVLooseIsolationMVArun2017v1DBoldDMwLT2017");
		mva_db_2017_explicit.push_back("byLooseIsolationMVArun2017v1DBoldDMwLT2017");
		mva_db_2017_explicit.push_back("byMediumIsolationMVArun2017v1DBoldDMwLT2017");
		mva_db_2017_explicit.push_back("byTightIsolationMVArun2017v1DBoldDMwLT2017");
		mva_db_2017_explicit.push_back("byVTightIsolationMVArun2017v1DBoldDMwLT2017");
		mva_db_2017_explicit.push_back("byVVTightIsolationMVArun2017v1DBoldDMwLT2017");
		
		mva_db_2017_explicit_raw.clear();
		mva_db_2017_explicit_raw.push_back("byIsolationMVArun2017v1DBoldDMwLTraw2017");


		mva_db_2016.clear();
		mva_db_2016.push_back("byVLooseIsolationMVArun2v1DBoldDMwLT2016");
		mva_db_2016.push_back("byLooseIsolationMVArun2v1DBoldDMwLT2016");
		mva_db_2016.push_back("byMediumIsolationMVArun2v1DBoldDMwLT2016");
		mva_db_2016.push_back("byTightIsolationMVArun2v1DBoldDMwLT2016");
		mva_db_2016.push_back("byVTightIsolationMVArun2v1DBoldDMwLT2016");
		mva_db_2016.push_back("byVVTightIsolationMVArun2v1DBoldDMwLT2016");
		
		mva_db_2016_raw.clear();
		mva_db_2016_raw.push_back("byIsolationMVArun2v1DBoldDMwLTraw2016");
		
		//std::vector<TString>mva3_db; mva3_db.clear();
		//mva3_db.push_back("byVLooseIsolationMVA3oldDMwLT");
		//mva3_db.push_back("byLooseIsolationMVA3oldDMwLT");
		//mva3_db.push_back("byMediumIsolationMVA3oldDMwLT");
		//mva3_db.push_back("byTightIsolationMVA3oldDMwLT");
		//mva3_db.push_back("byVTightIsolationMVA3oldDMwLT");
		//mva3_db.push_back("byVVTightIsolationMVA3oldDMwLT");
		
		//photonPtSumOutsideSignalCone_ptGt1.0
		std::vector<TString>cutbased_db_raw;
		cutbased_db_raw.clear();
		cutbased_db_raw.push_back("byCombinedIsolationDeltaBetaCorrRaw3Hits");

	// Construct ROC curves from root-files
		dout("\n\n+++++++++++++++++++++cutbased_db+++++++++++++++++++++");
		TGraph *gr_cut = (TGraph*)getROC(cutbased_db);
		

		dout("\n\n+++++++++++++++++++++mva_db+++++++++++++++++++++");
		TGraph *gr_mva = (TGraph*)getROC(mva_db);
		// TGraph *gr_mva3 = (TGraph*)getROC(mva3_db);
		double x1(0.), y1(0.), x2(0.), y2(0.);
		gr_mva->GetPoint(0, x1, y1);
		gr_mva->GetPoint(5, x2, y2);
		float xmax = x1, xmin = x2;
		dout("\n\n+++++++++++++++++++++cutbased_db_raw, xmin, xmax:,", xmin, ",", xmax, "+++++++++++++++++++++");
		TGraph *gr_cut_raw = (TGraph*)getROC(cutbased_db_raw, xmin, xmax);
		std::cout << " xmin " << xmin << " xmax " << xmax << std::endl;


		dout("\n\n+++++++++++++++++++++mva_db_2017_explicit+++++++++++++++++++++");
		TGraph *gr_mva_2017_explicit = (TGraph*)getROC(mva_db_2017_explicit);
		// TGraph *gr_mva3 = (TGraph*)getROC(mva3_db);
		x1 = 0; y1 = 0; x2 = 0; y2 = 0;
		gr_mva_2017_explicit->GetPoint(0, x1, y1);
		gr_mva_2017_explicit->GetPoint(5, x2, y2);
		xmax = x1; xmin = x2;
		dout("\n\n+++++++++++++++++++++mva_db_2017_explicit_raw, xmin, xmax:,", xmin, ",", xmax, "+++++++++++++++++++++");
		TGraph *gr_mva_db_2017_explicit_raw = (TGraph*)getROC(mva_db_2017_explicit_raw, xmin, xmax);
		std::cout << " xmin " << xmin << " xmax " << xmax << std::endl;


		dout("\n\n+++++++++++++++++++++mva_db_2016+++++++++++++++++++++");
		TGraph *gr_mva_2016 = (TGraph*)getROC(mva_db_2016);
		// TGraph *gr_mva3 = (TGraph*)getROC(mva3_db);
		x1 = 0; y1 = 0; x2 = 0; y2 = 0;
		gr_mva_2016->GetPoint(0, x1, y1);
		gr_mva_2016->GetPoint(5, x2, y2);
		xmax = x1; xmin = x2;
		dout("\n\n+++++++++++++++++++++mva_db_2016_raw, xmin, xmax:,", xmin, ",", xmax, "+++++++++++++++++++++");
		TGraph *gr_mva_db_2016_raw = (TGraph*)getROC(mva_db_2016_raw, xmin, xmax);
		std::cout << " xmin " << xmin << " xmax " << xmax << std::endl;

		

	
	// Plot styling & legend
		//TCanvas* canvas = new TCanvas("canvas", "canvas", 800, 900);
		TCanvas* canvas = new TCanvas();
		//canvas->SetFillColor(10);
		//canvas->SetBorderSize(2);
		//canvas->SetLeftMargin(0.12);
		//canvas->SetBottomMargin(0.12);
		//canvas->SetRightMargin(0.05);
		canvas->SetLogy();
		canvas->cd();

		int colors[] = {6, 2, 1, 10};//, 6};
		int markerStyles[] = {23, 21, 22, 25};//, 22};
		
		double legendX0 = 0.20;
		double legendY0 = 0.75;
		TLegend* legend = new TLegend(legendX0, legendY0, legendX0 + 0.30, legendY0 + 0.15, "", "brNDC"); 
		legend->SetBorderSize(0);
		legend->SetFillColor(0);
		//legend->SetTextSize(1.5);

		const std::string yAxisTitle("Misidentification rate");
		const std::string xAxisTitle("#tau_{h} identification efficiency");
		//double yAxisOffset = 1.1;
		//double xAxisOffset = 1.1;
		double yMin = 0.0005;
		double yMax = 0.05;

		TH1F* histogram_base = new TH1F("histogram_base", "", 60, 0.25, 1);//
		histogram_base->SetTitle("");
		histogram_base->SetStats(false);
		histogram_base->SetMinimum(yMin);
		histogram_base->SetMaximum(yMax);
		//histogram_base->GetXaxis()->SetRangeUser(xmin-0.02, xmax+0.02);
		histogram_base->GetXaxis()->SetRangeUser(0.36, 0.78);
		histogram_base->Draw("hist");

		TAxis* xAxis_top = histogram_base->GetXaxis();
		xAxis_top->SetTitle(xAxisTitle.data());
		//xAxis_top->SetTitleOffset(xAxisOffset);
		//xAxis_top->SetTitleSize(0.05);
		TAxis* yAxis_top = histogram_base->GetYaxis();
		yAxis_top->SetTitle(yAxisTitle.data());
		//yAxis_top->SetTitleOffset(yAxisOffset);
		//yAxis_top->SetTitleSize(0.05);


		gr_mva->SetLineColor(colors[1]);
		gr_mva->SetLineWidth(2);
		gr_mva->SetMarkerColor(colors[1]);
		gr_mva->SetMarkerStyle(markerStyles[1]);
		gr_mva->SetMarkerSize(2.0);

		gr_mva_2017_explicit->SetLineColor(3);
		gr_mva_2017_explicit->SetLineWidth(2);
		gr_mva_2017_explicit->SetMarkerColor(3);
		gr_mva_2017_explicit->SetMarkerStyle(markerStyles[3]);
		gr_mva_2017_explicit->SetMarkerSize(2.0);
		gr_mva_db_2017_explicit_raw->SetLineColor(4);
		gr_mva_db_2017_explicit_raw->SetLineWidth(4);

		gr_mva_2016->SetLineColor(1);
		gr_mva_2016->SetLineWidth(2);
		gr_mva_2016->SetMarkerColor(1);
		gr_mva_2016->SetMarkerStyle(markerStyles[3]);
		gr_mva_2016->SetMarkerSize(2.0);
		gr_mva_db_2016_raw->SetLineColor(2);
		gr_mva_db_2016_raw->SetLineWidth(4);

		gr_cut->SetLineColor(colors[0]);
		gr_cut->SetLineWidth(2);
		gr_cut->SetMarkerColor(colors[0]);
		gr_cut->SetMarkerStyle(markerStyles[0]);
		gr_cut->SetMarkerSize(2.0);
		gr_cut_raw->SetLineColor(colors[0]);
		gr_cut_raw->SetLineWidth(2);
		
		//gr_mva3->SetLineColor(colors[2]);
		//gr_mva3->SetLineWidth(2);
		//gr_mva3->SetMarkerColor(colors[2]);
		//gr_mva3->SetMarkerStyle(markerStyles[2]);
		//gr_mva3->SetMarkerSize(2.0);

		legend->AddEntry(gr_cut, "cut-based", "pl");
		legend->AddEntry(gr_mva, "MVA-based, 2017", "pl");
		legend->AddEntry(gr_mva_2016, "MVA-based, 2016", "pl");
		legend->AddEntry(gr_mva_2017_explicit, "MVA-based, 2017, exp.", "pl");
		
		// gr_mva_db_2017_explicit_raw
		// legend->AddEntry(gr_mva_db_2016_raw, "MVA-based, raw", "pl");

		//legend->AddEntry(gr_mva3, "run-1 MVA", "pl");
		//legend->AddEntry(gr_mva, "run-2 MVA", "pl");

	// Draw
		gr_cut_raw->Draw("Lsame");
		gr_cut->Draw("Psame");
		gr_mva->Draw("PLsame");
		gr_mva_2016->Draw("PLsame");
		gr_mva_2017_explicit->Draw("PLsame");
		// gr_mva_db_2017_explicit_raw
		// gr_mva_db_2016_raw->Draw("PLsame");
		//gr_mva3->Draw("PLsame");
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
		//leg3->AddEntry(histogram_base, "Fake rate : QCD multi-jet MC (15 < #hat{p_{T}} < 3000 GeV flat)","");
		leg3->AddEntry(histogram_base, "Fake rate : QCD multi-jet MC (20 < #hat{p_{T}} < 1000 GeV)","");
		leg3->Draw();

	canvas->cd();
	canvas->Update();
	TString st = "plots/roc_cut_vs_run2mva_";
	// Save the ROC-curves
	canvas->Print(st + sample + "_RelValQCD_FlatPt_15_3000HS_13_pt18.png");
	canvas->Print(st + sample + "_RelValQCD_FlatPt_15_3000HS_13_pt18.pdf");
	canvas->Print(st + sample + "_RelValQCD_FlatPt_15_3000HS_13_pt18.C");
}