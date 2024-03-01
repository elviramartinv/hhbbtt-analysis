from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import os

from config.llr_2018 import Config as base_config

class Config(base_config):
    # def add_processes(self):
    #     processes = [
    #         Process("ggf_s0", Label("HH_{ggF}"), color=(0, 0, 0), isSignal=True),
    #         Process("ggf_s2", Label("HH_{ggF}"), color=(0, 0, 0), isSignal=True)
    #     ]
    #     processes_v9 = super(Config, self).add_processes()
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
    #         ]
    #     }
    #     process_training_names = {
    #         "default": [
    #             "ggf_sm",
    #             "dy"
    #         ]
    #     }
    #     # process_group_names = super(Config, self).add_process_group_names()
    #     # process_training_names = super(Config, self).add_process_training_names()   
    #     return ObjectCollection(processes + processes_v9), process_group_names, process_training_names
        
    def add_datasets(self):
        skim_directory = "/eos/user/l/lportale/hhbbtautau/skims/SKIMS_UL18"
        datasets = [
            Dataset("ggf_s0_m250",
                folder=os.path.join(skim_directory, "SKIM_ggF_Radion_m250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("ggf_s2_m250",
                folder=os.path.join(skim_directory, "SKIM_ggF_BulkGraviton_m250"),
                process=self.processes.get("ggf"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tt_dl",
                folder=os.path.join(skim_directory, "SKIM_TT_fullyLep"),
                process=self.processes.get("tt_dl"),
                file_pattern="output_.*root",
                xs=1.),             
            Dataset("tt_sl",
                folder=os.path.join(skim_directory, "SKIM_TT_semiLep"),
                process=self.processes.get("tt_sl"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("tt_fh",
                folder=os.path.join(skim_directory, "SKIM_TT_fullyHad"),
                process=self.processes.get("tt_fh"),
                file_pattern="output_.*root",
                xs=1.),
            Dataset("dy",
                folder=os.path.join(skim_directory, "SKIM_DY_amc_incl"),
                process=self.processes.get("dy"),
                file_pattern="output_.*root",
                xs=1.,
                tags=["ul"]),
        ]
        return ObjectCollection(datasets)
    
config = Config("qcd_llr_2018", year=2018, ecm=13, lumi_pb=59741)