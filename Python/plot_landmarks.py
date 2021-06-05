import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from plotting import plot_3D_scatter

def main():
    directory = "/home/martin/dev/Trajectory/Data/SLAM/" \
        + "Segments-Georeferenced/"
    paths = [ directory + "Segment-01-Landmarks.csv",
        directory + "Segment-02-Landmarks.csv", \
        directory + "Segment-03-Landmarks.csv", \
        directory + "Segment-04-Landmarks.csv", \
        directory + "Segment-05-Landmarks.csv", \
        directory + "Segment-06-Landmarks.csv", \
        directory + "Segment-07-Landmarks.csv", \
        directory + "Segment-08-Landmarks.csv", \
        directory + "Segment-09-Landmarks.csv", \
        directory + "Segment-10-Landmarks.csv" ];

    maps = []
    for path in paths:
        maps.append(pd.read_csv(path))

    fused_maps = np.vstack(maps)
    fused_maps = fused_maps[:, 1:]

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.scatter(fused_maps[:, 1], fused_maps[:, 0], c=fused_maps[:, 2], 
        cmap="gray", s=0.1)
    ax.axis("equal")

    plt.show()

if __name__ == "__main__":
    main()
