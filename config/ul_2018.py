from analysis_tools import ObjectCollection, Category, Process, Dataset, Feature, Systematic
from analysis_tools.utils import DotDict
from analysis_tools.utils import join_root_selection as jrs
from plotting_tools import Label
from collections import OrderedDict

from config.base_config import Config as base_config
from cmt.config.ul_2018 import Config_ul_2018 as cmt_ul_2018


class Config_ul_2018(base_config, cmt_ul_2018):
    def __init__(self, *args, **kwargs):
        super(Config_ul_2018, self).__init__(*args, **kwargs)

    def add_weights(self):
        weights = DotDict()
        weights.default = "1"
        # weights.total_events_weights = ["genWeight", "puWeight", "DYstitchWeight"]
        weights.total_events_weights = ["genWeight", "puWeight"]

        weights.mutau = ["genWeight", "puWeight", "prescaleWeight", "trigSF",
            "idAndIsoAndFakeSF", "L1PreFiringWeight", "PUjetID_SF",
            "bTagweightReshape"]

        weights.etau = weights.mutau
        weights.tautau = weights.mutau
        weights.base_selection = weights.mutau
        weights.base = weights.mutau

        # weights.channels_mult = {channel: jrs(weights.channels[channel], op="*")
            # for channel in weights.channels}
        return weights

    def add_default_module_files(self):
        defaults = {}
        defaults["PreprocessRDF"] = "modulesrdf"
        defaults["PreCounter"] = "weights"
        return defaults


config = Config_ul_2018("ul_2018", year=2018, ecm=13, lumi_pb=59741, isUL=True)
