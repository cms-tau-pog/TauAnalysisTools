
#include <TFile.h>
#include <TChain.h>
#include <TTree.h>
#include <TTreeFormula.h>
#include <TString.h>
#include <TObjArray.h>
#include <TObjString.h>
#include <TH1.h>
#include <TH2.h>
#include <TGraphAsymmErrors.h>
#include <TGraphErrors.h>
#include <TF1.h>
#include <TFormula.h>
#include <TPaveText.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TMath.h>
#include <TROOT.h>
#include <TSystem.h>
#include <TStyle.h>

#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <iomanip>
#include <assert.h>
#include <math.h>
#include <limits>


void normalizeHistogram(TH1* histogram)
{
  if ( !histogram->GetSumw2N() ) histogram->Sumw2();

  int numBins = histogram->GetNbinsX();
  for ( int iBin = 1; iBin <= numBins; ++iBin ) {
    double binContent = histogram->GetBinContent(iBin);
    double binError = histogram->GetBinError(iBin);
    double binWidth = histogram->GetBinWidth(iBin);
    histogram->SetBinContent(iBin, binContent/binWidth);
    histogram->SetBinError(iBin, binError/binWidth);
  }

  if ( histogram->Integral() > 0. ) {
    histogram->Scale(1./histogram->Integral());
  } 
}

//-------------------------------------------------------------------------------
void getBinomialBounds(Int_t n, Int_t r, Float_t& rMin, Float_t& rMax)
{
  rMin = 0.;
  rMax = 0.;

  if ( n == 0 ){
    return;
  }
  if ( r < 0 ){
    std::cerr << "Error in <getBinomialBounds>: n = " << n << ", r = " << r << std::endl;
    return;
  }
  
  if ( ((Double_t)r*(n - r)) > (9.*n) ){
    rMin = r - TMath::Sqrt((Double_t)r*(n - r)/((Double_t)n));
    rMax = r + TMath::Sqrt((Double_t)r*(n - r)/((Double_t)n));
    return;
  }

  Double_t binomialCoefficient = 1.;

  Double_t rMinLeft       = 0.;
  Double_t rMinMiddle     = TMath::Max(0.5*r, n - 1.5*r);
  Double_t rMinRight      = n;
  //Double_t rMinLeftProb   = 0.;
  Double_t rMinMiddleProb = 0.5;
  //Double_t rMinRightProb  = 1.;
  while ( (rMinRight - rMinLeft) > (0.001*n) ){

    rMinMiddleProb = 0;
    for ( Int_t i = r; i <= n; i++ ){
      binomialCoefficient = 1;

      for ( Int_t j = n; j > i; j-- ){
        binomialCoefficient *= j/((Double_t)(j - i));
      }

      rMinMiddleProb += binomialCoefficient*TMath::Power(rMinMiddle/((Double_t)(n)), i)
                       *TMath::Power((n - rMinMiddle)/((Double_t)(n)), n - i);
    }

    if ( rMinMiddleProb > 0.16 ){
      rMinRight     = rMinMiddle;
      //rMinRightProb = rMinMiddleProb;
    } else if ( rMinMiddleProb < 0.16 ){
      rMinLeft      = rMinMiddle;
      //rMinLeftProb  = rMinMiddleProb;
    } else {
      rMinLeft      = rMinRight     = rMinMiddle;
      //rMinLeftProb  = rMinRightProb = rMinMiddleProb;
    }

    rMinMiddle = 0.5*(rMinLeft + rMinRight);

    if ( rMinLeft > r ){
      rMinMiddle = rMinLeft = rMinRight = 0;
    }
  }

  Double_t rMaxLeft       = 0.;
  Double_t rMaxMiddle     = TMath::Min(1.5*r, n - 0.5*r);
  Double_t rMaxRight      = n;
  //Double_t rMaxLeftProb   = 1.;
  Double_t rMaxMiddleProb = 0.5;
  //Double_t rMaxRightProb  = 0.;
  while ( (rMaxRight - rMaxLeft) > (0.001*n) ){

    rMaxMiddleProb = 0;
    for ( Int_t i = 0; i <= r; i++ ){
      binomialCoefficient = 1;
      
      for ( Int_t j = n; j > (n - i); j-- ){
        binomialCoefficient *= j/((Double_t)(i - (n - j)));
      }

      rMaxMiddleProb += binomialCoefficient*TMath::Power(rMaxMiddle/((Double_t)(n)), i)
                       *TMath::Power((n - rMaxMiddle)/((Double_t)(n)), n - i);
    }

    if ( rMaxMiddleProb > 0.16 ){
      rMaxLeft      = rMaxMiddle;
      //rMaxLeftProb  = rMaxMiddleProb;
    } else if ( rMaxMiddleProb < 0.16 ){
      rMaxRight     = rMaxMiddle;
      //rMaxRightProb = rMaxMiddleProb;
    } else {
      rMaxLeft      = rMaxRight     = rMaxMiddle;
      //rMaxLeftProb  = rMaxRightProb = rMaxMiddleProb;
    }

    rMaxMiddle = 0.5*(rMaxLeft + rMaxRight);

    if ( rMaxRight < r ){
      rMaxMiddle = rMaxLeft = rMaxRight = n;
    }
  }

  rMin = rMinMiddle;
  rMax = rMaxMiddle;
}

TGraphAsymmErrors* getEfficiency(const TH1* histogram_numerator, const TH1* histogram_denominator)
{
  Int_t error = 0;
  if ( !(histogram_numerator->GetNbinsX()           == histogram_denominator->GetNbinsX())           ) error = 1;
  if ( !(histogram_numerator->GetXaxis()->GetXmin() == histogram_denominator->GetXaxis()->GetXmin()) ) error = 1;
  if ( !(histogram_numerator->GetXaxis()->GetXmax() == histogram_denominator->GetXaxis()->GetXmax()) ) error = 1;
  
  if ( error ){
    std::cerr << "Error in <getEfficiency>: Dimensionality of histograms does not match !!" << std::endl;
    return 0;
  }
  
  TAxis* xAxis = histogram_numerator->GetXaxis();

  Int_t nBins = xAxis->GetNbins();
  TArrayF x(nBins);
  TArrayF dxUp(nBins);
  TArrayF dxDown(nBins);
  TArrayF y(nBins);
  TArrayF dyUp(nBins);
  TArrayF dyDown(nBins);

  for ( Int_t ibin = 1; ibin <= nBins; ibin++ ){
    Int_t nObs = TMath::Nint(histogram_denominator->GetBinContent(ibin));
    Int_t rObs = TMath::Nint(histogram_numerator->GetBinContent(ibin));

    Float_t xCenter = histogram_denominator->GetBinCenter(ibin);
    Float_t xWidth  = histogram_denominator->GetBinWidth(ibin);

    x[ibin - 1]      = xCenter;
    dxUp[ibin - 1]   = 0.5*xWidth;
    dxDown[ibin - 1] = 0.5*xWidth;
    
    if ( nObs > 0 ){
      Float_t rMin = 0.;
      Float_t rMax = 0.;
      
      getBinomialBounds(nObs, rObs, rMin, rMax);

      y[ibin - 1]      = rObs/((Float_t)nObs);
      dyUp[ibin - 1]   = (rMax - rObs)/((Float_t)nObs);
      dyDown[ibin - 1] = (rObs - rMin)/((Float_t)nObs);
    } else{
      y[ibin - 1]      = 0.;
      dyUp[ibin - 1]   = 0.;
      dyDown[ibin - 1] = 0.;
    }
  }
  
  TString name  = TString(histogram_numerator->GetName()).Append("Graph");
  TString title = histogram_numerator->GetTitle();

  TGraphAsymmErrors* graph = 
    new TGraphAsymmErrors(nBins, x.GetArray(), y.GetArray(), 
			  dxDown.GetArray(), dxUp.GetArray(), dyDown.GetArray(), dyUp.GetArray());

  graph->SetName(name);
  graph->SetTitle(title);

  return graph;
}

void showEfficiency(const TString& title, double canvasSizeX, double canvasSizeY,
		    const TH1* histogram1_numerator, const TH1* histogram1_denominator, const std::string& legendEntry1,
		    const TH1* histogram2_numerator, const TH1* histogram2_denominator, const std::string& legendEntry2,
		    const TH1* histogram3_numerator, const TH1* histogram3_denominator, const std::string& legendEntry3,
		    const TH1* histogram4_numerator, const TH1* histogram4_denominator, const std::string& legendEntry4,
		    const TH1* histogram5_numerator, const TH1* histogram5_denominator, const std::string& legendEntry5,
		    const std::string& xAxisTitle, double xMin, double xMax,
                    bool useLogScale, double yMin, double yMax, const std::string& yAxisTitle,
		    double legendX0, double legendY0, 
		    const std::string& outputFileName)
{
  TCanvas* canvas = new TCanvas("canvas", "canvas", canvasSizeX, canvasSizeY);
  canvas->SetLogy(useLogScale);

  TH1* dummyHistogram = new TH1D("dummyH", "dummyH", 10, xMin, xMax);
  dummyHistogram->SetTitle("");
  dummyHistogram->SetStats(false);
  dummyHistogram->SetMaximum(yMax);
  dummyHistogram->SetMinimum(yMin);
  
  TAxis* xAxis = dummyHistogram->GetXaxis();
  xAxis->SetTitle(xAxisTitle.data());
  
  TAxis* yAxis = dummyHistogram->GetYaxis();
  yAxis->SetTitle(yAxisTitle.data());

  dummyHistogram->Draw();

  int colors[5] = { 1, 2, 3, 4, 7 };
  int markerStyles[5] = { 20, 21, 22, 23, 33 };
  float markerSizes[5] = { 1., 1., 1.3, 1.3, 1.8 };

  int numGraphs = 1;
  if ( histogram2_numerator && histogram2_denominator ) ++numGraphs;
  if ( histogram3_numerator && histogram3_denominator ) ++numGraphs;
  if ( histogram4_numerator && histogram4_denominator ) ++numGraphs;
  if ( histogram5_numerator && histogram5_denominator ) ++numGraphs;

  TLegend* legend = new TLegend(legendX0, legendY0, legendX0 + 0.30, legendY0 + 0.035*numGraphs, "", "brNDC"); 
  legend->SetFillColor(0);
  legend->SetShadowColor(0);
  
  TGraphAsymmErrors* graph1 = getEfficiency(histogram1_numerator, histogram1_denominator);
  graph1->SetLineColor(colors[0]);
  graph1->SetMarkerColor(colors[0]);
  graph1->SetMarkerStyle(markerStyles[0]);
  graph1->SetMarkerSize(markerSizes[0]);
  graph1->Draw("p");
  legend->AddEntry(graph1, legendEntry1.data(), "lp");    

  TGraphAsymmErrors* graph2 = 0;
  if ( histogram2_numerator && histogram2_denominator ) {
    graph2 = getEfficiency(histogram2_numerator, histogram2_denominator);
    graph2->SetLineColor(colors[1]);
    graph2->SetMarkerColor(colors[1]);
    graph2->SetMarkerStyle(markerStyles[1]);
    graph2->SetMarkerSize(markerSizes[1]);
    graph2->Draw("p");
    legend->AddEntry(graph2, legendEntry2.data(), "lp");
  }

  TGraphAsymmErrors* graph3 = 0;
  if ( histogram3_numerator && histogram3_denominator ) {
    graph3 = getEfficiency(histogram3_numerator, histogram3_denominator);
    graph3->SetLineColor(colors[2]);
    graph3->SetMarkerColor(colors[2]);
    graph3->SetMarkerStyle(markerStyles[2]);
    graph3->SetMarkerSize(markerSizes[2]);
    graph3->Draw("p");
    legend->AddEntry(graph3, legendEntry3.data(), "lp");
  }
  
  TGraphAsymmErrors* graph4 = 0;
  if ( histogram4_numerator && histogram4_denominator ) {
    graph4 = getEfficiency(histogram4_numerator, histogram4_denominator);
    graph4->SetLineColor(colors[3]);
    graph4->SetMarkerColor(colors[3]);
    graph4->SetMarkerStyle(markerStyles[3]);
    graph4->SetMarkerSize(markerSizes[3]);
    graph4->Draw("p");
    legend->AddEntry(graph4, legendEntry4.data(), "lp");
  }

  TGraphAsymmErrors* graph5 = 0;
  if ( histogram5_numerator && histogram5_denominator ) {
    graph5 = getEfficiency(histogram5_numerator, histogram5_denominator);
    graph5->SetLineColor(colors[4]);
    graph5->SetMarkerColor(colors[4]);
    graph5->SetMarkerStyle(markerStyles[4]);
    graph5->SetMarkerSize(markerSizes[4]);
    graph5->Draw("p");
    legend->AddEntry(graph5, legendEntry5.data(), "lp");
  }

  legend->Draw();

  TPaveText* label = 0;
  if ( title.Length() > 0 ) {
    label = new TPaveText(0.175, 0.94, 0.48, 0.98, "NDC");
    label->AddText(title.Data());
    label->SetTextAlign(13);
    label->SetTextSize(0.045);
    label->SetFillStyle(0);
    label->SetBorderSize(0);
    label->Draw();
  }

  canvas->Update();
  size_t idx = outputFileName.find_last_of('.');
  std::string outputFileName_plot = std::string(outputFileName, 0, idx);
  if ( idx != std::string::npos ) canvas->Print(std::string(outputFileName_plot).append(std::string(outputFileName, idx)).data());
  canvas->Print(std::string(outputFileName_plot).append(".png").data());
  canvas->Print(std::string(outputFileName_plot).append(".pdf").data());
  
  delete legend;
  delete label;
  delete dummyHistogram;
  delete canvas;
}
//-------------------------------------------------------------------------------

//-------------------------------------------------------------------------------
void showDistribution(const TString& title, double canvasSizeX, double canvasSizeY,
		      TH1* histogram1, const std::string& legendEntry1,
		      TH1* histogram2, const std::string& legendEntry2,
		      const std::string& xAxisTitle,
		      bool useLogScale, double yMin, double yMax, const std::string& yAxisTitle,
		      double legendX0, double legendY0, 
		      const std::string& outputFileName)
{
  TCanvas* canvas = new TCanvas("canvas", "canvas", canvasSizeX, canvasSizeY);
  canvas->SetLogy(useLogScale);

  int colors[2] = { 1, 2 };
  int markerStyles[2] = { 20, 21 };

  int numHistograms = 1;
  if ( histogram2 ) ++numHistograms;

  TLegend* legend = new TLegend(legendX0, legendY0, legendX0 + 0.30, legendY0 + 0.05*numHistograms, "", "brNDC"); 
  legend->SetFillColor(0);
  legend->SetShadowColor(0);

  histogram1->SetTitle("");
  histogram1->SetStats(false);
  histogram1->SetMinimum(yMin);
  histogram1->SetMaximum(yMax);
  histogram1->SetLineColor(colors[0]);
  histogram1->SetMarkerColor(colors[0]);
  histogram1->SetMarkerStyle(markerStyles[0]);
  histogram1->Draw("elp");
  legend->AddEntry(histogram1, legendEntry1.data(), "lp");

  TAxis* xAxis = histogram1->GetXaxis();
  xAxis->SetTitle(xAxisTitle.data());

  TAxis* yAxis = histogram1->GetYaxis();
  yAxis->SetTitle(yAxisTitle.data());

  if ( histogram2 ) {
    histogram2->SetLineColor(colors[1]);
    histogram2->SetMarkerColor(colors[1]);
    histogram2->SetMarkerStyle(markerStyles[1]);
    histogram2->Draw("elp,same");
    legend->AddEntry(histogram2, legendEntry2.data(), "lp");
  }

  legend->Draw();

  TPaveText* label = 0;
  if ( title.Length() > 0 ) {
    label = new TPaveText(0.175, 0.94, 0.48, 0.98, "NDC");
    label->AddText(title.Data());
    label->SetTextAlign(13);
    label->SetTextSize(0.045);
    label->SetFillStyle(0);
    label->SetBorderSize(0);
    label->Draw();
  }
  
  canvas->Update();
  size_t idx = outputFileName.find_last_of('.');
  std::string outputFileName_plot = std::string(outputFileName, 0, idx);
  if ( idx != std::string::npos ) canvas->Print(std::string(outputFileName_plot).append(std::string(outputFileName, idx)).data());
  canvas->Print(std::string(outputFileName_plot).append(".png").data());
  canvas->Print(std::string(outputFileName_plot).append(".pdf").data());
  
  delete legend;
  delete label;
  delete canvas;  
}
//-------------------------------------------------------------------------------

//-------------------------------------------------------------------------------
TGraph* compMVAcut(const TH2* histogramMVAoutput_vs_Pt, const TH1* histogramPt, double Efficiency_or_FakeRate)
{
  //std::cout << "<compMVAcut>:" << std::endl;
  //std::cout << " Efficiency_or_FakeRate = " << Efficiency_or_FakeRate << std::endl;

  const TAxis* xAxis = histogramMVAoutput_vs_Pt->GetXaxis();
  int numBinsX = xAxis->GetNbins();

  const TAxis* yAxis = histogramMVAoutput_vs_Pt->GetYaxis();
  int numBinsY = yAxis->GetNbins();

  TGraph* graph = new TGraphAsymmErrors(numBinsX);
  std::string graphName = Form("%s_graph", histogramMVAoutput_vs_Pt->GetName());
  graph->SetName(graphName.data());

  int numPoints = 0;

  for ( int iBinX = 1; iBinX <= numBinsX; ++iBinX ) {
    double ptMin = xAxis->GetBinLowEdge(iBinX);
    double ptMax = xAxis->GetBinUpEdge(iBinX);

    int binLowIndex = const_cast<TH1*>(histogramPt)->FindBin(ptMin);
    int binUpIndex  = const_cast<TH1*>(histogramPt)->FindBin(ptMax);
    //std::cout << "ptMin = " << ptMin << ", ptMax = " << ptMax << ": binLowIndex = " << binLowIndex << ", binUpIndex = " << binUpIndex << std::endl;
    histogramPt->GetXaxis()->SetRange(binLowIndex, binUpIndex);

    // CV: skip bins of low statistics
    if ( histogramPt->GetEntries() < 100 ) {
      std::cout << "Warning: bin @ x = " << xAxis->GetBinCenter(iBinX) << " has low statistics (#entries = " << histogramPt->GetEntries() << ") --> skipping !!" << std::endl;
      continue;
    }

    double x = histogramPt->GetMean();

    //std::cout << "iBinX = " << iBinX << ": xMean = " << x << std::endl;

    double normalization = 0.;
    for ( int iBinY = numBinsY; iBinY >= 1; --iBinY ) {
      normalization += histogramMVAoutput_vs_Pt->GetBinContent(iBinX, iBinY);
    }
    // CV: skip bins of low statistics
    if ( normalization < 1.e-6 ) {
      std::cout << "Warning: bin @ x = " << xAxis->GetBinCenter(iBinX) << " has low statistics (normalization = " << normalization << ") --> skipping !!" << std::endl;
      continue;
    }
    
    double y = -1.;

    double runningSum = 0.;
    for ( int iBinY = numBinsY; iBinY >= 1; --iBinY ) {
      double binContent_normalized = histogramMVAoutput_vs_Pt->GetBinContent(iBinX, iBinY)/normalization;
      if ( (runningSum + binContent_normalized) >= Efficiency_or_FakeRate ) {
	y = yAxis->GetBinUpEdge(iBinY) - ((Efficiency_or_FakeRate - runningSum)/binContent_normalized)*yAxis->GetBinWidth(iBinY);
	//std::cout << "iBinY = " << iBinY << " (yCenter = " << yAxis->GetBinCenter(iBinY) << "): binContent = " << binContent_normalized << std::endl;
	//std::cout << "--> setting y = " << y << std::endl;
	const double epsilon = 1.e-6;
	assert(y >= (yAxis->GetBinLowEdge(iBinY) - epsilon));
	break;
      } else {
	runningSum += binContent_normalized;
	//std::cout << "iBinY = " << iBinY << " (yCenter = " << yAxis->GetBinCenter(iBinY) << "): runningSum = " << runningSum << std::endl;
      }
    }
    
    graph->SetPoint(numPoints, x, y);
    ++numPoints;
  }

  for ( int iPoint = numBinsX; iPoint > numPoints; --iPoint ) {
    //std::cout << "removing point #" << iPoint << std::endl;
    graph->RemovePoint(graph->GetN() - 1);
  }

  // reset x-axis range selection 
  histogramPt->GetXaxis()->SetRange(1., 0.);

  return graph;
}

void showGraphs(const TString& title, double canvasSizeX, double canvasSizeY,
		TGraph* graph1, const std::string& legendEntry1,
		TGraph* graph2, const std::string& legendEntry2,
		TGraph* graph3, const std::string& legendEntry3,
		TGraph* graph4, const std::string& legendEntry4,
		TGraph* graph5, const std::string& legendEntry5,
		TGraph* graph6, const std::string& legendEntry6,
		double xMin, double xMax, unsigned numBinsX, const std::string& xAxisTitle,
		double yMin, double yMax, const std::string& yAxisTitle,
		double legendX0, double legendY0, 
		const std::string& outputFileName)
{
  TCanvas* canvas = new TCanvas("canvas", "canvas", canvasSizeX, canvasSizeY);

  int colors[6] = { 1, 2, 3, 4, 6, 7 };

  TLegend* legend = new TLegend(legendX0, legendY0, legendX0 + 0.3, legendY0 + 0.20, "", "brNDC");
  legend->SetFillColor(0);
  legend->SetShadowColor(0);

  TH1* dummyHistogram = new TH1D("dummyH", "dummyH", numBinsX, xMin, xMax);
  dummyHistogram->SetTitle("");
  dummyHistogram->SetStats(false);
  dummyHistogram->SetMinimum(yMin);
  dummyHistogram->SetMaximum(yMax);

  TAxis* xAxis = dummyHistogram->GetXaxis();
  xAxis->SetTitle(xAxisTitle.data());

  TAxis* yAxis = dummyHistogram->GetYaxis();
  yAxis->SetTitle(yAxisTitle.data());

  dummyHistogram->Draw("axis");

  graph1->SetLineColor(colors[0]);
  graph1->Draw("L");
  legend->AddEntry(graph1, legendEntry1.data(), "l");

  if ( graph2 ) {
    graph2->SetLineColor(colors[1]);
    graph2->Draw("L");
    legend->AddEntry(graph2, legendEntry2.data(), "l");
  }
  
  if ( graph3 ) {
    graph3->SetLineColor(colors[2]);
    graph3->Draw("L");
    legend->AddEntry(graph3, legendEntry3.data(), "l");
  }

  if ( graph4 ) {
    graph4->SetLineColor(colors[3]);
    graph4->Draw("L");
    legend->AddEntry(graph4, legendEntry4.data(), "l");
  }

  if ( graph5 ) {
    graph5->SetLineColor(colors[4]);
    graph5->Draw("L");
    legend->AddEntry(graph5, legendEntry5.data(), "l");
  }

  if ( graph6 ) {
    graph6->SetLineColor(colors[5]);
    graph6->Draw("L");
    legend->AddEntry(graph6, legendEntry6.data(), "l");
  }
  
  legend->Draw();
    
  TPaveText* label = 0;
  if ( title.Length() > 0 ) {
    label = new TPaveText(0.175, 0.96, 0.48, 0.98, "NDC");
    label->AddText(title.Data());
    label->SetTextAlign(13);
    label->SetTextSize(0.045);
    label->SetFillStyle(0);
    label->SetBorderSize(0);
    label->Draw();
  }

  canvas->Update();
  size_t idx = outputFileName.find_last_of('.');
  std::string outputFileName_plot = std::string(outputFileName, 0, idx);
  if ( idx != std::string::npos ) canvas->Print(std::string(outputFileName_plot).append(std::string(outputFileName, idx)).data());
  canvas->Print(std::string(outputFileName_plot).append(".png").data());
  canvas->Print(std::string(outputFileName_plot).append(".pdf").data());
  
  delete legend;
  delete label;
  delete dummyHistogram;
  delete canvas;  
}
//-------------------------------------------------------------------------------

struct plotEntryType
{
  plotEntryType(const std::string& name, const std::string& cuts, double eff)
    : name_(name),
      cuts_(cuts),
      targetEff_(eff),
      histogramPt_numerator_(0),
      histogramPt_denominator_(0),
      histogramEta_numerator_(0),
      histogramEta_denominator_(0),
      histogramNvtx_numerator_(0),
      histogramNvtx_denominator_(0),
      histogramMVAoutput_vs_Pt_(0),
      histogramPt_(0)
  {}
  ~plotEntryType()
  {
    delete cutsFile_;
    delete histogramPt_numerator_;
    delete histogramPt_denominator_;
    delete histogramEta_numerator_;
    delete histogramEta_denominator_;
    delete histogramNvtx_numerator_;
    delete histogramNvtx_denominator_;
    delete histogramMVAoutput_vs_Pt_;
    delete histogramPt_;
  }
  void bookCutThresholds()
  {
    cutsFile_ = TFile::Open(cuts_.data());
  }
  void bookHistograms()
  {
    //const int ptNumBins = 24;
    //double ptBinning[ptNumBins + 1] = { 
    //  20., 22.5, 25., 27.5, 30., 32.5, 35., 37.5, 40., 45., 50., 55., 60., 70., 80., 90., 100., 125., 150., 175., 200., 250., 300., 400., 500.
    //};
    //const int ptNumBins = 16;
    //double ptBinning[ptNumBins + 1] = { 
    //  20., 22.5, 25., 27.5, 30., 32.5, 35., 37.5, 40., 45., 50., 55., 60., 70., 80., 90., 100.
    //};
    const int ptNumBins = 10;
    double ptBinning[ptNumBins + 1] = { 
      20., 30., 40., 50., 60., 70., 80., 90., 100., 110., 120.
    };
    std::string histogramNamePt_numerator = Form("histogramPt_%s_numerator", name_.data());
    histogramPt_numerator_ = new TH1D(histogramNamePt_numerator.data(), histogramNamePt_numerator.data(), ptNumBins, ptBinning);
    std::string histogramNamePt_denominator = Form("histogramPt_%s_denominator", name_.data());
    histogramPt_denominator_ = new TH1D(histogramNamePt_denominator.data(), histogramNamePt_denominator.data(), ptNumBins, ptBinning);
    std::string histogramNameEta_numerator = Form("histogramEta_%s_numerator", name_.data());
    histogramEta_numerator_ = new TH1D(histogramNameEta_numerator.data(), histogramNameEta_numerator.data(), 24, -2.3, 2.3);
    std::string histogramNameEta_denominator = Form("histogramEta_%s_denominator", name_.data());
    histogramEta_denominator_ = new TH1D(histogramNameEta_denominator.data(), histogramNameEta_denominator.data(), 24, -2.3, 2.3);
    std::string histogramNameNvtx_numerator = Form("histogramNvtx_%s_numerator", name_.data());
    histogramNvtx_numerator_ = new TH1D(histogramNameNvtx_numerator.data(), histogramNameNvtx_numerator.data(), 9, 0., 35.);
    std::string histogramNameNvtx_denominator = Form("histogramNvtx_%s_denominator", name_.data());
    histogramNvtx_denominator_ = new TH1D(histogramNameNvtx_denominator.data(), histogramNameNvtx_denominator.data(), 9, 0., 35.);
    std::string histogramNameMVAoutput_vs_Pt = Form("histogramMVAoutput_vs_Pt_%s", name_.data());
    histogramMVAoutput_vs_Pt_ = new TH2D(histogramNameMVAoutput_vs_Pt.data(), histogramNameMVAoutput_vs_Pt.data(), ptNumBins, ptBinning, 20200, -1.01, +1.01);
    std::string histogramNamePt = Form("histogramPt_%s", name_.data());
    histogramPt_ = new TH1D(histogramNamePt.data(), histogramNamePt.data(), 2500, 0., 2500.);
  }
  void fillHistograms(double mvaOutput, int category, double pt, double eta, double Nvtx, double evtWeight)
  {
    TGraphErrors* cutThresholds = (TGraphErrors*) cutsFile_->Get(Form("eff%1.0fcat%i", targetEff_*100, category));

    if ( !cutThresholds ){
      std::cerr << "plotEntryType::fillHistograms: graph named " << Form("eff%1.0fcat%i", targetEff_*100, category) << " not found in file " << cutsFile_->GetName() << std::endl;

      exit(0);
    }

    histogramPt_denominator_->Fill(pt, evtWeight);
    histogramEta_denominator_->Fill(eta, evtWeight);
    histogramNvtx_denominator_->Fill(Nvtx, evtWeight);

    bool passesCuts = (mvaOutput > cutThresholds->Eval(pt));
    //std::cout << "passesCuts = " << passesCuts << std::endl;
    if ( passesCuts ) {
      histogramPt_numerator_->Fill(pt, evtWeight);
      histogramEta_numerator_->Fill(eta, evtWeight);
      histogramNvtx_numerator_->Fill(Nvtx, evtWeight);
    }
    double y = mvaOutput;
    TAxis* yAxis = histogramMVAoutput_vs_Pt_->GetYaxis();
    int binY = yAxis->FindBin(y);
    int numBinsY = yAxis->GetNbins();
    if ( binY <  1       ) binY = 1;
    if ( binY > numBinsY ) binY = numBinsY;
    histogramMVAoutput_vs_Pt_->Fill(pt, y, evtWeight);
    histogramPt_->Fill(pt, evtWeight);

    delete cutThresholds;
  }
  std::string name_;
  std::string cuts_;
  double targetEff_;
  TFile* cutsFile_;
  TH1* histogramPt_numerator_;
  TH1* histogramPt_denominator_;
  TH1* histogramEta_numerator_;
  TH1* histogramEta_denominator_;
  TH1* histogramNvtx_numerator_;
  TH1* histogramNvtx_denominator_;
  TH2* histogramMVAoutput_vs_Pt_;
  TH1* histogramPt_;
};

void fillPlots(const std::string& inputFileName, const std::string& treeName, plotEntryType* plots_signal, plotEntryType* plots_background)
{
  TFile* inputFile = new TFile(inputFileName.data());

  TTree* tree = dynamic_cast<TTree*>(inputFile->Get(treeName.data()));

  Float_t recTauPt, recTauEta;
  tree->SetBranchAddress("Tau_Pt", &recTauPt);
  tree->SetBranchAddress("Tau_EtaAtEcalEntrance", &recTauEta);
  
  Int_t numVertices;
  tree->SetBranchAddress("NumPV", &numVertices);

  Float_t mvaOutput;
  Int_t category;
  tree->SetBranchAddress("mva", &mvaOutput);
  tree->SetBranchAddress("Tau_Category", &category);

  Float_t evtWeight;
  tree->SetBranchAddress("evtWeight", &evtWeight);
  
  const int maxEvents = -1;
  int numEntries = tree->GetEntries();

  double normalization_signal = 0.;
  double normalization_background = 0.;
  for ( int iEntry = 0; iEntry < numEntries && (iEntry < maxEvents || maxEvents == -1); ++iEntry ) {
    if ( iEntry > 0 && (iEntry % 200000) == 0 ) {
      std::cout << "processing Entry " << iEntry << std::endl;
    }
    
    tree->GetEntry(iEntry);

    // remove un-categorized taus
    if ( category == 0)
      continue;

    if ( inputFileName.find("signal.root") != std::string::npos ) normalization_signal += evtWeight;
    else if ( inputFileName.find("background.root") != std::string::npos ) normalization_background += evtWeight;
  }
  std::cout << "normalization: signal = " << normalization_signal << ", background = " << normalization_background << std::endl;  

  for ( int iEntry = 0; iEntry < numEntries && (iEntry < maxEvents || maxEvents == -1); ++iEntry ) {
    if ( iEntry > 0 && (iEntry % 200000) == 0 ) {
      std::cout << "processing Entry " << iEntry << std::endl;
    }
    
    tree->GetEntry(iEntry);

    // remove un-categorized taus
    if ( category == 0)
      continue;
 
    if ( inputFileName.find("signal.root") != std::string::npos )
      plots_signal->fillHistograms(mvaOutput, TMath::Log2(category), recTauPt, recTauEta, numVertices, evtWeight);
    else if ( inputFileName.find("background.root") != std::string::npos )
      plots_background->fillHistograms(mvaOutput, TMath::Log2(category), recTauPt, recTauEta, numVertices, evtWeight);
  }

  delete tree;
  delete inputFile;
}

struct mvaEntryType
{
  mvaEntryType(const std::string& sigFileName, const std::string& bkgFileName, const std::string& cutsFileName, double targetSignalEff)
    : inputSignal_(sigFileName),
      inputBkg_(bkgFileName),
      cutsFileName_(cutsFileName),
      targetSignalEff_(targetSignalEff)      
  {
    legendEntry_ = Form("MVA %1.0f%% signal eff", targetSignalEff * 100);
    plots_signal_ = new plotEntryType("signal", cutsFileName, targetSignalEff);
    plots_signal_->bookHistograms();
    plots_signal_->bookCutThresholds();
    plots_background_ = new plotEntryType("background", cutsFileName, targetSignalEff);
    plots_background_->bookHistograms();
    plots_background_->bookCutThresholds(); 
  }
  ~mvaEntryType() {}
  std::string inputSignal_;
  std::string inputBkg_;
  std::string cutsFileName_;
  std::string legendEntry_;
  double targetSignalEff_;
  plotEntryType* plots_signal_;
  plotEntryType* plots_background_;
};

void plotAntiElectronDiscrMVAEfficiency_and_FakeRate()
{
//--- stop ROOT from keeping references to all histograms
  TH1::AddDirectory(false);

//--- suppress the output canvas 
  gROOT->SetBatch(true);

//--- load a nicer ROOT style
  gROOT->LoadMacro("$CMSSW_BASE/src/TauAnalysisTools/TauAnalysisTools/macros/tdrstyle.C");
  gROOT->ProcessLine("setTDRStyle()");
  gROOT->ProcessLine("tdrGrid(true)");
  gStyle->SetFrameLineWidth(3);
  gStyle->SetLineWidth(3);
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadBottomMargin(0.15);
  gStyle->SetPadLeftMargin(0.18);
  gStyle->SetPadRightMargin(0.05);
  gStyle->SetTitleFontSize(0.055);
  gStyle->SetTitleSize(0.055, "XYZ");
  gStyle->SetTitleXOffset(1.25);
  gStyle->SetTitleYOffset(1.60);
  gStyle->SetLabelSize(0.04, "XYZ");
  gStyle->SetLabelOffset(0.013, "XYZ"); 
  
  std::string path = "/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/antiElectronDiscrMVATraining/fixTauGSF_scenario3_v2_lessVars_onlyZJets/";
  std::string sigFileName = "preselectTreeAntiElectronDiscrMVA_mvaAntiElectronDiscr5_signal.root";
  std::string bkgFileName = "preselectTreeAntiElectronDiscrMVA_mvaAntiElectronDiscr5_background.root";
  std::string treeName = "preselectedAntiElectronDiscrMVATrainingNtuple"; 
  std::string mvaCutsFile = "/nfs/dust/cms/user/fcolombo/HiggsToTauTau/TauPOG/CMSSW_7_2_3/src/TauAnalysisTools/TauAnalysisTools/macros/dumpWPsAntiElectronDiscr.root";

  std::vector<mvaEntryType*> mvaEntries;
  mvaEntries.push_back(new mvaEntryType(path+sigFileName, path+bkgFileName, mvaCutsFile, 0.95));
  mvaEntries.push_back(new mvaEntryType(path+sigFileName, path+bkgFileName, mvaCutsFile, 0.90));
  mvaEntries.push_back(new mvaEntryType(path+sigFileName, path+bkgFileName, mvaCutsFile, 0.85));
  mvaEntries.push_back(new mvaEntryType(path+sigFileName, path+bkgFileName, mvaCutsFile, 0.80));
  mvaEntries.push_back(new mvaEntryType(path+sigFileName, path+bkgFileName, mvaCutsFile, 0.75)); 

  for ( std::vector<mvaEntryType*>::iterator mvaEntry = mvaEntries.begin();
	mvaEntry != mvaEntries.end(); ++mvaEntry ) {
    std::cout << "processing " << (*mvaEntry)->legendEntry_ << std::endl;
    std::cout << "signal file: " << (*mvaEntry)->inputSignal_ << std::endl;
    std::cout << "background file: " << (*mvaEntry)->inputBkg_ << std::endl;

    fillPlots((*mvaEntry)->inputSignal_, treeName, (*mvaEntry)->plots_signal_, (*mvaEntry)->plots_background_);
    fillPlots((*mvaEntry)->inputBkg_, treeName, (*mvaEntry)->plots_signal_, (*mvaEntry)->plots_background_);
  }


//--- print summary informations on integrated efficiency/fake-rate
  for ( std::vector<mvaEntryType*>::iterator mvaEntry = mvaEntries.begin();
	mvaEntry != mvaEntries.end(); ++mvaEntry ) {

    double integralSignalNum = (*mvaEntry)->plots_signal_->histogramNvtx_numerator_->Integral();
    double integralSignalDen = (*mvaEntry)->plots_signal_->histogramNvtx_denominator_->Integral();
    double integralBkgNum = (*mvaEntry)->plots_background_->histogramNvtx_numerator_->Integral();
    double integralBkgDen = (*mvaEntry)->plots_background_->histogramNvtx_denominator_->Integral();

    std::cout << (*mvaEntry)->legendEntry_ << std::endl;
    std::cout << "integrated eff: " << integralSignalNum << "/" << integralSignalDen << " = " << integralSignalNum/integralSignalDen << std::endl;
    std::cout << "integrated fake-rate: " << integralBkgNum << "/" << integralBkgDen << " = " << integralBkgNum/integralBkgDen << std::endl;

  }


//--- efficiency/fake-rate plots (vs. pT, eta, Nvtx) 
  showEfficiency("Z #rightarrow #tau#tau", 600, 600,
    mvaEntries[0]->plots_signal_->histogramPt_numerator_, mvaEntries[0]->plots_signal_->histogramPt_denominator_, mvaEntries[0]->legendEntry_,
    mvaEntries[1]->plots_signal_->histogramPt_numerator_, mvaEntries[1]->plots_signal_->histogramPt_denominator_, mvaEntries[1]->legendEntry_,
    mvaEntries[2]->plots_signal_->histogramPt_numerator_, mvaEntries[2]->plots_signal_->histogramPt_denominator_, mvaEntries[2]->legendEntry_,
    mvaEntries[3]->plots_signal_->histogramPt_numerator_, mvaEntries[3]->plots_signal_->histogramPt_denominator_, mvaEntries[3]->legendEntry_,
    mvaEntries[4]->plots_signal_->histogramPt_numerator_, mvaEntries[4]->plots_signal_->histogramPt_denominator_, mvaEntries[4]->legendEntry_,
    "P_{T} / GeV", 10., 130.,
    false, 0.2, 1.4, "Efficiency",
    0.6, 0.7, 
    "plots/plotAntiElectronMVAEfficiency_vs_Pt.png");

  showEfficiency("Z #rightarrow #tau#tau", 600, 600,
    mvaEntries[0]->plots_signal_->histogramEta_numerator_, mvaEntries[0]->plots_signal_->histogramEta_denominator_, mvaEntries[0]->legendEntry_,
    mvaEntries[1]->plots_signal_->histogramEta_numerator_, mvaEntries[1]->plots_signal_->histogramEta_denominator_, mvaEntries[1]->legendEntry_,
    mvaEntries[2]->plots_signal_->histogramEta_numerator_, mvaEntries[2]->plots_signal_->histogramEta_denominator_, mvaEntries[2]->legendEntry_,
    mvaEntries[3]->plots_signal_->histogramEta_numerator_, mvaEntries[3]->plots_signal_->histogramEta_denominator_, mvaEntries[3]->legendEntry_,
    mvaEntries[4]->plots_signal_->histogramEta_numerator_, mvaEntries[4]->plots_signal_->histogramEta_denominator_, mvaEntries[4]->legendEntry_,
    "#eta", -2.9, 2.9,
    false, 0.2, 1.4, "Efficiency", 
    0.6, 0.7, 
    "plots/plotAntiElectronMVAEfficiency_vs_Eta.png");

  showEfficiency("Z #rightarrow #tau#tau", 600, 600,
    mvaEntries[0]->plots_signal_->histogramNvtx_numerator_, mvaEntries[0]->plots_signal_->histogramNvtx_denominator_, mvaEntries[0]->legendEntry_,
    mvaEntries[1]->plots_signal_->histogramNvtx_numerator_, mvaEntries[1]->plots_signal_->histogramNvtx_denominator_, mvaEntries[1]->legendEntry_,
    mvaEntries[2]->plots_signal_->histogramNvtx_numerator_, mvaEntries[2]->plots_signal_->histogramNvtx_denominator_, mvaEntries[2]->legendEntry_,
    mvaEntries[3]->plots_signal_->histogramNvtx_numerator_, mvaEntries[3]->plots_signal_->histogramNvtx_denominator_, mvaEntries[3]->legendEntry_,
    mvaEntries[4]->plots_signal_->histogramNvtx_numerator_, mvaEntries[4]->plots_signal_->histogramNvtx_denominator_, mvaEntries[4]->legendEntry_,
    "N_{vtx}", -4., 39.,
    false, 0.2, 1.4, "Efficiency",
    0.6, 0.7, 
    "plots/plotAntiElectronMVAEfficiency_vs_Nvtx.png");


  showEfficiency("Z #rightarrow ee", 600, 600,
    mvaEntries[0]->plots_background_->histogramPt_numerator_, mvaEntries[0]->plots_background_->histogramPt_denominator_, mvaEntries[0]->legendEntry_,
    mvaEntries[1]->plots_background_->histogramPt_numerator_, mvaEntries[1]->plots_background_->histogramPt_denominator_, mvaEntries[1]->legendEntry_,
    mvaEntries[2]->plots_background_->histogramPt_numerator_, mvaEntries[2]->plots_background_->histogramPt_denominator_, mvaEntries[2]->legendEntry_,
    mvaEntries[3]->plots_background_->histogramPt_numerator_, mvaEntries[3]->plots_background_->histogramPt_denominator_, mvaEntries[3]->legendEntry_,
    mvaEntries[4]->plots_background_->histogramPt_numerator_, mvaEntries[4]->plots_background_->histogramPt_denominator_, mvaEntries[4]->legendEntry_,
    "P_{T} / GeV", 10., 130.,
    true, 1.e-5, 10., "Fake-rate",
    0.6, 0.7,
    "plots/plotAntiElectronMVAFakeRate_vs_Pt.png");

  showEfficiency("Z #rightarrow ee", 600, 600,
    mvaEntries[0]->plots_background_->histogramEta_numerator_, mvaEntries[0]->plots_background_->histogramEta_denominator_, mvaEntries[0]->legendEntry_,
    mvaEntries[1]->plots_background_->histogramEta_numerator_, mvaEntries[1]->plots_background_->histogramEta_denominator_, mvaEntries[1]->legendEntry_,
    mvaEntries[2]->plots_background_->histogramEta_numerator_, mvaEntries[2]->plots_background_->histogramEta_denominator_, mvaEntries[2]->legendEntry_,
    mvaEntries[3]->plots_background_->histogramEta_numerator_, mvaEntries[3]->plots_background_->histogramEta_denominator_, mvaEntries[3]->legendEntry_,
    mvaEntries[4]->plots_background_->histogramEta_numerator_, mvaEntries[4]->plots_background_->histogramEta_denominator_, mvaEntries[4]->legendEntry_,
    "#eta", -2.9, 2.9,
    true, 1.e-5, 10., "Fake-rate",
    0.6, 0.7,
    "plots/plotAntiElectronMVAFakeRate_vs_Eta.png");

  showEfficiency("Z #rightarrow ee", 600, 600,
    mvaEntries[0]->plots_background_->histogramNvtx_numerator_, mvaEntries[0]->plots_background_->histogramNvtx_denominator_, mvaEntries[0]->legendEntry_,
    mvaEntries[1]->plots_background_->histogramNvtx_numerator_, mvaEntries[1]->plots_background_->histogramNvtx_denominator_, mvaEntries[1]->legendEntry_,
    mvaEntries[2]->plots_background_->histogramNvtx_numerator_, mvaEntries[2]->plots_background_->histogramNvtx_denominator_, mvaEntries[2]->legendEntry_,
    mvaEntries[3]->plots_background_->histogramNvtx_numerator_, mvaEntries[3]->plots_background_->histogramNvtx_denominator_, mvaEntries[3]->legendEntry_,
    mvaEntries[4]->plots_background_->histogramNvtx_numerator_, mvaEntries[4]->plots_background_->histogramNvtx_denominator_, mvaEntries[4]->legendEntry_,
    "N_{vtx}", -4., 39.,
    true, 1.e-5, 10., "Fake-rate",
    0.6, 0.7,
    "plots/plotAntiElectronMVAFakeRate_vs_Nvtx.png");


//--- normalize histograms and plot single distributions (pT, eta, Nvtx)
  for ( std::vector<mvaEntryType*>::iterator mvaEntry = mvaEntries.begin();
	mvaEntry != mvaEntries.end(); ++mvaEntry ) {

    normalizeHistogram((*mvaEntry)->plots_signal_->histogramPt_numerator_);
    normalizeHistogram((*mvaEntry)->plots_signal_->histogramPt_denominator_);
    normalizeHistogram((*mvaEntry)->plots_signal_->histogramEta_numerator_);
    normalizeHistogram((*mvaEntry)->plots_signal_->histogramEta_denominator_);
    normalizeHistogram((*mvaEntry)->plots_signal_->histogramNvtx_numerator_);
    normalizeHistogram((*mvaEntry)->plots_signal_->histogramNvtx_denominator_);

    normalizeHistogram((*mvaEntry)->plots_background_->histogramPt_numerator_);
    normalizeHistogram((*mvaEntry)->plots_background_->histogramPt_denominator_);
    normalizeHistogram((*mvaEntry)->plots_background_->histogramEta_numerator_);
    normalizeHistogram((*mvaEntry)->plots_background_->histogramEta_denominator_);
    normalizeHistogram((*mvaEntry)->plots_background_->histogramNvtx_numerator_);
    normalizeHistogram((*mvaEntry)->plots_background_->histogramNvtx_denominator_);

    showDistribution("", 600, 600,
      (*mvaEntry)->plots_signal_->histogramPt_denominator_, "Signal",
      (*mvaEntry)->plots_background_->histogramPt_denominator_, "Background",
      "P_{T} / GeV",
      true, 1.e-3, 1., "a.u.",
      0.6, 0.78,
      TString(Form("plots/plotAntiElectronMVAEfficiency_and_FakeRate_denominatorPt_%s.png", (*mvaEntry)->legendEntry_.data())).ReplaceAll(" ", "").Data());

    showDistribution("", 600, 600,
      (*mvaEntry)->plots_signal_->histogramEta_denominator_, "Signal",
      (*mvaEntry)->plots_background_->histogramEta_denominator_, "Background",
      "#eta",
      true, 1.e-3, 1., "a.u.",
      0.6, 0.78,
      TString(Form("plots/plotAntiElectronMVAEfficiency_and_FakeRate_denominatorEta_%s.png", (*mvaEntry)->legendEntry_.data())).ReplaceAll(" ", "").Data());

    showDistribution("", 600, 600,
      (*mvaEntry)->plots_signal_->histogramNvtx_denominator_, "Signal",
      (*mvaEntry)->plots_background_->histogramNvtx_denominator_, "Background",
      "N_{vtx}",
      true, 1.e-5, 1., "a.u.",
      0.6, 0.78,
      TString(Form("plots/plotAntiElectronMVAEfficiency_and_FakeRate_denominatorNvtx_%s.png", (*mvaEntry)->legendEntry_.data())).ReplaceAll(" ", "").Data());

/*
    TGraph* graphEffEq40percent = compMVAcut((*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_signal_->histogramPt_, 0.40);
    TGraph* graphEffEq50percent = compMVAcut((*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_signal_->histogramPt_, 0.50);
    TGraph* graphEffEq60percent = compMVAcut((*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_signal_->histogramPt_, 0.60);
    TGraph* graphEffEq70percent = compMVAcut((*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_signal_->histogramPt_, 0.70);
    TGraph* graphEffEq80percent = compMVAcut((*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_signal_->histogramPt_, 0.80);
    TGraph* graphEffEq90percent = compMVAcut((*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_signal_->histogramPt_, 0.90);

    showGraphs("#tau_{had} Efficiency", 600, 600,
      graphEffEq90percent, "90%",
      graphEffEq80percent, "80%",
      graphEffEq70percent, "70%",
      graphEffEq60percent, "60%",
      graphEffEq50percent, "50%",
      graphEffEq40percent, "40%",
      0., 100., 10, "P_{T} / GeV",
      0.0, 1.0, "MVA_{cut}",
      0.55, 0.2,
      TString(Form("plots/plotAntiElectronMVAEfficiency_MVAcutVsPtConstEfficiency_%s.png", (*mvaEntry)->legendEntry_.data())).ReplaceAll(" ", "").Data());

    std::string outputFileName_MVAoutput_vs_Pt = Form("plots/plotAntiElectronMVAEfficiency_and_FakeRate_MVAoutput_vs_Pt_%s.root", "MVA");
    TFile* outputFile_MVAoutput_vs_Pt = new TFile(outputFileName_MVAoutput_vs_Pt.data(), "RECREATE");
    (*mvaEntry)->plots_signal_->histogramMVAoutput_vs_Pt_->Write();
    delete outputFile_MVAoutput_vs_Pt;

    std::string outputFileName_effGraphs = Form("plots/wpDiscriminationByIsolationMVA3_%s.root", "MVA");
    graphEffEq90percent->SetName("MVAEff90");
    graphEffEq80percent->SetName("MVAEff80");
    graphEffEq70percent->SetName("MVAEff70");
    graphEffEq60percent->SetName("MVAEff60");
    graphEffEq50percent->SetName("MVAEff50");
    graphEffEq40percent->SetName("MVAEff40");      
    TFile* outputFile_effGraphs = new TFile(outputFileName_effGraphs.data(), "RECREATE");
    graphEffEq90percent->Write();
    graphEffEq80percent->Write();
    graphEffEq70percent->Write();
    graphEffEq60percent->Write();
    graphEffEq50percent->Write();
    graphEffEq40percent->Write();
    (*mvaEntry)->plots_signal_->histogramPt_numerator_->Write();
    (*mvaEntry)->plots_signal_->histogramPt_denominator_->Write();
    (*mvaEntry)->plots_signal_->histogramEta_numerator_->Write();
    (*mvaEntry)->plots_signal_->histogramEta_denominator_->Write();
    (*mvaEntry)->plots_background_->histogramPt_numerator_->Write();
    (*mvaEntry)->plots_background_->histogramPt_denominator_->Write();
    (*mvaEntry)->plots_background_->histogramEta_numerator_->Write();
    (*mvaEntry)->plots_background_->histogramEta_denominator_->Write();
    delete outputFile_effGraphs;

    TGraph* graphFakeRateEq001percent = compMVAcut((*mvaEntry)->plots_background_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_background_->histogramPt_, 0.001);
    TGraph* graphFakeRateEq002percent = compMVAcut((*mvaEntry)->plots_background_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_background_->histogramPt_, 0.002);
    TGraph* graphFakeRateEq005percent = compMVAcut((*mvaEntry)->plots_background_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_background_->histogramPt_, 0.005);
    TGraph* graphFakeRateEq010percent = compMVAcut((*mvaEntry)->plots_background_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_background_->histogramPt_, 0.010);
    TGraph* graphFakeRateEq020percent = compMVAcut((*mvaEntry)->plots_background_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_background_->histogramPt_, 0.020);
    TGraph* graphFakeRateEq050percent = compMVAcut((*mvaEntry)->plots_background_->histogramMVAoutput_vs_Pt_, (*mvaEntry)->plots_background_->histogramPt_, 0.050);
    
    showGraphs("#tau_{had} Fake-rate", 600, 600,
      graphFakeRateEq050percent, "5%",
      graphFakeRateEq020percent, "2%",
      graphFakeRateEq010percent, "1%",
      graphFakeRateEq005percent, "0.5%",
      graphFakeRateEq002percent, "0.2%",
      graphFakeRateEq001percent, "0.1%",
      0., 100., 10, "P_{T} / GeV",
      0.0, 1.0, "MVA_{cut}",
      0.55, 0.2, 
      TString(Form("plots/plotAntiElectronMVAEfficiency_MVAcutVsPtConstFakeRate_%s.png", (*mvaEntry)->legendEntry_.data())).ReplaceAll(" ", "").Data());
*/
  }


  for ( std::vector<mvaEntryType*>::iterator it = mvaEntries.begin();
	it != mvaEntries.end(); ++it ) {
    delete (*it);
  }
}
