import copy

from typing import Dict, Tuple

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import msgpack
import numpy as np
import quaternion as quat

import optimization

from configuration import Configuration
from data_structures import Map, MapUnpacker, Trajectory
from plotting import plot_3D_line, plot_3D_scatter
from utilities import closest_point, clamp_signal, quat_from_axis_angle, \
    quat_array_to_vec3_array, vec4_array_to_quat_array

def visualize_results(trajectories: Dict, config: Configuration):
    # Create variables.
    ground_truth = trajectories["Ground-Truth"]
    keyframes = trajectories["Keyframes"]
    frames = trajectories["Frames"]
    matched_ground_truth = trajectories["Matched-Ground-Truth"]
    matched_keyframes = trajectories["Matched-Keyframes"]

    # Plot parameters.
    plot_margin_position = 2
    plot_margin_attitude = 10 * np.pi / 180

    # Visualize trajectory - Figure.
    fig3, ax3 = plt.subplots(nrows=3, ncols=1, figsize=(8, 5))
    fig3.tight_layout(h_pad=2)

    # Visualize trajectory - Northing.
    ax3[0].plot(keyframes.timestamps, keyframes[:, 0], label="Keyframes")
    ax3[0].plot(ground_truth.timestamps, ground_truth[:, 0], \
        label="Ground truth")
    ax3[0].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    ax3[0].set_ylim([ np.min(keyframes[:, 0]) - plot_margin_position, \
        np.max(keyframes[:, 0]) + plot_margin_position ])
    ax3[0].set_xlabel(r"Time, $t$ $[s]$")
    ax3[0].set_ylabel(r"Northing, $N$ $[m]$")
    ax3[0].legend(loc="lower right")

    # Visualize trajectory - Easting.
    ax3[1].plot(keyframes.timestamps, keyframes[:, 1], label="Keyframes")
    ax3[1].plot(ground_truth.timestamps, ground_truth[:, 1], \
        label="Ground truth")
    ax3[1].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    ax3[1].set_ylim([ np.min(keyframes[:, 1]) - plot_margin_position, \
        np.max(keyframes[:, 1]) + plot_margin_position ])
    ax3[1].set_xlabel(r"Time, $t$ $[s]$")
    ax3[1].set_ylabel(r"Easting, $E$ $[m]$")
    ax3[1].legend(loc="lower right")

    # Visualize trajectory - Depth.
    ax3[2].plot(keyframes.timestamps, keyframes[:, 2], label="Keyframes")
    ax3[2].plot(ground_truth.timestamps, ground_truth[:, 2], \
        label="Ground truth")
    ax3[2].set_ylim([ np.min(keyframes[:, 2]) - plot_margin_position, \
        np.max(keyframes[:, 2]) + plot_margin_position ])
    ax3[2].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    ax3[2].set_xlabel(r"Time, $t$ $[s]$")
    ax3[2].set_ylabel(r"Depth, $D$ $[m]$")
    ax3[2].legend(loc="lower right")

    # Get ground truth attitude.
    quat_ground_truth = vec4_array_to_quat_array(ground_truth.attitudes)
    quat_keyframes = vec4_array_to_quat_array(keyframes.attitudes)

    angles_ground_truth = quat.as_rotation_vector(quat_ground_truth)
    angles_keyframes = quat.as_rotation_vector(quat_keyframes)

    angles_ground_truth *= 180 / np.pi
    angles_keyframes *= 180 / np.pi

    angles_ground_truth = clamp_signal(angles_ground_truth, 0, 360)
    angles_keyframes = clamp_signal(angles_keyframes, 0, 360)

    # Visualize attitudes - Figure.
    fig4, ax4 = plt.subplots(nrows=3, ncols=1, figsize=(8, 5))
    fig4.tight_layout(h_pad=2)

    ax4[0].plot(keyframes.timestamps, angles_keyframes[:, 0], \
        label="Keyframes")
    ax4[0].plot(ground_truth.timestamps, angles_ground_truth[:, 0], \
        label="Ground truth")
    ax4[0].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    """
    ax4[0].set_ylim([ \
        np.min(attitudes_keyframes[:, 0]) - plot_margin_attitude, \
        np.max(attitudes_keyframes[:, 0]) + plot_margin_attitude ])
    """
    ax4[0].set_xlabel(r"Time, $t$ $[s]$")
    ax4[0].set_ylabel(r"Euler X, $r_{x}$ $[-]$")
    ax4[0].legend(loc="lower right")

    ax4[1].plot(keyframes.timestamps, angles_keyframes[:, 1], \
        label="Keyframes")
    ax4[1].plot(ground_truth.timestamps, angles_ground_truth[:, 1], \
        label="Ground truth")
    ax4[1].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    """
    ax4[1].set_ylim([ \
        np.min(attitudes_keyframes[:, 1]) - plot_margin_position, \
        np.max(attitudes_keyframes[:, 1]) + plot_margin_position ])
    """
    ax4[1].set_xlabel(r"Time, $t$ $[s]$")
    ax4[1].set_ylabel(r"Euler Y, $r_{y}$ $[-]$")
    ax4[1].legend(loc="lower right")

    ax4[2].plot(keyframes.timestamps, angles_keyframes[:, 2], \
        label="Keyframes")
    ax4[2].plot(ground_truth.timestamps, angles_ground_truth[:, 2], \
        label="Ground truth")
    ax4[2].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    """
    ax4[2].set_ylim([ \
        np.min(attitudes_keyframes[:, 2]) - plot_margin_position, \
        np.max(attitudes_keyframes[:, 2]) + plot_margin_position ])
    """
    ax4[2].set_xlabel(r"Time, $t$ $[s]$")
    ax4[2].set_ylabel(r"Euler Z, $r_{z}$ $[-]$")
    ax4[2].legend(loc="lower right")

    # Visualize matched window.
    if config.optim.window:
        fig6, ax6 = plot_3D_line(matched_ground_truth[:, 0], \
            matched_ground_truth[:, 1], matched_ground_truth[:, 2], 
            label="Matched Camera", xlabel= "Northing", ylabel="Easting", \
            zlabel="Depth", title="Trajectory", equal_axes=True)
        ax6.plot(matched_keyframes[:, 0], matched_keyframes[:, 1], \
            matched_keyframes[:, 2], label="Matched keyframes")
        ax6.legend()
   
    if config.show_figures:
        plt.show()

    if config.save_figures:
        # TODO: Save figures.
        pass

def georeference(trajectories: Dict, map: Map, config: Configuration):
    """
    """
    # Get trajectories.
    ground_truth = trajectories["Ground-Truth"]
    keyframes = trajectories["Keyframes"]
    frames = trajectories["Frames"]

    # Get map landmarks.
    landmarks = map.get_landmarks()

    # Perform temporal and spatial optimization.
    results = optimization.optimize(keyframes, ground_truth, config.optim)
    rotation = results.rotation
    translation = results.translation
    matched_keyframes = results.matched_keyframes
    matched_ground_truth = results.matched_ground_truth

    # Add matched trajectories.
    trajectories["Matched-Keyframes"] = matched_keyframes
    trajectories["Matched-Ground-Truth"] = matched_ground_truth

    # Add bias and apply rotation and translation.
    keyframes.add_time_bias(config.optim.bias)
    frames.add_time_bias(config.optim.bias)
    keyframes.apply_SE3_transform(rotation, translation)
    frames.apply_SE3_transform(rotation, translation)
    landmarks.apply_SE3_transform(rotation, translation)

    visualize_results(trajectories, config)

    # Temporary.
    start, _ = closest_point(keyframes.timestamps[0], ground_truth.timestamps)
    end, _ = closest_point(keyframes.timestamps[-1], ground_truth.timestamps)

    truncated = Trajectory(ground_truth.timestamps[start:end], \
        ground_truth.positions[start:end], ground_truth.attitudes[start:end])

    kf_directions = np.zeros(( len(keyframes.positions), 4 ))
    gt_directions = np.zeros(( len(truncated.positions), 4 ))
    kf_directions[:, 3] = 1.0
    gt_directions[:, 3] = 1.0
    kf_directions = vec4_array_to_quat_array(kf_directions)
    gt_directions = vec4_array_to_quat_array(gt_directions)

    kf_quats = vec4_array_to_quat_array(keyframes.attitudes)
    gt_quats = vec4_array_to_quat_array(truncated.attitudes)

    # Rotate directions.
    kf_directions = kf_quats * kf_directions * kf_quats.conjugate()
    gt_directions = gt_quats * gt_directions * gt_quats.conjugate()
    kf_directions = quat_array_to_vec3_array(kf_directions)
    gt_directions = quat_array_to_vec3_array(gt_directions)

    fig, ax = plot_3D_line(keyframes.positions[:, 0], \
        keyframes.positions[:, 1], keyframes.positions[:, 2], \
        equal_axes=True, color="b", label="Keyframes")

    ax.plot(truncated[:, 0], truncated[:, 1], truncated[:, 2], \
        color="r", label="Ground truth")

    ax.quiver(keyframes[:, 0], keyframes[:, 1], keyframes[:, 2], \
        kf_directions[:, 0], kf_directions[:, 1], kf_directions[:, 2], \
        color="b", length=0.4)

    ax.quiver(truncated[:, 0], truncated[:, 1], truncated[:, 2], \
        gt_directions[:, 0], gt_directions[:, 1], gt_directions[:, 2], \
        color="r", length=0.4)

    ax.legend()

    

    plt.show()

    if config.save_output:
        keyframes.save_as_csv(config.output_dir + config.keyframes_file)
        frames.save_as_csv(config.output_dir + config.frames_file)
        landmarks.save_as_csv(config.output_dir + config.map_file)
        matched_keyframes.save_as_csv(config.output_dir + "test1.csv")
        matched_ground_truth.save_as_csv(config.output_dir + "test2.csv")
