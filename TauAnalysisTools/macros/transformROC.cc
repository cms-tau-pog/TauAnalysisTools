void transformROC()
{
    TFile* finput  = new TFile("makeROCcurveTauIdMVA_all.root", "READ");
    TFile* foutput = new TFile("transformedROCcurves.root", "RECREATE");

    std::vector<TString> graphs;

    // Push the TGraphs
        // // recTauNphoton 0.5
        // graphs.push_back("mvaIsolation3HitsDeltaR05opt1aLTDB_TestTree_tauPtLt50");
        // graphs.push_back("mvaIsolation3HitsDeltaR05opt1aLTDB_TestTree_tauPt50to100");
        // graphs.push_back("mvaIsolation3HitsDeltaR05opt1aLTDB_TestTree_tauPt100to200");

        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPtLt50");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPt50to100");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPt100to200");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPt200to400");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPt400to600");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPt600to900");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPt900to1200");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree_tauPtGt1200");
        graphs.push_back("rawMVAoldDMwLT2016_TestTree");

        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPtLt50");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPt50to100");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPt100to200");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPt200to400");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPt400to600");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPt600to900");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPt900to1200");
        graphs.push_back("rawMVAoldDMwLT_TestTree_tauPtGt1200");
        graphs.push_back("rawMVAoldDMwLT_TestTree");

        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPtLt50");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPt50to100");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPt100to200");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPt200to400");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPt400to600");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPt600to900");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPt900to1200");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree_tauPtGt1200");
        graphs.push_back("rawMVAoldDMwLT2017v1_TestTree");

        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPtLt50");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPt50to100");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPt100to200");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPt200to400");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPt400to600");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPt600to900");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPt900to1200");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree_tauPtGt1200");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TestTree");

        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPtLt50");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPt50to100");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPt100to200");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPt200to400");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPt400to600");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPt600to900");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPt900to1200");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree_tauPtGt1200");
        graphs.push_back("mvaIsolation3HitsDeltaR05opt2aLTDB_1p0_TrainTree");

        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPtLt50");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPt50to100");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPt100to200");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPt200to400");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPt400to600");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPt600to900");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPt900to1200");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree_tauPtGt1200");
        graphs.push_back("rawMVAoldDMwLT2017v2_TestTree");


    for(unsigned iGraph = 0; iGraph < graphs.size(); iGraph++)
    {
        TGraph* graph = (TGraph*)finput->Get(graphs.at(iGraph));

        for(unsigned iPoint = 0; iPoint < graph->GetN(); iPoint++)
        {
            double x, y;
            graph->GetPoint(iPoint, x, y);
            graph->SetPoint(iPoint, x, 1. - y);
        }

        graph->Write();
    }
    foutput->Close();
}
