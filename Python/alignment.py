import copy

import numpy as np

from utilities import closest_point
from trajectory import Trajectory

def temporal_alignment(from_traj: Trajectory, to_traj: Trajectory, \
    threshold: float=0.5):
    """
    """
    len_from = len(from_traj.timestamps)
    len_to = len(to_traj.timestamps)

    # Set reference to the trajectory with the least entries, assuming that
    # it has less frequent entries.
    if len_from < len_to:
        m = len_from
        n = len_to
        references = copy.deepcopy(from_traj)
        values = copy.deepcopy(to_traj)
    else:
        m = len_to
        n = len_from
        references = copy.deepcopy(to_traj)
        values = copy.deepcopy(from_traj)

    # Allocate arrays.
    match_indices_val = np.full(m, -1, dtype=int)
    match_times_val = np.full(m, threshold, dtype=float)
    match_indices_ref = np.full(n, -1, dtype=int)
    match_times_ref = np.full(n, threshold, dtype=float)

    # Loop through reference points and find the best temporal match.
    for index_ref in range(m):
        index_val, time = closest_point(references.timestamps[index_ref], \
            values.timestamps)
        
        # Perform matching by checking that the time difference is lower
        # than the threshold.
        if match_times_val[index_ref] > time and time < threshold:
            match_indices_val[index_ref] = index_val
            match_times_val[index_ref] = time
            match_indices_ref[index_val] = index_ref
            match_times_ref[index_val] = time

    # Set up mask filter.
    mask_ref = match_indices_ref != -1
    mask_val = match_indices_val != -1

    # Filter indices based on mask.
    match_indices_ref = match_indices_ref[mask_ref]
    match_indices_val = match_indices_val[mask_val]

    # Take values based on indices.
    references.timestamps = np.take(references.timestamps, match_indices_ref, \
        axis=0)
    references.positions = np.take(references.positions, match_indices_ref, \
        axis=0)
    references.attitudes = np.take(references.attitudes, match_indices_ref, \
        axis=0)

    values.timestamps = np.take(values.timestamps, match_indices_val, axis=0)
    values.positions = np.take(values.positions, match_indices_val, axis=0)
    values.attitudes = np.take(values.attitudes, match_indices_val, axis=0)

    # Switch back to to and from trajectories.
    if len_from < len_to:
        return references, values
    else:
        return values, references

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
    
    delta_from = from_points - mean_from # N x m
    delta_to = to_points - mean_to       # N x m
    
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
