import sys 

from typing import Dict, List

import numpy as np
import pandas as pd
import quaternion as quat

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


# ------------------------------------------------------------------------------
# ---- Quaternions. ------------------------------------------------------------
# ------------------------------------------------------------------------------

# Axis-angle.

def quat_from_axis_angle(axis: np.ndarray, angle: float):
    assert axis.shape == (3,), "The axis vector must be (3,)."
    assert np.linalg.norm(axis) == 1.0, "The axis vector must have norm 1."
    real = np.cos(angle/2)
    imaginary = np.sin(angle/2) * axis
    return quat.quaternion(real, imaginary[0], imaginary[1], imaginary[2])

# Vector 3.

def vec3_to_quat(vec: np.ndarray):
    assert vec.shape == (3,), "Vector must be (3,)."
    return quat.quaternion(0.0, vec[0], vec[1], vec[2])

def quat_to_vec3(q: np.ndarray):
    assert type(q) == quat.quaternion, "Invalid type."
    v = quat.as_float_array(q)
    return v[1:]

def vec3_array_to_quat_array(vecs: np.ndarray):
    assert vecs.ndim == 2, "Invalid vectors dimension."
    assert vecs.shape[1] == 3, "Invalid vectors length."
    vs = np.zeros((len(vecs), 4))
    vs[:, 1:] = vecs
    return quat.as_quat_array(vs)

def quat_array_to_vec3_array(qs: np.ndarray):
    vs = quat.as_float_array(qs)
    return vs[:, 1:]

# Vector 4.

def vec4_to_quat(vec: np.ndarray):
    assert vec.shape == (4,), "Vector must be (4,)."
    return quat.quaternion(vec[0], vec[1], vec[2], vec[3])

def quat_to_vec4(q: np.ndarray):
    assert type(q) == quat.quaternion, "Invalid type."
    return quat.as_float_array(q)

def vec4_array_to_quat_array(vecs: np.ndarray):
    assert vecs.ndim == 2, "Invalid vectors dimension."
    assert vecs.shape[1] == 4, "Invalid vectors length."
    return quat.as_quat_array(vecs)

def quat_array_to_vec4_array(qs: np.ndarray):
    return quat.as_float_array(qs)
