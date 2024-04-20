from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import os
import re

from config.llr_2018 import Config as base_config

class Config(base_config):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.btag=DotDict(tight=0.7264, medium=0.2783, loose=0.0490) # DeepJet WP from KLUB framework https://github.com/LLRCMS/KLUBAnalysis/blob/master/config/selectionCfg_MuTau_UL18.cfg 
        self.pnet=DotDict(tight=0.988, medium=0.9734, loose=0.9172) # PNet WP from KLUB framework
        self.deeptau=DotDict(
            vsjet=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                          Tight=6, VTight=7, VVTight=8),
            vse=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vsmu=DotDict(VLoose=1, Loose=1, Medium=3, Tight=4),
        )
        self.regions = self.add_regions()
        self.categories = self.add_categories(btag="bjet{}_bID_deepFlavor")
        # self.skipped_files_must_be_in_dataset = False # This and the tree name must be changed at analysis_tools/dataset.py


    def add_categories(self, **kwargs):
        categories = super(Config, self).add_categories(**kwargs)
        sel = DotDict()
        btag = kwargs.pop("btag", "bjet{}_bID_deepFlavor")
        pnet = kwargs.pop("pnet", "fatjet_particleNetMDJetTags_score")
        df = lambda i, op, wp: "{} {} {}".format(btag.format(i), op, self.btag[wp])
        df_pnet = lambda op, wp: "{} {} {}".format(pnet, op, self.pnet[wp])
        sel["btag"] = DotDict(
            m_first=[df(1, ">", "medium")],
            m_second=[df(2, ">", "medium")],
            m_any=[jrs(df(1, ">", "medium"), df(2, ">", "medium"), op="or")],
            l=[df(1, ">", "loose"), df(2, "<", "loose")],
            ll=[df(1, ">", "loose"), df(2, ">", "loose")],
            m=[jrs(jrs(df(1, ">", "medium"), df(2, "<", "medium"), op="and"),
                jrs(df(1, "<", "medium"), df(2, ">", "medium"), op="and"), op="or")],
            mm=[df(1, ">", "medium"), df(2, ">", "medium")],
            not_mm=[df(1, "<", "medium"), df(2, "<", "medium")],
        )
        sel["pnet"] = DotDict(
            l=[df_pnet(">", "loose")],
            m=[df_pnet(">", "medium")],
        )

        baseline = ["pairType >= 0 && pairType <= 2 && nbjetscand > 1 && nleps == 0"]
        baseline_boosted = ["pairType >= 0 && pairType <= 2 && nleps == 0 && isBoosted == 1"]
        
        massCut = ["{{Hbb_mass}} > 50 && {{Hbb_mass}} < 270 && {{Htt_mass}} > 20 && {{Htt_mass}} < 130"]
        massCutInv = ["{{Hbb_mass}} < 50 || {{Hbb_mass}} > 270 || {{Htt_mass}} < 20 || {{Htt_mass}} > 130"]
        
        sel["resolved_1b_llr"] = DotDict({
            ch: (sel.btag.m + massCut + ["isBoosted != 1"]
                + baseline)
            for ch in self.channels.names()
        })
        sel["resolved_1b_llr_combined"] = self.join_selection_channels(sel["resolved_1b_llr"])
        sel["resolved_2b_llr"] = DotDict({
            ch: (sel.btag.mm + massCut + ["isBoosted != 1"]
            + baseline)
            for ch in self.channels.names()
        })
        sel["resolved_2b_llr_combined"] = self.join_selection_channels(sel["resolved_2b_llr"])
        
        sel["resolved_1b_llr_inv"] = DotDict({
            ch: (sel.btag.m + massCutInv + ["isBoosted != 1"]
                + baseline)
            for ch in self.channels.names()
        })
        sel["resolved_1b_llr_combined_inv"] = self.join_selection_channels(sel["resolved_1b_llr_inv"])

        sel["boosted_l_llr"] = DotDict({
            ch: (sel.pnet.l + baseline_boosted)
            for ch in self.channels.names()
        })
        sel["boosted_l_llr_combined"] = self.join_selection_channels(sel["boosted_l_llr"])
        sel["boosted_m_llr"] = DotDict({
            ch: (sel.pnet.m + baseline_boosted)
            for ch in self.channels.names()
        })
        sel["boosted_m_llr_combined"] = self.join_selection_channels(sel["boosted_m_llr"])

        categories.get("baseline").selection = "pairType >= 0 && pairType <= 2 && nbjetscand > 1 && nleps == 0"
        categories.get("baseline_boosted").selection = "pairType >= 0 && pairType <= 2 && nleps == 0 && isBoosted == 1"
        categories.get("resolved_1b").selection = sel["resolved_1b_llr_combined"]
        categories.get("resolved_2b").selection = sel["resolved_2b_llr_combined"]
        categories.get("resolved_1b_inv").selection = sel["resolved_1b_llr_combined_inv"]
        categories.get("boosted_l").selection = sel["boosted_l_llr_combined"]
        categories.get("boosted_m").selection = sel["boosted_m_llr_combined"]
        return categories



    #     self.processes, self.process_group_names, self.process_training_names = self.add_processes()

    # def add_processes(self):
    #     processes, process_group_names, process_training_names = super(Config, self).add_processes()
    #     processes_qcd = [
    #         Process("dy", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #     ]
    #     for process in processes_qcd:
    #         processes.add(process)
    #     # print(processes)
        
    #     process_group_names = {
    #         "default": [
    #             # "ggf_sm",
    #         ]

    #     }
    #     # print(process_group_names)

    #     # process_group_names = super(Config, self).add_process_group_names()
    #     # process_training_names = super(Config, self).add_process_training_names()  
    #     return ObjectCollection(processes), process_group_names, process_training_names
        
    def add_datasets(self):
        skim_directory = "/eos/user/l/lportale/hhbbtautau/skims/SKIMS_UL18"

        skimdatasets = {
            "dy":"DY_Incl",
            "dy_0j":"DY_0J",
            "dy_1j":"DY_1J",
            "dy_2j":"DY_2J",
            "dy_PtZ_0To50":"DY_PtZ0To50",
            "dy_PtZ_50To100":"DY_PtZ50To100",
            "dy_PtZ_100To250":"DY_PtZ100To250",
            "dy_PtZ_250To400":"DY_PtZ250To400",
            "dy_PtZ_400To650":"DY_PtZ400To650",
            "dy_PtZ_650ToInf":"DY_PtZ650ToInf",
            "tt_dl":"TT_FullyLep",
            "tt_sl":"TT_SemiLep",
            "tt_fh":"TT_Hadronic",
            "tth_bb":"ttHTobb",
            "tth_nonbb":"ttHToNonbb",
            "tth_tautau":"ttHToTauTau",
            "data_mutau": "Muon",
            "data_etau":"EGamma",
            "data_tau":"Tau",
            "ST_tW_top":"ST_tW_top",
            "ST_tW_antitop":"ST_tW_antitop",
            "WJets_HT0To70": "WJets_HT0To70", 
            "WJets_HT70To100": "WJets_HT70To100", 
            "WJets_HT100To200": "WJets_HT100To200", 
            "WJets_HT200To400": "WJets_HT200To400",
            "WJets_HT400To600": "WJets_HT400To600", 
            "WJets_HT600To800": "WJets_HT600To800", 
            "WJets_HT800To1200": "WJets_HT800To1200", 
            "WJets_HT1200To2500": "WJets_HT1200To2500", 
            "WJets_HT2500ToInf": "WJets_HT2500ToInf",
            "EWKWMinus2Jets_WToLNu": "EWKWMinus2Jets_WToLNu",
            "EWKWPlus2Jets_WToLNu": "EWKWPlus2Jets_WToLNu",
            "EWKZ2Jets_ZToLL": "EWKZ2Jets_ZToLL",
            "ST_t-channel_top": "ST_t-channel_top",
            "ST_t-channel_antitop": "ST_t-channel_antitop",
            "WW": "WW",
            "WZ": "WZ",
            "ZZ": "ZZ",
            "TTZZ": "TTZZ",
            "TTWW": "TTWW",
            "TTWZ": "TTWZ",
            "TTWH": "TTWH",
            "TTZH": "TTZH",
            "TTWJetsToLNu": "TTWJetsToLNu",
            "TTWJetsToQQ": "TTWJetsToQQ",
            "TTZToLLNuNu": "TTZToLLNuNu",
            "TTZToQQ": "TTZToQQ",
            "GluGluHToTauTau": "GluGluHToTauTau",
            "VBFHToTauTau": "VBFHToTauTau",
            "WWW": "WWW",
            "WZZ": "WZZ",
            "ZZZ": "ZZZ",
            "WWZ": "WWZ",
            "WminusHToTauTau": "WminusHToTauTau",
            "WplusHToTauTau": "WplusHToTauTau",
            "ZH_HToBB_ZToLL": "ZH_HToBB_ZToLL",
            "ZH_HToBB_ZToQQ": "ZH_HToBB_ZToQQ",
            "ZHToTauTau":"ZHToTauTau",


        }
        skipFiles_dict = {}

        for dataset_name, dataset in skimdatasets.items():
            skipFiles = []
            if dataset_name in ["data_etau", "data_mutau", "data_tau"]:
                
                for era in ["A", "B", "C", "D"]:
                    folder = os.path.join(skim_directory, dataset + era)
                    goodfiles = os.path.join(folder, "goodfiles.txt")

                    if os.path.exists(goodfiles):
                        with open(goodfiles, "r") as f:
                            goodfiles = f.read().splitlines()
                        goodfiles = [re.search('output_(.*).root', file).group(1) for file in goodfiles]
                        allfiles = [re.search('output_(.*).root', file).group(1) for file in os.listdir(folder) if file.endswith('.root')]

                        skipFiles += [os.path.join(folder, f"output_{file}.root") for file in allfiles if file not in goodfiles]
            else:
                folder = os.path.join(skim_directory, dataset)
                goodfiles = os.path.join(folder, "goodfiles.txt")

                if os.path.exists(goodfiles):
                    with open(goodfiles, "r") as f:
                        goodfiles = f.read().splitlines()
                    goodfiles = [re.search('output_(.*).root', file).group(1) for file in goodfiles]
                    allfiles = [re.search('output_(.*).root', file).group(1) for file in os.listdir(folder) if file.endswith('.root')]

                    skipFiles = [os.path.join(folder, f"output_{file}.root") for file in allfiles if file not in goodfiles]
            
                else:
                    skipFiles = []

            skipFiles_dict[dataset_name] = skipFiles   

        # print("SKIPFILES dict", skipFiles_dict)
                
        datasets = [
            Dataset("rad250",
                folder=os.path.join(skim_directory, "Rad250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad260",
                folder=os.path.join(skim_directory, "Rad260"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad270",
                folder=os.path.join(skim_directory, "Rad270"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad280",
                folder=os.path.join(skim_directory, "Rad280"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad300",
                folder=os.path.join(skim_directory, "Rad300"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad320",
                folder=os.path.join(skim_directory, "Rad320"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad350",
                folder=os.path.join(skim_directory, "Rad350"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad400",
                folder=os.path.join(skim_directory, "Rad400"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad450",
                folder=os.path.join(skim_directory, "Rad450"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad500",
                folder=os.path.join(skim_directory, "Rad500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad550",
                folder=os.path.join(skim_directory, "Rad550"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad600",
                folder=os.path.join(skim_directory, "Rad600"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad650",
                folder=os.path.join(skim_directory, "Rad650"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad700",
                folder=os.path.join(skim_directory, "Rad700"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad750",
                folder=os.path.join(skim_directory, "Rad750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad800",
                folder=os.path.join(skim_directory, "Rad800"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad850",
                folder=os.path.join(skim_directory, "Rad850"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad900",
                folder=os.path.join(skim_directory, "Rad900"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad1000",
                folder=os.path.join(skim_directory, "Rad1000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad1250",
                folder=os.path.join(skim_directory, "Rad1250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad1500",
                folder=os.path.join(skim_directory, "Rad1500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad1750",
                folder=os.path.join(skim_directory, "Rad1750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad2000",
                folder=os.path.join(skim_directory, "Rad2000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad2500",
                folder=os.path.join(skim_directory, "Rad2500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("rad3000",
                folder=os.path.join(skim_directory, "Rad3000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav250",
                folder=os.path.join(skim_directory, "Grav250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav260",
                folder=os.path.join(skim_directory, "Grav260"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav270",
                folder=os.path.join(skim_directory, "Grav270"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav280",
                folder=os.path.join(skim_directory, "Grav280"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav300",
                folder=os.path.join(skim_directory, "Grav300"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav320",
                folder=os.path.join(skim_directory, "Grav320"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav350",
                folder=os.path.join(skim_directory, "Grav350"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav400",
                folder=os.path.join(skim_directory, "Grav400"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.), 
            Dataset("grav450",
                folder=os.path.join(skim_directory, "Grav450"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav500",
                folder=os.path.join(skim_directory, "Grav500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav550",
                folder=os.path.join(skim_directory, "Grav550"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav600",
                folder=os.path.join(skim_directory, "Grav600"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav650",
                folder=os.path.join(skim_directory, "Grav650"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav700",
                folder=os.path.join(skim_directory, "Grav700"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav750",
                folder=os.path.join(skim_directory, "Grav750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav800",
                folder=os.path.join(skim_directory, "Grav800"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav850",
                folder=os.path.join(skim_directory, "Grav850"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav900",
                folder=os.path.join(skim_directory, "Grav900"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav1000",
                folder=os.path.join(skim_directory, "Grav1000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav1250",
                folder=os.path.join(skim_directory, "Grav1250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav1500",
                folder=os.path.join(skim_directory, "Grav1500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav1750",
                folder=os.path.join(skim_directory, "Grav1750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav2000",
                folder=os.path.join(skim_directory, "Grav2000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav2500",
                folder=os.path.join(skim_directory, "Grav2500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("grav3000",
                folder=os.path.join(skim_directory, "Grav3000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tt_dl",
                folder=os.path.join(skim_directory, "TT_FullyLep"),
                process=self.processes.get("tt_dl"),
                file_pattern="output_.*root",
                merging={
                    "boosted_l": 5,
                    "boosted_m": 5,
                },
                xs=1.),             
            Dataset("tt_sl",
                folder=os.path.join(skim_directory, "TT_SemiLep"),
                process=self.processes.get("tt_sl"),
                file_pattern="output_.*root",
                merging={
                    "tautau": 20,
                    "mutau": 60,
                    "etau": 40,
                    "baseline": 10,
                    "boosted_l": 10,
                    "boosted_m": 10,
                },
                xs=1.),
            Dataset("tt_fh",
                folder=os.path.join(skim_directory, "TT_Hadronic"),
                process=self.processes.get("tt_fh"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy",
                folder=os.path.join(skim_directory, "DY_Incl"),
                process=self.processes.get("dy"),
                file_pattern="output_.*root",
                skipFiles=skipFiles_dict["dy"],
                xs=1.),
            Dataset("dy_0j",
                folder=os.path.join(skim_directory, "DY_0J"),
                process=self.processes.get("dy_0j"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_1j",
                folder=os.path.join(skim_directory, "DY_1J"),
                process=self.processes.get("dy_1j"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_2j",
                folder=os.path.join(skim_directory, "DY_2J"),
                process=self.processes.get("dy_2j"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_0To50",
                folder=os.path.join(skim_directory, "DY_PtZ0To50"),
                process=self.processes.get("dy_PtZ_0To50"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_50To100",
                folder=os.path.join(skim_directory, "DY_PtZ50To100"),
                process=self.processes.get("dy_PtZ_50To100"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_100To250",
                folder=os.path.join(skim_directory, "DY_PtZ100To250"),
                process=self.processes.get("dy_PtZ_100To250"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_250To400",
                folder=os.path.join(skim_directory, "DY_PtZ250To400"),
                process=self.processes.get("dy_PtZ_250To400"),
                skipFiles=skipFiles_dict["dy_PtZ_250To400"],
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_400To650",
                folder=os.path.join(skim_directory, "DY_PtZ400To650"),
                process=self.processes.get("dy_PtZ_400To650"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_650ToInf",
                folder=os.path.join(skim_directory, "DY_PtZ650ToInf"),
                process=self.processes.get("dy_PtZ_650ToInf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tth_bb",
                folder=os.path.join(skim_directory, "ttHTobb"),
                process=self.processes.get("tth_bb"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tth_nonbb",
                folder=os.path.join(skim_directory, "ttHToNonbb"),
                process=self.processes.get("tth_nonbb"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tth_tautau",
                folder=os.path.join(skim_directory, "ttHToTauTau"),
                process=self.processes.get("tth_tautau"),
                file_pattern="output_.*root",
                xs=1.),
            #### DATA
            Dataset("data_mutau",
                folder=[os.path.join(skim_directory, "Muon%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 0",
                process=self.processes.get("data_mutau"),
                file_pattern="output_.*root",
                # merging={
                #     "mutau": 40,
                # },
                xs=1.),
            Dataset("data_etau",
                # folder=os.path.join(skim_directory, "SKIM_SingleMuon_Run2018A"),
                folder=[os.path.join(skim_directory, "EGamma%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 1",
                process=self.processes.get("data_etau"),
                file_pattern="output_.*root",
                # merging={
                #     "etau": 1,
                # },
                xs=1.),
            Dataset("data_tau",
                # folder=os.path.join(skim_directory, "SKIM_SingleMuon_Run2018A"),
                folder=[os.path.join(skim_directory, "Tau%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 2",
                process=self.processes.get("data_tau"),
                file_pattern="output_.*root",
                # merging={
                #     "mutau": 20,
                # },
                xs=1.),
            # Dataset("data_MET",
            #     folder=[os.path.join(skim_directory, "MET_Run2018%s" % era)
            #         for era in ["A", "B", "C", "D"]],
            #     process=self.processes.get("data_MET"),
            #     file_pattern="output_.*root",
            #     xs=1.),

        ]
        other_backgrounds = {
            "wjets": [
                "WJets_HT0To70", "WJets_HT70To100", "WJets_HT100To200", "WJets_HT200To400", 
                "WJets_HT400To600", "WJets_HT600To800", "WJets_HT800To1200", "WJets_HT1200To2500", "WJets_HT2500ToInf",
            ],
            "ewk": [
                "EWKWMinus2Jets_WToLNu", "EWKWPlus2Jets_WToLNu", "EWKZ2Jets_ZToLL",
            ],
            "singlet": [
                "ST_t-channel_antitop", "ST_t-channel_top",
            ],
            "tw": [
                "ST_tW_antitop", "ST_tW_top",
            ],
            "zh": [
                "ZH_HToBB_ZToLL", "ZHToTauTau", "ZH_HToBB_ZToQQ"
            ],
            "wh": [
                "WminusHToTauTau", "WplusHToTauTau",
            ],
            "vv": [
                "WW",  
                "WZ",  
                "ZZ",  
            ],
            "ttx": [
                "TTZZ", "TTWW", "TTWZ", "TTWH", "TTZH", "TTWJetsToLNu", "TTWJetsToQQ", "TTZToLLNuNu", "TTZToQQ"
            ],
            "ggh": [
                "GluGluHToTauTau",
            ],
            "vbfh": [
                "VBFHToTauTau",
            ],
            "vvv": [
                "WWW", "WZZ", "ZZZ", "WWZ",
            ]
        }

        for process, minor_datasets in other_backgrounds.items():
            for name in minor_datasets:
                datasets.append(
                    Dataset(name,
                        folder=os.path.join(skim_directory, "%s" % name),
                        process=self.processes.get(process),
                        file_pattern="output_.*root",
                        skipFiles=skipFiles_dict[name],
                        xs=1.),  # already normalised to xs
                )
                print("process", self.processes.get(process))
        return ObjectCollection(datasets)

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"
        weights.total_events_weights = ["MC_weight", "PUReweight", "L1pref_weight", "trigSF", "IdFakeSF_deep_2d", "PUjetID_SF", "bTagweightReshape"]
        weights.base = ["MC_weight", "PUReweight", "L1pref_weight", "trigSF", "IdFakeSF_deep_2d", "PUjetID_SF", "bTagweightReshape"]
        weights.baseline = weights.base
        weights.resolved_1b = weights.base
        weights.resolved_2b = weights.base
        weights.resolved_1b_inv = weights.base
        weights.boosted_l = weights.base
        weights.boosted_m = weights.base
        return weights



config = Config("qcd_llr_2018", year=2018, ecm=13, lumi_pb=59741)