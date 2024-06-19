import os
import shutil

years = ["2016", "2016APV", "2017", "2018"]
categories = ["baseline", "resolved_1b", "resolved_2b", "boosted_l", "boosted_m"]
channels = ["etau", "mutau", "tautau"]
version = "10May"
region = ["os_iso"]

for year in years:
    for cat in categories:
        for ch in channels:
            or_dir = f"/eos/user/e/emartinv/cmt/FeaturePlot/qcd_llr_{year}/cat_{cat}/{version}/"
            if not os.path.exists(or_dir):
                print("Directory does not exist: ", or_dir)
                continue
            des_dir = f"/eos/user/e/emartinv/www/Resonant/Control_Plots/{year}/{cat}/{ch}/"
            if not os.path.exists(des_dir):
                print("Directory does not exist: ", des_dir, "Creating...")
                os.makedirs(des_dir)

            files = os.listdir(or_dir)
            if not files:
                print("No files in directory: ", or_dir)
                continue

            for file in files:
                if file.endswith(('.png', '.pdf')) and ch in file and region[0] in file:
                    or_path = os.path.join(or_dir, file)
                    des_path = os.path.join(des_dir, file)
                    shutil.copy2(or_path, des_path)
                    print(f"Copying {or_path} to {des_path}")

