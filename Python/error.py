import math

import numpy as np
import quaternion as quat

from data_structures import Trajectory
from utilities import quat_to_vec4

def get_distance_from_start(gt_translation):
    distances = np.diff(gt_translation[:, 0:3], axis=0)
    distances = np.sqrt(np.sum(np.multiply(distances, distances), 1))
    distances = np.cumsum(distances)
    distances = np.concatenate(([0], distances))
    return distances

def compute_comparison_indices_length(distances, dist, max_dist_diff):
    """
    Parameters
    ----------
    distances
        Distances from the trajectory start.
    dist
    max_dist_diff
    """
    max_idx = len(distances)
    comparisons = []
    for idx, d in enumerate(distances):
        best_idx = -1
        error = max_dist_diff
        for i in range(idx, max_idx):
            if np.abs(distances[i]-(d+dist)) < error:
                best_idx = i
                error = np.abs(distances[i] - (d+dist))
        if best_idx != -1:
            comparisons.append(best_idx)
    return comparisons

def compute_angle(transform):
    """
    Compute the rotation angle from a 4x4 homogeneous matrix.
    """
    x = np.trace(transform[0:3, 0:3]) - 1.0
    return np.arccos(min(1.0, max(-1.0, x / 2.0))) * 180.0 / np.pi

def compute_relative_error(estimate, ground_truth, dist, max_dist_diff):
    """
    Computes the relative trajectory error from two aligned and synchronized
    trajectories that are scaled.
    """
    # Get timestamps, positions, and attitudes.
    t_es = estimate.get_timestamps()
    p_es, q_es = estimate.get_positions(), estimate.get_attitudes()
    p_gt, q_gt = ground_truth.get_positions(), ground_truth.get_attitudes()

    # Get homogeneous transforms.
    T_es = estimate.get_homogeneous_transforms()
    T_gt = ground_truth.get_homogeneous_transforms()

    # Get cumulative distances.
    accum_distances = get_distance_from_start(p_gt)

    # Compute comparisons.
    comparisons = compute_comparison_indices_length(accum_distances, dist, \
        max_dist_diff)

    assert len(comparisons) >= 2, "Too few samples!"

    ts = []
    rpes = []
    for k, delta in enumerate(comparisons):
        if not delta == -1:
            # Estimated values.
            t = t_es[k]
            T_es_k = T_es[k]
            T_es_delta = T_es[delta]
            T_error_es = np.dot( np.linalg.inv(T_es_k), T_es_delta )

            # Ground truth values.
            T_gt_k = T_gt[k]
            T_gt_delta = T_gt[delta]
            T_error_gt = np.dot( np.linalg.inv(T_gt_k), T_gt_delta )

            rpe = np.dot( np.linalg.inv(T_error_gt), T_error_es )

            ts.append(t)
            rpes.append(rpe)

    rpe_trans_norm = []
    rpe_trans_perc = []
    rpe_rot = []
    rpe_rot_deg_per_m = []
    for rpe in rpes:
        rpe_trans = np.linalg.norm(rpe[0:3, 3])
        rpe_trans_norm.append(rpe_trans)
        rpe_trans_perc.append((rpe_trans / dist) * 100)
        rpe_rot.append(compute_angle(rpe))
        rpe_rot_deg_per_m.append(rpe_rot[-1] / dist)

    results = {}
    results["Timestamp"] = np.array(ts)
    results["RPE"] = np.array(rpes)
    results["Translation"] = np.array(rpe_trans_norm)
    results["Translation-Perc"] = np.array(rpe_trans_perc)
    results["Rotation"] = np.array(rpe_rot)
    results["Rotation-Norm"] = np.array(rpe_rot_deg_per_m)

    return results


def compute_absolute_error(estimate: Trajectory, ground_truth: Trajectory):
    """
    Computes the absolute trajectory error from two aligned and synchronized
    trajectories that are scaled.
    """
    ts = estimate.get_timestamps()
    p_es, q_es = estimate.get_positions(), estimate.get_attitudes()
    p_gt, q_gt = ground_truth.get_positions(), ground_truth.get_attitudes()

    # Translation errors.
    translation_comp_errors = (p_gt - p_es)
    translation_errors = np.sqrt(np.sum(translation_comp_errors**2, 1))

    # Attitude errors.
    rotation_errors = np.zeros(len(translation_comp_errors))
    rotation_comp_errors = np.zeros(p_es.shape)
    for i in range(p_es.shape[0]):
        R_es = quat.as_rotation_matrix(q_es[i])
        R_gt = quat.as_rotation_matrix(q_gt[i])

        R_error = np.dot(R_es, np.linalg.inv(R_gt))
        q_error = quat.from_rotation_matrix(R_error)
        rotation_comp_errors[i, :] = quat.as_euler_angles(q_error)

        canonicals = np.array([ R_error[2, 1] - R_error[1, 2], \
            R_error[0, 2] - R_error[2, 0], \
            R_error[1, 0] - R_error[0, 1] ])
        rotation_errors[i] = np.rad2deg(np.linalg.norm(canonicals))
    
    results = {}
    results["Timestamp"] = ts
    results["Translation"] = translation_errors
    results["Translation-Components"] = translation_comp_errors
    results["Rotation"] = rotation_errors
    results["Rotation-Components"] = rotation_comp_errors
    return results
