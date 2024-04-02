from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import os

from config.llr_2018 import Config as base_config

class Config(base_config):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.btag=DotDict(tight=0.73, medium=0.3196, loose=0.0614) # DeepJet WP From https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22EE/
        # self.btag=DotDict(tight=0.6915, medium=0.2605, loose=0.0499) # PNet WP From https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22EE/
        self.deeptau=DotDict(
            vsjet=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                          Tight=6, VTight=7, VVTight=8),
            vse=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vsmu=DotDict(VLoose=1, Loose=1, Medium=3, Tight=4),
        )
        self.regions = self.add_regions()
    #     self.processes, self.process_group_names, self.process_training_names = self.add_processes()

    # def add_processes(self):
    #     processes, process_group_names, process_training_names = super(Config, self).add_processes()
    #     processes_qcd = [
    #         Process("dy_m-50", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_0j", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_1j", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_2j", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_PtZ_0To50", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_PtZ_50To100", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_PtZ_100To250", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_PtZ_250To400", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_PtZ_400To650", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),
    #         Process("dy_PtZ_650ToInf", Label("DY"), color=(255, 102, 102), isDY=True, parent_process="dy"),

    #     ]
    #     for process in processes_qcd:
    #         processes.add(process)
    #     # print(processes)
        
    #     process_group_names = {
    #         "default": [
    #             # "ggf_sm",
    #             # "data_tau",
    #             # "dy_high",
    #             # "tt_dl",
    #             # "data",
    #             "dy",
    #             "tt",
    #             "others"
    #         ],
    #         "signal": [
    #             "ggf"
    #         ],
    #         "other_bck": [
    #             "others"
    #         ],
    #         "data": [
    #             "data"
    #         ],
    #         "plots" : [
    #             "tt_sl",
    #             "tt_dl",
    #             "tt_fh",
    #             "tth_nonbb",
    #             "tth_bb",
    #             # "dy_m-50"
    #             # "dy_0j",
    #             # "others",
    #             "data_mutau",
    #             "dy_m-50",
    #             "dy_0j",
    #             "dy_1j",
    #             "wjets"

    #         ]

    #     }
    #     # print(process_group_names)

    #     # process_group_names = super(Config, self).add_process_group_names()
    #     # process_training_names = super(Config, self).add_process_training_names()  
    #     return ObjectCollection(processes), process_group_names, process_training_names
        
    def add_datasets(self):
        skim_directory = "/eos/user/l/lportale/hhbbtautau/skims/SKIMS_UL18"
        datasets = [
            Dataset("ggf_s0_m250",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m260",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m260"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m270",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m270"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m280",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m280"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m300",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m300"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m320",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m320"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m350",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m350"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m400",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m400"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m450",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m450"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m500",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m550",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m550"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m600",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m600"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m650",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m650"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m700",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m700"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m750",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m800",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m800"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m850",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m850"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m900",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m900"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m1000",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m1000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m1250",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m1250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m1500",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m1500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m1750",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m1750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m2000",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m2000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m2500",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m2500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s0_m3000",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m3000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m250",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m260",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m260"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m270",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m270"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m280",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m280"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m300",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m300"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m320",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m320"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m350",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m350"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m400",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m400"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.), 
            Dataset("ggf_s2_m450",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m450"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m500",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m550",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m550"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m600",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m600"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m650",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m650"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m700",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m700"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m750",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m800",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m800"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m850",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m850"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m900",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m900"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m1000",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m1000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m1250",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m1250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m1500",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m1500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m1750",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m1750"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m2000",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m2000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m2500",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m2500"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m3000",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m3000"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tt_dl",
                folder=os.path.join(skim_directory, "TTTo2L2Nu"),
                process=self.processes.get("tt_dl"),
                file_pattern="output_.*root",
                xs=1.),             
            Dataset("tt_sl",
                folder=os.path.join(skim_directory, "TTToSemiLeptonic"),
                process=self.processes.get("tt_sl"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tt_fh",
                folder=os.path.join(skim_directory, "TTToHadronic"),
                process=self.processes.get("tt_fh"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_m-50",
                folder=os.path.join(skim_directory, "DYJetsToLL_M-50_TuneCP5_13TeV-amc"),
                process=self.processes.get("dy_m-50"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_0j",
                folder=os.path.join(skim_directory, "DYJetsToLL_0J"),
                process=self.processes.get("dy_0j"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_1j",
                folder=os.path.join(skim_directory, "DYJetsToLL_1J"),
                process=self.processes.get("dy_1j"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_2j",
                folder=os.path.join(skim_directory, "DYJetsToLL_2J"),
                process=self.processes.get("dy_2j"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_0To50",
                folder=os.path.join(skim_directory, "DYJetsToLL_LHEFilterPtZ-0To50"),
                process=self.processes.get("dy_PtZ_0To50"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_50To100",
                folder=os.path.join(skim_directory, "DYJetsToLL_LHEFilterPtZ-50To100"),
                process=self.processes.get("dy_PtZ_50To100"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_100To250",
                folder=os.path.join(skim_directory, "DYJetsToLL_LHEFilterPtZ-100To250"),
                process=self.processes.get("dy_PtZ_100To250"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_250To400",
                folder=os.path.join(skim_directory, "DYJetsToLL_LHEFilterPtZ-250To400"),
                process=self.processes.get("dy_PtZ_250To400"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_400To650",
                folder=os.path.join(skim_directory, "DYJetsToLL_LHEFilterPtZ-400To650"),
                process=self.processes.get("dy_PtZ_400To650"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy_PtZ_650ToInf",
                folder=os.path.join(skim_directory, "DYJetsToLL_LHEFilterPtZ-650ToInf"),
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
                folder=[os.path.join(skim_directory, "SingleMuon__Run2018%s" % era)
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
                folder=[os.path.join(skim_directory, "EGamma__Run2018%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 1",
                process=self.processes.get("data_etau"),
                file_pattern="output_.*root",
                merging={
                    "etau": 1,
                },
                xs=1.),
            Dataset("data_tautau",
                # folder=os.path.join(skim_directory, "SKIM_SingleMuon_Run2018A"),
                folder=[os.path.join(skim_directory, "Tau__Run2018%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 2",
                process=self.processes.get("data_tau"),
                file_pattern="output_.*root",
                merging={
                    "mutau": 20,
                },
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
                "WJetsToLNu_TuneCP5_13TeV-madgraph", "WJetsToLNu_HT-70To100", "WJetsToLNu_HT-100To200", "WJetsToLNu_HT-200To400", 
                "WJetsToLNu_HT-400To600", "WJetsToLNu_HT-600To800", "WJetsToLNu_HT-800To1200", "WJetsToLNu_HT-1200To2500", "WJetsToLNu_HT-2500ToInf",
            ],
            "ewk": [
                "EWKWMinus2Jets_WToLNu", "EWKWPlus2Jets_WToLNu", "EWKZ2Jets_ZToLL",
            ],
            "singlet": [
                "ST_tchannel_antitop", "ST_tchannel_top",
            ],
            "tw": [
                "ST_tW_antitop_5f_inclusive", "ST_tW_top_5f_inclusive",
            ],
            "zh": [
                "ZH_HToBB_ZToLL", "ZHToTauTau", "ZH_HToBB_ZToQQ"
            ],
            "wh": [
                "WminusHToTauTau", "WplusHToTauTau",
            ],
            "vv": [
                "_WW_TuneCP5",  
                "_WZ_TuneCP5",  
                "_ZZ_TuneCP5",  
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
                "49_WWW", "50_WWW", "53_WZZ", "54_WZZ", "55_ZZZ", "56_ZZZ", "51_WWZ", "52_WWZ",
            ]
        }

        for process, minor_datasets in other_backgrounds.items():
            for name in minor_datasets:
                datasets.append(
                    Dataset(name,
                        folder=os.path.join(skim_directory, "%s" % name),
                        process=self.processes.get(process),
                        file_pattern="output_.*root",
                        xs=1.),  # already normalised to xs
                )
                # print("process", self.processes.get(process))
        return ObjectCollection(datasets)

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"
        weights.total_events_weights = ["totalWeights"]
        # weights.total_events_weights = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight", "prescaleWeight",
            # "trigSF", "bTagweightReshape"]
        weights.mutau = ["totalWeights"]
        # weights.mutau = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight", "prescaleWeight",
        #     "trigSF", "bTagweightReshape", "0.9890"]
        weights.etau = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight", "prescaleWeight",
            "trigSF", "bTagweightReshape", "0.9831"]
        weights.tautau = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight",
            # "prescaleWeight", "trigSF", "IdAndIsoAndFakeSF_deep_pt", "DYscale_MTT", "customTauIdSF",
            "prescaleWeight", "trigSF", "bTagweightReshape", "1.0038"]
        weights.base= ["(((pairType == {0}) * {1}) + ((pairType != {0}) * 1))".format(
            ic, " * ".join(weights[c.name]))
            for ic, c in enumerate(self.channels)]
        weights.baseline = weights.base
        weights.base_selection = weights.base
        weights.resolved_1b = weights.base
        weights.resolved_2b = weights.base
        weights.boosted = weights.base
        weights.vbf = weights.base 
        return weights


    # def get_dataset_process_mapping(datasets, process_group_name):
    #     mapping = {}
    #     _processes = []
    #     _datasets = []
    #     for process in config.process_group_names:
    #         for i, dataset in datasets:
    #             _process = dataset.processes.get_first()
    #             if process == _process or process.has_process(_process, deep=True):
    #                 mapping[dataset] = process
    #                 _processes.append((i, process))
    #                 _datasets.append((i, dataset))
    #     unique_processes = []
    #     for _, process in _processes:
    #         if process not in unique_processes:
    #             unique_processes.append(process)

    #     unique_datasets = []    
    #     for _, dataset in _datasets:
    #         if dataset not in unique_datasets:
    #             unique_datasets.append(dataset)

    #     return mapping, unique_processes, unique_datasets
    
    
    # def get_dataset_process_mapping(datasets):
    #     mapping = {}
    #     _datasets = []
    #     for dataset in datasets:
    #         mapping[dataset] = process
    #         _datasets.append(dataset)
    #     # for process in config.process_group_names:
    #     #     for i, dataset in datasets:
    #     #         _process = dataset.processes.get_first()
    #     #         if process == _process or process.has_process(_process, deep=True):
    #     #             mapping[dataset] = process
    #     #             _processes.append((i, process))
    #     #             _datasets.append((i, dataset))
    #     # unique_processes = []
    #     # for _, process in _processes:
    #     #     if process not in unique_processes:
    #     #         unique_processes.append(process)

    #     unique_datasets = []    
    #     for _, dataset in _datasets:
    #         if dataset not in unique_datasets:
    #             unique_datasets.append(dataset)

    #     return mapping, unique_datasets


config = Config("qcd_llr_2018", year=2018, ecm=13, lumi_pb=59830)