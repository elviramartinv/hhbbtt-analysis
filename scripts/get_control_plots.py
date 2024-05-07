from subprocess import call
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-v', '--version', dest='version', default = None, help='version')
options = parser.parse_args()



command = ("law run FeaturePlot --version " + options.version + " --config-name qcd_llr_{} "
        "--category-name {} --region-name {}_os_iso --process-group-name plots_no_signal "
        "--do-qcd True --tree-name HTauTauTree --stack True --MergeCategorization-version {} "
        "--MergeCategorizationStatsLLR-version {} --apply-weights True "
        "--feature-names {} --is-llr --hide-data False --save-png")


years = ["2016", "2016APV", "2017", "2018"]
channels = ["tautau", "mutau", "etau"]
categories = ["baseline", "resolved_1b", "resolved_2b", "boosted_l", "boosted_m"]
feature_names = ("lep1_eta,lep1_pt,lep1_pt,lep2_eta,lep2_pt,lep2_phi,lep1_dtvsmu,lep1_dtvse,lep1_dtvsjet,"
            "lep2_dtvsmu,lep2_dtvse,lep2_dtvsjet,bjet1_pt,bjet1_eta,bjet1_phi,bjet2_pt,bjet2_eta,bjet2_phi,bjet1_df,bjet2_df")

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