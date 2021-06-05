import copy

import numpy as np
import quaternion as quat

from ssdts_matching import dynamic_timestamp_match

from data_structures import Trajectory
from utilities import closest_point

class OptimizationResult:
    def __init__(self, bias, scale, rotation, translation, frames, \
        ground_truth, win_frames=None, win_ground_truth=None):
        self.bias = bias
        self.scale = scale
        self.rotation = rotation
        self.translation = translation
        self.matched_frames = frames
        self.matched_ground_truth = ground_truth
        self.windowed_frames = win_frames
        self.windowed_ground_truth = win_ground_truth

def temporal_alignment(traj_from: Trajectory, traj_to: Trajectory, \
    threshold: float=0.3, bias: float=0.0):
    """
    """
    traj_from = copy.deepcopy(traj_from)
    traj_to = copy.deepcopy(traj_to)

    traj_from.add_time_bias(bias)

    # Perform matching.
    matching = dynamic_timestamp_match(traj_from.timestamps, \
        traj_to.timestamps, delta=threshold)

    # Create arrays.
    matches = np.array(list(matching.items()))
    matches_from = matches[:, 0]
    matches_to = matches[:, 1]

    # Get matching indices for trajectories.
    m, n = matches_from.shape[0], matches_to.shape[0]
    assert m == n, "Size of matches is inconsistent."
    indices_from, indices_to = np.empty(m, dtype=int), np.empty(n, dtype=int)
    for i, (match_from, match_to) in enumerate(zip(matches_from, matches_to)):
        index_from = np.where(traj_from.timestamps == match_from)[0]
        index_to = np.where(traj_to.timestamps == match_to)[0]
        indices_from[i] = index_from[0]
        indices_to[i] = index_to[0]
        assert len(index_from) == 1, \
            "Invalid matches from: {0}".format(index_from)
        assert len(index_to) == 1, \
            "Invalid matches to: {0}".format(index_to)

    # Sort indices.
    indices_from = np.sort(indices_from)
    indices_to = np.sort(indices_to)

    # Take the values for the matched indices.
    traj_from.timestamps = np.take(traj_from.timestamps, indices_from, axis=0)
    traj_from.positions = np.take(traj_from.positions, indices_from, axis=0)
    traj_from.attitudes = np.take(traj_from.attitudes, indices_from, axis=0)

    traj_to.timestamps = np.take(traj_to.timestamps, indices_to, axis=0)
    traj_to.positions = np.take(traj_to.positions, indices_to, axis=0)
    traj_to.attitudes = np.take(traj_to.attitudes, indices_to, axis=0)

    return traj_from, traj_to

def spatial_alignment(from_traj: Trajectory, to_traj: Trajectory):
    """
    """
    assert len(from_traj.positions.shape) == 2, \
        "Trajectory must be a m x n array."
    assert from_traj.positions.shape == to_traj.positions.shape, \
        "Trajectory and reference must have the same shape."

    from_points = from_traj.positions
    to_points = to_traj.positions
    
    N, m = from_points.shape
    
    mean_from = from_points.mean(axis = 0)
    mean_to = to_points.mean(axis = 0)
    
    delta_from = from_points - mean_from # m x n 
    delta_to = to_points - mean_to       # m x n 
    
    sigma_from = (delta_from * delta_from).sum(axis = 1).mean()
    sigma_to = (delta_to * delta_to).sum(axis = 1).mean()
    
    cov_matrix = delta_to.T.dot(delta_from) / N
    
    U, d, V_t = np.linalg.svd(cov_matrix, full_matrices = True)
    cov_rank = np.linalg.matrix_rank(cov_matrix)
    S = np.eye(m)
    
    if cov_rank >= m - 1 and np.linalg.det(cov_matrix) < 0:
        S[m-1, m-1] = -1
    elif cov_rank < m-1:
        raise ValueError("colinearility detected in covariance matrix:\n{}"\
            .format(cov_matrix))
    
    R = U.dot(S).dot(V_t)
    c = (d * S.diagonal()).sum() / sigma_from
    t = mean_to - c*R.dot(mean_from)
    
    return c, R, t

def optimize(config, frames, ground_truth):
    # Temporal matching.
    matched_frames, matched_ground_truth = temporal_alignment(frames, \
        ground_truth, config.threshold, config.bias)

    # If local window - Truncate matched keyframes and estimates.
    if config.window:
        windowed_frames = matched_frames.get_windowed_trajectory( \
            config.window_start, config.window_length)
        windowed_ground_truth = matched_ground_truth.get_windowed_trajectory( \
            config.window_start, config.window_length)
        # Spatial alignment.
        scale, rotation, translation = spatial_alignment(windowed_frames, \
            windowed_ground_truth)
    else:
        scale, rotation, translation = spatial_alignment(matched_frames, \
            matched_ground_truth)

    rotation = quat.from_rotation_matrix(rotation)

    # Apply transform.
    if config.window:
        windowed_frames.apply_SE3_transform(rotation, translation)

    matched_frames.apply_SE3_transform(rotation, translation)

    # Add to results.
    if config.window:
        result = OptimizationResult(config.bias, scale, rotation, \
            translation, matched_frames, matched_ground_truth, \
            windowed_frames, windowed_ground_truth)
    else:
        result = OptimizationResult(config.bias, scale, rotation, \
            translation, matched_frames, matched_ground_truth)

    return result
