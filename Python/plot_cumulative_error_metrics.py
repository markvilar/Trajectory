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
    est_paths["BLF"]   = directory + "BLF-Matched-Keyframes.csv"
    est_paths["HE"]    = directory + "HE-Matched-Keyframes.csv"
    est_paths["CLAHE"] = directory + "CLAHE-Matched-Keyframes.csv"

    gt_paths = {}
    gt_paths["BLF"]   = directory + "BLF-Matched-Ground-Truth.csv"
    gt_paths["HE"]    = directory + "HE-Matched-Ground-Truth.csv"
    gt_paths["CLAHE"] = directory + "CLAHE-Matched-Ground-Truth.csv"

    est_trajs = {}
    est_trajs["BLF"] = Trajectory()
    est_trajs["HE"] = Trajectory()
    est_trajs["CLAHE"] = Trajectory()

    est_trajs["BLF"].load_from_csv(est_paths["BLF"])
    est_trajs["HE"].load_from_csv(est_paths["HE"])
    est_trajs["CLAHE"].load_from_csv(est_paths["CLAHE"])

    gt_trajs = {}
    gt_trajs["BLF"] = Trajectory()
    gt_trajs["HE"] = Trajectory()
    gt_trajs["CLAHE"] = Trajectory()

    gt_trajs["BLF"].load_from_csv(gt_paths["BLF"])
    gt_trajs["HE"].load_from_csv(gt_paths["HE"])
    gt_trajs["CLAHE"].load_from_csv(gt_paths["CLAHE"])

    # Compute relative errors.

    relative_errors = {}
    rpe_dist = 5
    rpe_max_dist = 1
    relative_errors["BLF"] = compute_relative_error(est_trajs["BLF"], \
        gt_trajs["BLF"], rpe_dist, rpe_max_dist)
    relative_errors["HE + BLF"] = compute_relative_error(est_trajs["HE"], \
        gt_trajs["HE"], rpe_dist, rpe_max_dist)
    relative_errors["CLAHE + BLF"] = compute_relative_error( \
        est_trajs["CLAHE"], gt_trajs["CLAHE"], rpe_dist, rpe_max_dist)

    # Relative pose error plot.
    fig2, ax2 = plt.subplots(nrows=2, ncols=1, figsize=(7, 3.5))
    for key, error in relative_errors.items():
        ax2[0].plot(error["Timestamp"], error["Translation"], label=key)
        ax2[0].set_ylabel("RPE, trans. [m]")
        ax2[1].plot(error["Timestamp"], error["Rotation"])
        ax2[1].set_ylabel("RPE, rot. [deg]")
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
