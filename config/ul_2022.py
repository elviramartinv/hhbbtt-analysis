from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict

from config.ul_2018_v10 import Config_ul_2018 as base_config


class Config_ul_2022(base_config):
    def add_datasets(self):
        datasets = [
            Dataset("ggf_sm",
                dataset="/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv10-Poisson60KeepRAW_124X_mcRun3_2022_realistic_postEE_v1-v2/NANOAODSIM",
                process=self.processes.get("ggf_sm"),
                xs=0.03105,
                tags=["ul", "nanoV10"]),
            Dataset("vbf_sm",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-1_C3-1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22EENanoAODv10-Poisson60KeepRAW_124X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                process=self.processes.get("vbf_sm"),
                xs=0.001726,
                tags=["ul", "nanoV10"]),
            Dataset("tt",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                process=self.processes.get("tt"),
                xs=0.001726,
                tags=["ul", "nanoV10"]),
            Dataset("dy",
                dataset="/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/"
                    "Run3Summer22EENanoAODv11-forPOG_126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                process=self.processes.get("dy"),
                xs=0.001726,
                tags=["ul", "nanoV10"]),
            Dataset("dy_2jets",
                dataset="/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                process=self.processes.get("dy"),
                xs=0.001726,
                tags=["ul", "nanoV10"]),
        ]
        return ObjectCollection(datasets)

config = Config_ul_2022("ul_2022", year=2022, ecm=13.6, lumi_pb=1, isRun3=True)
