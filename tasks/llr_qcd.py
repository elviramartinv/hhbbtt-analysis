# coding: utf-8

"""
QCD test tasks.
"""

# __all__ = []


import law
import luigi

from cmt.base_tasks.base import (
    ConfigTaskWithCategory, DatasetWrapperTask, ProcessGroupNameTask,
    )
from cmt.util import import_root, create_file_dir
from cmt.base_tasks.plotting import FeaturePlot, BasePlotTask


class FeaturePlotQCDTest(ConfigTaskWithCategory, DatasetWrapperTask, BasePlotTask):
    qcd_wps = law.CSVParameter(default=("vvvl_vvl", "vvl_vl", "vl_l", "l_m"),
        description="list of qcd working points to plot, default: vvvl_vvl, vvl_vl, vl_l, l_m")
    add_normal_wp = luigi.BoolParameter(default=True, description="whether to show the normal "
        "points used for qcd computation, default=True")
    normalize = luigi.BoolParameter(default=True, description="whether to plot also normalizing to "
        "normal wp, default=True")
    feature_names = law.CSVParameter(default=(), description="names of features to plot, uses all "
        "features when empty, default: ()")
    tree_name = luigi.Parameter(default="HTauTauTree", description="name of the tree to use, default: "
        "HTauTauTree")
    
    allow_composite_category = True

    def __init__(self, *args, **kwargs):
        super(FeaturePlotQCDTest, self).__init__(*args, **kwargs)
        self.channel = self.get_channel(self.region_name)
        # print("processes names", self.config.processes)
        # print("dataset", self.config.datasets[5].name)

    def requires(self):
        from copy import deepcopy
        wps = deepcopy(list(self.qcd_wps))
        if self.add_normal_wp:
            wps.append(law.NO_STR)
        return {
            qcd_wp: FeaturePlot.req(self, version=self.version + "__" + qcd_wp, do_qcd=True,
                stack=True, qcd_wp=qcd_wp, hide_data=False, save_yields=True, save_pdf=True,
                save_png=True, feature_names=self.feature_names)
            for qcd_wp in wps
        }

    def output(self):
        outputs = {}
        for feature in self.feature_names:
            postfix = "__{}__{}".format(self.channel, feature)
            outputs[(feature, "pdf")] = self.local_target(
                "qcd_inviso{}.pdf".format(postfix))
            outputs[(feature, "png")] = self.local_target(
                "qcd_inviso{}.png".format(postfix))
            outputs[(feature, "txt")] = self.local_target(
                "qcd_inviso{}.txt".format(postfix))
            outputs[(feature, "txt_b")] = self.local_target(
                "n_ss_iso{}.txt".format(postfix))
            outputs[(feature, "CD_txt")] = self.local_target(
                "CD_regions{}.txt".format(postfix))
            if self.add_normal_wp:
                outputs[(feature, "txt_c")] = self.local_target(
                    "n_os_inviso{}.txt".format(postfix))
                outputs[(feature, "txt_d")] = self.local_target(
                    "n_ss_inviso{}.txt".format(postfix))
            if self.normalize:
                outputs[(feature, "pdf_norm")] = self.local_target(
                    "qcd_inviso_norm{}.pdf".format(postfix))
                outputs[(feature, "png_norm")] = self.local_target(
                    "qcd_inviso_norm{}.png".format(postfix))
        return outputs

    def get_channel(self, region_name):
        channel = region_name.split("_")[0]
        if channel not in ["mutau", "etau", "tautau"]:
            channel = ""
        return channel

    def run(self):
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
        import json
        import os
        import scipy.optimize as opt
        import numpy as np
        import math
        from copy import deepcopy

        year = r"{}".format(self.config.year)
        category = r"{} category".format(self.category_name)
        channel = r"${}$".format(self.get_channel(self.region_name))
        channel = channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace(
            "e", "\\tau_e")
        upper_texts = [year, category, channel]

        inputs = self.input()

        def plot(x_axis, y_axis, y_errors, x_st, y_st, y_st_error, funcs, fit_params, text,
                x_title, y_title, upper_text, pdf_output_path, png_output_path):
            wps = list(x_axis) + [x_st]
            qcd_inviso = list(y_axis) + [y_st]
            qcd_inviso_errors = list(y_errors) + [y_st_error]
            ax = plt.subplot()

            x_to_plot = []
            bad_x = []
            y_to_plot = []
            y_errors_to_plot = []
            for i, wp in enumerate(wps):
                if qcd_inviso[i] == 0 and qcd_inviso_errors[i] == 0:
                    bad_x.append(i)
                else:
                    x_to_plot.append(i)
                    y_to_plot.append(qcd_inviso[i])
                    y_errors_to_plot.append(qcd_inviso_errors[i])

            plt.errorbar(x_to_plot, y_to_plot, y_errors_to_plot, marker="o", linestyle="")
            ax.set_xticks([x for x in range(len(wps))])
            ax.set_xticklabels(wps)

            min_values = [value - error for value, error in zip(qcd_inviso, qcd_inviso_errors)]
            max_values = [value + error for value, error in zip(qcd_inviso, qcd_inviso_errors)]
            
            for func, fit in zip(funcs, fit_params):
                min_values += [func(x, *fit) for x in range(len(x_axis))]
                max_values += [func(x, *fit) for x in range(len(x_axis))]

            min_value = min(min_values)
            max_value = max(max_values)
            size = max(max_values) - min(min_values)
            if min_value == 0 and max_value == 0:
                max_value = 1
            else:
                min_value -= 0.1 * size
                max_value += 0.1 * size
            ax.set_ylim(min_value, max_value)

            fit_colors = ["r", "g"]
            if len(fit_params) > len(fit_colors):
                raise ValueError("You have setted only {} colors, add some more".format(
                    len(fit_colors)))
            if fit_params:
                for func, fit, color in zip(funcs, fit_params, fit_colors):
                    ok = False
                    for p in fit:
                        if p != 0:
                            ok = True
                    if ok:
                        plt.plot(x_axis, [func(x, *fit) for x in range(len(x_axis))], color=color)

            if x_st:
                x_line = [len(x_axis) - 0.5 for x in [0, 1]]
                y_line = [min_value, max_value]
                plt.plot(x_line, y_line, '--r', color='k')
                ax.set_ylim(min_value, max_value)

            if bad_x:
                for x in bad_x:
                    x_fill = [x + (- 1 + 2 * i) * 0.25 for i in [0, 1]]
                    min_y_fill = [min_value, min_value]
                    max_y_fill = [max_value, max_value]
                    plt.fill_between(x_fill, min_y_fill, max_y_fill, facecolor="none",
                        hatch="//", edgecolor="k")

            if upper_text:
                plt.text(0, 1.01, upper_text, transform=ax.transAxes)

            if text:
                x_text = 0.6
                y_text = 1.01
                for t in text:
                    plt.text(x_text, y_text, t, transform=ax.transAxes)
                    y_text -= 0.05

            if y_title:
                plt.ylabel(y_title)

            create_file_dir(pdf_output_path)
            print("Saving figure in", pdf_output_path)
            plt.savefig(pdf_output_path)
            print("Saving figure in", png_output_path)
            plt.savefig(png_output_path)
            plt.close("all")

        for feature in self.feature_names:
            texts = deepcopy(upper_texts)
            upper_text = ", ".join(texts)

            qcd_inviso = []
            qcd_inviso_errors = []
            n_ss_iso = []
            n_ss_iso_errors = []
            valids = []
            for qcd_wp in self.qcd_wps:
                filename = inputs[qcd_wp]["yields"].targets[feature].path
                # print("inputs", inputs)
                # print("filename", filename)
                d = json.load(open(os.path.expandvars(filename), "r"))
                print("d", d)
                qcd_inviso.append(d["qcd_inviso"])
                qcd_inviso_errors.append(d["qcd_inviso_error"])
                n_ss_iso.append(d["n_ss_iso"]) ######TODO: check if this is the right name
                n_ss_iso_errors.append(d["n_ss_iso_error"])
                if qcd_inviso[-1] == 0 and qcd_inviso_errors[-1] == 0:
                    valids.append(False)
                else:
                    valids.append(True)

            def linear(x, a, b):
                return a * x + b

            def constant(x, a):
                return a

            print("Values to fit:", qcd_inviso)
            print("Statistical errors:", qcd_inviso_errors)

            

            if len([a for a in valids if a]) >= 2:
                opt_param_linear, pcov_linear = opt.curve_fit(linear,
                    [x for x in range(len(self.qcd_wps)) if valids[x]],
                    [qcd_inviso[iy] for iy in range(len(qcd_inviso)) if valids[iy]],
                    sigma=[qcd_inviso_errors[ie] for ie in range(len(qcd_inviso_errors))
                    if valids[ie]])
                opt_param_const, pcov_const = opt.curve_fit(constant,
                    [x for x in range(len(self.qcd_wps)) if valids[x]],
                    [qcd_inviso[iy] for iy in range(len(qcd_inviso)) if valids[iy]],
                    sigma=[qcd_inviso_errors[ie] for ie in range(len(qcd_inviso_errors))
                    if valids[ie]])
                # pcov_linear_sigmas = np.sqrt(np.diag(pcov_linear))
                pcov_const_sigmas = np.sqrt(np.diag(pcov_const))
                fitting = True
            else:  # not enough points to perform a fit
                # opt_param_linear, pcov_linear = None, None
                opt_param_const, pcov_const = None, None
                # pcov_linear_sigmas, pcov_const_sigmas = None, None
                fitting = False

            # if not fitting:
            #     linear_a = 0
            #     linear_error_a = 0
            #     linear_b = 0
            #     linear_error_b = 0
            # else:
            #    linear_a = opt_param_linear[0]
            #    linear_error_a = pcov_linear_sigmas[0]
            #    linear_b = opt_param_linear[1]
            #    linear_error_b = pcov_linear_sigmas[1]
            if not fitting:
                const_a = 0
                const_error_a = 0
            else:
                const_a = opt_param_const[0]
                const_error_a = pcov_const_sigmas[0]

            if self.add_normal_wp:
                wp_st = "standard"
                filename = inputs[law.NO_STR]["yields"].targets[feature].path
                d = json.load(open(os.path.expandvars(filename), "r"))
                y_st = d["qcd_inviso"]
                y_st_error = d["qcd_inviso_error"]
                n_ss_iso.append(d["n_ss_iso"])
                n_ss_iso_errors.append(d["n_ss_iso_error"])
                n_ss_inviso = d["n_ss_inviso"]
                n_ss_inviso_error = d["n_ss_inviso_error"]
                n_os_inviso = d["n_os_inviso"]
                n_os_inviso_error = d["n_os_inviso_error"]
            else:
                wp_st = ""
                y_st = ""
                y_st_error = ""
            
            print("y_st", y_st)
            print("qcd inviso", qcd_inviso)


            outputs = self.output()
            
            create_file_dir(outputs[(feature, "CD_txt")].path)

            with open(outputs[(feature, "CD_txt")].path, "w") as f:
                for wp, value, error in zip(self.qcd_wps, qcd_inviso, qcd_inviso_errors):
                    f.write("{} {:.3f} {:.3f}\n".format(wp, value, error))

            print("output cd txt", outputs[(feature, "CD_txt")].path)
            print("qcd inviso", qcd_inviso)



            if self.normalize and not self.add_normal_wp:
                raise ValueError("Can't normalize values without considering the "
                    "'normal' working points!")
            elif self.normalize and y_st != 0:
                y_title = "C/D (normalized to vvl_m)"
                plot(self.qcd_wps, [value / y_st for value in qcd_inviso],
                    [value / y_st for value in qcd_inviso_errors], wp_st, 1., y_st_error / y_st,
                    [], [], [], "", y_title, upper_text,
                    pdf_output_path=outputs[(feature, "pdf_norm")].path,
                    png_output_path=outputs[(feature, "png_norm")].path)
            elif self.normalize:
                y_title = "C/D"
                plot(self.qcd_wps, [value for value in qcd_inviso],
                    [value for value in qcd_inviso_errors], wp_st, y_st, y_st_error,
                    [], [], [], "", y_title, upper_text,
                    pdf_output_path=outputs[(feature, "pdf_norm")].path,
                    png_output_path=outputs[(feature, "png_norm")].path)
                
            

            y_title = "C/D"
            text = []
            # if fitting:
            # text.append(r'Linear fit: ({:.2f}$\pm${:.2f})x+({:.2f}$\pm${:.2f})'.format(
            #     linear_a, linear_error_a, linear_b, linear_error_b))
            if fitting:
                text.append(r'Constant fit: ({:.2f}$\pm${:.2f})'.format(
                    const_a, const_error_a))
            plot(self.qcd_wps, qcd_inviso, qcd_inviso_errors, wp_st, y_st, y_st_error,
                [constant], [[const_a]], text, "", y_title,
                # [linear, constant], [[linear_a, linear_b], [const_a]], text, "", y_title,
                upper_text, pdf_output_path=outputs[(feature, "pdf")].path,
                png_output_path=outputs[(feature, "png")].path)

            # computing mean
            total_value = 0
            total_value_error = 0
            for i in range(len(qcd_inviso)):
                if not valids[i]:
                    continue
                val, error = qcd_inviso[i], qcd_inviso_errors[i]
                total_value += val / error
            total_inv_error = sum([1 / error for i, error in enumerate(qcd_inviso_errors)
                if valids[i]])
            total_value /= total_inv_error if total_inv_error != 0 else 1
            total_value_error = math.sqrt(len([a for a in valids if a])
                * (1 / total_inv_error) * (1 / total_inv_error)) if total_inv_error != 0 else 0

            print ("******************************")
            print ("{}, {}".format(self.category_name, self.get_channel(self.region_name)))
            print ("Constant Fit: {:.3f} +- {:.3f}".format(
                const_a, const_error_a))
            print ("Mean:         {:.3f} +- {:.3f}".format(total_value, total_value_error))
            print ("Standard:     {:.3f} +- {:.3f}".format(y_st, y_st_error))
            print ("******************************")

            postfix = "*" * len([a for a in valids if not a])
            create_file_dir(outputs[(feature, "txt")].path)
            with open(os.path.expandvars(outputs[(feature, "txt")].path), "w") as f:
                f.write("Fit {:.3f} {:.3f}\n".format(const_a, const_error_a))
                f.write("Mean {:.3f} {:.3f}\n".format(total_value, total_value_error))
                f.write("Standard {:.3f} {:.3f}{}\n".format(y_st, y_st_error, postfix))               

            with open(os.path.expandvars(outputs[(feature, "txt_b")].path), "w") as f:
                for wp, n, error in zip(list(self.qcd_wps) + ["vvl_m"], n_ss_iso, n_ss_iso_errors):
                    f.write("{} {:.3f} {:.3f}\n".format(wp, n, error))
                    f.write("{} {:.3f}\n".format(wp, error))

            if self.add_normal_wp:
                with open(os.path.expandvars(outputs[(feature, "txt_d")].path), "w") as f:
                    f.write("{:.3f} {:.3f}\n".format(n_ss_inviso, n_ss_inviso_error))
                with open(os.path.expandvars(outputs[(feature, "txt_c")].path), "w") as f:
                    f.write("{:.3f} {:.3f}\n".format(n_os_inviso, n_os_inviso_error))


class QCDTest2(ConfigTaskWithCategory, ProcessGroupNameTask, BasePlotTask):
    allow_composite_category = True

    tree_name = luigi.Parameter(default="HTauTauTree", description="name of the tree to use, default: "
        "HTauTauTree")

    def __init__(self, *args, **kwargs):
        super(QCDTest2, self).__init__(*args, **kwargs)
        self.channel = self.get_channel(self.region_name)

    def requires(self):
        reqs = {}
        reqs["qcd"] = FeaturePlot.vreq(self, do_qcd=True, stack=True,
            hide_data=False, save_root=True, save_pdf=True, save_png=True,
            plot_systematics=True, process_group_name="plots")
        reqs["no_qcd"] = FeaturePlot.vreq(self, do_qcd=False, stack=True,
            hide_data=False, save_root=True, save_pdf=True, save_png=True,
            plot_systematics=True, process_group_name="plots")
        return reqs

    def output(self):
        outputs = {}
        postfix = "{}__{}".format(self.channel, self.requires()["qcd"].features[0].name)
        # postfix = (self.requires()["qcd"].features[0].name, self.get_channel(self.region_name))
        print("postfix", postfix)
        outputs["plot"] = self.local_target("qcd_comparison_{}.pdf".format(postfix))
        outputs["plot_png"] = self.local_target("qcd_comparison_{}.png".format(postfix))
        outputs["plot_norm"] = self.local_target("qcd_comparison_norm_{}.pdf".format(postfix))
        outputs["plot_norm_png"] = self.local_target("qcd_comparison_norm_{}.png".format(postfix))
        return outputs
    
    def get_channel(self, region_name):
        channel = region_name.split("_")[0]
        if channel not in ["mutau", "etau", "tautau"]:
            channel = ""
        return channel

    def run(self):
        ROOT = import_root()
        inputs = self.input()
        outputs = self.output()
        filename = inputs["qcd"]["root"].targets[self.requires()["qcd"].features[0].name]
        filename_noqcd = inputs["no_qcd"]["root"].targets[self.requires()["qcd"].features[0].name]
        # print("inputs", inputs)
        # print("filename", filename)
        # print("filname no qcd", filename_noqcd)
        # print("self requires", self.requires())
        # print("target", self.requires().features[0].name)
        # print("all features", self.requires().features)

        qcd_file = ROOT.TFile(filename.path)
        bck_file = ROOT.TFile(filename_noqcd.path)
        print("qcd file", qcd_file)
        print("bck file", bck_file)
        qcd_histo = qcd_file.Get("histograms/qcd").Clone() 
        new_qcd_histo = bck_file.Get("histograms/data").Clone() 
        bck_histo = bck_file.Get("histograms/background").Clone()
        # print("data copy", [new_qcd_histo.GetBinContent(i) for i in range(1, new_qcd_histo.GetNbinsX() + 1)])
        new_qcd_histo.Add(bck_histo, -1)
       

        c = ROOT.TCanvas("c", "c", 800, 800)
        c.SetLeftMargin(0.11)
        c.SetGrid()

        # plot style
        qcd_histo.SetLineColor(ROOT.kRed)
        qcd_histo.SetMarkerColor(ROOT.kRed)
        new_qcd_histo.SetLineColor(ROOT.kBlue)
        new_qcd_histo.SetMarkerColor(ROOT.kBlue)

        feature = self.requires()["qcd"].features[0]
        # print(feature, dir(feature))
        # y_title = feature.get_full_y_title(root=True, bin_width=None)
        # x_title = feature.get_full_x_title(root=True)
        y_title = qcd_histo.GetYaxis().GetTitle()
        x_title = (str(feature.get_aux("x_title"))
            + (" [%s]" % feature.get_aux("units") if feature.get_aux("units") else ""))
        qcd_histo.GetXaxis().SetTitle(x_title)
        qcd_histo.GetYaxis().SetTitle(y_title)
        qcd_histo.SetTitle("")

        max_y = max([qcd_histo.GetMaximum(), new_qcd_histo.GetMaximum()])
        qcd_histo.SetMinimum(0)
        qcd_histo.SetMaximum(1.3 * max_y)

        # legend
        leg = ROOT.TLegend(0.6, 0.8, 0.9, 0.9)
        leg.AddEntry(qcd_histo, "ABCD method", "l")
        leg.AddEntry(new_qcd_histo, "Data - Bkg", "l")

        # drawing
        qcd_histo.Draw("l")
        print("ABCD", [qcd_histo.GetBinContent(i) for i in range(1, qcd_histo.GetNbinsX() + 1)])
        new_qcd_histo.Draw("l, same")
        print("Data - Bkg", [new_qcd_histo.GetBinContent(i) for i in range(1, new_qcd_histo.GetNbinsX() + 1)])
        leg.Draw("same")
        create_file_dir(outputs["plot"].path)
        c.SaveAs(outputs["plot"].path)
        c.SaveAs(outputs["plot_png"].path)

        # plotting the ratio between ABCD and data - mc
        leg = ROOT.TLegend(0.6, 0.8, 0.9, 0.9)
        qcd_histo.Divide(new_qcd_histo)
        leg.AddEntry(qcd_histo, "ABCD / Data - Bkg", "l")
        print("ABCD / Data - Bkg", [qcd_histo.GetBinContent(i) for i in range(1, qcd_histo.GetNbinsX() + 1)])
        qcd_histo.SetMinimum(-5.0) 
        qcd_histo.SetMaximum(5.0) 
        qcd_histo.Draw("l")
        leg.Draw("same")
        create_file_dir(outputs["plot_norm"].path)
        c.SaveAs(outputs["plot_norm"].path)
        c.SaveAs(outputs["plot_norm_png"].path)


class QCDTest3(ConfigTaskWithCategory, DatasetWrapperTask, BasePlotTask):
    feature_names = law.CSVParameter(default=(), description="names of features to plot, uses all "
        "features when empty, default: ()")
    feature_tags = law.CSVParameter(default=(), description="tags of features to plot, uses all "
        "features when empty, default: ()")
    tree_name = luigi.Parameter(default="HTauTauTree", description="name of the tree to use, default: "
        "HTauTauTree")

    allow_composite_category = True

    def __init__(self, *args, **kwargs):
        super(QCDTest3, self).__init__(*args, **kwargs)
        self.channel = self.get_channel(self.region_name)
        self.use_dnns = False

    def requires(self):
        reqs = {}
        reqs["os_inviso"] = FeaturePlot.vreq(self, version= "B_29Apr", do_qcd=True, stack=True,
            hide_data=True, save_root=True, save_pdf=True, save_png=True, plot_systematics=True,
            process_group_name="plots", 
            feature_names=self.feature_names,
            feature_tags=self.feature_tags, blinded=True)
        reqs["ss_iso"] = FeaturePlot.vreq(self, version = "C_29Apr", do_qcd=True, stack=True,
            hide_data=True, save_root=True, save_pdf=True, save_png=True, plot_systematics=True,
            process_group_name="plots", 
            shape_region="ss_iso",
            feature_names=self.feature_names, feature_tags=self.feature_tags, blinded=True)
        reqs["mean"] = FeaturePlot.vreq(self, version = "mean_29Apr", do_qcd=True, stack=True, save_png=True, hide_data=True,
            save_root=True, save_pdf=True, plot_systematics=True,
            process_group_name="plots", 
            qcd_sym_shape=True, blinded=True,
            feature_names=self.feature_names, feature_tags=self.feature_tags)
        return reqs

    def output(self):
        outputs = {}
        for feature in [feature.name for feature in self.requires()["os_inviso"].features]:
            postfix = "__{}__{}".format(self.channel, feature)
            outputs[(feature, "plot")] = self.local_target(
                "qcd_comparison_{}.pdf".format(postfix))
            outputs[(feature, "plot_png")] = self.local_target(
                "qcd_comparison_{}.png".format(postfix))
            outputs[(feature, "plot_norm")] = self.local_target(
                "qcd_comparison_norm_{}.pdf".format(postfix))
            outputs[(feature, "plot_norm_png")] = self.local_target(
                "qcd_comparison_norm_{}.png".format(postfix))
        return outputs

    def get_channel(self, region_name):
        channel = region_name.split("_")[0]
        if channel not in ["mutau", "etau", "tautau"]:
            channel = ""
        return channel

    def run(self):
        ROOT = import_root()
        inputs = self.input()
        outputs = self.output()
        print("Inputs", self.input())
        print("output", self.output())

        for feature_name in self.feature_names:
            filename_os_inviso = inputs["os_inviso"]["root"].targets[feature_name].path
            filename_ss_iso = inputs["ss_iso"]["root"].targets[feature_name].path
            # filename_os_inviso = "/eos/user/e/emartinv/cmt/FeaturePlot/qcd_llr_2018/cat_resolved_1b/24Apr/root/lep1_eta__etau_os_inviso__pg_plots.root"
            # filename_ss_iso = "/eos/user/e/emartinv/cmt/FeaturePlot/qcd_llr_2018/cat_resolved_1b/24Apr/root/lep1_eta__etau_ss_iso__pg_plots.root"
            print("inputs", inputs["os_inviso"]["root"])
            print("inputs target", inputs["os_inviso"]["root"].targets)
            print("inputs target feature", inputs["os_inviso"]["root"].targets[feature_name])
            print("inputs target feature path", inputs["os_inviso"]["root"].targets[feature_name].path)
            print("os inviso", filename_os_inviso)
            print("ss iso", filename_ss_iso)

            qcd_os_inviso_file = ROOT.TFile(filename_os_inviso)
            qcd_os_inviso = qcd_os_inviso_file.Get("histograms/qcd").Clone()
            print("os inviso content", [qcd_os_inviso.GetBinContent(i) for i in range(1, qcd_os_inviso.GetNbinsX() + 1)])

            qcd_ss_iso_file = ROOT.TFile(filename_ss_iso)
            qcd_ss_iso = qcd_ss_iso_file.Get("histograms/qcd").Clone()
            print("ss iso content", [qcd_ss_iso.GetBinContent(i) for i in range(1, qcd_ss_iso.GetNbinsX() + 1)])

            c = ROOT.TCanvas("c", "c", 800, 800)
            c.SetGrid()

            # plot style
            qcd_os_inviso.SetLineColor(ROOT.kRed)
            qcd_os_inviso.SetMarkerColor(ROOT.kRed)
            qcd_ss_iso.SetLineColor(ROOT.kBlue)
            qcd_ss_iso.SetMarkerColor(ROOT.kBlue)

            feature = self.config.features.get(feature_name)
            # y_title = feature.get_full_y_title(root=True, bin_width=None)
            # x_title = feature.get_full_x_title(root=True)
            # y_title = "OS inv. iso / SS iso"
            y_title = "" 
            x_title = (str(feature.get_aux("x_title"))
                + (" [%s]" % feature.get_aux("units") if feature.get_aux("units") else ""))
            qcd_os_inviso.GetXaxis().SetTitle(x_title)
            qcd_os_inviso.GetYaxis().SetTitle(y_title)
            qcd_os_inviso.SetTitle("")

            max_y = max([qcd_os_inviso.GetMaximum(), qcd_ss_iso.GetMaximum()])
            qcd_os_inviso.SetMinimum(0)
            qcd_os_inviso.SetMaximum(1.3 * max_y)

            # legend
            leg = ROOT.TLegend(0.6, 0.8, 0.9, 0.9)
            leg.AddEntry(qcd_os_inviso, "Region B (OS inv. iso.)", "l")
            leg.AddEntry(qcd_ss_iso, "Region C (SS iso.)", "l")

            # drawing
            qcd_os_inviso.Draw("l")
            qcd_ss_iso.Draw("l, same")
            leg.Draw("same")
            create_file_dir(outputs[(feature_name, "plot")].path)
            c.SaveAs(outputs[(feature_name, "plot")].path)
            c.SaveAs(outputs[(feature_name, "plot_png")].path)

            # plotting the ratio between ABCD and data - mc
            leg = ROOT.TLegend(0.5, 0.8, 0.9, 0.9)
            qcd_os_inviso.Divide(qcd_ss_iso)
            leg.AddEntry(qcd_os_inviso, "Region B / Region C", "l")
            qcd_os_inviso.SetMinimum(0.5)
            qcd_os_inviso.SetMaximum(1.5)
            qcd_os_inviso.Draw("l")
            leg.Draw("same")
            create_file_dir(outputs[(feature_name, "plot_norm")].path)
            c.SaveAs(outputs[(feature_name, "plot_norm")].path)
            c.SaveAs(outputs[(feature_name, "plot_norm_png")].path)
            del c


class QCDTest4(ConfigTaskWithCategory, DatasetWrapperTask, BasePlotTask):
    feature_names = law.CSVParameter(default=(), description="names of features to plot, uses all "
        "features when empty, default: ()")
    process_group_name = "plots"
    tree_name = luigi.Parameter(default="HTauTauTree", description="name of the tree to use, default: "
        "HTauTauTree")

    allow_composite_category = True

    def __init__(self, *args, **kwargs):
        super(QCDTest4, self).__init__(*args, **kwargs)
        self.channel = self.get_channel(self.region_name)
        self.use_dnns = False

    def requires(self):
        reqs = {}
        for region_name in ["ss_iso", "os_inviso", "ss_inviso"]:
            reqs[region_name] = FeaturePlot.vreq(self, do_qcd=False, stack=True, hide_data=False, 
                save_root=True, save_pdf=True, save_png=True, plot_systematics=True,
                feature_names=self.feature_names, process_group_name=self.process_group_name,
                region_name=self.channel + "_" + region_name)
        return reqs

    def output(self):
        outputs = {}
        for feature in self.feature_names:
            for region_pair in [("ss_iso", "os_inviso"), ("ss_iso", "ss_inviso")]:
                postfix = "__{}__{}__{}__{}".format(self.channel, feature,
                    region_pair[0], region_pair[1])
                outputs[(feature, region_pair, "plot")] = self.local_target(
                    "qcd_comparison_{}.pdf".format(postfix))
                outputs[(feature, region_pair, "plot_norm")] = self.local_target(
                    "qcd_comparison_norm_{}.pdf".format(postfix))
        return outputs

    def get_channel(self, region_name):
        channel = region_name.split("_")[0]
        if channel not in ["mutau", "etau", "tautau"]:
            channel = ""
        return channel

    def run(self):
        from cmt.util import create_file_dir
        from plotlib.util import create_random_name
        ROOT = import_root()
        inputs = self.input()
        outputs = self.output()

        
        # signal_names = []
        # data_names = []
        # background_names = []
        # for process in self.datasets:
        #     print(self.datasets)
        #     print(process)
        #     if process.process.isSignal:
        #         signal_names.append(process.name)
        #     elif process.process.isData:
        #         data_names.append(process.name)
        #     else:
        #         background_names.append(process.name)

        # print("signal names", signal_names)
        # print("data names", data_names)
        # print("background names", background_names)

        def get_qcd(files, region, bin_limit=0.):
            # d_hist = files[region].Get("histograms/data")
            d_hist = files[region].Get("histograms/data")
            if not d_hist:
                raise Exception("data histogram not found for region '{}' in tfile {}".format(
                    region, files[region]))

            b_hist = files[region].Get("histograms/background")
            if not b_hist:
                raise Exception("background histogram not found in region '{}' in tfile {}".format(
                    region, files[region]))

            qcd_hist = d_hist.Clone(create_random_name("qcd_" + region))
            qcd_hist.Add(b_hist, -1.)
            # removing negative bins
            for ibin in range(1, qcd_hist.GetNbinsX() + 1):
                if qcd_hist.GetBinContent(ibin) < bin_limit:
                    qcd_hist.SetBinContent(ibin, 1.e-6)

            return qcd_hist
 
        files = {}
        histos = {}
        for feature_name in self.feature_names:
            for region_name in ["ss_iso", "os_inviso", "ss_inviso"]:
                files[region_name] = ROOT.TFile.Open(
                    inputs[region_name]["root"].targets[feature_name].path)
                print("inputs", inputs["ss_iso"]["root"].targets[feature_name].path)
                print("files", files)
                print("region_name", region_name)
                histos[region_name] = get_qcd(files, region_name).Clone()
                histos[region_name].Scale(1. / histos[region_name].Integral())
                print("histos", histos)

            for region_pair in [("ss_iso", "os_inviso"), ("ss_iso", "ss_inviso")]:
                c = ROOT.TCanvas("c", "c", 800, 800)
                c.SetGrid()

                histos[region_pair[0]].SetLineColor(ROOT.kRed)
                histos[region_pair[0]].SetMarkerColor(ROOT.kRed)
                histos[region_pair[1]].SetLineColor(ROOT.kBlue)
                histos[region_pair[1]].SetMarkerColor(ROOT.kBlue)

                feature = self.config.features.get(feature_name)
                # y_title = feature.get_full_y_title(root=True, bin_width=None)
                # x_title = feature.get_full_x_title(root=True)
                y_title = "Events" 
                x_title = (str(feature.get_aux("x_title"))
                    + (" [%s]" % feature.get_aux("units") if feature.get_aux("units") else ""))
                histos[region_pair[0]].GetXaxis().SetTitle(x_title)
                histos[region_pair[0]].GetYaxis().SetTitle(y_title)
                histos[region_pair[0]].SetTitle("")

                # max_y = max([histos[region_pair[0]].GetMaximum(),
                #     histos[region_pair[1]].GetMaximum()])
                histos[region_pair[0]].SetMinimum(0.01)
                histos[region_pair[0]].SetMaximum(1)

                # legend
                leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
                leg.AddEntry(histos[region_pair[0]], region_pair[0], "l")
                leg.AddEntry(histos[region_pair[1]], region_pair[1], "l")

                # drawing
                histos[region_pair[0]].Draw("l")
                histos[region_pair[1]].Draw("l, same")
                leg.Draw("same")
                create_file_dir(outputs[(feature_name, region_pair, "plot")].path)
                c.SetLogy()
                c.SaveAs(outputs[(feature_name, region_pair, "plot")].path)

                # plotting the ratio between ABCD and data - mc
                leg = ROOT.TLegend(0.7, 0.8, 0.9, 0.9)
                ratio_plot = histos[region_pair[0]].Clone()
                ratio_plot.Divide(histos[region_pair[1]])
                leg.AddEntry(ratio_plot, "{}/{}".format(region_pair[0], region_pair[1]), "l")
                ratio_plot.SetMinimum(0.5)
                ratio_plot.SetMaximum(1.5)
                ratio_plot.Draw("l")
                leg.Draw("same")
                create_file_dir(outputs[(feature_name, region_pair, "plot_norm")].path)
                c.SetLogy(0)
                c.SaveAs(outputs[(feature_name, region_pair, "plot_norm")].path)
                del c


class QCDTest5(ConfigTaskWithCategory, DatasetWrapperTask, BasePlotTask):
    qcd_wps = law.CSVParameter(default=("vl_l", "l_m", "m_h", "h_vh"),
        description="list of qcd working points to plot, default: (vl_l, l_m, m_h, h_vh)")
    add_normal_wp = luigi.BoolParameter(default=True, description="whether to show the normal "
        "points used for qcd computation, default=True")
    normalize = luigi.BoolParameter(default=True, description="whether to plot also normalizing to "
        "normal mass, default=True")
    feature_names = law.CSVParameter(default=(), description="names of features to plot, uses all "
        "features when empty, default: ()")
    tree_name = luigi.Parameter(default="HTauTauTree", description="name of the tree to use, default: "
        "HTauTauTree")
    
    allow_composite_category = True

    def __init__(self, *args, **kwargs):
        super(FeaturePlotQCDTest, self).__init__(*args, **kwargs)
        self.channel = self.get_channel(self.region_name)
        # print("processes names", self.config.processes)
        # print("dataset", self.config.datasets[5].name)

    def requires(self):
        from copy import deepcopy
        wps = deepcopy(list(self.qcd_wps))
        if self.add_normal_wp:
            wps.append(law.NO_STR)
        return {
            qcd_wp: FeaturePlot.req(self, version=self.version + "__" + qcd_wp, do_qcd=True,
                stack=True, qcd_wp=qcd_wp, hide_data=False, save_yields=True, save_pdf=True,
                save_png=True, feature_names=self.feature_names)
            for qcd_wp in wps
        }

    def output(self):
        outputs = {}
        for feature in self.feature_names:
            postfix = "__{}__{}".format(self.channel, feature)
            outputs[(feature, "pdf")] = self.local_target(
                "qcd_inviso{}.pdf".format(postfix))
            outputs[(feature, "png")] = self.local_target(
                "qcd_inviso{}.png".format(postfix))
            outputs[(feature, "txt")] = self.local_target(
                "qcd_inviso{}.txt".format(postfix))
            outputs[(feature, "txt_b")] = self.local_target(
                "n_ss_iso{}.txt".format(postfix))
            outputs[(feature, "CD_txt")] = self.local_target(
                "CD_regions{}.txt".format(postfix))
            if self.add_normal_wp:
                outputs[(feature, "txt_c")] = self.local_target(
                    "n_os_inviso{}.txt".format(postfix))
                outputs[(feature, "txt_d")] = self.local_target(
                    "n_ss_inviso{}.txt".format(postfix))
            if self.normalize:
                outputs[(feature, "pdf_norm")] = self.local_target(
                    "qcd_inviso_norm{}.pdf".format(postfix))
                outputs[(feature, "png_norm")] = self.local_target(
                    "qcd_inviso_norm{}.png".format(postfix))
        return outputs

    def get_channel(self, region_name):
        channel = region_name.split("_")[0]
        if channel not in ["mutau", "etau", "tautau"]:
            channel = ""
        return channel

    def run(self):
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
        import json
        import os
        import scipy.optimize as opt
        import numpy as np
        import math
        from copy import deepcopy

        year = r"{}".format(self.config.year)
        category = r"{} category".format(self.category_name)
        channel = r"${}$".format(self.get_channel(self.region_name))
        channel = channel.replace("tau", "\\tau_h").replace("mu", "\\tau_\\mu").replace(
            "e", "\\tau_e")
        upper_texts = [year, category, channel]

        inputs = self.input()

        def plot(x_axis, y_axis, y_errors, x_st, y_st, y_st_error, funcs, fit_params, text,
                x_title, y_title, upper_text, pdf_output_path, png_output_path):
            wps = list(x_axis) + [x_st]
            qcd_inviso = list(y_axis) + [y_st]
            qcd_inviso_errors = list(y_errors) + [y_st_error]
            ax = plt.subplot()

            x_to_plot = []
            bad_x = []
            y_to_plot = []
            y_errors_to_plot = []
            for i, wp in enumerate(wps):
                if qcd_inviso[i] == 0 and qcd_inviso_errors[i] == 0:
                    bad_x.append(i)
                else:
                    x_to_plot.append(i)
                    y_to_plot.append(qcd_inviso[i])
                    y_errors_to_plot.append(qcd_inviso_errors[i])

            plt.errorbar(x_to_plot, y_to_plot, y_errors_to_plot, marker="o", linestyle="")
            ax.set_xticks([x for x in range(len(wps))])
            ax.set_xticklabels(wps)

            min_values = [value - error for value, error in zip(qcd_inviso, qcd_inviso_errors)]
            max_values = [value + error for value, error in zip(qcd_inviso, qcd_inviso_errors)]
            
            for func, fit in zip(funcs, fit_params):
                min_values += [func(x, *fit) for x in range(len(x_axis))]
                max_values += [func(x, *fit) for x in range(len(x_axis))]

            min_value = min(min_values)
            max_value = max(max_values)
            size = max(max_values) - min(min_values)
            if min_value == 0 and max_value == 0:
                max_value = 1
            else:
                min_value -= 0.1 * size
                max_value += 0.1 * size
            ax.set_ylim(min_value, max_value)

            fit_colors = ["r", "g"]
            if len(fit_params) > len(fit_colors):
                raise ValueError("You have setted only {} colors, add some more".format(
                    len(fit_colors)))
            if fit_params:
                for func, fit, color in zip(funcs, fit_params, fit_colors):
                    ok = False
                    for p in fit:
                        if p != 0:
                            ok = True
                    if ok:
                        plt.plot(x_axis, [func(x, *fit) for x in range(len(x_axis))], color=color)

            if x_st:
                x_line = [len(x_axis) - 0.5 for x in [0, 1]]
                y_line = [min_value, max_value]
                plt.plot(x_line, y_line, '--r', color='k')
                ax.set_ylim(min_value, max_value)

            if bad_x:
                for x in bad_x:
                    x_fill = [x + (- 1 + 2 * i) * 0.25 for i in [0, 1]]
                    min_y_fill = [min_value, min_value]
                    max_y_fill = [max_value, max_value]
                    plt.fill_between(x_fill, min_y_fill, max_y_fill, facecolor="none",
                        hatch="//", edgecolor="k")

            if upper_text:
                plt.text(0, 1.01, upper_text, transform=ax.transAxes)

            if text:
                x_text = 0.6
                y_text = 1.01
                for t in text:
                    plt.text(x_text, y_text, t, transform=ax.transAxes)
                    y_text -= 0.05

            if y_title:
                plt.ylabel(y_title)

            create_file_dir(pdf_output_path)
            print("Saving figure in", pdf_output_path)
            plt.savefig(pdf_output_path)
            print("Saving figure in", png_output_path)
            plt.savefig(png_output_path)
            plt.close("all")

        for feature in self.feature_names:
            texts = deepcopy(upper_texts)
            upper_text = ", ".join(texts)

            qcd_inviso = []
            qcd_inviso_errors = []
            n_ss_iso = []
            n_ss_iso_errors = []
            valids = []
            for qcd_wp in self.qcd_wps:
                filename = inputs[qcd_wp]["yields"].targets[feature].path
                # print("inputs", inputs)
                # print("filename", filename)
                d = json.load(open(os.path.expandvars(filename), "r"))
                print("d", d)
                qcd_inviso.append(d["qcd_inviso"])
                qcd_inviso_errors.append(d["qcd_inviso_error"])
                n_ss_iso.append(d["n_ss_iso"]) ######TODO: check if this is the right name
                n_ss_iso_errors.append(d["n_ss_iso_error"])
                if qcd_inviso[-1] == 0 and qcd_inviso_errors[-1] == 0:
                    valids.append(False)
                else:
                    valids.append(True)

            def linear(x, a, b):
                return a * x + b

            def constant(x, a):
                return a

            print("Values to fit:", qcd_inviso)
            print("Statistical errors:", qcd_inviso_errors)

            

            if len([a for a in valids if a]) >= 2:
                opt_param_linear, pcov_linear = opt.curve_fit(linear,
                    [x for x in range(len(self.qcd_wps)) if valids[x]],
                    [qcd_inviso[iy] for iy in range(len(qcd_inviso)) if valids[iy]],
                    sigma=[qcd_inviso_errors[ie] for ie in range(len(qcd_inviso_errors))
                    if valids[ie]])
                opt_param_const, pcov_const = opt.curve_fit(constant,
                    [x for x in range(len(self.qcd_wps)) if valids[x]],
                    [qcd_inviso[iy] for iy in range(len(qcd_inviso)) if valids[iy]],
                    sigma=[qcd_inviso_errors[ie] for ie in range(len(qcd_inviso_errors))
                    if valids[ie]])
                # pcov_linear_sigmas = np.sqrt(np.diag(pcov_linear))
                pcov_const_sigmas = np.sqrt(np.diag(pcov_const))
                fitting = True
            else:  # not enough points to perform a fit
                # opt_param_linear, pcov_linear = None, None
                opt_param_const, pcov_const = None, None
                # pcov_linear_sigmas, pcov_const_sigmas = None, None
                fitting = False

            # if not fitting:
            #     linear_a = 0
            #     linear_error_a = 0
            #     linear_b = 0
            #     linear_error_b = 0
            # else:
            #    linear_a = opt_param_linear[0]
            #    linear_error_a = pcov_linear_sigmas[0]
            #    linear_b = opt_param_linear[1]
            #    linear_error_b = pcov_linear_sigmas[1]
            if not fitting:
                const_a = 0
                const_error_a = 0
            else:
                const_a = opt_param_const[0]
                const_error_a = pcov_const_sigmas[0]

            if self.add_normal_wp:
                wp_st = "standard"
                filename = inputs[law.NO_STR]["yields"].targets[feature].path
                d = json.load(open(os.path.expandvars(filename), "r"))
                y_st = d["qcd_inviso"]
                y_st_error = d["qcd_inviso_error"]
                n_ss_iso.append(d["n_ss_iso"])
                n_ss_iso_errors.append(d["n_ss_iso_error"])
                n_ss_inviso = d["n_ss_inviso"]
                n_ss_inviso_error = d["n_ss_inviso_error"]
                n_os_inviso = d["n_os_inviso"]
                n_os_inviso_error = d["n_os_inviso_error"]
            else:
                wp_st = ""
                y_st = ""
                y_st_error = ""
            
            print("y_st", y_st)
            print("qcd inviso", qcd_inviso)


            outputs = self.output()

            with open(outputs[(feature, "CD_txt")].path, "w") as f:
                for wp, value, error in zip(self.qcd_wps, qcd_inviso, qcd_inviso_errors):
                    f.write("{} {:.3f} {:.3f}\n".format(wp, value, error))

            print("output cd txt", outputs[(feature, "CD_txt")].path)
            print("qcd inviso", qcd_inviso)



            if self.normalize and not self.add_normal_wp:
                raise ValueError("Can't normalize values without considering the "
                    "'normal' working points!")
            elif self.normalize and y_st != 0:
                y_title = "C/D (normalized to vvl_m)"
                plot(self.qcd_wps, [value / y_st for value in qcd_inviso],
                    [value / y_st for value in qcd_inviso_errors], wp_st, 1., y_st_error / y_st,
                    [], [], [], "", y_title, upper_text,
                    pdf_output_path=outputs[(feature, "pdf_norm")].path,
                    png_output_path=outputs[(feature, "png_norm")].path)
            elif self.normalize:
                y_title = "C/D"
                plot(self.qcd_wps, [value for value in qcd_inviso],
                    [value for value in qcd_inviso_errors], wp_st, y_st, y_st_error,
                    [], [], [], "", y_title, upper_text,
                    pdf_output_path=outputs[(feature, "pdf_norm")].path,
                    png_output_path=outputs[(feature, "png_norm")].path)
                
            

            y_title = "C/D"
            text = []
            # if fitting:
            # text.append(r'Linear fit: ({:.2f}$\pm${:.2f})x+({:.2f}$\pm${:.2f})'.format(
            #     linear_a, linear_error_a, linear_b, linear_error_b))
            if fitting:
                text.append(r'Constant fit: ({:.2f}$\pm${:.2f})'.format(
                    const_a, const_error_a))
            plot(self.qcd_wps, qcd_inviso, qcd_inviso_errors, wp_st, y_st, y_st_error,
                [constant], [[const_a]], text, "", y_title,
                # [linear, constant], [[linear_a, linear_b], [const_a]], text, "", y_title,
                upper_text, pdf_output_path=outputs[(feature, "pdf")].path,
                png_output_path=outputs[(feature, "png")].path)

            # computing mean
            total_value = 0
            total_value_error = 0
            for i in range(len(qcd_inviso)):
                if not valids[i]:
                    continue
                val, error = qcd_inviso[i], qcd_inviso_errors[i]
                total_value += val / error
            total_inv_error = sum([1 / error for i, error in enumerate(qcd_inviso_errors)
                if valids[i]])
            total_value /= total_inv_error if total_inv_error != 0 else 1
            total_value_error = math.sqrt(len([a for a in valids if a])
                * (1 / total_inv_error) * (1 / total_inv_error)) if total_inv_error != 0 else 0

            print ("******************************")
            print ("{}, {}".format(self.category_name, self.get_channel(self.region_name)))
            print ("Constant Fit: {:.3f} +- {:.3f}".format(
                const_a, const_error_a))
            print ("Mean:         {:.3f} +- {:.3f}".format(total_value, total_value_error))
            print ("Standard:     {:.3f} +- {:.3f}".format(y_st, y_st_error))
            print ("******************************")

            postfix = "*" * len([a for a in valids if not a])
            create_file_dir(outputs[(feature, "txt")].path)
            with open(os.path.expandvars(outputs[(feature, "txt")].path), "w") as f:
                f.write("Fit {:.3f} {:.3f}\n".format(const_a, const_error_a))
                f.write("Mean {:.3f} {:.3f}\n".format(total_value, total_value_error))
                f.write("Standard {:.3f} {:.3f}{}\n".format(y_st, y_st_error, postfix))               

            with open(os.path.expandvars(outputs[(feature, "txt_b")].path), "w") as f:
                for wp, n, error in zip(list(self.qcd_wps) + ["vvl_m"], n_ss_iso, n_ss_iso_errors):
                    f.write("{} {:.3f} {:.3f}\n".format(wp, n, error))
                    f.write("{} {:.3f}\n".format(wp, error))

            if self.add_normal_wp:
                with open(os.path.expandvars(outputs[(feature, "txt_d")].path), "w") as f:
                    f.write("{:.3f} {:.3f}\n".format(n_ss_inviso, n_ss_inviso_error))
                with open(os.path.expandvars(outputs[(feature, "txt_c")].path), "w") as f:
                    f.write("{:.3f} {:.3f}\n".format(n_os_inviso, n_os_inviso_error))