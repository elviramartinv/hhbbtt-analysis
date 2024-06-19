from subprocess import call
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-v', '--version', dest='version', default = None, help='version')
options = parser.parse_args()


command = ("law run FeaturePlotQCDTest --version " + options.version + " --config-name qcd_llr_{} "
        "--category-name {} --region-name {}_os_iso --FeaturePlot-process-group-name plots "
        "--PrePlot-tree-name HTauTauTree --MergeCategorization-version {} "
        "--MergeCategorizationStatsLLR-version {} --apply-weights True "
        "--feature-names {} --FeaturePlot-is-llr")


years = ["2017"]
# years = ["2018"]
channels = ["tautau", "mutau", "etau"]
categories = ["baseline", "resolved_1b", "resolved_2b", "boosted_l", "boosted_m"]
# categories = ["baseline", "resolved_1b", "resolved_2b"]
# feature_names = ("lep1_eta,lep1_phi,lep1_pt,lep2_eta,lep2_pt,lep2_phi,lep1_deepTauVSmu,lep1_deepTauVSe,lep1_deepTauVSjet,"
#             "lep2_deepTauVSmu,lep2_deepTauVSe,lep2_deepTauVSjet,bjet1_pt,bjet1_eta,bjet1_phi,bjet2_pt,bjet2_eta,bjet2_phi,bjet1_deepFlav,bjet2_deepFlav")
feature_names =  ("lep1_eta")

params = OrderedDict()
params["2016APV"] = (["2May"])
params["2016"] = (["20Apr"])
params["2017"] = (["20Apr"])
params["2018"] = (["5Apr"])

for year in years:
    for channel in channels:
        for category in categories:
            command_to_run = command.format(year, category, channel, params[year][0], params[year][0], feature_names)
            print(command_to_run)
            call(command_to_run, shell=True)
