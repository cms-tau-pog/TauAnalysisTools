#ifndef RecoTauTag_TauAnalysisTools_GBRForestWriter_h
#define RecoTauTag_TauAnalysisTools_GBRForestWriter_h

/** \class GBRForestWriter
 *
 * Read GBRForest objects from ROOT file input
 * and store it in SQL-lite output file
 *
 * \author Christian Veelken, LLR
 *
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <vector>
#include <string>

class GBRForestWriter : public edm::EDAnalyzer
{
 public:
  GBRForestWriter(const edm::ParameterSet&);
  ~GBRForestWriter();

 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);

  std::string moduleLabel_;

  bool hasRun_;

  typedef std::vector<std::string> vstring;

  struct categoryEntryType
  {
    categoryEntryType(const edm::ParameterSet& cfg)
    {
      if ( cfg.existsAs<edm::FileInPath>("inputFileName") )
      {
        edm::FileInPath inputFileName_fip = cfg.getParameter<edm::FileInPath>("inputFileName");
        if ( inputFileName_fip.location()!=edm::FileInPath::Local)
          throw cms::Exception("GBRForestWriter") << " Failed to find File = " << inputFileName_fip << " !!\n";
        inputFileName_ = inputFileName_fip.fullPath();
      }
      else if ( cfg.existsAs<std::string>("inputFileName") )
	     inputFileName_ = cfg.getParameter<std::string>("inputFileName");
      else
        throw cms::Exception("GBRForestWriter") << " Undefined Configuration Parameter 'inputFileName !!\n";

      std::string inputFileType_string = cfg.getParameter<std::string>("inputFileType");
      if      ( inputFileType_string == "XML"       ) inputFileType_ = kInputXML;
      else if ( inputFileType_string == "GBRForest" ) inputFileType_ = kInputGBRForest;
      else throw cms::Exception("GBRForestWriter") << " Invalid Configuration Parameter 'inputFileType' = " << inputFileType_string << " !!\n";

      if ( inputFileType_ == kInputXML )
      {
      	inputVariables_ = cfg.getParameter<vstring>("inputVariables");
      	spectatorVariables_ = cfg.getParameter<vstring>("spectatorVariables");
      }

      gbrForestName_ = cfg.getParameter<std::string>("gbrForestName");
    }

    ~categoryEntryType() {}

    std::string inputFileName_;
    enum { kInputUndefined, kInputXML, kInputGBRForest };
    int inputFileType_;
    vstring inputVariables_;
    vstring spectatorVariables_;
    std::string gbrForestName_;
  };

  struct jobEntryType
  {
    jobEntryType(const edm::ParameterSet& cfg)
    {
      if ( cfg.exists("categories") )
      {
        edm::VParameterSet cfgCategories = cfg.getParameter<edm::VParameterSet>("categories");
        for ( edm::VParameterSet::const_iterator cfgCategory = cfgCategories.begin(); cfgCategory != cfgCategories.end(); ++cfgCategory )
        {
          categoryEntryType* category = new categoryEntryType(*cfgCategory);
          categories_.push_back(category);
        }
      }
      else
      {
        categoryEntryType* category = new categoryEntryType(cfg);
        categories_.push_back(category);
      }

      std::string outputFileType_string = cfg.getParameter<std::string>("outputFileType");
      if      ( outputFileType_string == "GBRForest" ) outputFileType_ = kOutputGBRForest;
      else if ( outputFileType_string == "SQLLite"   ) outputFileType_ = kOutputSQLLite;
      else throw cms::Exception("GBRForestWriter") << " Invalid Configuration Parameter 'outputFileType' = " << outputFileType_string << " !!\n";

      if ( outputFileType_ == kOutputGBRForest )
      outputFileName_ = cfg.getParameter<std::string>("outputFileName");

      if ( outputFileType_ == kOutputSQLLite )
      outputRecord_ = cfg.getParameter<std::string>("outputRecord");
    }

    ~jobEntryType()
    {
      for ( std::vector<categoryEntryType*>::iterator it = categories_.begin(); it != categories_.end(); ++it )
      	delete (*it);
    }

    std::vector<categoryEntryType*> categories_;
    enum { kOutputUndefined, kOutputGBRForest, kOutputSQLLite };
    int outputFileType_;
    std::string outputFileName_;
    std::string outputRecord_;
  };

  std::vector<jobEntryType*> jobs_;
};

#endif
