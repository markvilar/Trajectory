import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from plotting import plot_3D_scatter

def get_features(data):
    features = {}
    for key, values in data.items():
        timestamps, counts = np.unique(values["Timestamp"], return_counts=True)
        features[key] = np.array([timestamps, counts]).T
    return features

def get_octaves(data):
    octaves = pd.DataFrame()
    for index, (key, values) in enumerate(data.items()):
        octave, counts = np.unique(values["Octave"], return_counts=True)
        octaves.insert(index, key, counts)
    return octaves

def feature_plot(features, xlims, ylims):
    fig, ax = plt.subplots(figsize=(7, 2.0))
    for key, value in features.items():
        ax.plot(value[:, 0], value[:, 1], label=key)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Num. of features [-]")
    ax.set_ylim(ylims)
    ax.set_xlim(xlims)

    lg = fig.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr = lg.get_frame()
    fr.set_edgecolor("black")
    fr.set_facecolor("white")

    fig.subplots_adjust(left=0.10, right=0.975, top=0.75, bottom=0.17, \
        wspace=0.2, hspace=0.675)

    return fig

def octave_plot(octave_data):
    # Octave distribution.
    margin = 0.4
    lefts, rights, centers = [], [], []
    fig, ax = plt.subplots(figsize=(7, 2.5))
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
        ax.barh(levels, fracs, left=-fracs/2+center, height=0.8, color="b", \
            label=method)

    ax.set_ylabel("Image Pyramid Level [-]")
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7, 8], minor=False)
    ax.set_yticklabels([1, 2, 3, 4, 5, 6, 7, 8])
    ax.set_xticks(centers, minor=False)
    ax.set_xlim([lefts[0]-margin, rights[-1]+margin])
    ax.set_xticklabels([col for col in octave_data.columns])
    fig.tight_layout()

    return fig

def main():
    directory = "/home/martin/dev/Trajectory/Data/SLAM/"
    time_lims = [ 1611313305.76, 1611313730 ]

    paths = {}
    paths["Raw"] = directory + "RAW-Keypoint-Statistics.csv"
    paths["BLF"] = directory + "BLF-Keypoint-Statistics.csv"
    paths["HE"] = directory + "HE-Keypoint-Statistics.csv"
    paths["CLAHE"] = directory + "CLAHE-Keypoint-Statistics.csv"
    paths["UIENet"] = directory + "UIENet-Keypoint-Statistics.csv"

    data = {}
    data["Raw"] = pd.read_csv(paths["Raw"])
    data["BLF"] = pd.read_csv(paths["BLF"])
    data["HE-BLF"] = pd.read_csv(paths["HE"])
    data["CLAHE-BLF"] = pd.read_csv(paths["CLAHE"])
    data["UIENet"] = pd.read_csv(paths["UIENet"])

    masked_data = {}
    for key, values in data.items():
        mask = np.logical_and(values["Depth"] != -1, values["Depth"] < 5)
        masked_data[key] = values[mask]

    # Extract features.
    extracted_features = get_features(data)
    tracked_features = get_features(masked_data)

    # Extract octaves.
    extracted_octaves = get_octaves(data)
    matched_octaves = get_octaves(masked_data)

    # Plot features.
    fig1 = feature_plot(extracted_features, time_lims, [0, 1400])
    fig2 = feature_plot(tracked_features, time_lims, [0, 650])

    # Plot octaves.
    fig3 = octave_plot(extracted_octaves)
    fig4 = octave_plot(matched_octaves)

    fig1.savefig("./Data/Output/Extracted-Features.pdf", dpi=300)
    fig2.savefig("./Data/Output/Matched-Features.pdf", dpi=300)
    fig3.savefig("./Data/Output/Extracted-Pyramid.pdf", dpi=300)
    fig4.savefig("./Data/Output/Matched-Pyramid.pdf", dpi=300)

    plt.show()

if __name__ == "__main__":
    main()
