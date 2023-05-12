from cmt.base_tasks.plotting import FeaturePlot
from tasks.llr_counting import MergeCounterLLR
from tasks.vbf_plotting import VBFFeaturePlot
from tasks.ggf_plotting import ggFFeaturePlot
from collections import OrderedDict
import json


class FeaturePlotLLR(FeaturePlot):

    def __init__(self, *args, **kwargs):
        super(FeaturePlotLLR, self).__init__(*args, **kwargs)
        self.tree_name = "HTauTauTree"

    def requires(self):
        reqs = FeaturePlot.requires(self)

        if not self.avoid_normalization:
            reqs["stats"] = OrderedDict()
            for dataset in self.datasets_to_run:
                if dataset.process.isData:
                    continue

                reqs["stats"][dataset.name] = MergeCounterLLR.vreq(self, dataset_name=dataset.name)

        if self.do_qcd:
            reqs["qcd"] = {
                key: FeaturePlotLLR.vreq(self, region_name=region.name, blinded=False, hide_data=False,
                    do_qcd=False, stack=True, save_root=True, save_pdf=True, save_yields=False,
                    remove_horns=False,_exclude=["feature_tags", "shape_region",
                    "qcd_category_name", "qcd_sym_shape", "qcd_signal_region_wp"])
                for key, region in self.qcd_regions.items()
            }
            if self.qcd_category_name != "default":
                reqs["qcd"]["ss_iso"] = FeaturePlotLLR.vreq(self,
                    region_name=self.qcd_regions.ss_iso.name, category_name=self.qcd_category_name,
                    blinded=False, hide_data=False, do_qcd=False, stack=True, save_root=True,
                    save_pdf=True, save_yields=False, feature_names=(self.qcd_feature,),
                    bin_opt_version=law.NO_STR, remove_horns=self.remove_horns, _exclude=["feature_tags",
                        "shape_region", "qcd_category_name", "qcd_sym_shape", "bin_opt_version",
                        "qcd_signal_region_wp"])
                # reqs["qcd"]["os_inviso"] = FeaturePlotLLR.vreq(self,
                    # region_name=self.qcd_regions.os_inviso.name, category_name=self.qcd_category_name,
                    # blinded=False, hide_data=False, do_qcd=False, stack=True, save_root=True,
                    # save_pdf=True, save_yields=True, feature_names=(self.qcd_feature,),
                    # remove_horns=self.remove_horns, _exclude=["feature_tags", "bin_opt_version"])
                reqs["qcd"]["ss_inviso"] = FeaturePlotLLR.vreq(self,
                    region_name=self.qcd_regions.ss_inviso.name,
                    category_name=self.qcd_category_name,
                    blinded=False, hide_data=False, do_qcd=False, stack=True, save_root=True,
                    save_pdf=True, save_yields=False, feature_names=(self.qcd_feature,),
                    bin_opt_version=law.NO_STR, remove_horns=self.remove_horns, _exclude=["feature_tags", 
                        "shape_region", "qcd_category_name", "qcd_sym_shape", "bin_opt_version",
                        "qcd_signal_region_wp"])

        return reqs

    def get_nevents(self):
        nevents = {}
        for iproc, (process, datasets) in enumerate(self.processes_datasets.items()):
            if not process.isData and not self.avoid_normalization:
                for dataset in datasets:
                    inp = self.input()["stats"][dataset.name]
                    with open(inp.path) as f:
                        stats = json.load(f)
                        # nevents += stats["nevents"]
                        nevents[dataset.name] = stats["evt_den"]
        return nevents


class VBFFeaturePlotLLR(VBFFeaturePlot):
    def __init__(self, *args, **kwargs):
        super(VBFFeaturePlotLLR, self).__init__(*args, **kwargs)
        self.tree_name = "HTauTauTree"

    def get_nevents(self):
        return FeaturePlotLLR.get_nevents(self)

    def requires(self):
        reqs = VBFFeaturePlot.requires(self)
        reqs["stats"] = OrderedDict(
            (dataset.name, MergeCounterLLR.vreq(self, dataset_name=dataset.name))
            for dataset in self.datasets_to_run if not dataset.process.isData
        )
        return reqs


class ggFFeaturePlotLLR(ggFFeaturePlot):
    def __init__(self, *args, **kwargs):
        super(ggFFeaturePlotLLR, self).__init__(self, *args, **kwargs)
        self.tree_name = "HTauTauTree"

    def get_nevents(self):
        return FeaturePlotLLR.get_nevents(self)

    def requires(self):
        reqs = ggFFeaturePlot.requires(self)
        print(self.dataset_names)
        reqs["stats"] = OrderedDict(
            (dataset.name, MergeCounterLLR.vreq(self, dataset_name=dataset.name))
            for dataset in self.datasets_to_run if not dataset.process.isData
        )
        return reqs
