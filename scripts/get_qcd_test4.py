from subprocess import call
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-v', '--version', dest='version', default = None, help='version')
options = parser.parse_args()


##### NEED TO CHANGE THE REGIONS
print("check the regions")

command = ("law run FeaturePlot --version " + options.version + " --config-name qcd_llr_{} "
        "--category-name {} --region-name {}_os_iso --FeaturePlot-hide-data False "
        "--tree-name HTauTauTree --MergeCategorization-version {} --do-qcd True"
        "--MergeCategorizationStatsLLR-version {} --apply-weights True "
        "--feature-names {} --FeaturePlot-is-llr --save-png --stack True")


years = ["2016", "2016APV", "2017", "2018"]
channels = ["tautau", "mutau", "etau"]
categories = ["baseline", "resolved_1b", "resolved_2b", "boosted_l", "boosted_m"]
feature_names = ("lep1_eta,lep2_eta,lep1_pt,lep2_pt,bjet1_pt,bjet1_eta,bjet2_pt,bjet2_eta,"
                "met_pt,met_phi,Htt_svfit_mass,Htt_mass,Hbb_mass")

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