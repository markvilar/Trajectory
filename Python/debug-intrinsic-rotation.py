import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import quaternion as quat

from utilities import quat_from_axis_angle, vec3_to_quat, quat_to_vec3

def main():

    # -------------------------------------------------------------------------
    # ---- Camera -------------------------------------------------------------
    # -------------------------------------------------------------------------
    
    # Rotations.
    alpha_x = 0.0
    alpha_y = 90.0 - 48.0
    alpha_z = 90.0

    # Translation.
    b_t_c = np.array([ 2.0, 0.21, 1.40 ])

    q_x = quat_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
        alpha_x  * np.pi / 180.0)
    q_y = quat_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
        alpha_y  * np.pi / 180.0)
    q_z = quat_from_axis_angle(np.array([ 0.0, 0.0, 1.0 ]), \
        alpha_z * np.pi / 180.0)

    b_q_c = q_x * q_y * q_z

    # Origin and unit vectors in camera coordinate system.
    c_p_c = np.array([ 0.0, 0.0, 0.0 ])
    c_u_x = np.array([ 1.0, 0.0, 0.0 ])
    c_u_y = np.array([ 0.0, 1.0, 0.0 ])
    c_u_z = np.array([ 0.0, 0.0, 1.0 ])
    c_u_x = vec3_to_quat(c_u_x)
    c_u_y = vec3_to_quat(c_u_y)
    c_u_z = vec3_to_quat(c_u_z)

    # Translate and rotate from camera to body.
    b_p_c = c_p_c + b_t_c
    b_u_x = b_q_c * c_u_x * b_q_c.conjugate()
    b_u_y = b_q_c * c_u_y * b_q_c.conjugate()
    b_u_z = b_q_c * c_u_z * b_q_c.conjugate()

    # -------------------------------------------------------------------------
    # ---- Body ---------------------------------------------------------------
    # -------------------------------------------------------------------------
    
    # Body frame orientation.
    b_t = np.array([ 1.0, 2.0, 3.0 ])
    roll = 20
    pitch = 30
    yaw = 145

    q_roll = quat_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
        roll * np.pi / 180.0)
    q_pitch = quat_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
        pitch * np.pi / 180.0)
    q_yaw = quat_from_axis_angle(np.array([ 0.0, 0.0, 1.0 ]), \
        yaw * np.pi / 180.0)

    w_q_b = q_roll * q_pitch * q_yaw

    # Origin and unit vectors in camera coordinate system.
    b_origin = np.array([ 0.0, 0.0, 0.0 ])
    b_v_x = np.array([ 1.0, 0.0, 0.0 ])
    b_v_y = np.array([ 0.0, 1.0, 0.0 ])
    b_v_z = np.array([ 0.0, 0.0, 1.0 ])

    """
    b_origin = vec3_to_quat(c_p)
    b_u_x = vec3_to_quat(c_u_x)
    b_u_y = vec3_to_quat(c_u_y)
    b_u_z = vec3_to_quat(c_u_z)
    """
    b_u_x = quat_to_vec3(b_u_x)
    b_u_y = quat_to_vec3(b_u_y)
    b_u_z = quat_to_vec3(b_u_z)

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1 = fig1.add_subplot(111, projection='3d')

    ax1.quiver(b_o_b[0], b_o_b[1], b_o_b[2], b_v_x[0], b_v_x[1], b_v_x[2], \
        color="r")
    ax1.quiver(b_o_b[0], b_o_b[1], b_o_b[2], b_v_y[0], b_v_y[1], b_v_y[2], \
        color="g")
    ax1.quiver(b_o_b[0], b_o_b[1], b_o_b[2], b_v_z[0], b_v_z[1], b_v_z[2], \
        color="b")

    ax1.quiver(b_p_c[0], b_p_c[1], b_p_c[2], b_u_x[0], b_u_x[1], b_u_x[2], \
        color="r")
    ax1.quiver(b_p_c[0], b_p_c[1], b_p_c[2], b_u_y[0], b_u_y[1], b_u_z[2], \
        color="g")
    ax1.quiver(b_p_c[0], b_p_c[1], b_p_c[2], b_u_z[0], b_u_z[1], b_u_z[2], \
        color="b")

    ax1.set_xlabel(r"$x_{b}$")
    ax1.set_ylabel(r"$y_{b}$")
    ax1.set_zlabel(r"$z_{b}$")
    ax1.set_title(r"Body frame")
    ax1.set_xlim([-5, 5])
    ax1.set_ylim([-5, 5])
    ax1.set_zlim([-5, 5])

    plt.show()

if __name__ == "__main__":
    main()
