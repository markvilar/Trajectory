from typing import Dict

import numpy as np
import pandas as pd
import quaternion as quat

from configuration import SensorConfiguration
from data_structures import DataSeries, Trajectory
from utilities import closest_point, quat_from_axis_angle, \
    vec3_to_quat, vec4_to_quat, \
    vec3_array_to_quat_array, vec4_array_to_quat_array, \
    quat_array_to_vec3_array, quat_array_to_vec4_array

def format_navigation_series(data: Dict):
    aps_timestamps = data["APS"]["Epoch"].to_numpy()
    aps_series = np.stack([ data["APS"]["UTM Northing"], \
        data["APS"]["UTM Easting"], data["APS"]["Depth"] ]).T

    gyro_timestamps = data["Gyroscope"]["Epoch"].to_numpy()
    gyro_series = np.stack([ data["Gyroscope"]["Roll"], \
        data["Gyroscope"]["Pitch"], data["Gyroscope"]["Heading"] ]).T

    gyro_series = gyro_series * np.pi / 180

    print(gyro_series[:10])

    aps = DataSeries(aps_timestamps, aps_series)
    gyro = DataSeries(gyro_timestamps, gyro_series)

    return aps, gyro

def estimate_camera_trajectory(aps: DataSeries, gyro: DataSeries, \
    sensor: SensorConfiguration):
    """
    """
    K = len(aps.timestamps)

    # Allocate.
    timestamps = np.zeros(K)
    world_translations_camera= vec4_array_to_quat_array(np.zeros((K, 4)))
    world_rotations_camera = vec4_array_to_quat_array(np.zeros((K, 4)))

    world_translations_body = vec4_array_to_quat_array(np.zeros((K, 4)))
    world_rotations_body =  vec4_array_to_quat_array(np.zeros((K, 4)))    

    # Get sensor configuration as quaternion arrays.
    body_translations_camera = sensor.get_translation_quat_array(K)
    body_rotations_camera = sensor.get_orientation_quat_array(K)

    # For every APS measurement, estimate the camera position.
    for k in range(K):
        aps_timestamp = aps.timestamps[k]
        aps_position = aps.series[k]

        timestamps[k] = aps_timestamp

        j, _ = closest_point(aps_timestamp, gyro.timestamps)
        gyro_timestamp = gyro.timestamps[j]
        gyro_attitude = gyro.series[j]

        # Create roll, pitch and yaw quaternions.
        q_roll = quat_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
            gyro_attitude[0])
        q_pitch = quat_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
            gyro_attitude[1])
        q_yaw = quat_from_axis_angle(np.array([ 0.0, 0.0, 1.0 ]), \
            gyro_attitude[2])

        world_translations_body[k] = vec3_to_quat(aps_position)
        world_rotations_body[k] =  q_yaw * q_pitch * q_roll

        # Translation / position.
        world_translations_camera[k] = \
             world_rotations_body[k] * body_translations_camera[k] \
             * world_rotations_body[k].conjugate() + world_translations_body[k]

        # Rotation.
        world_rotations_camera[k] = \
            world_rotations_body[k] * body_rotations_camera[k]
        
    camera_positions = quat_array_to_vec3_array(world_translations_camera)
    camera_attitudes = quat_array_to_vec4_array(world_rotations_camera)

    camera_trajectory = Trajectory(timestamps, camera_positions, \
        camera_attitudes)

    return camera_trajectory


def main():
    declination = 40.0 # 48.0
    camera_translation = np.array([ 2.00, 0.21, 1.40 ])
    camera_orientation = np.array([ 0.00, 90.0 - declination, 90.0 ]) \
        * np.pi / 180

    # Sensor configuration.
    sensor_config = SensorConfiguration(camera_translation, camera_orientation)

    data = {}
    data["APS"] = pd.read_csv( \
        "/home/martin/dev/Trajectory/Data/Navigation/Dive-02-ROV-APS.csv")
    data["Gyroscope"] = pd.read_csv( \
        "/home/martin/dev/Trajectory/Data/Navigation/Dive-02-ROV-Gyroscope.csv")

    # Extract navigation data series.
    aps, gyro = format_navigation_series(data)

    # Estimate camera positions from APS and gyroscope measurements.
    reference = estimate_camera_trajectory(aps, gyro, sensor_config)

    # Write csv.
    reference.save_as_csv(\
        "/home/martin/dev/Trajectory/Output/Ground-Truth-Dive-02.csv")

if __name__ == "__main__":
    main()
