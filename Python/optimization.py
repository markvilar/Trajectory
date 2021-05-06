from typing import Dict, Tuple

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import msgpack
import numpy as np
import quaternion 

import alignment
import utilities

from map import MapUnpacker
from plotting import plot_3D_trajectory
from series import DataSeries
from trajectory import Trajectory


def format_slam_trajectory(data: Dict, key: str):
    timestamps = np.array(data[key]["TimestampSynced"])
    
    positions = np.stack([ data[key]["PositionX"], data[key]["PositionY"], \
        data[key]["PositionZ"] ]).T
    
    attitudes = np.stack([ data[key]["Quaternion1"], data[key]["Quaternion2"], \
        data[key]["Quaternion3"], data[key]["Quaternion4"] ]).T

    return Trajectory(timestamps, positions, attitudes)

def format_navigation_series(data: Dict):
    aps_timestamps = data["APS"]["Epoch"].to_numpy()
    aps_series = np.stack([ data["APS"]["UTM Northing"], \
        data["APS"]["UTM Easting"], data["APS"]["Depth"] ]).T

    gyro_timestamps = data["Gyroscope"]["Epoch"].to_numpy()
    gyro_series = np.stack([ data["Gyroscope"]["Roll"], \
        data["Gyroscope"]["Pitch"], data["Gyroscope"]["Heading"] ]).T

    gyro_series = gyro_series * np.pi / 180

    aps = DataSeries(aps_timestamps, aps_series)
    gyro = DataSeries(gyro_timestamps, gyro_series)

    return aps, gyro

def estimate_camera_trajectory(aps, gyro, lever_arms, declination):
    """
    """
    K = len(aps.timestamps)

    cam_attitudes = np.zeros((K, 4))
    cam_timestamps = np.zeros(K)

    cam_attitudes = quaternion.as_quat_array(cam_attitudes)
    lever_arms = utilities.vector_to_quaternion(lever_arms)

    q_dec = utilities.quaternion_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
        declination)
    
    for k in range(K):
        aps_timestamp = aps.timestamps[k]
        aps_position = aps.series[k]

        cam_timestamps[k] = aps_timestamp

        j, _ = utilities.closest_point(aps_timestamp, gyro.timestamps)
        gyro_timestamp = gyro.timestamps[j]
        gyro_attitude = gyro.series[j]

        q_roll = utilities.quaternion_from_axis_angle( \
            np.array([ 1.0, 0.0, 0.0 ]), gyro_attitude[0])
        q_pitch = utilities.quaternion_from_axis_angle( \
            np.array([ 0.0, 1.0, 0.0 ]), gyro_attitude[1])
        q_yaw = utilities.quaternion_from_axis_angle( \
            np.array([ 0.0, 0.0, 1.0 ]), gyro_attitude[2])

        q_body = q_roll * q_pitch * q_yaw

        # Rotate lever arms and direction vectors.
        lever_arms[k]  = q_body * lever_arms[k] * q_body.conjugate()

        q_cam = q_dec * q_body

        cam_attitudes[k] = q_cam
        
    lever_arms = utilities.quaternion_to_vector(lever_arms)
    cam_attitudes = quaternion.as_float_array(cam_attitudes)

    cam_positions = aps.series + lever_arms

    cam_trajectory = Trajectory(cam_timestamps, cam_positions, cam_attitudes)

    return cam_trajectory

def georeference_optimization(data: Dict):
    # Extract SLAM trajectories.
    keyframes = format_slam_trajectory(data, "Keyframes")
    frames = format_slam_trajectory(data, "Frames")

    # Extract navigation data series.
    aps, gyro = format_navigation_series(data)

    # Set up sensor configuration.
    lever_arm = np.array([ 2.00, 0.21, 1.40 ])
    declination = 48 * np.pi / 180
    lever_arms = np.tile(lever_arm, ( len(aps.timestamps), 1 ))

    # Estimate camera positions from APS and gyroscope measurements.
    estimates = estimate_camera_trajectory(aps, gyro, lever_arms, declination)
        
    # Alignment, temporal and spatial.
    matched_keyframes, matched_estimates = alignment.temporal_alignment( \
        keyframes, estimates)
    scale, rotation, translation = alignment.spatial_alignment( \
        matched_keyframes, matched_estimates)

    # Georeference keyframe trajectory, frame trajectory, and map.
    keyframes.apply_SE3_transform(rotation, translation)
    frames.apply_SE3_transform(rotation, translation)

    # Load map.
    map = data["Map"].load()

    # Visualize trajectories.
    fig1, ax1 = plot_3D_trajectory(aps.series, \
        label="Transducer", xlabel= "Northing", ylabel="Easting", \
        zlabel="Depth", title="Trajectory")
    ax1.plot(estimates.positions[:, 0], estimates.positions[:, 1], \
        estimates.positions[:, 2], label="Camera")
    ax1.plot(keyframes.positions[:, 0], keyframes.positions[:, 1], \
        keyframes.positions[:, 2], label="Keyframe")
    ax1.plot(frames.positions[:, 0], frames.positions[:, 1], \
        frames.positions[:, 2], label="Frame")
    ax1.legend()
   
    # TODO: Save to file.

