### python3

import ROOT
import glob


# categories = ["cat_baseline" , "cat_resolved_1b" , "cat_resolved_2b" , "cat_boosted_l" , "cat_boosted_m"]
categories = ["cat_resolved_1b_inv"]
datasets = ["data_etau", "data_mutau", "data_tau", "data_met", "tt_dl", "tt_sl", "tt_fh", "tth_bb", "tth_nonbb", "tth_tautau",
            "dy", "dy_0j", "dy_1j", "dy_2j", "dy_PtZ_0To50", "dy_PtZ_50To100", "dy_PtZ_100To250", "dy_PtZ_250To400", 
            "dy_PtZ_400To650", "dy_PtZ_650ToInf", "ST_tW_top", "ST_tW_antitop", "WJets_HT0To70", "WJets_HT70To100", 
            "WJets_HT100To200", "WJets_HT200To400", "WJets_HT400To600", "WJets_HT600To800", "WJets_HT800To1200", 
            "WJets_HT1200To2500", "WJets_HT2500ToInf", "EWKWMinus2Jets_WToLNu", "EWKWPlus2Jets_WToLNu", "EWKZ2Jets_ZToLL", 
            "ST_t-channel_top", "ST_t-channel_antitop", "WW", "WZ", "ZZ", "TTZZ", "TTWW", "TTWZ", "TTWH", "TTZH", 
            "TTWJetsToLNu", "TTWJetsToQQ", "TTZToLLNuNu", "TTZToQQ", "GluGluHToTauTau", "VBFHToTauTau", "WWW", "WZZ", 
            "ZZZ", "WWZ", "WminusHToTauTau", "WplusHToTauTau", "ZH_HToBB_ZToLL", "ZH_HToBB_ZToQQ", "ZHToTauTau"]

# datasets = ["data_etau", "data_mutau", "data_tau", "data_met", "tt_dl", "tt_sl", "tt_fh", "tth_bb", "tth_nonbb", "tth_tautau",
#             "dy", "dy_0j", "dy_1j", "dy_2j", "dy_PtZ_0To50", "dy_PtZ_50To100", "dy_PtZ_100To250", "dy_PtZ_250To400", 
#             "dy_PtZ_400To650", "dy_PtZ_650ToInf", "ST_tW_top", "ST_tW_antitop", "WJets_HT0To70", "WJets_HT70To100", 
#             "WJets_HT100To200", "WJets_HT200To400", "WJets_HT400To600", "WJets_HT600To800", "WJets_HT800To1200", 
#             "WJets_HT1200To2500", "WJets_HT2500ToInf", "EWKWMinus2Jets_WToLNu", "EWKWPlus2Jets_WToLNu", "EWKZ2Jets_ZToLL", 
#             "ST_tchannel_top", "ST_tchannel_antitop", "WW", "WZ", "ZZ", "TTZZ", "TTWW", "TTWZ", "TTWH", "TTZH", 
#             "TTWJetsToLNu", "TTWJetsToQQ", "TTZToLLNuNu", "TTZToQQ", "GluGluHToTauTau", "VBFHToTauTau", "WWW", "WZZ", 
#             "ZZZ", "WWZ", "WminusHToTauTau", "WplusHToTauTau", "ZH_HToBB_ZToLL", "ZH_HToBB_ZToQQ", "ZHToTauTau"]
# datasets = ["dy_1j"]

# datasets = ["data_etau"]
# datasets = ["tt_sl", "tt_fh"]

### version for cat_resolved_1b_inv 2018 : 10 Apr
### version for 2017
# categories = ["cat_resolved_1b_inv"]
# datasets = ["data_etau"]
### version for 2016


for cat in categories:
    # pbar = tqdm(datasets, bar_format="{l_bar}%s{bar}%s{r_bar}" % ('\033[32m', '\033[0m'), desc="Processing Datasets")
    for dataset in datasets:

        ##### 2018
        # folder = "/eos/user/e/emartinv/cmt/MergeCategorization/qcd_llr_2018/" + dataset + "/" + cat + "/10Apr/"
        ##### 2017
        # folder = "/eos/user/e/emartinv/cmt/MergeCategorization/qcd_llr_2017/" + dataset + "/" + cat + "/20Apr/"
        ##### 2016
        folder = "/eos/user/e/emartinv/cmt/MergeCategorization/qcd_llr_2016/" + dataset + "/" + cat + "/20Apr/"
        
        
        input_files = glob.glob(folder + "data_*.root")

        for input_file_name in input_files:

            print("Input file", input_file_name)
                
            file = ROOT.TFile.Open(input_file_name)
            if not file or file.IsZombie():
                print("Error: No se pudo abrir el archivo de entrada", input_file_name)
                continue

            if not file.GetListOfKeys().Contains("HTauTauTree"):
                print(f'File "{input_file_name}" does not contain "HTauTauTree" tree : skiping filtering')
                continue

            tree = file.Get("HTauTauTree")

            # Crea un RDataFrame a partir del tree
            rdf = ROOT.RDataFrame(tree)

            condition = "(isLeptrigger || isMETtrigger || isSingleTautrigger)"

            filtered_rdf = rdf.Filter(condition)

            # Guarda el RDataFrame filtrado en un nuevo archivo .root
            # new_file = filtered_rdf.Snapshot("HTauTauTree", input_file_name.replace(".root", "_filtered.root"))
            new_file = filtered_rdf.Snapshot("HTauTauTree", input_file_name)

            # Cierra los archivos .root
            file.Close()
