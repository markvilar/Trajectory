import copy

from typing import Dict, List, Tuple

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")
import matplotlib.patches as patches
import msgpack
import numpy as np
import quaternion as quat

import optimization

from configuration import Configuration
from data_structures import Map, MapUnpacker, Trajectory
from plotting import plot_3D_line, plot_3D_scatter
from utilities import closest_point, clamp_signal, quat_from_axis_angle, \
    quat_array_to_vec3_array, vec4_array_to_quat_array

def get_extremas_array_2D(arrays: List):
    m, n = arrays[0].shape

    extremas = []
    for array in arrays:
        extremas.append([ np.min(array, axis=0), np.max(array, axis=0) ])

    extremas = np.array(extremas)

    mins = np.min(np.min(extremas, axis=0), axis=0)
    maxs= np.max(np.max(extremas, axis=0), axis=0)

    return np.stack([mins, maxs], axis=1)

def visualize_alignment_results(config: Configuration, trajectories: Dict, \
    key_est, key_gt, label_est: str="Keyframes", label_gt: str="Ground Truth"):
    # Plot parameters.
    margins_pos = np.array([ -2, 2 ])
    margins_ang = np.array([ -10, 10 ])
    pad = 2.0
    w_pad = 2.0
    h_pad = 2.0
    patch_color = "y"
    patch_alpha = 0.5

    # Assign to variables.
    ground_truth = trajectories[key_gt]
    estimate = trajectories[key_est]

    # Truncate ground truth.
    start, _ = closest_point(estimate.timestamps[0], ground_truth.timestamps)
    end, _ = closest_point(estimate.timestamps[-1], ground_truth.timestamps)
    ground_truth.timestamps = ground_truth.timestamps[start:end+1]
    ground_truth.positions= ground_truth.positions[start:end+1]
    ground_truth.attitudes= ground_truth.attitudes[start:end+1]

    # Get ground truth attitude.
    q_ground_truth = vec4_array_to_quat_array(ground_truth.attitudes)
    q_estimate = vec4_array_to_quat_array(estimate.attitudes)
    angles_ground_truth = quat.as_euler_angles(q_ground_truth) * 180 / np.pi
    angles_estimate = quat.as_euler_angles(q_estimate) * 180 / np.pi
    angles_ground_truth = clamp_signal(angles_ground_truth, 0, 360)
    angles_estimate = clamp_signal(angles_estimate, 0, 360)

    # Calculate limits.
    lims_time = [ estimate.timestamps[0], estimate.timestamps[-1] ]
    lims_pos = get_extremas_array_2D( \
        [ estimate.positions, ground_truth.positions ])
    lims_ang = get_extremas_array_2D( \
        [ angles_estimate, angles_ground_truth ])
    lims_pos += margins_pos
    lims_ang += margins_ang

    # Visualize trajectory - Figure.
    fig1, ax1 = plt.subplots(nrows=3, ncols=1, figsize=(7, 4.5))
    fig1.tight_layout(pad=pad, w_pad=w_pad, h_pad=h_pad)

    # Position figure - Northing.
    ax1[0].plot(estimate.timestamps, estimate[:, 0])
    ax1[0].plot(ground_truth.timestamps, ground_truth[:, 0])
    ax1[0].set_xlim(lims_time)
    ax1[0].set_ylim(lims_pos[0])
    ax1[0].set_xlabel(r"Time, $t$ $[s]$")
    ax1[0].set_ylabel(r"Northing, $N$ $[m]$")
   
    # Position figure - Easting.
    ax1[1].plot(estimate.timestamps, estimate[:, 1])
    ax1[1].plot(ground_truth.timestamps, ground_truth[:, 1])
    ax1[1].set_xlim(lims_time)
    ax1[1].set_ylim(lims_pos[1])
    ax1[1].set_xlabel(r"Time, $t$ $[s]$")
    ax1[1].set_ylabel(r"Easting, $E$ $[m]$")

    # Position figure - Depth.
    ax1[2].plot(estimate.timestamps, estimate[:, 2], label=label_est)
    ax1[2].plot(ground_truth.timestamps, ground_truth[:, 2], \
        label=label_gt)
    ax1[2].set_xlim(lims_time)
    ax1[2].set_ylim(lims_pos[2])
    ax1[2].set_xlabel(r"Time, $t$ $[s]$")
    ax1[2].set_ylabel(r"Depth, $D$ $[m]$")

    # Position figure - legend.
    lg1 = fig1.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr1 = lg1.get_frame()
    fr1.set_facecolor("white")
    fr1.set_edgecolor("black")

    # Visualize attitudes - Figure.
    fig2, ax2 = plt.subplots(nrows=3, ncols=1, figsize=(7, 4.5))
    fig2.tight_layout(pad=2.0, w_pad=2.0, h_pad=2.0)

    ax2[0].plot(estimate.timestamps, angles_estimate[:, 0])
    ax2[0].plot(ground_truth.timestamps, angles_ground_truth[:, 0])
    ax2[0].set_xlim(lims_time)
    ax2[0].set_ylim(lims_ang[0])
    ax2[0].set_xlabel(r"Time, $t$ $[s]$")
    ax2[0].set_ylabel(r"Euler X, $r_{x}$ $[\text{deg}]$")

    ax2[1].plot(estimate.timestamps, angles_estimate[:, 1])
    ax2[1].plot(ground_truth.timestamps, angles_ground_truth[:, 1])
    ax2[1].set_xlim(lims_time)
    ax2[1].set_ylim(lims_ang[1])
    ax2[1].set_xlabel(r"Time, $t$ $[s]$")
    ax2[1].set_ylabel(r"Euler Y, $r_{y}$ $[\text{deg}]$")

    ax2[2].plot(estimate.timestamps, angles_estimate[:, 2], label=label_est)
    ax2[2].plot(ground_truth.timestamps, angles_ground_truth[:, 2], \
        label=label_gt)
    ax2[2].set_xlim(lims_time)
    ax2[2].set_ylim(lims_ang[2])
    ax2[2].set_xlabel(r"Time, $t$ $[s]$")
    ax2[2].set_ylabel(r"Euler Z, $r_{z}$ $[\text{deg}]$")

    lg2 = fig2.legend(bbox_to_anchor=(1, 1), loc="upper right", frameon=True, \
        fancybox=False)
    fr2 = lg2.get_frame()
    fr2.set_facecolor("white")
    fr2.set_edgecolor("black")

    if config.save_figures:
        fig1.savefig(config.output_dir + config.name + "-" + "Positions.pdf", \
            dpi=300)
        fig2.savefig(config.output_dir + config.name + "-" + "Attitudes.pdf", \
            dpi=300)

    if config.show_figures:
        plt.show()

def georeference(config: Configuration, trajectories: Dict, map: Map):
    """
    """
    # Get trajectories.
    ground_truth = trajectories["Ground-Truth"]
    keyframes = trajectories["Keyframes"]
    frames = trajectories["Frames"]

    # Get map landmarks.
    landmarks = map.get_landmarks()

    # Perform temporal and spatial optimization.
    results = optimization.optimize(config.optim, keyframes, ground_truth)
    rotation = results.rotation
    translation = results.translation
    matched_keyframes = results.matched_frames
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

    trajectories["Keyframes"] = keyframes
    trajectories["Frames"] = frames

    visualize_alignment_results(config, trajectories, "Keyframes", \
        "Ground-Truth")

    if config.save_output:
        keyframes.save_as_csv(config.output_dir + config.name + "-" \
            + "Keyframes.csv")
        frames.save_as_csv(config.output_dir + config.name + "-" \
            + "Frames.csv")
        landmarks.save_as_csv(config.output_dir + config.name + "-" \
            + "Landmarks.csv")
        matched_keyframes.save_as_csv(config.output_dir + config.name + "-" \
            + "Matched-Keyframes.csv")
        matched_ground_truth.save_as_csv(config.output_dir + config.name + "-" \
            + "Matched-Ground-Truth.csv")
