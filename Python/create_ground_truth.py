from typing import Dict

import numpy as np
import pandas as pd
import quaternion as quat

from configuration import SensorConfiguration
from data_structures import DataSeries, Trajectory
from utilities import closest_point, quaternion_from_axis_angle, \
    quaternion_to_vec3, quaternion_to_vec4, vec4_to_quaternion

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

def estimate_camera_trajectory(aps: DataSeries, gyro: DataSeries, \
    sensor: SensorConfiguration):
    """
    """
    K = len(aps.timestamps)

    # Allocate.
    cam_attitudes = np.zeros((K, 4))
    cam_timestamps = np.zeros(K)
    cam_attitudes = vec4_to_quaternion(cam_attitudes)
    
    # Get sensor configuration as quaternion arrays.
    cam_translations = sensor.get_translation_quat_array(K)
    cam_orientations = sensor.get_orientation_quat_array(K)

    # For every APS measurement, estimate the camera position.
    for k in range(K):
        aps_timestamp = aps.timestamps[k]
        aps_position = aps.series[k]

        cam_timestamps[k] = aps_timestamp

        j, _ = closest_point(aps_timestamp, gyro.timestamps)
        gyro_timestamp = gyro.timestamps[j]
        gyro_attitude = gyro.series[j]

        q_roll = quaternion_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
            gyro_attitude[0])
        q_pitch = quaternion_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
            gyro_attitude[1])
        q_yaw = quaternion_from_axis_angle(np.array([ 0.0, 0.0, 1.0 ]), \
            gyro_attitude[2])

        q_body = q_roll * q_pitch * q_yaw

        # Rotate lever arms and direction vectors.
        cam_translations[k]  = q_body * cam_translations[k] * q_body.conjugate()
        cam_attitudes[k] = cam_orientations[k] * q_body
        
    cam_translations = quaternion_to_vec3(cam_translations)
    cam_positions = aps.series + cam_translations
    cam_attitudes = quaternion_to_vec4(cam_attitudes)

    cam_trajectory = Trajectory(cam_timestamps, cam_positions, cam_attitudes)

    return cam_trajectory


def main():
    # Sensor configuration
    camera_translation = np.array([ 2.00, 0.21, 1.40 ])
    camera_orientation = np.array([ 0.00, 48.0, 0.00 ]) * np.pi / 180
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
        "/home/martin/dev/Trajectory/Output/Groundtruth-Dive-02.csv")

if __name__ == "__main__":
    main()
