import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from plotting import plot_3D_scatter

def main():
    directory = "/home/martin/dev/Trajectory/Data/SLAM/"
    paths = {}
    paths["Raw"] = directory + "RAW-Keypoint-Statistics.csv"
    paths["BLF"] = directory + "BLF-Keypoint-Statistics.csv"
    paths["HE"] = directory + "HE-Keypoint-Statistics.csv"
    paths["CLAHE"] = directory + "CLAHE-Keypoint-Statistics.csv"
    paths["UIENet"] = directory + "UIENet-Keypoint-Statistics.csv"

    data = {}
    data["Raw"] = pd.read_csv(paths["Raw"])
    data["BLF"] = pd.read_csv(paths["BLF"])
    data["HE + BLF"] = pd.read_csv(paths["HE"])
    data["CLAHE + BLF"] = pd.read_csv(paths["CLAHE"])
    data["UIENet"] = pd.read_csv(paths["UIENet"])

    masked_data = {}
    for key, values in data.items():
        mask = np.logical_and(values["Depth"] != -1, values["Depth"] < 5)
        masked_data[key] = values[mask]

    # Extract features.
    extracted_features = {}
    for key, values in data.items():
        timestamps, counts = np.unique(values["Timestamp"], return_counts=True)
        extracted_features[key] = np.array([timestamps, counts]).T

    # Tracked features.
    tracked_features = {}
    for key, values in masked_data.items():
        timestamps, counts = np.unique(values["Timestamp"], return_counts=True)
        tracked_features[key] = np.array([timestamps, counts]).T

    # Extract octave data.
    octave_data = pd.DataFrame()
    for index, (key, values) in enumerate(masked_data.items()):
        octave, counts = np.unique(values["Octave"], return_counts=True)
        octave_data.insert(index, key, counts)

    # Extracted features.
    fig1, ax1 = plt.subplots(figsize=(7, 2.0))
    for key, value in extracted_features.items():
        ax1.plot(value[:, 0], value[:, 1], label=key)

    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Num. of features [-]")
    ax1.set_ylim([ 0, 1700 ])
    ax1.set_xlim([ 1611313305.76, 1611313696.87 ])

    lg1 = fig1.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr1 = lg1.get_frame()
    fr1.set_edgecolor("black")
    fr1.set_facecolor("white")

    fig1.subplots_adjust(left=0.10, right=0.975, top=0.75, bottom=0.17, \
        wspace=0.2, hspace=0.675)

    # Tracked features.
    fig2, ax2 = plt.subplots(figsize=(7, 2.0))
    for key, value in tracked_features.items():
        ax2.plot(value[:, 0], value[:, 1], label=key)

    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Num. of features [-]")
    ax2.set_ylim([ 0, 800 ])
    ax2.set_xlim([ 1611313305.76, 1611313696.87 ])

    lg2 = fig2.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr2 = lg2.get_frame()
    fr2.set_edgecolor("black")
    fr2.set_facecolor("white")

    fig2.subplots_adjust(left=0.10, right=0.975, top=0.75, bottom=0.17, \
        wspace=0.2, hspace=0.675)


    # Octave distribution.
    margin = 0.4
    lefts, rights, centers = [], [], []
    fig3, ax3 = plt.subplots(figsize=(7, 2.5))
    for index, method in enumerate(octave_data):
        counts = octave_data[method]
        fracs = counts / max(counts)
        levels = np.arange(1, len(counts)+1)
        center = (1.0 + margin) * index
        left = center - 0.5
        right = center + 0.5
        lefts.append(left)
        centers.append(center)
        rights.append(right)
        ax3.barh(levels, fracs, left=-fracs/2+center, height=0.8, color="b", \
            label=method)

    ax3.set_ylabel("Image Pyramid Level [-]")
    ax3.set_yticks([1, 2, 3, 4, 5, 6, 7, 8], minor=False)
    ax3.set_yticklabels([1, 2, 3, 4, 5, 6, 7, 8])
    ax3.set_xticks(centers, minor=False)
    ax3.set_xlim([lefts[0]-margin, rights[-1]+margin])
    ax3.set_xticklabels([col for col in octave_data.columns])
    fig3.tight_layout()

    fig1.savefig("./Data/Output/Extracted-Features.pdf", dpi=300)
    fig2.savefig("./Data/Output/Tracked-Features.pdf", dpi=300)
    fig3.savefig("./Data/Output/Image-Pyramid-Distribution.pdf", dpi=300)

    plt.show()

if __name__ == "__main__":
    main()
