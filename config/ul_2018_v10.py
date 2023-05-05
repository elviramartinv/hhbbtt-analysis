from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict

from config.ul_2018 import Config_ul_2018 as base_config


class Config_ul_2018(base_config):
    def __init__(self, *args, **kwargs):
        super(Config_ul_2018, self).__init__(*args, **kwargs)
        self.deeptau=DotDict(
            vsjet=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vse=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vsmu=DotDict(VLoose=1, Loose=1, Medium=3, Tight=4),
        )
        self.regions = self.add_regions()

    def add_datasets(self):
        p = "/eos/home-k/kandroso/cms-hh-bbtautau/nanoAOD/Run2_2018/"
        v9_datasets = super(Config_ul_2018, self).add_datasets()
        datasets = [
            Dataset("ggf_sm",
                folder=p + "GluGluToHHTo2B2Tau_node_SM",
                process=self.processes.get("ggf_sm"),
                xs=0.03105,
                tags=["ul", "nanoV10"], 
                secondary_dataset="ggf_sm_aux"),
            Dataset("ggf_sm_aux",
                dataset="/GluGluToHHTo2B2Tau_TuneCP5_PSWeights_node_SM_13TeV-madgraph-pythia8/"
                    "RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                process=self.processes.get("ggf_sm"),
                xs=0.03105,
                tags=["ul", "secondary"]),
            Dataset("dy",
                folder=p + "DYJetsToLL_M-50",
                process=self.processes.get("dy_high"),
                # prefix="xrootd-cms.infn.it//",
                # prefix="cms-xrd-global.cern.ch//",
                xs=6077.22,
                merging={
                    "tautau": 10,
                    "etau": 10,
                    "mutau": 10,
                },
                secondary_dataset="dy_nlo_aux",
                tags=["ul", "nanoV10"]),

            # TT
            Dataset("tt_dl",
                folder=p + "TTTo2L2Nu",
                process=self.processes.get("tt_dl"),
                xs=88.29,
                merging={
                    "tautau": 20,
                    "mutau": 20,
                    "etau": 40,
                },
                scaling=(0.96639, 0.00863),
                secondary_dataset="tt_dl_aux",
                tags=["ul", "nanoV10"]),
            Dataset("tt_sl",
                folder=p + "TTToSemiLeptonic",
                process=self.processes.get("tt_sl"),
                # prefix="xrootd-cms.infn.it//",
                xs=365.34,
                merging={
                    "tautau": 20,
                    "mutau": 60,
                    "etau": 40,
                },
                scaling=(0.96639, 0.00863),
                secondary_dataset="tt_sl_aux",
                tags=["ul", "nanoV10"]),
            Dataset("tt_fh",
                folder=p + "TTToHadronic",
                process=self.processes.get("tt_fh"),
                # prefix="xrootd-cms.infn.it//",
                xs=377.96,
                scaling=(0.96639, 0.00863),
                secondary_dataset="tt_fh_aux",
                tags=["ul", "nanoV10"]),

            # ttH
            Dataset("tth_bb",
                folder=p + "ttHTobb",
                process=self.processes.get("tth_bb"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.2953,
                secondary_dataset="tth_bb_aux",
                tags=["ul", "nanoV10"]),

            Dataset("tth_tautau",
                folder=p + "ttHToTauTau",
                process=self.processes.get("tth_tautau"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.031805,
                secondary_dataset="tth_tautau_aux",
                tags=["ul", "nanoV10"]),

            Dataset("tth_nonbb",
                folder=p + "ttHToNonbb",
                process=self.processes.get("tth_nonbb"),
                # prefix="xrootd-cms.infn.it//",
                xs=0.17996,
                secondary_dataset="tth_nonbb_aux",
                tags=["ul", "nanoV10"]),

            # Wjets
            Dataset("wjets",
                folder=p + "WJetsToLNu",
                selection="event != 198018547",
                process=self.processes.get("wjets"),
                # prefix="xrootd-cms.infn.it//",
                xs=61526.7,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                splitting=200000,
                secondary_dataset="wjets_aux",
                tags=["ul", "nanoV10"]),

            # tW
            Dataset("st_tw_antitop",
                folder=p + "ST_tW_antitop_5f_inclusiveDecays",
                process=self.processes.get("tw"),
                xs=35.85,
                secondary_dataset="st_tw_antitop_aux",
                tags=["ul", "nanoV10"]),
            Dataset("st_tw_top",
                folder=p + "ST_tW_top_5f_inclusiveDecays",
                process=self.processes.get("tw"),
                xs=35.85,
                secondary_dataset="st_tw_top_aux",
                tags=["ul", "nanoV10"]),

            # single top
            Dataset("st_antitop",
                folder=p + "ST_t-channel_antitop_4f_InclusiveDecays",
                process=self.processes.get("singlet"),
                xs=80.95,
                secondary_dataset="st_antitop_aux",
                tags=["ul", "nanoV10"]),
            Dataset("st_top",
                folder=p + "ST_t-channel_top_4f_InclusiveDecays",
                process=self.processes.get("singlet"),
                xs=136.02,
                secondary_dataset="st_top_aux",
                tags=["ul", "nanoV10"]),

            # DATA
            # Tau 2018
            Dataset("data_tau_a",
                folder=p + "Tau_2018A",
                selection="pairType == 2",
                process=self.processes.get("data_tau"),
                runPeriod="A",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_tau_b",
                folder=p + "Tau_2018B",
                selection="pairType == 2",
                process=self.processes.get("data_tau"),
                runPeriod="B",
                # prefix="xrootd-cms.infn.it//",
                # locate="se-xrd01.jinr-t1.ru:1095/",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_tau_c",
                folder=p + "Tau_2018C",
                selection="pairType == 2",
                process=self.processes.get("data_tau"),
                runPeriod="C",
                # prefix="xrootd-cms.infn.it//",
                # locate="cms03.lcg.cscs.ch:1094/",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_tau_d",
                folder=p + "Tau_2018D",
                selection="pairType == 2",
                process=self.processes.get("data_tau"),
                runPeriod="D",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),

            # EGamma 2018
            Dataset("data_etau_a",
                folder=p + "EGamma_2018A",
                selection="pairType == 1",
                process=self.processes.get("data_etau"),
                runPeriod="A",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_etau_b",
                folder=p + "EGamma_2018B",
                process=self.processes.get("data_etau"),
                runPeriod="B",
                # prefix="xrootd-cms.infn.it//",
                # locate="se-xrd01.jinr-t1.ru:1095/",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_etau_c",
                folder=p + "EGamma_2018C",
                selection="pairType == 1",
                process=self.processes.get("data_etau"),
                runPeriod="C",
                # prefix="xrootd-cms.infn.it//",
                # locate="cms03.lcg.cscs.ch:1094/",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_etau_d",
                folder=p + "EGamma_2018D",
                selection="pairType == 1",
                process=self.processes.get("data_etau"),
                runPeriod="D",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "tautau": 2,
                    "etau": 2,
                },
                tags=["ul", "nanoV10"]),

            # SingleMuon 2018
            Dataset("data_mutau_a",
                folder=p + "SingleMuon_2018A",
                selection="pairType == 0",
                process=self.processes.get("data_mutau"),
                runPeriod="A",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "mutau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_mutau_b",
                folder=p + "SingleMuon_2018B",
                process=self.processes.get("data_mutau"),
                selection="pairType == 0",
                runPeriod="B",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "mutau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_mutau_c",
                folder=p + "SingleMuon_2018C",
                process=self.processes.get("data_mutau"),
                selection="pairType == 0",
                runPeriod="C",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "mutau": 2,
                },
                tags=["ul", "nanoV10"]),
            Dataset("data_mutau_d",
                folder=p + "SingleMuon_2018D",
                process=self.processes.get("data_mutau"),
                selection="pairType == 0",
                runPeriod="D",
                # prefix="xrootd-cms.infn.it//",
                splitting=-1,
                merging={
                    "mutau": 2,
                },
                tags=["ul", "nanoV10"]),
        ]
        datasets = ObjectCollection(datasets)

        for name in ["tt_dl", "tt_sl", "tt_fh", "tth_bb", "tth_tautau", "tth_nonbb",
                "dy_nlo", "wjets", "st_tw_antitop", "st_tw_top", "st_antitop", "st_top"]:
            datasets.add(
                Dataset(
                    v9_datasets.get(name), dataset_name="%s_aux" % name, tags=["ul", "secondary"])
            )

        return datasets

config = Config_ul_2018("ul_2018_v10", year=2018, ecm=13, lumi_pb=59741)
