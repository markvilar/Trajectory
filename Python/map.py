import os.path

import msgpack
import numpy as np

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
    def __init__(self, keyframes, landmarks, landmark_positions):
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
        self.landmark_array = None

    def get_landmark_array(self):
        n = len(self.landmarks["pos_w"])
        landmarks = np.zeros((n, 3), dtype=float)
        
        for i, (id, point) in enumerate(landmark_data.items()):
            landmarks[i] = np.asarray(point["pos_w"])

        return landmarks

    def apply_SE3_transform(self, rotation, translation):
        raise NotImplementedError

    def save_landmarks_as_csv(self, path: str):
        raise NotImplementedError
