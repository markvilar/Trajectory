from typing import Dict, Tuple

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import quaternion 

import trajectory
import utilities

def calculate_lever_arm(arm: np.ndarray, angle: float):
    """
    Calculates the lever arm of the camera in the camera coordinate system.

    Parameters
    ----------
    arm: Lever arm expressed in the ROV coordinate system.
    angle : Rotation of the camera relative to the ROV coordinate system.

    Return
    ------
    array: Lever arm in camera coordinate system.
    """
    a = arm[1]
    b = arm[2]
    c = np.sqrt(a*a + b*b)
    alpha = np.arccos(b / c)
    phi = angle - alpha
    d = c * np.cos(phi)
    e = c * np.sin(phi)

    x = -arm[0]
    y = e
    z = -d
    return np.array([ x, y, z ])

def calculate_transducer_trajectory(cam_positions: np.ndarray, \
    cam_attitudes: np.ndarray, lever_arms: np.ndarray):
    """
    Calculates the local transducer trajectory from the camera cam_positions,
    cam_attitudes, and relative lever arm.

    Parameters
    ----------
    cam_positions: (N, 3) - Camera positions in the object CS.
    cam_attitudes: (N, 4) - Camera attitudes in the object CS.
    lever_arms:    (N, 3) - Lever arm from camera to transducer in the camera CS.

    Returns
    -------
    np.array: The transducer trajectory.
    """
    # Set up camera direction vectors.
    cam_directions = np.zeros(cam_positions.shape, dtype=float)
    cam_directions[:, -1] = 1.0

    # Convert lever arm, position and attitude to quaternions.
    lever_arms = utilities.vector_to_quaternion(lever_arms)
    cam_directions = utilities.vector_to_quaternion(cam_directions)
    cam_attitudes = quaternion.as_quat_array(cam_attitudes)

    # Calculate camera directions.
    cam_directions = cam_attitudes * cam_directions * cam_attitudes.conjugate()
    cam_directions = utilities.quaternion_to_vector(cam_directions)

    # Calculate trajectory of transducer with SLAM trajectory and lever arm.
    lever_arms = cam_attitudes * lever_arms * cam_attitudes.conjugate()
    lever_arms = utilities.quaternion_to_vector(lever_arms)
    trans_positions = cam_positions + lever_arms

    return trans_positions

def align_trajectories(cam_positions: np.ndarray, cam_attitudes: np.ndarray, \
    trans_positions: np.ndarray, inclination: float):
    """
    Calculates aligned trajectories, accounting for the camera 
    inclination, as well as different CS axis.

    Parameters
    ----------
    cam_positions:   (N, 3) - Camera cam_positions in the object CS.
    cam_attitudes:   (N, 4) - Camera cam_attitudes in the object CS.
    trans_positions: (N, 3) - Transducer cam_positions in the object CS.
    inclination:            - The camera inclination angle.

    Returns
    -------
    np.array: The camera trajectory.
    np.array: The camera attitudes.
    np.array: The transducer trajectory.
    """
    # Calculate quaternions for inclination and axis alignment rotations.
    q_i = utilities.quaternion_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
        -inclination)
    q_1 = utilities.quaternion_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
        90 * np.pi / 180)
    q_2 = utilities.quaternion_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
        90 * np.pi / 180)

    # Set up the entire transform as a quaternion product.
    rotation = q_2 * q_1 * q_i

    # Create direction vectors for the camera positions.
    cam_directions = np.zeros(cam_positions.shape, dtype=float)
    cam_directions[:, -1] = 1.0

    # Convert to quaternions.
    cam_positions = utilities.vector_to_quaternion(cam_positions)
    cam_attitudes = quaternion.as_quat_array(cam_attitudes)
    cam_directions = utilities.vector_to_quaternion(cam_directions)
    trans_positions = utilities.vector_to_quaternion(trans_positions)

    # Calculate the transformed camera attitudes.
    cam_attitudes = rotation * cam_attitudes

    # Positions are rotated with the object CS.
    cam_positions = rotation * cam_positions * rotation.conjugate()
    trans_positions = rotation * trans_positions * rotation.conjugate()
    cam_directions = cam_attitudes * cam_directions * cam_attitudes.conjugate()

    # Convert to vectors.
    cam_positions = utilities.quaternion_to_vector(cam_positions)
    cam_attitudes = quaternion.as_float_array(cam_attitudes)
    cam_directions = utilities.quaternion_to_vector(cam_directions)
    trans_positions = utilities.quaternion_to_vector(trans_positions)

    return cam_positions, cam_attitudes, trans_positions

def georeference_trajectories(cam_positions: np.ndarray, \
    cam_attitudes: np.ndarray, trans_positions: np.ndarray, \
    init_position: np.ndarray, init_attitude: np.ndarray):
    """
    Calculates the georeferenced trajectories, accounting for roll, pitch,
    and yaw, as well as transducer start position and lever arm.

    Parameters
    ----------
    cam_positions:   (N, 3) - Camera positions in the object CS.
    cam_attitudes:   (N, 4) - Camera attitudes in the object CS.
    trans_positions: (N, 3) - Transducer positions in the object CS.
    init_position:   (3,)   -
    init_attitude:   (3,)   -

    Returns
    -------
    np.array: The transducer trajectory.
    """
    # Set up quaternion for initial attitude.
    q_roll = utilities.quaternion_from_axis_angle( \
        np.array([ 1.0, 0.0, 0.0 ]), init_attitude[0])
    q_pitch = utilities.quaternion_from_axis_angle( \
        np.array([ 0.0, 1.0, 0.0 ]), init_attitude[1])
    q_yaw = utilities.quaternion_from_axis_angle( \
        np.array([ 0.0, 0.0, 1.0 ]), init_attitude[2])

    rotation = q_yaw * q_pitch * q_roll

    # Create direction vectors for the camera positions.
    cam_directions = np.zeros(cam_positions.shape, dtype=float)
    cam_directions[:, -1] = 1.0

    # Convert to quaternions.
    cam_positions = utilities.vector_to_quaternion(cam_positions)
    trans_positions = utilities.vector_to_quaternion(trans_positions)
    cam_directions = utilities.vector_to_quaternion(cam_directions)
    cam_attitudes = quaternion.as_quat_array(cam_attitudes)

    # Calculate attitudes.
    cam_attitudes = rotation * cam_attitudes

    # Calculate positions.
    cam_positions = rotation * cam_positions * rotation.conjugate()
    trans_positions = rotation * trans_positions * rotation.conjugate()
    cam_directions = rotation * cam_directions * rotation.conjugate()

    # Convert to vectors.
    cam_positions = utilities.quaternion_to_vector(cam_positions)
    trans_positions = utilities.quaternion_to_vector(trans_positions)
    cam_directions = utilities.quaternion_to_vector(cam_directions)
    cam_attitudes = quaternion.as_float_array(cam_attitudes)

    # Translate camera and transducer positions.
    trans_init_position = trans_positions[0, :]
    trans_positions = trans_positions - trans_init_position + init_position
    cam_positions = cam_positions - trans_init_position + init_position

    return cam_positions, cam_attitudes, trans_positions

def georeference_model(data: Dict):
    # Set up sensor configuration.
    measured_distances = np.array([ 0.21, 1.40, 2.00 ])
    measured_inclination = 48 * np.pi / 180
    lever_arm = calculate_lever_arm(measured_distances, measured_inclination)
    inclination = measured_inclination

    # Extract data.
    aps_positions = np.stack([ data["APS"]["UTM Northing"], \
        data["APS"]["UTM Easting"], -data["APS"]["Depth"] ]).T
    cam_positions = np.stack([ \
        data["Camera"]["PositionX"], \
        data["Camera"]["PositionY"], \
        data["Camera"]["PositionZ"] ]).T
    cam_attitudes = np.stack([ \
        data["Camera"]["Quaternion1"], \
        data["Camera"]["Quaternion2"], \
        data["Camera"]["Quaternion3"], \
        data["Camera"]["Quaternion4"] ]).T

    # Initialization point.
    init_position = np.array([ data["APS"]["UTM Northing"].iloc[0], \
        data["APS"]["UTM Easting"].iloc[0], data["APS"]["Depth"].iloc[0] ])
    init_attitude = np.array([ data["Gyroscope"]["Roll"].iloc[0], \
        data["Gyroscope"]["Pitch"].iloc[0], \
        data["Gyroscope"]["Heading"].iloc[0] ])

    # Convert measurements to radians.
    init_attitude = init_attitude * np.pi / 180

    # Allocate lever arm array.
    lever_arms = np.tile(lever_arm, ( cam_positions.shape[0], 1 ))

    # Calculate transducer positions in object coordinate system.
    trans_positions = calculate_transducer_trajectory(cam_positions, \
        cam_attitudes, lever_arms)

    # Calculate levelled trajectory.
    cam_positions, cam_attitudes, trans_positions = align_trajectories( \
        cam_positions, cam_attitudes, trans_positions, inclination)

    # Calculate georeferenced trajectory.
    cam_positions, cam_attitudes, trans_positions = \
        georeference_trajectories(cam_positions, cam_attitudes, \
        trans_positions, init_position, init_attitude)

    # Visualize the APS trajectory.
    fig1, ax1 = plot_3D_trajectory(aps_positions, label="Measured Transducer", \
        xlabel= "Northing", ylabel="Easting", zlabel="Depth", \
        title="Trajectory", equal_axes=True)

    ax1.plot(cam_positions[:, 0], cam_positions[:, 1], -cam_positions[:, 2],
        label="Camera")
    ax1.plot(trans_positions[:, 0], trans_positions[:, 1], \
        -trans_positions[:, 2], label="Estimated Transducer")
    ax1.legend()

