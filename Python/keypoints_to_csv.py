import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import pandas as pd

from data_structures import Map, MapUnpacker
from utilities import progress_bar

def main():
    map_path = "./Data/SLAM/Comparison/UIENet-01-Map.msg"
    output_path = "./Data/Output/UIENet-Keypoint-Statistics.csv"
    save = True

    unpacker = MapUnpacker(map_path)
    keyframes = unpacker.load().get_keyframes()

    total_keypoints = 0
    for id, frame in keyframes.items():
        total_keypoints += frame["n_keypts"]

    headers = ["Keyframe-ID", "Timestamp", "PositionX", "PositionY", \
        "Depth", "Angle", "Octave"]
    
    count = 0
    keypoints = []
    for id, frame in keyframes.items():
        for keypt, depth in zip(frame["keypts"], frame["depths"]):
            row = [ int(id), float(frame["ts"]), float(keypt["pt"][0]), \
                float(keypt["pt"][1]), float(depth), float(keypt["ang"]), \
                int(keypt["oct"]) ]
            keypoints.append(row)
            count += 1
            progress_bar((count / total_keypoints) * 100)
    
    keypoints = pd.DataFrame(keypoints, columns=headers)

    if save:
        keypoints.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()
