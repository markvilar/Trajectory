import os.path

import msgpack
import numpy as np
import pandas as pd
import quaternion as quat

from utilities import vec3_array_to_quat_array, quat_array_to_vec3_array, \
    vec4_array_to_quat_array, quat_array_to_vec4_array

class DataSeries:
    def __init__(self, timestamps, series):
        self.timestamps = timestamps
        self.series = series

    def __getitem__(self, key):
        return self.series[key]

def read_msgpack(path: str):
    assert os.path.isfile(path), \
        "Msgpack file does not exist."
    assert os.path.splitext(path)[-1] == ".msg", \
        "Msgpack file does not end with \".msg\"."
    return MapUnpacker(path)


class MapUnpacker:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "rb") as f:
            data = msgpack.unpackb(f.read(), use_list=False, raw=False)
            keyframes = data["keyframes"]
            landmarks = data["landmarks"]
            return Map(keyframes, landmarks)


class Map:
    def __init__(self, keyframes, landmarks):
        """
        Keyframe keys
        -------------
            depths, descs, keypts, lm_ids, undists, x_rights
            loop_edges
            n_keypts
            n_scale_levels, scale_factor
            span_children, span_parent
            rot_cw, trans_cw
            src_frm_id 
            ts

        Landmark keys
        -------------
            1st_keyfrm, n_fnd, n_vis, pos_w, ref_keyfrm
        """

        self.keyframes = keyframes
        self.landmarks = landmarks

    def get_landmarks(self):
        m = len(self.landmarks.items())
        landmarks = np.zeros((m, 3), dtype=float)
        
        for i, (id, point) in enumerate(self.landmarks.items()):
            landmarks[i] = np.asarray(point["pos_w"])

        return Landmarks(landmarks)

class Landmarks():
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def __getitem__(self, key):
        return self.landmarks[key]
    
    def apply_SE3_transform(self, rotation, translation):
        m = len(self.landmarks)
        q = np.tile(rotation, m)
        l = vec3_array_to_quat_array(self.landmarks)

        l = q * l * q.conjugate()

        l = quat_array_to_vec3_array(l)

        self.landmarks = l + translation

    def save_as_csv(self, path: str):
        table = pd.DataFrame(self.landmarks, columns=["PositionX", \
            "PositionY", "PositionZ"])
        table.to_csv(path)

class Trajectory():
    def __init__(self, timestamps: np.ndarray, positions: np.ndarray, \
        attitudes: np.ndarray):
        """
        """
        self.timestamps = timestamps
        self.positions = positions
        self.attitudes = attitudes

    def __getitem__(self, key):
        return self.positions[key]

    def add_time_bias(self, bias: float):
        self.timestamps += bias

    def get_windowed_trajectory(self, start: int, length: int):
        assert start >= 0, "Trajectory window start must be positive."
        assert length >= 1, "Trajectory window length must be larger than 1."
        assert len(self.timestamps) > start + length, \
            "Trajectory window out of bounds."

        window = Trajectory( self.timestamps[start:start+length], \
            self.positions[start:start+length], \
            self.attitudes[start:start+length] )

        return window

    def apply_SE3_transform(self, rotation: np.ndarray, \
        translation: np.ndarray):
        """
        Applies a SE3 transform (rotate and translate) to the trajectory
        positions and attitudes.
        """
        q = np.tile(rotation, len(self.timestamps))
        p = vec3_array_to_quat_array(self.positions)
        a = vec4_array_to_quat_array(self.attitudes)

        p = q * p * q.conjugate()
        a = q * a

        p = quat_array_to_vec3_array(p)
        a = quat_array_to_vec4_array(a)

        self.positions = p + translation
        self.attitudes = a

    def save_as_csv(self, path: str):
        """
        Saves the trajectory to file.
        """
        # Create pandas data frame.
        table = np.hstack(( self.timestamps[:, np.newaxis], self.positions, \
            self.attitudes ))
        table = pd.DataFrame(table, columns=["Timestamp", "PositionX", \
            "PositionY", "PositionZ", "QuaternionReal", \
            "QuaternionImaginary1", "QuaternionImaginary2", \
            "QuaternionImaginary3", ])
        
        # Save.
        table.to_csv(path)

    def save_as_txt(self, path: str):
        with open(path, "w") as file:
            for i in range(len(self.timestamps)):
                file.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format( \
                    self.timestamps[i], self.positions[i, 0], \
                    self.positions[i, 1], self.positions[i, 2], \
                    self.attitudes[i, 0], self.attitudes[i, 1], \
                    self.attitudes[i, 2], self.attitudes[i, 3] ))
