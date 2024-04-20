from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict
import os

from config.base_config import Config as cmt_config


class Config(cmt_config):
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.deeptau=DotDict(
            vsjet=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=8),
            vse=DotDict(VVVLoose=1, VVLoose=2, VLoose=3, Loose=4, Medium=5,
                Tight=6, VTight=7, VVTight=5),
            vsmu=DotDict(VLoose=1, Loose=2, Medium=3, Tight=4),
        )
        # self.processes = self.add_processes()
        self.regions = self.add_regions()
        self.categories = self.add_categories(btag="bjet{}_bID_deepFlavor")
        self.tree_name = "HTauTauTree"

    def add_categories(self, **kwargs):
        categories = super(Config, self).add_categories(**kwargs)
        categories.get("baseline").selection = "pairType >= 0 && pairType <= 2 && nbjetscand > 1 && nleps == 0"
        return categories

    def add_regions(self):
        selection = OrderedDict()
        region_names = ["Signal region", "OS inv. iso", "SS iso", "SS inv. iso", "OS inv. iso vvvl_vvl", 
            "OS inv. iso vvl_vl", "OS inv. iso vl_l", "OS inv. iso l_m", "SS inv. iso vvvl_vvl",
            "SS inv. iso vvl_vl", "SS inv. iso vl_l", "SS inv. iso l_m"]
        selection["os_iso"] = {
            "mutau": ["isOS == 1", "dau1_iso < 0.15",
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium],
            "etau": ["isOS == 1", "dau1_eleMVAiso == 1",
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium],
            "tautau": ["isOS == 1",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium],
        }
        selection["os_inviso"] = {
            "mutau": ["isOS == 1", "dau1_iso < 0.15", "dau2_deepTauVsJet >= 1",
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "etau": ["isOS == 1", "dau1_eleMVAiso == 1", "dau2_deepTauVsJet >= 1",
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "tautau": ["isOS == 1",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= 1",
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
        }
        selection["ss_iso"] = {
            "mutau": ["isOS == 0", "dau1_iso < 0.15",
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium],
            "etau": ["isOS == 0", "dau1_eleMVAiso == 1",
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium],
            "tautau": ["isOS == 0",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium],
        }
        selection["ss_inviso"] = {
            "mutau": ["isOS == 0", "dau1_iso < 0.15", "dau2_deepTauVsJet >= 1",
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "etau": ["isOS == 0", "dau1_eleMVAiso == 1", "dau2_deepTauVsJet >= 1",
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "tautau": ["isOS == 0",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= 1",
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
        }
        selection["os_inviso__vvvl_vvl"] = {
            "mutau": ["isOS == 1", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VVLoose],
            "etau": ["isOS == 1", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VVLoose],
            "tautau": ["isOS == 1",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VVLoose],
        }
        selection["os_inviso__vvl_vl"] = { 
            "mutau": ["isOS == 1", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VLoose],
            "etau": ["isOS == 1", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VLoose],
            "tautau": ["isOS == 1",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VLoose],
        }
        selection["os_inviso__vl_l"] = {
            "mutau": ["isOS == 1", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Loose],
            "etau": ["isOS == 1", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Loose],
            "tautau": ["isOS == 1",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Loose],
        }
        selection["os_inviso__l_m"] = {
            "mutau": ["isOS == 1", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Loose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "etau": ["isOS == 1", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Loose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "tautau": ["isOS == 1",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Loose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
        }
        selection["ss_inviso__vvvl_vvl"] = {
            "mutau": ["isOS == 0", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VVLoose],
            "etau": ["isOS == 0", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VVLoose],
            "tautau": ["isOS == 0",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VVLoose],
        }
        selection["ss_inviso__vvl_vl"] = {
            "mutau": ["isOS == 0", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VLoose],
            "etau": ["isOS == 0", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VLoose],
            "tautau": ["isOS == 0",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VVLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.VLoose],
        }
        selection["ss_inviso__vl_l"] = {
            "mutau": ["isOS == 0", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Loose],
            "etau": ["isOS == 0", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Loose],
            "tautau": ["isOS == 0",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.VLoose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Loose],
        }
        selection["ss_inviso__l_m"] = {
            "mutau": ["isOS == 0", "dau1_iso < 0.15", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Loose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "etau": ["isOS == 0", "dau1_eleMVAiso == 1", 
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Loose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
            "tautau": ["isOS == 0",
                "dau1_deepTauVsJet >= %s" % self.deeptau.vsjet.Medium,
                "dau2_deepTauVsJet >= %s" % self.deeptau.vsjet.Loose,
                "dau2_deepTauVsJet < %s" % self.deeptau.vsjet.Medium],
        }
        regions = []
        for channel in self.channels:
            regions.append(channel)
            regions.append(
                Category(channel.name + "_os", label=channel.label,
                    selection=" (%s) && (isOS == 1)" % channel.selection)
            )
        regions.append(
            Category("dummy", label="#tau_{#mu}#tau_{h}, #tau_{e}#tau_{h}, #tau_{h}#tau_{h} channels",
                selection="1")
        )
        for ikey, key in enumerate(selection):
            regions.append(Category(key, label=Label(region_names[ikey]),
                selection=self.join_selection_channels(selection[key])))
            for channel in self.channels:
                regions.append(Category("_".join([channel.name, key]),
                    label=Label(", ".join([channel.label.root, region_names[ikey]])),
                    selection=jrs(channel.selection,
                        jrs(selection[key][channel.name], op="and"), op="and")))
        return ObjectCollection(regions)

    def add_features(self):
        features = [
            # bjet features
            Feature("bjet1_pt", "bjet1_pt", binning=(20, 20, 220),
                x_title=Label("b_{1} p_{T}"),
                units="GeV"),
            Feature("bjet1_pt_unsmeared", "bjet1_pt / bjet1_smearFactor", binning=(20, 20, 220),
                x_title=Label("b_{1} p_{T}"),
                units="GeV"),
            Feature("bjet1_eta", "bjet1_eta", binning=(20, -5., 5.),
                x_title=Label("b_{1} #eta")),
            Feature("bjet1_phi", "bjet1_phi", binning=(20, -3.2, 3.2),
                x_title=Label("b_{1} #phi")),
            # Feature("bjet1_mass", "bjet1_mass", binning=(10, 50, 150),
                # x_title=Label("b_{1} m"),
                # units="GeV"),
            # Feature("bjet1_mass_unsmeared", "bjet1_mass / bjet1_smearFactor", binning=(10, 50, 150),
                # x_title=Label("b_{1} m"),
                # units="GeV"),
            Feature("bjet1_e", "bjet1_e", binning=(38, 10, 390),
                x_title=Label("b_{1} energy"),
                units="GeV"),
            Feature("bjet1_e_unsmeared", "bjet1_e / bjet1_smearFactor", binning=(58, 10, 590),
                x_title=Label("b_{1} energy"),
                units="GeV"),
            Feature("bjet2_pt", "bjet2_pt", binning=(20, 20, 220),
                x_title=Label("b_{2} p_{T}"),
                units="GeV"),
            Feature("bjet2_eta", "bjet2_eta", binning=(20, -5., 5.),
                x_title=Label("b_{2} #eta")),
            Feature("bjet2_phi", "bjet2_phi", binning=(20, -3.2, 3.2),
                x_title=Label("b_{2} #phi")),
            # Feature("bjet2_mass", "bjet2_mass", binning=(10, 50, 150),
                # x_title=Label("b_{2} m"),
                # units="GeV"),
            Feature("bjet2_e", "bjet2_e", binning=(38, 10, 390),
                x_title=Label("b_{2} energy"),
                units="GeV"),
            Feature("bjet1_smearFactor", "bjet1_smearFactor", binning=(40, 0.8, 1.2),
                x_title=Label("b_{1} smearing factor")),
            Feature("bjet2_smearFactor", "bjet2_smearFactor", binning=(40, 0.8, 1.2),
                x_title=Label("b_{2} smearing factor")),

            Feature("ctjet1_pt", "addJetCentr1_pt", binning=(10, 50, 150),
                x_title=Label("add. central jet 1 p_{t}"),
                units="GeV"),
            Feature("ctjet1_eta", "addJetCentr1_eta", binning=(20, -5., 5.),
                x_title=Label("add. central jet 1 #eta")),
            Feature("ctjet1_phi", "addJetCentr1_phi", binning=(20, -3.2, 3.2),
                x_title=Label("add. central jet 1 #phi")),
            Feature("ctjet1_mass", "addJetCentr1_mass", binning=(10, 50, 150),
                x_title=Label("add. central jet 1 m"),
                units="GeV"),
            Feature("fwjet1_pt", "addJetForw1_pt", binning=(10, 50, 150),
                x_title=Label("add. forward jet 1 p_t"),
                units="GeV"),
            Feature("fwjet1_eta", "addJetForw1_eta", binning=(20, -5., 5.),
                x_title=Label("add. forward jet 1 #eta")),
            Feature("fwjet1_phi", "addJetForw1_phi", binning=(20, -3.2, 3.2),
                x_title=Label("add. forward jet 1  #phi")),
            Feature("fwjet1_mass", "addJetForw1_mass", binning=(10, 50, 150),
                x_title=Label("add. forward jet 1  m"),
                units="GeV"),

            Feature("bjet_difpt", "abs({{bjet1_pt}} - {{bjet2_pt}})", binning=(10, 50, 150),
                x_title=Label("bb #Delta p_t"),
                units="GeV"),

            # lepton features
            Feature("lep1_pt", "dau1_pt", binning=(15, 20, 170),
                x_title=Label("#tau_{1} p_{t}"),
                units="GeV"),
            Feature("lep1_eta", "dau1_eta", binning=(20, -5., 5.),
                x_title=Label("#tau_{1} #eta")),
            Feature("lep1_phi", "dau1_phi", binning=(20, -3.2, 3.2),
                x_title=Label("#tau_{1} #phi")),
            # Feature("lep1_mass", "dau1_mass", binning=(10, 50, 150),
                # x_title=Label("#tau_{1} m"),
                # units="GeV"),
            Feature("lep1_e", "dau1_e", binning=(28, 10, 290),
                x_title=Label("#tau_{1} e"),
                units="GeV"),
            Feature("lep2_pt", "dau2_pt", binning=(15, 20, 170),
                x_title=Label("#tau_{2} p_{t}"),
                units="GeV"),
            Feature("lep2_eta", "dau2_eta", binning=(20, -5., 5.),
                x_title=Label("#tau_{2} #eta")),
            Feature("lep2_phi", "dau2_phi", binning=(20, -3.2, 3.2),
                x_title=Label("#tau_{2} #phi")),
            # Feature("lep2_mass", "dau2_mass", binning=(10, 50, 150),
                # x_title=Label("#tau_{2} m"),
                # units="GeV"),
            Feature("lep2_e", "dau2_e", binning=(28, 10, 290),
                x_title=Label("#tau_{2} e"),
                units="GeV"),

            # MET
            Feature("met_pt", "met_et", binning=(10, 50, 150),
                x_title=Label("MET p_t"),
                units="GeV"),
            Feature("met_phi", "met_phi", binning=(20, -3.2, 3.2),
                x_title=Label("MET #phi")),

            # Hbb
            Feature("Hbb_pt", "bH_pt", binning=(20, 20, 220),
                x_title=Label("H(bb) p_t"),
                units="GeV"),
            Feature("Hbb_eta", "bH_eta", binning=(20, -5., 5.),
                x_title=Label("H(bb) #eta")),
            Feature("Hbb_phi", "bH_phi", binning=(20, -3.2, 3.2),
                x_title=Label("H(bb) #phi")),
            Feature("Hbb_mass", "bH_mass", binning=(30, 0, 300),
                x_title=Label("H(bb) mass"),
                units="GeV"),

            # Htt
            Feature("Htt_pt", "tauH_pt", binning=(20, 0, 400),
                x_title=Label("H(#tau#tau) p_t"),
                units="GeV"),
            Feature("Htt_eta", "tauH_eta", binning=(20, -5., 5.),
                x_title=Label("H(#tau#tau) #eta")),
            Feature("Htt_phi", "tauH_phi", binning=(20, -3.2, 3.2),
                x_title=Label("H(#tau#tau) #phi")),
            Feature("Htt_mass", "tauH_mass", binning=(30, 0, 300),
                x_title=Label("H(#tau#tau) mass"),
                units="GeV"),
                #systematics=["tes"]),

            # Htt (SVFit)
            Feature("Htt_svfit_pt", "tauH_SVFIT_pt", binning=(10, 50, 150),
                x_title=Label("H(#tau#tau) p_{t} (SVFit)"),
                units="GeV"),
            Feature("Htt_svfit_eta", "tauH_SVFIT_eta", binning=(20, -5., 5.),
                x_title=Label("H(#tau#tau) #eta (SVFit)")),
            Feature("Htt_svfit_phi", "tauH_SVFIT_phi", binning=(20, -3.2, 3.2),
                x_title=Label("H(#tau#tau) #phi (SVFit)")),
            Feature("Htt_svfit_mass", "tauH_SVFIT_mass", binning=(40, 0, 400),
                x_title=Label("H(#tau#tau) mass (SVFit)"),
                units="GeV"),

            # HH
            Feature("HH_pt", "HH_pt", binning=(20, 20, 220),
                x_title=Label("HH p_t"),
                units="GeV"),
            Feature("HH_eta", "HH_eta", binning=(20, -5., 5.),
                x_title=Label("HH #eta")),
            Feature("HH_phi", "HH_phi", binning=(20, -3.2, 3.2),
                x_title=Label("HH #phi")),
            Feature("HH_mass", "HH_mass", binning=(50, 0, 1000),
                x_title=Label("HH m"),
                units="GeV"),

            # HH (SVFit)
            Feature("HH_svfit_pt", "HHsvfit_pt", binning=(10, 50, 150),
                x_title=Label("HH p_t (SVFit)"),
                units="GeV"),
            Feature("HH_svfit_eta", "HHsvfit_eta", binning=(20, -5., 5.),
                x_title=Label("HH #eta (SVFit)")),
            Feature("HH_svfit_phi", "HHsvfit_phi", binning=(20, -3.2, 3.2),
                x_title=Label("HH #phi (SVFit)")),
            Feature("HH_svfit_mass", "HHsvfit_mass", binning=(50, 0, 1000),
                x_title=Label("HH m (SVFit)"),
                units="GeV"),

            # HH KinFit
            Feature("HHKinFit_mass", "HHKin_mass_raw", binning=(50, 200, 1200),
                x_title=Label("HH mass"),
                units="GeV"),
            Feature("HHKinFit_chi2", "HHKin_mass_raw_chi2", binning=(30, 0, 10),
                x_title=Label("HH #chi^2 (Kin. Fit)")),

            # VBFjet features
            # Feature("vbfjet1_pt", "VBFjet1_pt", binning=(20, 20, 220),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 1 p_{T}"),
            #     units="GeV"),
            # Feature("vbfjet1_eta", "VBFjet1_eta", binning=(20, -5., 5.),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 1 #eta")),
            # Feature("vbfjet1_phi", "VBFjet1_phi", binning=(20, -3.2, 3.2),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 1 #phi")),
            # Feature("vbfjet1_mass", "VBFjet1_mass", binning=(10, 50, 150),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 1 m"),
            #     units="GeV"),
            # Feature("vbfjet2_pt", "VBFjet2_pt", binning=(20, 20, 220),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 2 p_{T}"),
            #     units="GeV"),
            # Feature("vbfjet2_eta", "VBFjet2_eta", binning=(20, -5., 5.),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 2 #eta")),
            # Feature("vbfjet2_phi", "VBFjet2_phi", binning=(20, -3.2, 3.2),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 2 #phi")),
            # Feature("vbfjet2_mass", "VBFjet2_mass", binning=(10, 50, 150),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jet 2 m"),
            #     units="GeV"),

            # # VBFjj
            # Feature("VBFjj_mass", "VBFjj_mass", binning=(40, 0, 1200),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("VBF jj mass"),
            #     units="GeV"),
            # Feature("VBFjj_deltaEta", "VBFjj_deltaEta", binning=(40, 0, 8),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("#Delta#eta(VBFjj)")),
            # Feature("VBFjj_deltaPhi", "VBFjj_deltaPhi", binning=(40, 0, 6.4),
            #     selection="VBFjet1_pt > -999",
            #     x_title=Label("#Delta#phi(VBFjj)")),

            # weights
            # Feature("PUjetID_SF", "PUjetID_SF", binning=(100, 0, 2),
            #     x_title=Label("PUjetID_SF"), tags=["weight"], systematic=["pujetsyst"]),
            # Feature("PUReweight", "PUReweight", binning=(100, 0, 0.05),
            #     x_title=Label("PUReweight"), tags=["weight"]),
            # Feature("bTagweightReshape", "bTagweightReshape", binning=(100, 0, 2),
            #     x_title=Label("b-tag efficiency weight"), tags=["weight"],
            #     systematics=["jet_1", "jet_2", "jet_3", "jet_4", "jet_5", "jet_6",
            #         "jet_7", "jet_8", "jet_9", "jet_10", "jet_11",
            #         "ls", "hf", "hfstats1", "hfstats2", "lfstats1", "lfstats2", "cferr1", "cferr2"]),
            # Feature("trigSF", "trigSF", binning=(100, 0.6, 1.1),
            #     x_title=Label("Trigger efficiency scale factor"), tags=["weight"],
            #     systematics=["trigSFmuon", "trigSFele", "trigSFDM0", "trigSFDM1", "trigSFDM10", "trigSFDM11", "trigSFVBFjet"]),
            # Feature("IdAndIsoSF_deep_pt", "IdAndIsoAndFakeSF_deep_pt", binning=(100, 0.8, 1.2),
            #     x_title=Label("Lepton identification and isolation scale factor"), tags=["weight"],
            #     systematics=["idAndIsoAndFakeSF_tauid_pt20to25", "idAndIsoAndFakeSF_tauid_pt25to30",
            #         "idAndIsoAndFakeSF_tauid_pt30to35", "idAndIsoAndFakeSF_tauid_pt35to40",
            #         "idAndIsoAndFakeSF_tauid_pt40toInf", "idAndIsoAndFakeSF_mutauFR_etaLt0p4",
            #         "idAndIsoAndFakeSF_mutauFR_eta0p4to0p8", "idAndIsoAndFakeSF_mutauFR_eta0p8to1p2",
            #         "idAndIsoAndFakeSF_mutauFR_eta1p2to1p7", "idAndIsoAndFakeSF_mutauFR_etaGt1p7",
            #         "idAndIsoAndFakeSF_etauFR_barrel", "idAndIsoAndFakeSF_etauFR_endcap"]),
            # Feature("smearing_factor", "{bjet1_smearFactor, bjet1_smearFactor2}", binning=(100, 0, 2),
            #     x_title=Label("smearing_factor"), tags=["weight"]),
            # Feature("L1pref_weight", "L1pref_weight", binning=(100, 0.9, 1.1),
            #     x_title=Label("L1 prefiring weight"), tags=["weight"]),
            # Feature("prescaleWeight", "prescaleWeight", binning=(100, 0, 2),
            #     x_title=Label("prescaleWeight"), tags=["weight"]),

            # DNN
            Feature("dnn", "DNNoutSM_kl_1", binning=(50, 0, 1),
                x_title=Label("DNN output"),
                systematics=["muon", "electron_dm0", "electron_dm1",
                    "tau_dm0", "tau_dm1", "tau_dm10", "tau_dm11",
                    "jet_1", "jet_2", "jet_3", "jet_4", "jet_5", "jet_6",
                    "jet_7", "jet_8", "jet_9", "jet_10", "jet_11"]),
        ]
        return ObjectCollection(features)
           
    def add_datasets(self):
        skim_directory = "/eos/user/j/jmotta/SKIMMED_Legacy2018_16Feb2021_HHbtag"
        datasets = [
            Dataset("vbf_sm",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_1_C2V_1_C3_1_xs"),
                process=self.processes.get("vbf_sm"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("vbf_0p5_1_1",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_0_5_C2V_1_C3_1_xs"),
                process=self.processes.get("vbf_0p5_1_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("vbf_1p5_1_1",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_1_5_C2V_1_C3_1_xs"),
                process=self.processes.get("vbf_1p5_1_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("vbf_1_0_1",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_1_C2V_0_C3_1_xs"),
                process=self.processes.get("vbf_1_0_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("vbf_1_1_0",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_1_C2V_1_C3_0_xs"),
                process=self.processes.get("vbf_1_1_0"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("vbf_1_1_2",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_1_C2V_1_C3_2_xs"),
                process=self.processes.get("vbf_1_1_2"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("vbf_1_2_1",
                folder=os.path.join(skim_directory, "SKIM_VBFHH_CV_1_C2V_2_C3_1_xs"),
                process=self.processes.get("vbf_1_2_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("ggf_sm",
                folder=os.path.join(skim_directory, "SKIM_GGHH_NLO_cHHH1_xs"),
                process=self.processes.get("ggf_sm"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("ggf_sm_syst",
                folder=os.path.join(skim_directory, "SKIM_GGHH_NLO_cHHH1_xs"),
                process=self.processes.get("ggf_sm"),
                file_pattern="syst_output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("ggf_0_1",
                folder=os.path.join(skim_directory, "SKIM_GGHH_NLO_cHHH0_xs"),
                process=self.processes.get("ggf_0_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("ggf_2p45_1",
                folder=os.path.join(skim_directory, "SKIM_GGHH_NLO_cHHH2p45_xs"),
                process=self.processes.get("ggf_2p45_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("ggf_5_1",
                folder=os.path.join(skim_directory, "SKIM_GGHH_NLO_cHHH5_xs"),
                process=self.processes.get("ggf_5_1"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            # Backgrounds
            Dataset("tt_dl",
                folder=os.path.join(skim_directory, "SKIM_TT_fullyLep"),
                process=self.processes.get("tt_dl"),
                file_pattern="output_.*root",
                merging={
                    # "mutau": 20,
                    # "etau": 20,
                    # "resolved_1b": 5,
                    # "resolved_2b": 5,
                    # "vbf": 5,
                },
                # scaling=(0.96639, 0.00863),
                xs=1.),  # already normalised to xs

            Dataset("tt_sl",
                folder=os.path.join(skim_directory, "SKIM_TT_semiLep"),
                process=self.processes.get("tt_sl"),
                file_pattern="output_.*root",
                merging={
                    # "mutau": 20,
                    # "etau": 20,
                    # "resolved_1b": 5,
                    # "resolved_2b": 5,
                    # "vbf": 5,
                },
                # scaling=(0.96639, 0.00863),
                xs=1.),  # already normalised to xs

            Dataset("tt_fh",
                folder=os.path.join(skim_directory, "SKIM_TT_fullyHad"),
                process=self.processes.get("tt_fh"),
                file_pattern="output_.*root",
                merging={
                    # "mutau": 20,
                    # "etau": 20,
                    # "resolved_1b": 5,
                    # "resolved_2b": 5,
                    # "vbf": 5,
                },
                # scaling=(0.96639, 0.00863),
                xs=1.),  # already normalised to xs

            Dataset("dy",
                folder=os.path.join(skim_directory, "SKIM_DY"),
                process=self.processes.get("dy_high"),
                file_pattern="output_.*root",
                merging={
                    # "mutau": 10,
                    # "etau": 10,
                    # "resolved_1b": 2,
                    # "resolved_2b": 2,
                    # "vbf": 2,
                },
                xs=1.),  # already normalised to xs

            Dataset("dy_low",
                folder=os.path.join(skim_directory, "SKIM_DY_lowMass"),
                process=self.processes.get("dy_low"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs


            Dataset("tth_bb",
                folder=os.path.join(skim_directory, "SKIM_ttHJetToBB"),
                process=self.processes.get("tth_bb"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("tth_nonbb",
                folder=os.path.join(skim_directory, "SKIM_ttHJetTononBB"),
                process=self.processes.get("tth_nonbb"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            Dataset("tth_tautau",
                folder=os.path.join(skim_directory, "SKIM_ttHJetToTauTau"),
                process=self.processes.get("tth_tautau"),
                file_pattern="output_.*root",
                xs=1.),  # already normalised to xs

            # DATA
            Dataset("data_mutau",
                folder=[os.path.join(skim_directory, "SKIM_SingleMuon2018%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 0",
                process=self.processes.get("data_mutau"),
                file_pattern="output_.*root",
                merging={
                    "mutau": 40,
                },
                xs=1.),  # already normalised to xs

            Dataset("data_etau",
                folder=[os.path.join(skim_directory, "SKIM_SingleElectron2018%s" % era)
                    for era in ["A", "B", "C", "D"]],
                selection="pairType == 1",
                process=self.processes.get("data_etau"),
                file_pattern="output_.*root",
                merging={
                    "etau": 1,
                },
                xs=1.),  # already normalised to xs

            Dataset("data_tautau",
                selection="pairType == 2",
                folder=[os.path.join(skim_directory, "SKIM_Tau2018%s" % era)
                    for era in ["A", "B", "C", "D"]],
                process=self.processes.get("data_tau"),
                file_pattern="output_.*root",
                merging={
                    "mutau": 20,
                },
                xs=1.),  # already normalised to xs
        ]
        other_backgrounds = {
            "wjets": [
                "WJets_HT_0_100", "WJets_HT_100_200", "WJets_HT_1200_2500", "WJets_HT_200_400",
                "WJets_HT_2500_Inf", "WJets_HT_400_600", "WJets_HT_600_800", "WJets_HT_800_1200",
            ],
            "ewk": [
                "EWKWMinus2Jets_WToLNu", "EWKWPlus2Jets_WToLNu", "EWKZ2Jets_ZToLL",
            ],
            "singlet": [
                "ST_tchannel_antitop", "ST_tchannel_top",
            ],
            "tw": [
                "ST_tW_antitop", "ST_tW_top",
            ],
            "zh": [
                "ZH_HBB_ZLL", "ZH_HTauTau", "ZH_HBB_ZQQ"
            ],
            "wh": [
                "WminusHTauTau", "WplusHTauTau",
            ],
            "vv": [
                "WWTo2L2Nu", "WWTo4Q", "WWToLNuQQ",  # WW
                "WZTo1L1Nu2Q", "WZTo1L3Nu", "WZTo2L2Q", "WZTo3LNu",  # WZ
                "ZZTo2L2Nu", "ZZTo2L2Q", "ZZTo2Q2Nu", "ZZTo4L",  # ZZ
            ],
            "ttx": [
                "TTZZ", "TTWW", "TTWZ", "TTWH", "TTZH", "TTWJetsToLNu", "TTWJetsToQQ", "TTZToLLNuNu", "TTZToQQ"
            ],
            "ggh": [
                "ggHTauTau",
            ],
            "vbfh": [
                "VBFHTauTau",
            ],
            "vvv": [
                "WWW", "WZZ", "ZZZ", "WWZ",
            ]
        }

        for process, minor_datasets in other_backgrounds.items():
            for name in minor_datasets:
                datasets.append(
                    Dataset(name.lower(),
                        folder=os.path.join(skim_directory, "SKIM_%s" % name),
                        process=self.processes.get(process),
                        file_pattern="output_.*root",
                        xs=1.),  # already normalised to xs
                )

        return ObjectCollection(datasets)

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"

        # The last number is the needed scaling to correct the bTagweightReshape weights
        # each channel has its own, and this should be propagated correctly to each category.
        # when considering the three channels at once, for now we take the etau number, but 
        # this should be fixed

        weights.mutau = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight", "prescaleWeight",
            "trigSF", "IdAndIsoAndFakeSF_deep_pt", "DYscale_MTT", "bTagweightReshape", "0.9890"]
        weights.etau = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight", "prescaleWeight",
            "trigSF", "IdAndIsoAndFakeSF_deep_pt", "DYscale_MTT", "bTagweightReshape", "0.9831"]
        weights.tautau = ["MC_weight", "PUReweight", "PUjetID_SF", "L1pref_weight",
            # "prescaleWeight", "trigSF", "IdAndIsoAndFakeSF_deep_pt", "DYscale_MTT", "customTauIdSF",
            "prescaleWeight", "trigSF", "IdAndIsoAndFakeSF_deep_pt", "DYscale_MTT",
            "bTagweightReshape", "1.0038"]
        weights.baseline = ["(((pairType == {0}) * {1}) + ((pairType != {0}) * 1))".format(
            ic, " * ".join(weights[c.name]))
            for ic, c in enumerate(self.channels)]
        weights.resolved_1b = weights.baseline
        weights.resolved_2b = weights.baseline
        weights.boosted = weights.baseline
        weights.vbf = weights.baseline
        # weights.channels_mult = {channel: jrs(weights.channels[channel], op="*")
            # for channel in weights.channels}
        return weights

    def add_systematics(self):
        systematics = [
            Systematic("trigSFmuon", "_mu"),
            Systematic("trigSFele", "_ele"),
            Systematic("trigSFDM0", "_DM0"),
            Systematic("trigSFDM1", "_DM1"),
            Systematic("trigSFDM10", "_DM10"),
            Systematic("trigSFDM11", "_DM11"),
            Systematic("muon", "_mu", up="up", down="down"),
            Systematic("electron_dm0", "_ele", up="up_DM0", down="down_DM0"),
            Systematic("electron_dm1", "_ele", up="up_DM1", down="down_DM1"),
            Systematic("tau_dm0", "_tau", up="up_DM0", down="down_DM0"),
            Systematic("tau_dm1", "_tau", up="up_DM1", down="down_DM1"),
            Systematic("tau_dm10", "_tau", up="up_DM10", down="down_DM10"),
            Systematic("tau_dm11", "_tau", up="up_DM11", down="down_DM11"),
            Systematic("jet_1", "_jet", up="up1", down="down1"),
            Systematic("jet_2", "_jet", up="up2", down="down2"),
            Systematic("jet_3", "_jet", up="up3", down="down3"),
            Systematic("jet_4", "_jet", up="up4", down="down4"),
            Systematic("jet_5", "_jet", up="up5", down="down5"),
            Systematic("jet_6", "_jet", up="up6", down="down6"),
            Systematic("jet_7", "_jet", up="up7", down="down7"),
            Systematic("jet_8", "_jet", up="up8", down="down8"),
            Systematic("jet_9", "_jet", up="up9", down="down9"),
            Systematic("jet_10", "_jet", up="up10", down="down10"),
            Systematic("jet_11", "_jet", up="up11", down="down11"),
            Systematic("pujetsyst", ""),
            Systematic("jes", "_jes"),
            Systematic("ls", "_lf"),
            Systematic("hf", "_hf"),
            Systematic("hfstats1", "_hfstats1"),
            Systematic("hfstats2", "_hfstats2"),
            Systematic("lfstats1", "_lfstats1"),
            Systematic("lfstats2", "_lfstats2"),
            Systematic("cferr1", "_cferr1"),
            Systematic("cferr2", "_cferr2"),
            Systematic("trigSFVBFjet", "_vbfjet"),
            Systematic("idAndIsoAndFakeSF_tauid_pt20to25", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_tauid_pt20to25")),
            Systematic("idAndIsoAndFakeSF_tauid_pt25to30", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_tauid_pt25to30")),
            Systematic("idAndIsoAndFakeSF_tauid_pt30to35", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_tauid_pt30to35")),
            Systematic("idAndIsoAndFakeSF_tauid_pt35to40", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_tauid_pt35to40")),
            Systematic("idAndIsoAndFakeSF_tauid_pt40toInf", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_tauid_pt40toInf")),
            Systematic("idAndIsoAndFakeSF_mutauFR_etaLt0p4", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_mutauFR_etaLt0p4")),
            Systematic("idAndIsoAndFakeSF_mutauFR_eta0p4to0p8", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_mutauFR_eta0p4to0p8")),
            Systematic("idAndIsoAndFakeSF_mutauFR_eta0p8to1p2", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_mutauFR_eta0p8to1p2")),
            Systematic("idAndIsoAndFakeSF_mutauFR_eta1p2to1p7", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_mutauFR_eta1p2to1p7")),
            Systematic("idAndIsoAndFakeSF_mutauFR_etaGt1p7", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_mutauFR_etaGt1p7")),
            Systematic("idAndIsoAndFakeSF_etauFR_barrel", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_etauFR_barrel")),
            Systematic("idAndIsoAndFakeSF_etauFR_endcap", ("IdAndIsoAndFakeSF_deep_pt", "idAndIsoAndFakeSF_etauFR_endcap")),
        ]
        return ObjectCollection(systematics)


config = Config("base", year=2018, ecm=13, lumi_pb=59741)
