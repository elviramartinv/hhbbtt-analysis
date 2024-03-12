from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict

from config.base_config import Config as base_config


class Config_2022(base_config):
    def __init__(self, *args, **kwargs):
        super(Config_2022, self).__init__(*args, **kwargs)
        self.btag=DotDict(tight=0.7183, medium=0.3086, loose=0.0583) # DeepJet WP From https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22/
        # self.btag=DotDict(tight=0.6734, medium=0.245, loose=0.047) # PNet WP From https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22/
        self.deeptau=DotDict(
            vsjet=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                          Tight=6, VTight=7, VVTight=8),
            vse=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vsmu=DotDict(VLoose=1, Loose=1, Medium=3, Tight=4),
        )
        self.regions = self.add_regions()


    def add_processes(self):
        processes, process_group_names, process_training_names = super(Config_2022, self).add_processes()
        processes_22 = [
            Process("ggf_0_1_0", Label("HH_{ggf}^{(0,1,0)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_0_1_1", Label("HH_{ggf}^{(0,1,1)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_1_1_0p10", Label("HH_{ggf}^{(1,1,0.1)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_1_1_0p35", Label("HH_{ggf}^{(1,1,0.35)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_1_1_3", Label("HH_{ggf}^{(1,1,3)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_1_1_m2", Label("HH_{ggf}^{(1,1,2)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_2p45_1_0", Label("HH_{ggf}^{(2.45,1,0)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),
            Process("ggf_5_1_0", Label("HH_{ggf}^{(5,1,0)}"), color=(0, 0, 0), isSignal=True,
                parent_process="ggf"),

            Process("vbf_1p74_1p37_14p4", Label("HH_{VBF}^{(1.74,1.37,14.4)"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m0p012_0p030_10p2", Label("HH_{VBF}^{(0.012,0.03,10.2)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m0p758_1p44_m19p3", Label("HH_{VBF}^{(0.758,1.44,19.3)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m0p962_0p959_m1p43", Label("HH_{VBF}^{(0.962,0.959,1.43)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m1p21_1p94_m0p94", Label("HH_{VBF}^{(1.21,1.94,0.94)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m1p60_2p72_m1p36", Label("HH_{VBF}^{(1.6,2.72,1.36)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m1p38_3p57_m3p39", Label("HH_{VBF}^{(1.38,3.57,3.39)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf"),
            Process("vbf_m2p12_3p87_m5p96", Label("HH_{VBF}^{(2.12,3.87,5.96)}"), color=(0, 0, 0), isSignal=True,
                parent_process="vbf")
            ]
        processes.extend(processes_22)  
        process_group_names["test22"] = [
            "dy",
            "tt",
            "ggf_sm"
            ]

        return ObjectCollection(processes), process_group_names, process_training_names
    
    def add_datasets(self):
        datasets = [
            # Signal samples
            # ggF signal
            Dataset("ggf_sm",
                dataset="/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_sm"),
                xs=0.03105,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_0_1_0",
                dataset="/GluGlutoHHto2B2Tau_kl-0p00_kt-1p00_c2-0p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_0_1_0"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_0_1_1",
                dataset="/GluGlutoHHto2B2Tau_kl-0p00_kt-1p00_c2-1p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_0_1_1"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_1_1_0p10",
                dataset="/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p10_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_1_1_0p10"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_1_1_0p35",
                dataset="/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-0p35_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_1_1_0p35"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_1_1_3",
                dataset="/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-3p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_1_1_3"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_1_1_m2",
                dataset="/GluGlutoHHto2B2Tau_kl-1p00_kt-1p00_c2-m2p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_1_1_m2"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_2p45_1_0",
                dataset="/GluGlutoHHto2B2Tau_kl-2p45_kt-1p00_c2-0p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_2p45_1_0"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            Dataset("ggf_5_1_0",
                dataset="/GluGlutoHHto2B2Tau_kl-5p00_kt-1p00_c2-0p00_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggf_5_1_0"),
                xs=1.0,
                tags=["nanoV12"],
                runPeriod="preEE"),
            # VBF signal
            Dataset("vbf_sm",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-1_C3-1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_sm"),
                xs=0.001726,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_1_1_2",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-1_C3-2_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1_1_2"),
                xs=0.001423,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_1_2_1",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-2_C3-1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1_2_1"),
                xs=0.014218,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_1_0_1",
                dataset="/VBFHHto2B2Tau_CV_1_C2V_0_C3_1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1_0_1"),
                xs=0.027080,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_1p74_1p37_14p4",
                dataset="/VBFHHto2B2Tau_CV-1p74_C2V-1p37_C3-14p4_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1p74_1p37_14p4"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m0p012_0p030_10p2",
                dataset="/VBFHHto2B2Tau_CV-m0p012_C2V-0p030_C3-10p2_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m0p012_0p030_10p2"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m0p758_1p44_m19p3",
                dataset="/VBFHHto2B2Tau_CV-m0p758_C2V-1p44_C3-m19p3_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m0p758_1p44_m19p3"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m0p962_0p959_m1p43",
                dataset="/VBFHHto2B2Tau_CV-m0p962_C2V-0p959_C3-m1p43_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m0p962_0p959_m1p43"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m1p21_1p94_m0p94",
                dataset="/VBFHHto2B2Tau_CV-m1p21_C2V-1p94_C3-m0p94_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m1p21_1p94_m0p94"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m1p60_2p72_m1p36",
                dataset="/VBFHHto2B2Tau_CV-m1p60_C2V-2p72_C3-m1p36_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m1p60_2p72_m1p36"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m1p38_3p57_m3p39",
                dataset="/VBFHHto2B2Tau_CV-m1p38_C2V-3p57_C3-m3p39_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m1p38_3p57_m3p39"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_m2p12_3p87_m5p96",
                dataset="/VBFHHto2B2Tau_CV-m2p12_C2V-3p87_C3-m5p96_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_m2p12_3p87_m5p96"),
                xs=1.0,
                runPeriod="preEE",
                tags=["nanoV12"]),
                
            # Background samples
            # dy
            Dataset("dy",
                dataset="/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("dy"),
                xs=6077.22,
                runPeriod="preEE",
                # merging={
                #     "tautau":20,
                #     "etau":20,
                # }
                tags=["nanoV12"]),
            Dataset("dy_low",
                dataset="/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("dy_low"),
                xs=18610,
                runPeriod="preEE",
                tags=["nanoV12"]),
            # # DY_ptZ-binned

            # Dataset("DY_ptZ-40to100_1J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-40to100_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ1"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=477.2,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-40to100_2J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-40to100_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ1"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=177.7,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-100to200_1J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ2"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=45.50,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-100to200_2J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ2"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=52.23,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-200to400_1J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ3"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=3.370,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-200to400_2J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ3"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=7.216,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-400to600_1J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ4"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=0.1167,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-400to600_2J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ4"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=0.4203,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-600_1J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ5"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=0.01394,), # From GenXSecAnalyzer (NLO)

            # Dataset("DY_ptZ-600_2J",
            #     dataset="/DYto2L-2Jets_MLL-50_PTLL-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v1/"
            #         "NANOAODSIM",
            #     process=self.processes.get("DY_ptZ5"),
            #     #prefix="eoscms-ns-ip563.cern.ch:1098//",
            #     xs=0.07020,), # From GenXSecAnalyzer (NLO)

           
            # ttbar
            Dataset("tt_dl",
                dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tt_dl"),
                xs=88.29,
                runPeriod="preEE",
                # merging={
                #     "tautau": 20,
                #     "etau": 20,
                # },
                # scaling=(0.96639, 0.00863),
                tags=["nanoV12"]),
            # Dataset("tt_dl_ext1",
            #     dataset="/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM",
            #     process=self.processes.get("tt_dl_"),
            #     xs=88.29,
            #     # merging={
            #     #     "tautau": 20,
            #     #     "etau": 20,
            #     # },
            #     # scaling=(0.96639, 0.00863),
            #     tags=["nanoV12"]),
            Dataset("tt_sl",
                dataset="/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tt_sl"),
                xs=365.34,
                runPeriod="preEE",
                # merging={
                #     "tautau": 20,
                #     "etau": 40,
                # },
                # scaling=(0.96639, 0.00863),
                tags=["nanoV12"]),
            Dataset("tt_fh",
                dataset="/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tt_fh"),
                xs=377.96,
                runPeriod="preEE",
                # scaling=(0.96639, 0.00863),
                tags=["nanoV12"]),

            # Others
            # ttH
            Dataset("tth_bb",
                dataset="/TTHto2B_M-125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM",
                process=self.processes.get("tth_bb"),
                xs=0.2953,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("tth_nonbb",
                dataset="/TTHtoNon2B_M-125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v4/NANOAODSIM",
                process=self.processes.get("tth_nonbb"),
                xs=0.17996,
                runPeriod="preEE",
                tags=["nanoV12"]),

            # WJets
            Dataset("wjets",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("wjets"),
                xs=61526.7,
                runPeriod="preEE",
                # merging={
                #     "tautau": 5,
                #     "etau": 10,
                # },
                tags=["nanoV12"]),

            # Single top  ##### cross secctions need to be updated
            # st_tw_top
            Dataset("st_tw_top_dl",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tw"),
                xs=4.663, # From https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopNNLORef x BR
                runPeriod="preEE",
                tags=["nanoV12"]),
            # Dataset("st_tw_top_dl_ext1",
            #     dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM",
            #     process=self.processes.get("tw"),
            #     xs=4.663,
            #     tags=["nanoV12"]),
  
            Dataset("st_tw_top_sl",
                dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tw"),
                xs=19.31,
                runPeriod="preEE",
                tags=["nanoV12"]),
            # Dataset("st_tw_top_dl_ext1",
            #     dataset="/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
            #    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
            #     process=self.processes.get("tw"),
            #     xs=19.31,
            #     tags=["nanoV12"]),

            # st_tw_antitop
            Dataset("st_tw_antitop_dl",
                dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tw"),
                xs=4.663, 
                runPeriod="preEE",
                tags=["nanoV12"]),
            # Dataset("st_tw_antitop_dl_ext1",
            #     dataset="/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM",
            #     process=self.processes.get("tw"),
            #     xs=4.663,
            #     tags=["nanoV12"]),
            Dataset("st_tw_antitop_sl",
                dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("tw"),
                xs=19.31,
                runPeriod="preEE",
                tags=["nanoV12"]),
            # Dataset("st_tw_antitop_sl_ext1",
            #     dataset="/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/"
            #         "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2/NANOAODSIM",
            #     process=self.processes.get("tw"),
            #     xs=19.31,
            #     tags=["nanoV12"]),

                
            # st_top
            Dataset("st_top",
                dataset="/TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("singlet"),
                xs=136.02,
                runPeriod="preEE",
                tags=["nanoV12"]),

            # st_antitop
            Dataset("st_antitop",
                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("singlet"),
                xs=80.95,
                runPeriod="preEE",
                tags=["nanoV12"]),
            
            # single higgs
            Dataset("ggf_tautau",
                dataset="/GluGluHToTauTau_M125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggh"),
                xs=3.0469,
                runPeriod="preEE",
                tags=["nanoV12"]),
            Dataset("vbf_tautau",
                dataset="/VBFHToTauTau_M125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbfh"),
                xs=0.237,
                runPeriod="preEE",
                tags=["nanoV12"]),

            # DATA
            # Tau 2022
            Dataset("data_tau_a",
                dataset="/Tau/Run2022A-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="A"),
            Dataset("data_tau_b",
                dataset="/Tau/Run2022B-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="B"),
            Dataset("data_tau_c",
                dataset="/Tau/Run2022C-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="C"),
            Dataset("data_tau_d",
                dataset="/Tau/Run2022D-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="D"),
            Dataset("data_tau_e",
                dataset="/Tau/Run2022E-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="E"),
            Dataset("data_tau_f",
                dataset="/Tau/Run2022F-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="F"),
            Dataset("data_tau_g",
                dataset="/Tau/Run2022G-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="preEE",
                runEra="G"),

            # ETau 2022
            Dataset("data_etau_a",
                dataset="/EGamma/Run2022A-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="A"),
            Dataset("data_etau_b",
                dataset="/EGamma/Run2022B-22Sep2023-v2/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="B"),
            Dataset("data_etau_c",
                dataset="/EGamma/Run2022C-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="C"),
            Dataset("data_etau_d",
                dataset="/EGamma/Run2022D-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="D"),
            Dataset("data_etau_e",
                dataset="/EGamma/Run2022E-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="E"),
            Dataset("data_etau_f",
                dataset="/EGamma/Run2022F-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="F"),
            Dataset("data_etau_g",
                dataset="/EGamma/Run2022G-19Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="preEE",
                runEra="G"),

            # MuTau 2022
            Dataset("data_mutau_a",
                dataset="/SingleMuon/Run2022A-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="A"),
            Dataset("data_mutau_b",
                dataset="/SingleMuon/Run2022B-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="B"),
            Dataset("data_mutau_c",
                dataset="/SingleMuon/Run2022C-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="C"),
            Dataset("data_mutau_d",
                dataset="/Muon/Run2022D-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="D"),
            Dataset("data_mutau_e",
                dataset="/Muon/Run2022E-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="E"),
            Dataset("data_mutau_f",
                dataset="/Muon/Run2022F-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="F"),
            Dataset("data_mutau_g",
                dataset="/Muon/Run2022G-19Dec2023-v2/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="preEE",
                runEra="G")
        ]
    
        return ObjectCollection(datasets)
    
    def add_weights(self):
        weights = DotDict()
        weights.default = "1"
        # weights.total_events_weights = ["genWeight", "puWeight", "DYstitchWeight"]
        weights.total_events_weights = ["genWeight", "puWeight"]

        weights.mutau = ["genWeight", "puWeight"]
#        weights.mutau = ["genWeight", "prescaleWeight", "trigSF", 
       #     "idAndIsoAndFakeSF", "L1PreFiringWeight", "PUjetID_SF",
       #     "bTagweightReshape"]

        weights.etau = weights.mutau
        weights.tautau = weights.mutau
        weights.base_selection = weights.mutau
        weights.base = weights.mutau

        return weights
    

config = Config_2022("2022_v12_preEE", year=2022, ecm=13.6, lumi_pb=9739.0)
