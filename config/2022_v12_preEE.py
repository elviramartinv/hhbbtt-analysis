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
        self.deeptau=DotDict(
            vsjet=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                          Tight=6, VTight=7, VVTight=8),
            vse=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vsmu=DotDict(VLoose=1, Loose=1, Medium=3, Tight=4),
        )

    def add_processes(self):
        processes, process_group_names, process_training_names = super(Config_2022, self).add_processes()
        
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
                tags=["nanoV12"]),
            # VBF signal
            Dataset("vbf_sm",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-1_C3-1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_sm"),
                xs=0.001726,
                tags=["nanoV12"]),
            Dataset("vbf_1_1_2",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-1_C3-2_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1_1_2"),
                xs=0.001423,
                tags=["nanoV12"]),
            Dataset("vbf_1_2_1",
                dataset="/VBFHHto2B2Tau_CV-1_C2V-2_C3-1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1_2_1"),
                xs=0.014218,
                tags=["nanoV12"]),
            Dataset("vbf_1_0_1",
                dataset="/VBFHHto2B2Tau_CV_1_C2V_0_C3_1_TuneCP5_13p6TeV_madgraph-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbf_1_0_1"),
                xs=0.027080,
                tags=["nanoV12"]),
            # Background samples
            # dy
            Dataset("dy",
                dataset="/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("dy"),
                xs=6077.22,
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
                # scaling=(0.96639, 0.00863),
                tags=["nanoV12"]),

            # Others
            # ttH
            Dataset("tth_bb",
                dataset="/TTHto2B_M-125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v3/NANOAODSIM",
                process=self.processes.get("tth_bb"),
                xs=0.2953,
                tags=["nanoV12"]),
            Dataset("tth_nonbb",
                dataset="/TTHtoNon2B_M-125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v4/NANOAODSIM",
                process=self.processes.get("tth_nonbb"),
                xs=0.17996,
                tags=["nanoV12"]),

            # WJets
            Dataset("wjets",
                dataset="/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("wjets"),
                xs=61526.7,
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
                tags=["nanoV12"]),

            # st_antitop
            Dataset("st_antitop",
                dataset="/TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("singlet"),
                xs=80.95,
                tags=["nanoV12"]),
            
            # single higgs
            Dataset("ggf_tautau",
                dataset="/GluGluHToTauTau_M125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("ggh"),
                xs=3.0469,
                tags=["nanoV12"]),
            Dataset("vbf_tautau",
                dataset="/VBFHToTauTau_M125_TuneCP5_13p6TeV_powheg-pythia8/"
                    "Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2/NANOAODSIM",
                process=self.processes.get("vbfh"),
                xs=0.237,
                tags=["nanoV12"]),

            # DATA
            # Tau 2022
            Dataset("data_tau_a",
                dataset="/Tau/Run2022A-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="A"),
            Dataset("data_tau_b",
                dataset="/Tau/Run2022B-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="B"),
            Dataset("data_tau_c",
                dataset="/Tau/Run2022C-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="C"),
            Dataset("data_tau_d",
                dataset="/Tau/Run2022D-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="D"),
            Dataset("data_tau_e",
                dataset="/Tau/Run2022E-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="E"),
            Dataset("data_tau_f",
                dataset="/Tau/Run2022F-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="F"),
            Dataset("data_tau_g",
                dataset="/Tau/Run2022G-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_tau"),
                runPeriod="G"),

            # ETau 2022
            Dataset("data_etau_a",
                dataset="/EGamma/Run2022A-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="A"),
            Dataset("data_etau_b",
                dataset="/EGamma/Run2022B-22Sep2023-v2/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="B"),
            Dataset("data_etau_c",
                dataset="/EGamma/Run2022C-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="C"),
            Dataset("data_etau_d",
                dataset="/EGamma/Run2022D-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="D"),
            Dataset("data_etau_e",
                dataset="/EGamma/Run2022E-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="E"),
            Dataset("data_etau_f",
                dataset="/EGamma/Run2022F-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="F"),
            Dataset("data_etau_g",
                dataset="/EGamma/Run2022G-19Dec2023-v1/NANOAOD",
                process=self.processes.get("data_etau"),
                runPeriod="G"),

            # MuTau 2022
            Dataset("data_mutau_a",
                dataset="/SingleMuon/Run2022A-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="A"),
            Dataset("data_mutau_b",
                dataset="/SingleMuon/Run2022B-22Sep2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="B"),
            Dataset("data_mutau_c",
                dataset="/SingleMuon/Run2022C-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="C"),
            Dataset("data_mutau_d",
                dataset="/Muon/Run2022D-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="D"),
            Dataset("data_mutau_e",
                dataset="/Muon/Run2022E-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="E"),
            Dataset("data_mutau_f",
                dataset="/Muon/Run2022F-16Dec2023-v1/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="F"),
            Dataset("data_mutau_g",
                dataset="/Muon/Run2022G-19Dec2023-v2/NANOAOD",
                process=self.processes.get("data_mutau"),
                runPeriod="G")
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
    

config = Config_2022("2022_v12_preEE", year=2022, ecm=13.6, lumi_pb=8077.0, isRun3=True)
