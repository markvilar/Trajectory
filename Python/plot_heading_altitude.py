import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from data_structures import Map, MapUnpacker

def main():
    gyro_path = "./Data/Navigation/Dive-01-ROV-Gyroscope.csv"
    dvl_path = "./Data/Navigation/Dive-01-ROV-DVL.csv"
    figure_path = "./Data/Output/Comparison-Heading-Altitude.pdf"

    time_limits = [ 1611313305.76, 1611313730 ]
    heading_limits = [ 0, 360 ]
    altitude_limits = [ 0, 3.3 ]

    gyro = pd.read_csv(gyro_path)
    dvl = pd.read_csv(dvl_path)

    fig, ax = plt.subplots(nrows=2, figsize=(7, 3.0))
    ax[0].plot(gyro["Epoch"], gyro["Heading"])
    ax[0].set_ylabel(r"Heading [deg]")
    ax[0].set_xlabel(r"Time [s]")
    ax[0].set_xlim(time_limits)
    ax[0].set_ylim(heading_limits)

    ax[1].plot(dvl["Epoch"], dvl["Altitude"])
    ax[1].set_ylabel(r"Altitude [m]")
    ax[1].set_xlabel(r"Time [s]")
    ax[1].set_xlim(time_limits)
    ax[1].set_ylim(altitude_limits)

    fig.tight_layout()

    fig.savefig(figure_path, dpi=300)
    
    plt.show()

if __name__ == "__main__":
    main()
