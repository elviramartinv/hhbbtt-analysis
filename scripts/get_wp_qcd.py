from subprocess import call

import argparse
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-y', '--year', type=int, default = None, help='year to be run')
parser.add_argument('-c', '--category', dest='category', default=None, help='category to be run')
parser.add_argument('-ch', '--channel', dest='channel', default=None, help='channel to be run')
options = parser.parse_args()

command_vbf = (" law run TrainingOutputPlot --version test_qcd_shapeB --EvaluateData-version hyperopt6_{} --category-name vbf"
"    --config-name base_{}     --data-config-names {} --MergeCategorizationStats-version {} --workers 6"
"    --region-name {}_os_inviso__vvl_vl --skip-dataset-names dy_high,hh_ggf_0,hh_vbf_1_0_1,hh_vbf_c2v,{} --skip-dataset-tags ggf_lo"
"    --do-qcd --stack --hide-data False --SkimCategorization-version {} --Training-version hyperopt6 --training-category-name vbf_os"
"    --TrainingOutputPlot-cross-evaluation --training-config-name default     --architecture lbn_dense:30:default:0_4:tanh"
"    --feature-tag lbn_light     --l2-norm 1  --learning-rate 1    --dropout-rate 1 --random-seeds     1,2,3,4,5,6,7,8,9,10  --loss-name bsm"
"    --event-weights False --MergeCategorization-version {} --qcd-wp vvvl_vvl --qcd-signal-region-wp os_inviso__vvl_vl --FeaturePlot-qcd-category-name vbf"
"    --shape-region ss_iso")

command_others = (" law run FeaturePlot --version test_qcd_shapeB  --category-name {} --feature-names DNNoutSM_kl_1"
"    --config-name base_{}    --MergeCategorizationStats-version {} --workers 6"
"    --region-name {}_os_inviso__vvl_vl --skip-dataset-names dy_high,hh_ggf_0,hh_vbf_1_0_1,hh_vbf_c2v,{} --skip-dataset-tags ggf_lo"
"    --do-qcd --stack --hide-data False --SkimCategorization-version {}"
"    --MergeCategorization-version {} --qcd-wp vvvl_vvl --qcd-signal-region-wp os_inviso__vvl_vl --FeaturePlot-qcd-category-name {}"
"    --shape-region ss_iso")

versions = {"tautau": "prodFeb", "mutau": "prodFeb", "etau": "prodFebETau"}
qcd_category = {"boosted": "boosted_nobtag", "resolved_1b": "default", "resolved_2b": "default"}
years = [2016, 2017, 2018]

for year in years:
    if options.year:
        if year != options.year:
            continue
    for cat in ["resolved_1b", "resolved_2b", "boosted", "vbf"]:
        if options.category:
            if cat != options.category:
                continue
    # for cat in ["vbf"]:
        for channel, version in versions.items():
            if options.channel:
                if channel != options.channel:
                    continue
            skip_channels = ",".join(["data_%s" % ch for ch in versions.keys() if ch != channel])
            if cat == "vbf":
                data_years = ",".join(["base_%s" % y for y in years if y != year])
                command = command_vbf.format(version, year, data_years, version, channel, skip_channels, version, version)
            else:
                command = command_others.format(cat, year, version, channel, skip_channels, version, version, qcd_category[cat])
            print "Running '%s'" % command
            rc = call(command, shell=True) 
