import pandas as pd
from math import sqrt


def create_QCDdiagnosis_table(data):
    with open('scripts/QCD_diagnosis.tex', 'w') as f:
        f.write('\\renewcommand{\\familydefault}{\\sfdefault}\n')
        f.write('\\begin{table}[h]\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{c|c|c|c|c}\n')
        f.write('\\hline\n')
        f.write('Category & Channel & Region B & Region C & Region D \\\\ \\hline\n')
        last_cat = ""
        for i, row in enumerate(data):
            if row[0] != last_cat:
                cat_name = row[0].replace("_", " ")
                if i != 0:  
                    f.write('\cline{1-5}')  
                f.write('\multirow{3}{*}{' + cat_name + '}')
                last_cat = row[0]
            if row[1] == "etau":
                ch_name = "$e\\tau$"
            elif row[1] == "mutau":
                ch_name = "$\\mu\\tau$"
            elif row[1] == "tautau":
                ch_name = "$\\tau\\tau$"
            f.write(' & {} & {} $\\pm$ {} & {} $\\pm$ {} & {} $\\pm$ {} \\\\ \n'.format(
                ch_name, row[2], row[3], row[4], row[5], row[6], row[7]))
        f.write('\\end{tabular}\n')
        f.write('\\caption{QCD Diagnosis 2017}\n')
        f.write('\\label{tab:mi_tabla}\n')
        f.write('\\end{table}\n')

def create_summary_test1(data):
    with open('scripts/summary_test1.tex', 'w') as f:
        f.write('\\renewcommand{\\familydefault}{\\sfdefault}\n')
        f.write('\\begin{table}[h]\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{c|c|c|c|c|c}\n')
        f.write('\\hline\n')    
        f.write('Category & Channel & Standard (vvvl-m) & Average & Constant Fit & Add unc \\\\ \\hline\n')
        last_cat = ""
        for i, row in enumerate(data):
            if row[0] != last_cat:
                cat_name = row[0].replace("_", " ")
                if i !=0:
                    f.write('\cline{1-6}')
                f.write('\multirow{3}{*}{' + cat_name + '}')
                last_cat = row[0]
            if row[1] == "etau":
                ch_name = "$e\\tau$"
            elif row[1] == "mutau":
                ch_name = "$\\mu\\tau$"
            elif row[1] == "tautau":
                ch_name = "$\\tau\\tau$"
            if row[2] == "0" and row[5] == "-" and row[8] == "-":
                std_text = "{}".format(row[2])
                mean_text = "{}".format(row[5])
                fit_text = "{}".format(row[8])
            elif row[2] == "0" and row[5] != "-" and row[8] == "-":
                std_text = "{}".format(row[2])
                mean_text = "{} $\pm$ {} ({}\%)".format(row[5], row[6], row[7])
                fit_text = "{}".format(row[8])
            elif row[2] == "0" and row[5] != "-" and row[8] != "-":
                std_text = "{}".format(row[2])
                mean_text = "{} $\pm$ {} ({}\%)".format(row[5], row[6], row[7])
                fit_text = "{} $\pm$ {} ({}\%)".format(row[8], row[9], row[10])
            else:
                mean_text = "{} $\pm$ {} ({}\%)".format(row[5], row[6], row[7])
                fit_text = "{} $\pm$ {} ({}\%)".format(row[8], row[9], row[10])
                if row[11] != "-":
                    std_text = "\\color{red}{" + "{} $\pm$ {} ({}\%)".format(row[2], row[3], row[4]) + "}"
                else:
                    std_text = "{} $\pm$ {} ({}\%)".format(row[2], row[3], row[4])

            f.write(' & {} & {} & {} & {}  & {} \\\\ \n'.format(
                ch_name, std_text, mean_text, fit_text, row[11]))
        f.write('\\end{tabular}\n')
        f.write('\\caption{QCD Test 1 Summary}\n')
        f.write('\\label{tab:mi_tabla}\n')
        f.write('\\end{table}\n')

def create_QCD_uncertainty(data):
    with open('scripts/uncertainties.tex', 'w') as f:
        f.write('\\renewcommand{\\familydefault}{\\sfdefault}\n')
        f.write('\\begin{table}[h]\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{c|c|c|c}\n')
        f.write('\\hline\n')
        f.write('Category & Channel & $B/D$ & $\\ln N$ \\\\ \\hline\n')
        last_cat = ""
        for i, row in enumerate(data):
            if row[0] != last_cat:
                cat_name = row[0].replace("_", " ")
                if i != 0:
                    f.write('\cline{1-4}')
                f.write('\multirow{3}{*}{' + cat_name + '}')
                last_cat = row[0]
            if row[1] == "etau":
                ch_name = "$e\\tau$"
            elif row[1] == "mutau":
                ch_name = "$\\mu\\tau$"
            elif row[1] == "tautau":
                ch_name = "$\\tau\\tau$"
            f.write(' & {} & {} & {}  \\\\ \n'.format(
                ch_name, row[2], row[3]))
        f.write('\\end{tabular}\n')
        f.write('\\caption{QCD Uncertainties}\n')
        f.write('\\label{tab:mi_tabla}\n')
        f.write('\\end{table}\n' )

# def create_envelope_table(data_envelope):
#     with open('scripts/envelope.tex', 'w') as f:
#         f.write('\\renewcommand{\\familydefault}{\\sfdefault}\n')
#         f.write('\\begin{table}[h]\n')
#         f.write('\\centering\n')
#         f.write('\\begin{tabular}{c|c|c|c|c}\n')
#         f.write('\\hline\n')
#         f.write('Category & Channel & Standard & Max & Min \\\\ \\hline\n')
#         last_cat = ""
#         for i, row in enumerate(data_envelope):
#             if row[0] != last_cat:
#                 cat_name = row[0].replace("_", " ")
#                 if i != 0:
#                     f.write('\cline{1-5}')
#                 f.write('\multirow{3}{*}{' + cat_name + '}')
#                 last_cat = row[0]
#             if row[1] == "etau":
#                 ch_name = "$e\\tau$"
#             elif row[1] == "mutau":
#                 ch_name = "$\\mu\\tau$"
#             elif row[1] == "tautau":
#                 ch_name = "$\\tau\\tau$"
#             f.write(' & {} & {} $\pm$ {} & {} $\pm$ {} & {} $\pm$ {} \\\\ \n'.format(
#                 ch_name, row[2], row[3], row[4], row[5], row[6], row[7]))
#         f.write('\\end{tabular}\n')
#         f.write('\\caption{QCD Envelope}\n')
#         f.write('\\label{tab:mi_tabla}\n')
#         f.write('\\end{table}\n')

def create_envelope_table(data_envelope):
    with open('scripts/envelope.tex', 'w') as f:
        f.write('\\renewcommand{\\familydefault}{\\sfdefault}\n')
        f.write('\\begin{table}[h]\n')
        f.write('\\centering\n')
        f.write('\\begin{tabular}{c|c|c|c|c|c}\n')
        f.write('\\hline\n')
        f.write('Category & Channel & Std C/D & Max C/D & Min C/D & Envelope \\\\ \\hline\n')
        last_cat = ""
        for i, row in enumerate(data_envelope):
            if row[0] != last_cat:
                cat_name = row[0].replace("_", " ")
                if i != 0:
                    f.write('\cline{1-6}')
                f.write('\multirow{3}{*}{' + cat_name + '}')
                last_cat = row[0]
            if row[1] == "etau":
                ch_name = "$e\\tau$"
            elif row[1] == "mutau":
                ch_name = "$\\mu\\tau$"
            elif row[1] == "tautau":
                ch_name = "$\\tau\\tau$"
            if row[2] == "0":
                row[4] = "-"
                row[6] = "-"
                f.write(' & {} & {} & {} & {} & {} \\\\ \n'.format(
                    ch_name, row[2], row[4], row[6], row[2]))
            else:
                f.write(' & {} & {} & {} & {} & ${}^{{+{}({}\%)}}_{{-{}({}\%)}}$ \\\\ \n'.format(
                    ch_name, row[2], row[4], row[6], row[2], row[8], row[10], row[9], row[11]))
        f.write('\\end{tabular}\n')
        f.write('\\caption{QCD Envelope}\n')
        f.write('\\label{tab:mi_tabla}\n')
        f.write('\\end{table}\n')


def read_stuff(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            parts = l.split()
            if parts[0] == 'Fit':
                fit_val = float(parts[1])
                fit_error = float(parts[2])
            elif parts[0] == 'Mean':
                mean_val = float(parts[1])
                mean_error = float(parts[2])
            elif parts[0] == 'Standard':
                standard_val = float(parts[1])
                standard_error = float(parts[2].rstrip('*'))
                standard_stars = (parts[2]).strip('*')
        return fit_val, fit_error, mean_val, mean_error, standard_val, standard_error, standard_stars
def read_results_2(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        values = lines[0].strip().split(" ")
        # for l in lines:
        #     values = l.strip().split(' ')
        return float(values[1]), float(values[2])
def read_results(filename):
    # Leer los resultados del archivo de texto y devolver los valores relevantes
    with open(filename, 'r') as file:
        lines = file.readlines()
        for l in lines:
            values = l.strip().split(" ")
        return float(values[0]), float(values[1])  # Valor y error
    
def is_compatible(value, error):
    if value - error < 0 or value + error > 1:
        return True
    return False

def make_red(value):
    return "\color{red}{"+ str(value) + "}"
def make_green(value):
    return "\color{green}{"+ str(value) + "}"


    
channels = ["etau", "mutau", "tautau"]
categories = ["baseline", "resolved_1b","resolved_2b", "boosted_l", "boosted_m"]
# categories = ["baseline", "resolved_1b", "resolved_2b"]

data = []
data_stuff = []
data_unc = []
data_envelope = []
for cat in categories:
    for ch in channels:
        ###### 2018
        # txtname = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2018/cat_{}/24May_QCD1/qcd_inviso__{}__lep1_eta.txt".format(cat,ch)
        # ss_iso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2018/cat_{}/24May_QCD1/n_ss_iso__{}__lep1_eta.txt".format(cat,ch)
        # ss_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2018/cat_{}/24May_QCD1/n_ss_inviso__{}__lep1_eta.txt".format(cat,ch)
        # os_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2018/cat_{}/24May_QCD1/n_os_inviso__{}__lep1_eta.txt".format(cat,ch)
        # wps_value = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2018/cat_{}/24May_QCD1/CD_regions__{}__lep1_eta.txt".format(cat,ch)

        ###### 2017
        txtname = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2017/cat_{}/24May_QCD1/qcd_inviso__{}__lep1_eta.txt".format(cat,ch)
        ss_iso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2017/cat_{}/24May_QCD1/n_ss_iso__{}__lep1_eta.txt".format(cat,ch)
        ss_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2017/cat_{}/24May_QCD1/n_ss_inviso__{}__lep1_eta.txt".format(cat,ch)
        os_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2017/cat_{}/24May_QCD1/n_os_inviso__{}__lep1_eta.txt".format(cat,ch)

        ###### 2016
        # txtname = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016/cat_{}/13May_QCD1/qcd_inviso__{}__lep1_eta.txt".format(cat,ch)
        # ss_iso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016/cat_{}/13May_QCD1/n_ss_iso__{}__lep1_eta.txt".format(cat,ch)
        # ss_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016/cat_{}/13May_QCD1/n_ss_inviso__{}__lep1_eta.txt".format(cat,ch)
        # os_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016/cat_{}/13May_QCD1/n_os_inviso__{}__lep1_eta.txt".format(cat,ch)
        # wps_value = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016/cat_{}/13May_QCD1/CD_regions__{}__lep1_eta.txt".format(cat,ch)

        ###### 2016APV
        # txtname = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016APV/cat_{}/13May_QCD1/qcd_inviso__{}__lep1_eta.txt".format(cat,ch)
        # ss_iso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016APV/cat_{}/13May_QCD1/n_ss_iso__{}__lep1_eta.txt".format(cat,ch)
        # ss_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016APV/cat_{}/13May_QCD1/n_ss_inviso__{}__lep1_eta.txt".format(cat,ch)
        # os_inviso_name = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016APV/cat_{}/13May_QCD1/n_os_inviso__{}__lep1_eta.txt".format(cat,ch)
        # wps_value = "/eos/user/e/emartinv/cmt/FeaturePlotQCDTest/qcd_llr_2016APV/cat_{}/13May_QCD1/CD_regions__{}__lep1_eta.txt".format(cat,ch)


        fit_value, fit_err, mean_value, mean_err, std_value, std_err, std_star = read_stuff(txtname)

        fit_rel_err = (fit_err / fit_value)*100 if fit_value != 0 else ""
        if fit_rel_err != "":
            fit_rel_err = round(fit_rel_err, 2)
        mean_rel_err = (mean_err / mean_value)*100 if mean_value != 0 else ""
        if mean_rel_err != "":
            mean_rel_err = round(mean_rel_err, 2)
        std_rel_err = (std_err / std_value)*100 if std_value != 0 else ""
        if std_rel_err != "":
            std_rel_err = round(std_rel_err, 2)

        additional_syst = 0
        if mean_value == 0:
            mean_value = "-"
            mean_err = ""
        if fit_value == 0:
            fit_value = "-"
            fit_err = ""
        
        
        if mean_value != "-":
            if (std_value - std_err > mean_value or std_value + std_err < mean_value):
                if std_value != 0:
                    additional_syst = sqrt(((std_value - mean_value)/(std_value))**2
                    - ((std_err/std_value)**2))
                    additional_syst = round(additional_syst, 3)
                    # print(txtname, additional_syst)
        if additional_syst == 0:
            additional_syst = "-"
        # print(std_err, std_star)
        if std_value == 0:
            std_value = "0"
            std_err = ""

        
            
        
        
        # print(additional_syst)
        # print(mean_value)
        data_stuff.append([cat, ch, std_value, std_err, std_rel_err, mean_value, mean_err, mean_rel_err, fit_value, fit_err, fit_rel_err, additional_syst])
        ss_iso_value, ss_iso_error = read_results_2(ss_iso_name)
        # print(ss_iso_value, ss_iso_error)
        ss_inviso_value, ss_inviso_error = read_results(ss_inviso_name)
        # print(ss_inviso_value, ss_inviso_error)
        os_inviso_value, os_inviso_error = read_results(os_inviso_name)
        # print(os_inviso_value, os_inviso_error)
        ss_iso_value = round(ss_iso_value, 2)
        ss_iso_error = round(ss_iso_error, 2)
        ss_inviso_value = round(ss_inviso_value, 2)
        ss_inviso_error = round(ss_inviso_error, 2)
        os_inviso_value = round(os_inviso_value, 2)
        os_inviso_error = round(os_inviso_error, 2)
        # is_bad = any([is_compatible(ss_iso_value, ss_iso_error), is_compatible(ss_inviso_value, ss_inviso_error), is_compatible(os_inviso_value, os_inviso_error)])
        # value = any([ss_iso_value, ss_inviso_value, os_inviso_value])
        # error = any([ss_iso_error, ss_inviso_error, os_inviso_error])
        # # if value < 0 or value - error < 0:
        if std_value == 0 or ss_iso_value < 0 or ss_inviso_value < 0 or os_inviso_value < 0 or ss_iso_value - ss_iso_error < 0 or ss_inviso_value - ss_inviso_error < 0 or os_inviso_value - os_inviso_error < 0:
            BD_ratio = "-"
            BD_ratio_error = "-"
            lnN = "-"
        else:
            BD_ratio = ss_iso_value / ss_inviso_value
            BD_ratio = round(BD_ratio, 3)
            BD_ratio_error = sqrt((ss_iso_error / ss_iso_value) ** 2 + (ss_inviso_error / ss_inviso_value) ** 2)
            BD_ratio_error = round(BD_ratio_error, 3)
            # BD_ratio_error = BD_ratio * sqrt((ss_iso_error / ss_iso_value) ** 2 + (ss_inviso_error / ss_inviso_value) ** 2)
            if ss_inviso_value == 0 or ss_iso_value == 0:
                lnN = 1
            else:
                lnN = 1 + sqrt((ss_inviso_error / ss_inviso_value) ** 2 + (ss_iso_error / ss_iso_value) ** 2)
            lnN = round(lnN, 3)
        data_unc.append([cat, ch, BD_ratio, lnN])
        
        if ss_iso_value < 0 or ss_iso_value - ss_iso_error < 0:
            ss_iso_value = make_red(ss_iso_value)
            ss_iso_error = make_red(ss_iso_error)
        if ss_inviso_value < 0 or ss_inviso_value - ss_inviso_error < 0:
            ss_inviso_value = make_red(ss_inviso_value)
            ss_inviso_error = make_red(ss_inviso_error)
        if os_inviso_value < 0 or os_inviso_value - os_inviso_error < 0:
            os_inviso_value = make_red(os_inviso_value)
            os_inviso_error = make_red(os_inviso_error)
        
        

        data.append([cat, ch, ss_iso_value, ss_iso_error, os_inviso_value, os_inviso_error, ss_inviso_value, ss_inviso_error])

        qcd_wps = ["vvv_vl", "vvl_vl", "vl_l", "l_m"]

        # with open(wps_value, 'r') as file:
        #         lines = file.readlines()
        #         values = [float(line.split()[1]) for line in lines]
        #         errors = [float(line.split()[2]) for line in lines]
        #         max_wps_value = max(values)
        #         max_value_line = values.index(max_wps_value)
        #         max_wps_error = errors[max_value_line]
        #         min_wps_value = min(values)
        #         min_value_line = values.index(min_wps_value)
        #         min_wps_error = errors[min_value_line]

        # if std_value == "0":
        #     unc_plus = ""
        #     unc_minus = ""
        # else:
        #     # print("std", std_value)
        #     unc_plus = max_wps_value - std_value
        #     unc_plus = round(unc_plus, 3)
        #     rel_unc_plus = (unc_plus / std_value) * 100
        #     # print("unc_plus", unc_plus)
        #     unc_minus = std_value - min_wps_value
        #     unc_minus = round(unc_minus, 3)
        #     rel_unc_minus = (unc_minus / std_value) * 100
        #     rel_unc_plus = round(rel_unc_plus, 1)
        #     rel_unc_minus = round(rel_unc_minus, 1)
        # # print("max", max_wps_value, max_wps_error, "min", min_wps_value, min_wps_error)

        # data_envelope.append([cat, ch, std_value, std_err, max_wps_value, max_wps_error, min_wps_value, min_wps_error, unc_plus, unc_minus, rel_unc_plus, rel_unc_minus])


        # if additional_syst != "-" and std_value != 0 and lnN != "-":

        #     full_lnN = sqrt(lnN**2 + additional_syst**2)


create_QCDdiagnosis_table(data)
create_summary_test1(data_stuff)
create_QCD_uncertainty(data_unc)
# create_envelope_table(data_envelope)
# create_QCDdiagnosis_table(ss_iso_value, ss_iso_error, os_inviso_value, os_inviso_error, ss_inviso_value, ss_inviso_error)


# additional_syst = 0
# print(mean_value)
# if mean_value == "0":
#     mean_value = "-"
#     num_of_zeros = 0
# if fit_value == "0":
#     fit_value = "-"

# syst_to_print = "-"
# if mean_value != "-":
#     if (std_value - std_err > mean_value or std_value + std_err < mean_value):
#         if std_value != 0:
#             additional_syst = sqrt(((std_value - mean_value)/(std_value))**2
#             - ((std_err/std_value)**2))
#     print(additional_syst) #### check this

# # Calcular el error relativo
# def rel_error(value, error):
#     return error / value if value != 0 else 0


# # Calcular lnN
# lnN = 1 + sqrt(rel_error(ss_inviso_value, ss_inviso_error) ** 2 + rel_error(ss_iso_value, ss_iso_error) ** 2)
# # print("lnN", lnN)

# # if additional_syst != 0:
# #     lnN = sqrt(lnN**2 + additional_syst**2)
#     # print("lnN", lnN) ### check also this
# # Calcular B/D
# BD_ratio = ss_iso_value / ss_inviso_value
# # print("BD ratio", BD_ratio)

# # Calcular el error de B/D
# BD_ratio_error = BD_ratio * sqrt((ss_iso_error / ss_iso_value) ** 2 + (ss_inviso_error / ss_inviso_value) ** 2)


