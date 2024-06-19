from subprocess import call
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-v', '--version', dest='version', default = None, help='version')
options = parser.parse_args()



command = ("law run FeaturePlot --version " + options.version + " --config-name qcd_llr_{} "
        "--category-name {} --region-name {}_os_iso --process-group-name plots "
        "--do-qcd True --tree-name HTauTauTree --stack True --MergeCategorization-version {} "
        "--MergeCategorizationStatsLLR-version {} --apply-weights True "
        "--feature-names {} --is-llr --hide-data False --save-png --save-yields")


years = ["2016", "2016APV", "2017", "2018"]
# years = ["2017"]
channels = ["tautau", "mutau", "etau"]
categories = ["baseline"]
# categories = ["baseline", "resolved_1b", "resolved_2b"]
# feature_names = ("Htt_mass,Htt_svfit_mass,Hbb_mass,lep1_eta,lep1_phi,lep1_pt,lep2_eta,lep2_pt,lep2_phi,lep1_deepTauVSmu,lep1_deepTauVSe,lep1_deepTauVSjet,"
            # "lep2_deepTauVSmu,lep2_deepTauVSe,lep2_deepTauVSjet,bjet1_pt,bjet1_eta,bjet1_phi,bjet2_pt,bjet2_eta,bjet2_phi,bjet1_deepFlav,bjet2_deepFlav")
feature_names =  ("bjet2_pt")

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