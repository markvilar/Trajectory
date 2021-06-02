import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import quaternion as quat

from data_structures import Trajectory
from error import compute_absolute_error, compute_relative_error

def main():
    directory = "./Data/SLAM/Comparison-Georeferenced/"
    est_paths = {}
    est_paths["RAW"]   = directory + "RAW-Matched-Keyframes.csv"
    est_paths["BLF"]   = directory + "BLF-Matched-Keyframes.csv"
    est_paths["HE"]    = directory + "HE-Matched-Keyframes.csv"
    est_paths["CLAHE"] = directory + "CLAHE-Matched-Keyframes.csv"
    est_paths["UIENet"] = directory + "UIENet-Matched-Keyframes.csv"

    gt_paths = {}
    gt_paths["RAW"]   = directory + "RAW-Matched-Ground-Truth.csv"
    gt_paths["BLF"]   = directory + "BLF-Matched-Ground-Truth.csv"
    gt_paths["HE"]    = directory + "HE-Matched-Ground-Truth.csv"
    gt_paths["CLAHE"] = directory + "CLAHE-Matched-Ground-Truth.csv"
    gt_paths["UIENet"] = directory + "UIENet-Matched-Ground-Truth.csv"

    est_trajs = {}
    est_trajs["RAW"] = Trajectory()
    est_trajs["BLF"] = Trajectory()
    est_trajs["HE"] = Trajectory()
    est_trajs["CLAHE"] = Trajectory()
    est_trajs["UIENet"] = Trajectory()

    est_trajs["RAW"].load_from_csv(est_paths["RAW"])
    est_trajs["BLF"].load_from_csv(est_paths["BLF"])
    est_trajs["HE"].load_from_csv(est_paths["HE"])
    est_trajs["CLAHE"].load_from_csv(est_paths["CLAHE"])
    est_trajs["UIENet"].load_from_csv(est_paths["UIENet"])

    gt_trajs = {}
    gt_trajs["RAW"] = Trajectory()
    gt_trajs["BLF"] = Trajectory()
    gt_trajs["HE"] = Trajectory()
    gt_trajs["CLAHE"] = Trajectory()
    gt_trajs["UIENet"] = Trajectory()

    gt_trajs["RAW"].load_from_csv(gt_paths["RAW"])
    gt_trajs["BLF"].load_from_csv(gt_paths["BLF"])
    gt_trajs["HE"].load_from_csv(gt_paths["HE"])
    gt_trajs["CLAHE"].load_from_csv(gt_paths["CLAHE"])
    gt_trajs["UIENet"].load_from_csv(gt_paths["UIENet"])

    absolute_errors = {}
    absolute_errors["Raw"] = compute_absolute_error(est_trajs["RAW"], \
        gt_trajs["RAW"])
    absolute_errors["BLF"] = compute_absolute_error(est_trajs["BLF"], \
        gt_trajs["BLF"])
    absolute_errors["HE + BLF"] = compute_absolute_error(est_trajs["HE"], \
        gt_trajs["HE"])
    absolute_errors["CLAHE + BLF"] = compute_absolute_error(est_trajs["CLAHE"], \
        gt_trajs["CLAHE"])
    absolute_errors["UIENet"] = compute_absolute_error(est_trajs["UIENet"], \
        gt_trajs["UIENet"])

    relative_errors = {}
    rpe_dist = 5
    rpe_max_dist = 1
    relative_errors["Raw"] = compute_relative_error(est_trajs["RAW"], \
        gt_trajs["RAW"], rpe_dist, rpe_max_dist)
    relative_errors["BLF"] = compute_relative_error(est_trajs["BLF"], \
        gt_trajs["BLF"], rpe_dist, rpe_max_dist)
    relative_errors["HE + BLF"] = compute_relative_error(est_trajs["HE"], \
        gt_trajs["HE"], rpe_dist, rpe_max_dist)
    relative_errors["CLAHE + BLF"] = compute_relative_error( \
        est_trajs["CLAHE"], gt_trajs["CLAHE"], rpe_dist, rpe_max_dist)
    relative_errors["UIENet"] = compute_relative_error(est_trajs["UIENet"], \
        gt_trajs["UIENet"], rpe_dist, rpe_max_dist)

    # Absolute error plot.
    fig1, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(7, 3.5))
    for key, error in absolute_errors.items():
        ax1[0].plot(error["Timestamp"], error["Translation"], label=key)
        ax1[0].set_ylabel("RMSE, trans. [m]")
        ax1[1].plot(error["Timestamp"], error["Rotation"])
        ax1[1].set_ylabel("RMSE, rot. [deg]")
    ax1[0].set_xlabel("Time, $t$ [s]")
    ax1[1].set_xlabel("Time, $t$ [s]")
    ax1[0].set_xlim(est_trajs["HE"].get_timestamps()[0], \
        est_trajs["HE"].get_timestamps()[-10])
    ax1[1].set_xlim(est_trajs["HE"].get_timestamps()[0], \
        est_trajs["HE"].get_timestamps()[-10])
    lg1 = fig1.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr1 = lg1.get_frame()
    fr1.set_facecolor("white")
    fr1.set_edgecolor("black")
    fig1.subplots_adjust(left=0.10, right=0.975, top=0.85, bottom=0.17, \
        wspace=0.2, hspace=0.675)

    # Relative pose error plot.
    fig2, ax2 = plt.subplots(nrows=2, ncols=1, figsize=(7, 3.5))
    for key, error in relative_errors.items():
        ax2[0].plot(error["Timestamp"], error["Translation"], label=key)
        ax2[0].set_ylabel("RMSE, trans. [m]")
        ax2[1].plot(error["Timestamp"], error["Rotation"])
        ax2[1].set_ylabel("RMSE, rot. [deg]")
    ax2[0].set_xlabel("Time, $t$ [s]")
    ax2[1].set_xlabel("Time, $t$ [s]")
    ax2[0].set_xlim(est_trajs["HE"].get_timestamps()[0], \
        est_trajs["HE"].get_timestamps()[-10])
    ax2[1].set_xlim(est_trajs["HE"].get_timestamps()[0], \
        est_trajs["HE"].get_timestamps()[-10])
    lg2 = fig2.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr2 = lg2.get_frame()
    fr2.set_facecolor("white")
    fr2.set_edgecolor("black")
    fig2.subplots_adjust(left=0.10, right=0.975, top=0.85, bottom=0.17, \
        wspace=0.2, hspace=0.675)

    fig1.savefig("./Data/Output/SLAM-Metric-ATE.pdf", dpi=300)
    fig2.savefig("./Data/Output/SLAM-Metric-RPE.pdf", dpi=300)

    plt.show()

if __name__ == "__main__":
    main()
