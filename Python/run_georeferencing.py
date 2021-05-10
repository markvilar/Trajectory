import argparse

from typing import Dict

import numpy as np
import pandas as pd

from data_structures import read_msgpack, Trajectory

from configuration import Configuration, OptimizationConfiguration, \
    SensorConfiguration
from georeference import georeference
from utilities import closest_point

def format_trajectory(data: Dict, key: str):
    timestamps = np.array(data[key]["Timestamps"])
    positions = np.stack([ data[key]["PositionX"], data[key]["PositionY"], \
        data[key]["PositionZ"] ]).T
    attitudes = np.stack([ data[key]["Quaternion1"], data[key]["Quaternion2"], \
        data[key]["Quaternion3"], data[key]["Quaternion4"] ]).T

    return Trajectory(timestamps, positions, attitudes)

def format_data(args):
    # Optimization configuration.
    optim = OptimizationConfiguration(args.threshold, args.bias, \
        args.win, args.win_start, args.win_length)

    # Configuration.
    config = Configuration(optim, args.slam, args.output, args.gt, \
        args.keyframes, args.frames, args.map, args.save, args.show_fig, \
        args.save_fig)

    data = {}
    data["Ground-Truth"] = pd.read_csv(args.gt)
    data["Frames"]      = pd.read_csv(args.slam + args.frames)
    data["Keyframes"]   = pd.read_csv(args.slam + args.keyframes)
    data["Map"]         = read_msgpack(args.slam + args.map)

    groundtruth = format_trajectory(data, "Ground-Truth")
    keyframes = format_trajectory(data, "Keyframes")
    frames = format_trajectory(data, "Frames")
    map = data["Map"].load()

    trajectories = {}
    trajectories["Ground-Truth"] = groundtruth
    trajectories["Keyframes"] = keyframes
    trajectories["Frames"] = frames

    return trajectories, map, config

def main():
    parser = argparse.ArgumentParser(description="Georeference SLAM output \
        with the Umeyama absolute orientation algorithm.")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument("--slam", type=str, help="Output directory.")
    required.add_argument("--output", type=str, help="Output directory.")

    required.add_argument("--gt", type=str, help="Groundtruth CSV file.")
    required.add_argument("--keyframes", type=str, help="Keyframes CSV file.")
    required.add_argument("--frames", type=str, help="Frames CSV file.")
    required.add_argument("--map", type=str, help="Map MessagePack file.")
        
    optional.add_argument("--save", type=bool, default=False, \
        help="Save output.", action=argparse.BooleanOptionalAction)
    optional.add_argument("--save_fig", type=bool, default=False, \
        help="Save figures.", action=argparse.BooleanOptionalAction)
    optional.add_argument("--show_fig", type=bool, default=False, \
        help="Show figures.", action=argparse.BooleanOptionalAction)

    optional.add_argument("--threshold", type=float, default=0.3, \
        help="Matching threshold.")
    optional.add_argument("--bias", type=float, default=0.0, \
        help="Time bias.")
    optional.add_argument("--win", type=bool, default=False,
        help="Windowed optimization.", action=argparse.BooleanOptionalAction)
    optional.add_argument("--win_start", type=int, default=0, \
        help="Window start.")
    optional.add_argument("--win_length", type=int, default=30, \
        help="Window length.")

    trajectories, map, config = format_data(parser.parse_args())
    georeference(trajectories, map, config)

if __name__ == "__main__":
    main()
