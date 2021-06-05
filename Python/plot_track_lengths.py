import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from plotting import plot_3D_scatter

def main():
    directory = "/home/martin/dev/Trajectory/Data/SLAM/"
    time_lims = [ 1611313305.76, 1611313730 ]

    path = directory + "SLAM-Trajectory-Statistics.csv"

    data = pd.read_csv(path)

    lengths = {}
    lengths["Raw"]       = data["Raw Length"]
    lengths["BLF"]       = data["BLF Length"]
    lengths["HE-BLF"]    = data["HE Length"]
    lengths["CLAHE-BLF"] = data["CLAHE Length"]
    lengths["UIENet"]    = data["UIENET Length"]

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.boxplot(lengths.values(), labels=lengths.keys())
    ax.set_ylim([0, 10000])

    boxprops = dict(facecolor="white", edgecolor="black", alpha=0.8)
    ax.text(0.85, 0.85, r"$N = 10$", transform=ax.transAxes, fontsize=14, \
        bbox=boxprops)

    fig.savefig("./Data/Output/Track-Lengths.pdf", dpi=300)

    plt.show()

if __name__ == "__main__":
    main()
