from subprocess import call
from math import sqrt
from collections import OrderedDict
import argparse
parser = argparse.ArgumentParser(description='options')
parser.add_argument('-y', '--year', type=int, default = None, help='year to be run')
parser.add_argument('-sy', '--skipYear', type=int, default = None, help='year to be skipped')
parser.add_argument('-c', '--category', dest='category', default=None, help='category to be run')
parser.add_argument('-sc', '--skipCategory', dest='skipCategory', default=None, help='category to be skipped')
parser.add_argument('-ch', '--channel', dest='channel', default=None, help='channel to be run')
parser.add_argument('-sch', '--skipChannel', dest='skipChannel', default=None, help='channel to be skipped')
parser.add_argument('-v', '--version', dest='version', default="__feb", help='output version')
parser.add_argument('-s', '--skip', action='store_true', default = False)
parser.add_argument('-r', '--remove', type=int, default = -1, help='remove output')
options = parser.parse_args()

import time
print ("ATTENTION: Running with boosted instead of boosted_nobtag")
time.sleep(2)


command = ("law run FeaturePlotQCDTest --feature-names {}    --version qcd_test" + options.version + "__{}   --category-name {}    --region-name {}_os_iso --SkimCategorization-version prod{} "
    "--MergeCategorizationStats-version prod{} --MergeCategorization-version prod{} --workers 9 --skip-dataset-names hh_vbf_c2v,hh_vbf_1_0_1,hh_ggf_0 --config-name base_{} "
    "--data-config-names {} --event-weights False --FeaturePlot-qcd-category-name {}")
    
if options.remove >= 0:
    command += " --remove-output " + str(options.remove)
    
def make_red(string):
    return "\\textcolor{red}{" + string + "}"
def make_green(string):
    return "\\textcolor{mynicegreen}{" + string + "}"
def make_blue(string):
    return "\\textcolor{blue}{" + string + "}"
    
channels = ["tautau", "mutau", "etau"]

params = OrderedDict()
params[2016] = OrderedDict() 
params[2016]["boosted"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "boosted")
params[2016]["resolved_1b"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "default") 
params[2016]["resolved_2b"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "default") 

params[2017] = OrderedDict()
params[2017]["boosted"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "boosted")
params[2017]["resolved_1b"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "default") 
params[2017]["resolved_2b"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "default") 

params[2018] = OrderedDict()
params[2018]["boosted"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "boosted")
params[2018]["resolved_1b"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "default") 
params[2018]["resolved_2b"] = (["tautau", "mutau", "etau"], ["lep1_eta"], "default") 

txtname = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + options.version + "__{}/qcd_inviso__{}__{}.txt"
ss_iso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + options.version + "__{}/n_ss_iso__{}__{}.txt"
ss_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + options.version + "__{}/n_ss_inviso__{}__{}.txt"
os_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/base_{}/cat_{}/qcd_test" + options.version + "__{}/n_os_inviso__{}__{}.txt"

os_iso = OrderedDict() 
for year in params:
    if options.year:
        if year != options.year: continue
    if options.skipYear:
        if year == options.skipYear: continue
    os_iso[year] = OrderedDict()
    for category in params[year]:
        if options.category:
            if category != options.category: continue
        if options.skipCategory:
            if category == options.skipCategory: continue
        my_category = category
        my_category += (" ({}) ".format(params[year][category][2])
            if params[year][category][2] != "default" else "")
        os_iso[year][my_category] = OrderedDict()
        for channel in ["tautau", "mutau", "etau"]:
            if options.channel:
                if channel != options.channel: continue
            if options.skipChannel:
                if channel == options.skipChannel: continue
            os_iso[year][my_category][channel] = OrderedDict()
            for features in params[year][category][1]:
                for feature in features.split(","):
                    os_iso[year][my_category][channel][feature] = OrderedDict()
ss_iso = OrderedDict() 
ss_inviso = OrderedDict()
os_inviso = OrderedDict()
for year in params:
    if options.year:
        if year != options.year: continue
    if options.skipYear:
        if year == options.skipYear: continue
    ss_iso[year] = OrderedDict()
    ss_inviso[year] = OrderedDict()
    os_inviso[year] = OrderedDict()
    for category in params[year]:
        if options.category:
            if category != options.category: continue
        if options.skipCategory:
            if category == options.skipCategory: continue
        my_category = category
        my_category += (" ({}) ".format(params[year][category][2])
            if params[year][category][2] != "default" else "")
        ss_iso[year][my_category] = OrderedDict()
        ss_inviso[year][my_category] = OrderedDict()
        os_inviso[year][my_category] = OrderedDict()        
        for features in params[year][category][1]:
            for feature in features.split(","):
                ss_iso[year][my_category][feature] = OrderedDict()
                ss_inviso[year][my_category][feature] = OrderedDict()
                os_inviso[year][my_category][feature] = OrderedDict()         

def get_year(year, feature):
    years = ["2016", "2017", "2018"]
    return year
    # else:
        # return "_".join([str(year)] + [y for y in years if y != str(year)])


def add_multicategory(category, feature):
    category = category.split(" ")
    category[0] += ","
    category.insert(1, feature)
    category.insert(2, "class")
    return " ".join(category)


skip = (options.skip and "remove-output" not in command)
for year in params:
    if options.year:
        if year != options.year: continue
    if options.skipYear:
        if year == options.skipYear: continue
    for category in params[year]:
        if options.category:
            if category != options.category: continue
        if options.skipCategory:
            if category == options.skipCategory: continue
        for ic, channel in enumerate(channels):
            if options.channel:
                if channel != options.channel: continue
            if options.skipChannel:
                if channel == options.skipChannel: continue
            if not skip:
                if year == 2016:
                    data_config_names = "base_2017,qcd_llr_2018"
                elif year == 2017:
                    data_config_names = "base_2016,qcd_llr_2018"
                elif year == 2018:
                    data_config_names = "base_2016,base_2017"
                    
                datasets_to_skip = ",".join(["data_" + chan for chan in channels if chan != channel])
                    
                for features in params[year][category][1]:
                    command_to_run = command.format(features, channel, category, channel,
                        params[year][category][0][ic], params[year][category][0][ic],
                        params[year][category][0][ic], year, data_config_names,
                        params[year][category][0][ic], params[year][category][2],
                        datasets_to_skip)
                    print ("Running '{}'".format(command_to_run))
                    rc = call(command_to_run, shell=True)
            if "remove-output" not in command:
                my_category = category
                my_category += (" ({}) ".format(params[year][category][2])
                    if params[year][category][2] != "default" else "")
                for features in params[year][category][1]:
                    for feature in features.split(","):
                        name = txtname.format(get_year(year, feature), category, channel, channel, feature)
                        with open(name) as f:
                            lines = f.readlines()
                            for l in lines:
                                values = l.strip().split(" ")
                                # print name, values
                                os_iso[year][my_category][channel][feature][values[0]] = (values[1],
                                    values[2])
                        name = ss_iso_name.format(get_year(year, feature), category, channel, channel, feature)
                        with open(name) as f:
                            lines = f.readlines()
                            if lines: l = lines[0]
                            values = l.strip().split(" ")
                            ss_iso[year][my_category][feature][channel] = (float(values[1]),
                                float(values[2]))

                        name = ss_inviso_name.format(get_year(year, feature), category, channel, channel, feature)
                        with open(name) as f:
                            lines = f.readlines()
                            if lines: l = lines[0]
                            values = l.strip().split(" ")
                            ss_inviso[year][my_category][feature][channel] = (float(values[0]),
                                float(values[1]))

                        name = os_inviso_name.format(get_year(year, feature), category, channel, channel, feature)
                        with open(name) as f:
                            lines = f.readlines()
                            if lines: l = lines[0]
                            values = l.strip().split(" ")
                            os_inviso[year][my_category][feature][channel] = (float(values[0]),
                                float(values[1]))

def get_param(tup):
    if isinstance(tup[1], str):
        num = tup[1].split("*")
    else:
        num = [tup[1]]
    num_of_zeros = len(num) - 1
    value = float(tup[0])
    error = float(num[0])
    if value == 0.:
        return "0", num_of_zeros
    else:
       my_str = "${:.3f} \pm {:.3f}$ $({:>2.1f}\\%)$".format(value, error, 100 * error/value)
       return my_str, num_of_zeros
       
def redondear(value, error):
    dec = 1
    while (True):
        if round(value, dec + 1) != 0 and round(error, dec + 1) != 0:
            value = round(value, dec + 1)
            error = round(error, dec + 1)
            break
        if dec == 10:
            break
        dec += 1
    return value, error

def is_compatible(tup):
    if tup[0] - tup[1] < 0:
        return True
    return False

def rel_error(value):
    return value[1] / value[0] if value[0] != 0 else 0
    
def compute_lnn(ssinviso, ssiso):
    return sqrt(rel_error(ssinviso)**2 + rel_error(ssiso)**2)

additional_syst = {}
if "remove-output" not in command:
    for year in params:
        if options.year:
            if year != options.year: continue
        if options.skipYear:
            if year == options.skipYear: continue
        additional_syst[year] = {}
        print "********* {} *********".format(year)
        for category in params[year]:
            if options.category:
                if options.category != category: continue
            if options.skipCategory:
                if category == options.skipCategory: continue
            my_category = category
            my_category += (" ({}) ".format(params[year][category][2])
                if params[year][category][2] != "default" else "")
            additional_syst[year][category] = {}
            for features in params[year][category][1]:
                for feature in features.split(","):
                    additional_syst[year][category][feature] = {}
                    for i, channel in enumerate(["tautau", "mutau", "etau"]):
                        if options.channel:
                            if channel != options.channel: continue
                        if options.skipChannel:
                            if channel == options.skipChannel: continue
                        my_chan = "$" + channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace("e", "\\tau_e") + "$"
                        my_cat = my_category.replace("_", "\\_") if i == 1 else ""
                        my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                        my_feature = "" if i != 1 else my_feature
                        this_st = os_iso[year][my_category][channel][feature]
                        
                        Standard_str, num_of_zeros = get_param(this_st["Standard"])
                        mean_str, _ = get_param(this_st["Mean"])
                        if mean_str == "0":
                            mean_str = "-"
                            num_of_zeros = 0
                        fit_str, _ = get_param(this_st["Fit"])
                        # print fit_str
                        if fit_str == "0":
                            fit_str = "-"

                        Standard_val = float(this_st["Standard"][0])
                        Standard_error = float(this_st["Standard"][1].split("*")[0])
                        mean_val = float(this_st["Mean"][0])
                        if my_cat != "" and my_feature != "":
                            my_cat = add_multicategory(my_cat, my_feature)
                        
                        syst_to_print = "-"
                        additional_syst[year][category][feature][channel] = 0
                        if mean_str != "-":
                            if (Standard_val - Standard_error > mean_val or Standard_val + Standard_error < mean_val):
                                Standard_str = make_red(Standard_str)
                                if Standard_val != 0:
                                    additional_syst[year][category][feature][channel] = sqrt(
                                        ((Standard_val - mean_val)/(Standard_val))**2
                                        - ((Standard_error / Standard_val)**2))
                                # print  ((Standard_val - mean_val)/(Standard_val))**2,  (Standard_error / Standard_val)**2
                                    syst_to_print = "{:4.2f}".format(additional_syst[year][category][feature][channel])
                        print "{:<35} &{:<6} & {}{} & {} & {} & {:<4}\\\\".format(
                            my_cat, my_chan, Standard_str, "*" * num_of_zeros, mean_str, fit_str, syst_to_print)
                    print "\\hline"

    print
    print 
    
    # for year in ss_iso:
        # print "********* {} *********".format(year)
        # for category in ss_iso[year]:
            # for feature in params[year][category][1].split(","):
                # for i, channel in enumerate(["tautau", "mutau", "etau"]):
                    # my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
                    # my_cat = category.replace("_", "\\_") if i == 1 else ""
                    # my_str = (
                        # "0" if os_iso[year][category][channel]["Standard"] == 0
                        # else "${:<8.3f} \pm {:<8.3f}$ $({:>2.1f}\\%)$".format(
                            # ss_iso[year][category][channel][0], ss_iso[year][category][channel][1], 
                            # 100 * ss_iso[year][category][channel][1] / ss_iso[year][category][channel][0])
                    # )
                    # print "{:<15} & {:<10} & {}\\\\".format(
                        # my_cat, my_chan, my_str)
                # print "\\hline"

    # print
    # print 

    print "******************** lnN ***********************"


    year_string = "{:<35} & {:<10} ".format(" ", " ")
    for year in ss_inviso:
        if options.year:
            if year != options.year: continue
        if options.skipYear:
            if year == options.skipYear: continue
        year_string += "& {:<5} ".format(year)
      
    print year_string + "\\\\"

    for year in ss_inviso:
        if len(ss_inviso[year].keys()) > 0:
            first_year = year
            break

    total_categories = []
    for year in params:
        if options.year:
            if year != options.year: continue
        if options.skipYear:
            if year == options.skipYear: continue
        total_categories += [(cat, year) for cat in params[year] if not any([val[0] == cat for val in total_categories])]

    for category, cat_year in total_categories:
        if options.category:
            if category != options.category: continue
        if options.skipCategory:
            if category == options.skipCategory: continue
        my_category = category
        my_category += (" ({}) ".format(params[year][category][2])
            if params[cat_year][category][2] != "default" else "")
        for features in params[cat_year][category][1]:
            for feature in features.split(","):
                for i, channel in enumerate(["tautau", "mutau", "etau"]):
                    if options.channel:
                        if channel != options.channel: continue
                    if options.skipChannel:
                        if channel == options.skipChannel: continue
                    my_cat = my_category.replace("_", "\\_") if i == 1 else ""
                    my_chan = "$" + channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace("e", "\\tau_e") + "$"
                    my_str = ""
                    my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                    my_feature = "" if i != 1 else my_feature
                    for year in ss_inviso:
                        if options.year:
                            if year != options.year: continue
                        if my_category not in ss_inviso[year].keys():
                            my_str += "& - "
                        else:
                            # if ss_iso[year][my_category][feature][channel][0] - ss_iso[year][my_category][feature][channel][1] > 0\
                                    # and ss_inviso[year][my_category][feature][channel][0] - ss_inviso[year][my_category][feature][channel][1] > 0:
                                # lnN = ((ss_iso[year][category][channel][0] / ss_inviso[year][category][channel][0]) * 
                            lnN = compute_lnn(ss_inviso[year][my_category][feature][channel], ss_iso[year][my_category][feature][channel])
                            # else:
                                # lnN = -1
                            my_str += (
                                "& {:<5} ".format("$-$") if float(os_iso[year][my_category][channel][feature]["Standard"][0]) == 0
                                else "& {:<5.3f} ".format(1 + lnN)
                            )
                    if my_cat != "" and my_feature != "":
                        my_cat = add_multicategory(my_cat, my_feature)
                    print "{:<35} & {:<10} {}\\\\".format(
                        my_cat, my_chan, my_str)
                print "\\hline"
    print
    print
    
    print "******************** Full lnN ***********************"

    year_string = "{:<35} & {:<16} ".format(" ", " ")
    for year in ss_inviso:
        if options.year:
            if year != options.year: continue
        if options.skipYear:
            if year == options.skipYear: continue
        year_string += "& {:<20} ".format(year)
      
    print year_string + "\\\\\\hline"
    
    
    for category, cat_year in total_categories:
        if options.category:
            if category != options.category: continue
        if options.skipCategory:
            if category == options.skipCategory: continue
        my_category = category
        my_category += (" ({}) ".format(params[year][category][2])
            if params[cat_year][category][2] != "default" else "")
        for features in params[cat_year][category][1]:
            for feature in features.split(","):
                for i, channel in enumerate(["tautau", "mutau", "etau"]):
                    if options.channel:
                        if channel != options.channel: continue
                    if options.skipChannel:
                        if channel == options.skipChannel: continue
                    my_cat = my_category.replace("_", "\\_") if i == 1 else ""
                    my_chan = "$" + channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace("e", "\\tau_e") + "$"
                    my_str = ""
                    my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                    my_feature = "" if i != 1 else my_feature
                    for year in ss_inviso:
                        if options.year:
                            if year != options.year: continue
                        if my_category not in ss_inviso[year].keys():
                            my_str += "& - "
                        else:
                            # if ss_iso[year][my_category][feature][channel][0] - ss_iso[year][my_category][feature][channel][1] > 0\
                                    # and ss_inviso[year][my_category][feature][channel][0] - ss_inviso[year][my_category][feature][channel][1] > 0:
                                # lnN = ((ss_iso[year][category][channel][0] / ss_inviso[year][category][channel][0]) * 
                            lnN = compute_lnn(ss_inviso[year][my_category][feature][channel], ss_iso[year][my_category][feature][channel])
                            str_to_add = "{:<5.1f}".format(100. * lnN)
                            if additional_syst[year][category][feature][channel] != 0:
                                # lnN = sqrt(lnN**2 + (1 + additional_syst[year][category][feature][channel])**2)
                                str_to_add += ", {:<5.1f}".format(100 * additional_syst[year][category][feature][channel])
                                # str_to_add = make_red(" {:<5.3f} ".format(1 + lnN))
                            my_str += (
                                "& {:<12} ".format("$-$") if float(os_iso[year][my_category][channel][feature]["Standard"][0]) == 0
                                else "& {:<12} ".format(str_to_add)
                            )
                    if my_cat != "" and my_feature != "":
                        my_cat = add_multicategory(my_cat, my_feature)
                    print "{:<35} & {:<10} {}\\\\".format(
                        my_cat, my_chan, my_str)
                print "\\hline"
    print
    
    
    print "*" * 20
    print "{:^20}".format("QCD diagnosis")
    print "*" * 20
   
    final_table = []

    for year in params:
        if options.year:
            if year != options.year: continue
        if options.skipYear:
            if year == options.skipYear: continue
        print "********* {} *********".format(year)
        print "\\begin{tabular}{%s}" % ("|".join("c" for i in range(5)))
        print "Category & channel & B & C & D \\\\\\hline"
        for category in params[year]:
            if options.category:
                if category != options.category: continue
            if options.skipCategory:
                if category == options.skipCategory: continue
            my_category = category
            my_category += (" ({}) ".format(params[year][category][2])
                if params[year][category][2] != "default" else "")
            for features in params[year][category][1]:
                for feature in features.split(","):
                    for i, channel in enumerate(["tautau", "mutau", "etau"]):
                        if options.channel:
                            if channel != options.channel: continue
                        if options.skipChannel:
                            if channel == options.skipChannel: continue
                        my_chan = "$" + channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace("e", "\\tau_e") + "$"
                        my_cat = my_category.replace("_", "\\_") if i == 1 else ""
                        my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                        my_feature = "" if i != 1 else my_feature

                        if my_category not in ss_inviso[year].keys():
                            my_str = "& - & - & -"
                        else:
                            my_str = ""
                            is_bad = any([is_compatible(region[year][my_category][feature][channel])
                                for region in [ss_iso, os_inviso, ss_inviso]])
                            for region in [ss_iso, os_inviso, ss_inviso]:
                                value = region[year][my_category][feature][channel][0]
                                error = region[year][my_category][feature][channel][1]
                                value, error = redondear(value, error)                            
                                val_err = "${} \pm {}$".format(value, error)
                                if value <= 0:
                                    val_err = make_red(val_err)
                                elif value - error <= 0:
                                    val_err = make_blue(val_err)
                                if not is_bad:
                                    val_err = make_green(val_err)
                                my_str += "& {} ".format(val_err)
                        if my_cat != "" and my_feature != "":
                            my_cat = add_multicategory(my_cat, my_feature)
                        print "{:<35} & {:<10} {}\\\\".format(
                            my_cat, my_chan, my_str)
                    print "\\hline"

        print "\\end{tabular}"

    # print 
    # print
    # print year_string + "\\\\\\hline"
    # for category in ss_inviso[first_year]:
        # for i, channel in enumerate(["tautau", "mutau", "etau"]):
            # my_chan = "$" + channel.replace("tau", "\\tau").replace("mu", "\\mu") + "$"
            # my_cat = category.replace("_", "\\_") if i == 1 else ""
            # my_str = ""
            # for year in ss_inviso:
                # if category not in ss_inviso[year].keys():
                    # my_str += "& - "
                # else:
                    # if (not is_compatible(ss_iso[year][category][channel]) and not is_compatible(os_inviso[year][category][channel])
                            # and not is_compatible(ss_inviso[year][category][channel])):
                        # value = ss_iso[year][category][channel][0] * os_inviso[year][category][channel][0] / ss_inviso[year][category][channel][0]
                        # error = value * sqrt(sum([(region[year][category][channel][1] / region[year][category][channel][0]) ** 2
                            # for region in [ss_iso, os_inviso, ss_inviso]]))
                        # value, error = redondear(value, error)
                    # my_str += (
                        # "& {:^5} ".format("$-$") if os_iso[year][category][channel]["Standard"][0] == 0
                        # else "& $ {} \pm {}$ $({:>2.1f}\\%)$".format(str(value), str(error), error/value)
                    # )
            # print "{:<15} & {:<10} {:<20}\\\\".format(
                # my_cat, my_chan, my_str)
        # print "\\hline"
    # print
    
    print "******************** B/D ***********************"
    
    def print_b_d(year):
        print year_string + "\\\\\\hline"
        for category, cat_year in total_categories:
            if options.category:
                if category != options.category: continue
            if options.skipCategory:
                if category == options.skipCategory: continue
            my_category = category
            my_category += (" ({}) ".format(params[year][category][2])
                if params[cat_year][category][2] != "default" else "")
            for features in params[cat_year][category][1]:
                for feature in features.split(","):
                    for i, channel in enumerate(["tautau", "mutau", "etau"]):
                        if options.channel:
                            if channel != options.channel: continue
                        if options.skipChannel:
                            if channel == options.skipChannel: continue
                        my_cat = my_category.replace("_", "\\_") if i == 1 else ""
                        my_chan = "$" + channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace("e", "\\tau_e") + "$"
                        my_str = ""
                        my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                        my_feature = "" if i != 1 else my_feature
                        for year in ss_inviso:
                            if options.year:
                                if year != options.year: continue
                            if my_category not in ss_inviso[year].keys():
                                my_str += "& - "
                            else:
                                # if ss_iso[year][my_category][feature][channel][0] - ss_iso[year][my_category][feature][channel][1] > 0\
                                        # and ss_inviso[year][my_category][feature][channel][0] - ss_inviso[year][my_category][feature][channel][1] > 0:
                                    # lnN = ((ss_iso[year][category][channel][0] / ss_inviso[year][category][channel][0]) * 
                                BD = ss_iso[year][my_category][feature][channel][0] / ss_inviso[year][my_category][feature][channel][0]
                                str_to_add = "{:<5.3f}".format(BD)
                                my_str += (
                                    "& {:<12} ".format("$-$") if float(os_iso[year][my_category][channel][feature]["Standard"][0]) == 0
                                    else "& {:<12} ".format(str_to_add)
                                )
                        if my_cat != "" and my_feature != "":
                            my_cat = add_multicategory(my_cat, my_feature)
                        print "{:<35} & {:<10} {}\\\\".format(
                            my_cat, my_chan, my_str)
                    print "\\hline"
        print
    # print_b_d(year)
    
    def print_b_d_errors(year):
        print year_string + "\\\\\\hline"
        for category, cat_year in total_categories:
            if options.category:
                if category != options.category: continue
            if options.skipCategory:
                if category == options.skipCategory: continue
            my_category = category
            my_category += (" ({}) ".format(params[year][category][2])
                if params[cat_year][category][2] != "default" else "")
            for features in params[cat_year][category][1]:
                for feature in features.split(","):
                    for i, channel in enumerate(["tautau", "mutau", "etau"]):
                        if options.channel:
                            if channel != options.channel: continue
                        if options.skipChannel:
                            if channel == options.skipChannel: continue
                        my_cat = my_category.replace("_", "\\_") if i == 1 else ""
                        my_chan = "$" + channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace("e", "\\tau_e") + "$"
                        my_str = ""
                        my_feature = "" if not "DNN" in feature else feature.split("kl_1_")[1].split('_merged')[0].replace("_", "\\_")
                        my_feature = "" if i != 1 else my_feature
                        for year in ss_inviso:
                            if options.year:
                                if year != options.year: continue
                            if my_category not in ss_inviso[year].keys():
                                my_str += "& - "
                            else:
                                # if ss_iso[year][my_category][feature][channel][0] - ss_iso[year][my_category][feature][channel][1] > 0\
                                        # and ss_inviso[year][my_category][feature][channel][0] - ss_inviso[year][my_category][feature][channel][1] > 0:
                                    # lnN = ((ss_iso[year][category][channel][0] / ss_inviso[year][category][channel][0]) * 
                                BD = ss_iso[year][my_category][feature][channel][0] / ss_inviso[year][my_category][feature][channel][0]
                                BDerror = BD * sqrt((ss_iso[year][my_category][feature][channel][1] / ss_iso[year][my_category][feature][channel][0])**2
                                    + (ss_inviso[year][my_category][feature][channel][1] / ss_inviso[year][my_category][feature][channel][0])**2)
                                str_to_add = "${:<5.3f} \\pm {:<5.3f}$".format(BD, BDerror)
                                my_str += (
                                    "& {:<20} ".format("$-$") if float(os_iso[year][my_category][channel][feature]["Standard"][0]) == 0
                                    else "& {:<20} ".format(str_to_add)
                                )
                        if my_cat != "" and my_feature != "":
                            my_cat = add_multicategory(my_cat, my_feature)
                        print "{:<35} & {:<16} {}\\\\".format(
                            my_cat, my_chan, my_str)
                    print "\\hline"
        print
    print_b_d_errors(year)
