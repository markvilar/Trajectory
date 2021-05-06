import argparse

from typing import Dict

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd
import quaternion 

import utilities

import map 

from model import georeference_model
from optimization import georeference_optimization

def extract_data(data: Dict, reference: bool, \
    show_figures: bool):
    """
    Georeferences SLAM output in the UTM datum.
    """
    # Select APS and gyroscope segment for keyframe trajectory.
    keyframe_start = data["Keyframes"]["TimestampSynced"].iat[0]
    keyframe_end = data["Keyframes"]["TimestampSynced"].iat[-1]

    aps_timestamps = data["APS"]["Epoch"]
    gyro_timestamps = data["Gyroscope"]["Epoch"]

    aps_start, _ = utilities.closest_point(keyframe_start, aps_timestamps)
    aps_end, _ = utilities.closest_point(keyframe_end, aps_timestamps)
    aps_end += 1

    gyro_start, _ = utilities.closest_point(keyframe_start, gyro_timestamps)
    gyro_end, _ = utilities.closest_point(keyframe_end, gyro_timestamps)
    gyro_end += 1

    # Create data container.
    formatted = {}
    formatted["Keyframes"] = data["Keyframes"]
    formatted["Frames"] = data["Frames"]
    formatted["Map"] = data["Map"]
    formatted["APS"] = data["APS"].iloc[aps_start:aps_end]
    formatted["Gyroscope"] = data["Gyroscope"].iloc[gyro_start:gyro_end]

    if reference:
        georeference_model(formatted)
    else:
        georeference_optimization(formatted)

    if show_figures:
        plt.show()
        
def main():
    slam_directory = "/home/martin/dev/Trajectory/Data/SLAM-Test/"
    nav_directory = "/home/martin/dev/Trajectory/Data/Navigation/Dive-1/"

    show_figures = True
    reference = False

    paths = {}
    paths["Frames"] = slam_directory + "Frame-Trajectory.csv"
    paths["Keyframes"] = slam_directory + "Keyframe-Trajectory.csv"
    paths["Map"] = slam_directory + "Map.msg"
    paths["APS"] = nav_directory + "ROV-APS.csv"
    paths["Gyroscope"] = nav_directory + "ROV-Gyroscope.csv"

    data = {}
    data["Frames"] = pd.read_csv(paths["Frames"])
    data["Keyframes"] = pd.read_csv(paths["Keyframes"])
    data["Map"] = map.read_msgpack(paths["Map"])
    data["APS"] = pd.read_csv(paths["APS"])
    data["Gyroscope"] = pd.read_csv(paths["Gyroscope"])

    extract_data(data, reference, show_figures)

if __name__ == "__main__":
    main()
