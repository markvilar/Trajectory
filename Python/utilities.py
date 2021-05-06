import numpy as np
import pandas as pd
import quaternion 

from typing import Dict, List

def unclamp_signal(data: np.ndarray, min_value: float, max_value: float, \
    threshold: float=0.95):
    differences = np.insert(data[1:] - data[:-1], 0, 0.0)
    steps = np.zeros(differences.shape, dtype=int)
    steps[differences > threshold * (max_value - min_value)] = -1
    steps[differences < -threshold * (max_value - min_value)] = 1
    revolutions = np.cumsum(steps)
    return data + revolutions * (max_value - min_value)

def clamp_signal(data: np.ndarray, min_value: float, max_value: float):
    upper_mask = data > max_value
    lower_mask = data < min_value
    adjustments = np.zeros(data.shape, dtype=float)
    adjustments[upper_mask] = np.ceil(data[upper_mask] \
        / (max_value - min_value)) * (max_value - min_value)
    adjustments[lower_mask] = -np.floor(data[lower_mask] \
        / (max_value - min_value)) * (max_value - min_value)
    return data + adjustments

def progress_bar(percentage_done: int, bar_width: int=60):
	progress = int(bar_width * percentage_done / 100)
	bar = '=' * progress + ' ' * (bar_width - progress)
	sys.stdout.write('[{0}] {1:.2f}{2}\r'.format(bar, percentage_done, '%'))
	sys.stdout.flush()

def closest_point(reference, data):
    relative = np.abs(data - reference)
    index = np.argmin(relative)
    value = relative[index]
    return index, value

def quaternion_from_axis_angle(axis: np.ndarray, angle: float):
    assert axis.shape == (3,), "The axis vector must be (3,)."
    assert np.linalg.norm(axis) == 1.0, "The axis vector must have norm 1."
    imaginary = np.sin(angle/2) * axis
    real = np.cos(angle/2)
    return quaternion.quaternion(real, imaginary[0], imaginary[1], imaginary[2])

def vector_to_quaternion(vectors: np.ndarray):
    n = vectors.shape[0]
    quats = np.zeros(( n, 4 ), dtype=float)
    quats[:, 1:4] = vectors
    return quaternion.as_quat_array(quats)

def quaternion_to_vector(quats: np.ndarray):
    quats = quaternion.as_float_array(quats)
    vectors = quats[:, 1:4]
    return vectors
