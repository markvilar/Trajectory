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
from utilities import quat_from_axis_angle, quat_array_to_vec3_array, \
    vec4_array_to_quat_array

def visualize_results(trajectories: Dict, config: Configuration):
    # Create variables.
    ground_truth = trajectories["Ground-Truth"]
    keyframes = trajectories["Keyframes"]
    frames = trajectories["Frames"]

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
    q_wc = vec4_array_to_quat_array(ground_truth.attitudes)
    q_wc = vec4_array_to_quat_array(keyframes.attitudes)

    q_cb = quat_from_axis_angle()

    # Visualize attitudes - Figure.
    fig4, ax4 = plt.subplots(nrows=3, ncols=1, figsize=(8, 5))
    fig4.tight_layout(h_pad=2)

    # Visualize attitudes - Roll.
    ax4[0].plot(keyframes.timestamps, q_bc[:, 0], \
        label="BC")
    ax4[0].plot(ground_truth.timestamps, q_bw[:, 0], \
        label="BW")
    ax4[0].plot(ground_truth.timestamps, q_bw[:, 0], \
        label="BW")
    ax4[0].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    ax4[0].set_ylim([ \
        np.min(attitudes_keyframes[:, 0]) - plot_margin_attitude, \
        np.max(attitudes_keyframes[:, 0]) + plot_margin_attitude ])
    ax4[0].set_xlabel(r"Time, $t$ $[s]$")
    ax4[0].set_ylabel(r"Roll, $r_{x}$ $[-]$")
    ax4[0].legend(loc="lower right")

    # Visualize attitudes - Pitch.
    ax4[1].plot(keyframes.timestamps, attitudes_keyframes[:, 1], \
        label="Keyframes")
    ax4[1].plot(ground_truth.timestamps, attitudes_gt[:, 1], \
        label="Ground truth")
    ax4[1].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    ax4[1].set_ylim([ \
        np.min(attitudes_keyframes[:, 1]) - plot_margin_position, \
        np.max(attitudes_keyframes[:, 1]) + plot_margin_position ])
    ax4[1].set_xlabel(r"Time, $t$ $[s]$")
    ax4[1].set_ylabel(r"Pitch, $r_{y}$ $[-]$")
    ax4[1].legend(loc="lower right")

    # Visualize attitude - Heading.
    ax4[2].plot(keyframes.timestamps, attitudes_keyframes[:, 2], \
        label="Keyframes")
    ax4[2].plot(ground_truth.timestamps, attitudes_gt[:, 2], \
        label="Ground truth")
    ax4[2].set_xlim([ keyframes.timestamps[0], keyframes.timestamps[-1] ])
    ax4[2].set_ylim([ \
        np.min(attitudes_keyframes[:, 2]) - plot_margin_position, \
        np.max(attitudes_keyframes[:, 2]) + plot_margin_position ])
    ax4[2].set_xlabel(r"Time, $t$ $[s]$")
    ax4[2].set_ylabel(r"Heading, $r_{z}$ $[-]$")
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

    # Add original keyframe trajectory.
    trajectories["Original"] = copy.deepcopy(keyframes)


    # Add bias and apply rotation and translation.
    keyframes.add_time_bias(config.optim.bias)
    frames.add_time_bias(config.optim.bias)
    keyframes.apply_SE3_transform(rotation, translation)
    frames.apply_SE3_transform(rotation, translation)
    landmarks.apply_SE3_transform(rotation, translation)

    # Printout.
    print("Rotation, vector: {0}".format( \
        quat.as_rotation_vector(rotation) * 180 / np.pi))
    print("Rotation, angles: {0}".format( \
        quat.as_euler_angles(rotation) * 180 / np.pi))
    print("Translation: {0}".format(translation))
    print("Time interval: {0}, {1}".format(keyframes.timestamps[0], \
        keyframes.timestamps[-1]))

    visualize_results(trajectories, config)

    if config.save_output:
        keyframes.save_as_csv(config.output_dir + config.keyframes_file)
        frames.save_as_csv(config.output_dir + config.frames_file)
        landmarks.save_as_csv(config.output_dir + config.map_file)
        matched_keyframes.save_as_csv(config.output_dir + "test1.csv")
        matched_ground_truth.save_as_csv(config.output_dir + "test2.csv")
