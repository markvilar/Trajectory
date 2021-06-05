import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from data_structures import Map, MapUnpacker

def main():
    paths = {}
    paths["Processing"] = "./Data/SLAM/Processing-Times.csv"
    paths["Tracking"] = "./Data/SLAM/Tracking-Times.csv"

    time_limits = [ 1611313305.76, 1611313400.87 ]

    processing_times = pd.read_csv(paths["Processing"])
    tracking_times = pd.read_csv(paths["Tracking"])

    processing_ts = processing_times["Timestamp"]
    tracking_ts = tracking_times["Timestamp"]

    processing = {}
    processing["Raw"] = processing_times["RAW"]
    processing["BLF"] = processing_times["BLF"]
    processing["HE-BLF"] = processing_times["HE"]
    processing["CLAHE-BLF"] = processing_times["CLAHE"]
    processing["UIENet"] = processing_times["UIENet"]

    tracking = {}
    tracking["Raw"] = tracking_times["RAW"]
    tracking["BLF"] = tracking_times["BLF"]
    tracking["HE-BLF"] = tracking_times["HE"]
    tracking["CLAHE-BLF"] = tracking_times["CLAHE"]
    tracking["UIENet"] = tracking_times["UIENet"]

    # Processing times.
    fig1, ax1 = plt.subplots(nrows=2, figsize=(7, 3.5))
    for key, value in processing.items():
        times = value[value > 0.0]
        timestamps = processing_ts[value > 0.0]
        ax1[0].plot(timestamps, times, label=key)
        ax1[1].plot(timestamps, times)

    ax1[0].set_ylabel(r"Processing Time [s]")
    ax1[0].set_xlabel(r"Time [s]")
    ax1[0].set_xlim(time_limits)
    ax1[0].set_ylim([ 0.0, 0.7 ])

    ax1[1].set_ylabel(r"Processing Time [s]")
    ax1[1].set_xlabel(r"Time [s]")
    ax1[1].set_xlim(time_limits)
    ax1[1].set_ylim([ 0.0, 0.07 ])

    lg1 = fig1.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr1 = lg1.get_frame()
    fr1.set_edgecolor("black")
    fr1.set_facecolor("white")

    fig1.subplots_adjust(left=0.10, right=0.975, top=0.85, bottom=0.17, \
        wspace=0.2, hspace=0.675)

    fig1.savefig("./Data/Output/Processing-Times.pdf", dpi=300)

    # Tracking times.
    fig2, ax2 = plt.subplots(figsize=(7, 2.0))
    for key, value in tracking.items():
        times = value[value > 0.0]
        timestamps = tracking_ts[value > 0.0]
        ax2.plot(timestamps, times, label=key)

    ax2.set_ylabel(r"Tracking Time [s]")
    ax2.set_xlabel(r"Time [s]")
    ax2.set_xlim(time_limits)
    ax2.set_ylim([ 0.0, 0.25 ])

    lg2 = fig2.legend(bbox_to_anchor=(0.69, 1.0), loc="upper center", \
        frameon=True, fancybox=False, ncol=3)
    fr2 = lg2.get_frame()
    fr2.set_edgecolor("black")
    fr2.set_facecolor("white")

    fig2.subplots_adjust(left=0.10, right=0.975, top=0.75, bottom=0.17, \
        wspace=0.2, hspace=0.675)

    fig2.savefig("./Data/Output/Tracking-Times.pdf", dpi=300)

    
    plt.show()

if __name__ == "__main__":
    main()
