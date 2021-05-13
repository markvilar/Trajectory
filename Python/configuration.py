import numpy as np
import quaternion as quat

from utilities import quat_from_axis_angle, vec3_to_quat

class OptimizationConfiguration:
    def __init__(self, threshold, bias, window: bool=False, \
        window_start: int=0, window_length: int=10):
        self.threshold = threshold
        self.bias = bias
        self.window = window
        self.window_start = window_start
        self.window_length = window_length

class SensorConfiguration:
    def __init__(self, translation: np.ndarray, orientation: np.ndarray):
        assert len(translation) == 3, "Length of translation must be 3."
        assert translation.ndim == 1, "Translation must be a 1-dim vector."
        assert len(orientation) == 3, "Length of orientation must be 3."
        assert orientation.ndim == 1, "Orientation must be a 1-dim vector."
        self.translation = translation
        self.orientation = orientation

    def get_translation_quat(self):
        t = vec3_to_quat(self.translation)
        return t

    def get_translation_quat_array(self, n: int):
        t = self.get_translation_quat()
        ts = np.tile(t, n)
        return ts

    def get_orientation_quat(self):
        q_x = quat_from_axis_angle( np.array([1.0, 0.0, 0.0]), \
            self.orientation[0])
        q_y = quat_from_axis_angle( np.array([0.0, 1.0, 0.0]), \
            self.orientation[1])
        q_z = quat_from_axis_angle( np.array([0.0, 0.0, 1.0]), \
            self.orientation[2])

        # Equation 3.1d
        q = q_x * q_y * q_z
        return q

    def get_orientation_quat_array(self, n: int):
        q = self.get_orientation_quat()
        qs = np.tile(q, n)
        return qs

class Configuration:
    def __init__(self, optim: OptimizationConfiguration, name: str, \
        slam_input_dir: str, output_dir: str, ground_truth_file: str, \
        keyframes_file: str, frames_file: str, map_file: str, \
        save_output: bool, show_figures: bool, save_figures: bool):

        # Optimization configuration.
        self.optim = optim

        # Generic.
        self.name = name

        # Directories.
        self.slam_input_dir = slam_input_dir
        self.output_dir = output_dir

        # Files.
        self.ground_truth_file = ground_truth_file
        self.keyframes_file = keyframes_file
        self.frames_file = frames_file
        self.map_file = map_file
        
        # Options.
        self.save_output = save_output
        self.show_figures = show_figures
        self.save_figures = save_figures
        
    def __repr__(self):
        return "Configuration()"

    def __str__(self):
        string = "Configuration: \n - SLAM: {0}".format(self.slam_input_dir) \
            + "\n - Navigation: {0}".format(self.navi_input_dir) \
            + "\n - Output: {0} \n".format(self.output_dir)
        return string
