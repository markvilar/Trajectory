import numpy as np
import quaternion as quat

from utilities import vector_to_quaternion, quaternion_to_vector

class Trajectory():
    def __init__(self, timestamps: np.ndarray, positions: np.ndarray, \
        attitudes: np.ndarray):
        """
        """
        self.timestamps = timestamps
        self.positions = positions
        self.attitudes = attitudes

    def apply_SIM3_transform(self, scale: float, rotation: np.ndarray, \
        translation: np.ndarray):
        """
        Applies a SIM3 transform (scale, rotate, and translate) to the 
        trajectory positions and attitudes.
        """
        self.apply_SE3_transform(scale * rotation, translaiton)

    def apply_SE3_transform(self, rotation: np.ndarray, \
        translation: np.ndarray):
        """
        Applies a SE3 transform (rotate and translate) to the trajectory
        positions and attitudes.
        """
        q = np.tile(quat.from_rotation_matrix(rotation), len(self.timestamps))
        p = vector_to_quaternion(self.positions)
        a = quat.as_quat_array(self.attitudes)

        p = q * p * q.conjugate()
        a = q * a

        p = quaternion_to_vector(p)
        a = quat.as_float_array(a)

        self.positions = p + translation
        self.attitudes = a

    def save_to_file(self, path: str):
        """
        Saves the trajectory to file.
        """
        with open(path, "w") as file:
            for i in range(len(self.timestamps)):
                file.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format( \
                    self.timestamps[i], self.positions[i, 0], \
                    self.positions[i, 1], self.positions[i, 2], \
                    self.attitudes[i, 0], self.attitudes[i, 1], \
                    self.attitudes[i, 2], self.attitudes[i, 3] ))
