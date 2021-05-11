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
    b_t_c = vec3_to_quat(b_t_c)

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
    c_p_c = vec3_to_quat(c_p_c)
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
    w_t_b = np.array([ 1.0, 2.0, 3.0 ])
    w_t_b = vec3_to_quat(w_t_b)
    roll = 3
    pitch = -8
    yaw = 238

    q_roll = quat_from_axis_angle(np.array([ 1.0, 0.0, 0.0 ]), \
        roll * np.pi / 180.0)
    q_pitch = quat_from_axis_angle(np.array([ 0.0, 1.0, 0.0 ]), \
        pitch * np.pi / 180.0)
    q_yaw = quat_from_axis_angle(np.array([ 0.0, 0.0, 1.0 ]), \
        yaw * np.pi / 180.0)

    w_q_b = q_yaw * q_pitch * q_roll

    # Origin and unit vectors in body coordinate system.
    b_p_b = np.array([ 0.0, 0.0, 0.0 ])
    b_v_x = np.array([ 1.0, 0.0, 0.0 ])
    b_v_y = np.array([ 0.0, 1.0, 0.0 ])
    b_v_z = np.array([ 0.0, 0.0, 1.0 ])
    b_p_b = vec3_to_quat(b_p_b)
    b_v_x = vec3_to_quat(b_v_x)
    b_v_y = vec3_to_quat(b_v_y)
    b_v_z = vec3_to_quat(b_v_z)

    # -------------------------------------------------------------------------
    # ---- World ---------------------------------------------------------------
    # -------------------------------------------------------------------------

    # Translate and rotate - Body.
    w_p_b = b_p_b + w_t_b
    w_v_x = w_q_b * b_v_x * w_q_b.conjugate()
    w_v_y = w_q_b * b_v_y * w_q_b.conjugate()
    w_v_z = w_q_b * b_v_z * w_q_b.conjugate()

    # Translate and rotate - Camera.
    w_p_c = w_t_b + w_q_b * b_p_c * w_q_b.conjugate()
    w_u_x = w_q_b * b_u_x * w_q_b.conjugate()
    w_u_y = w_q_b * b_u_y * w_q_b.conjugate()
    w_u_z = w_q_b * b_u_z * w_q_b.conjugate()

    # Origin and unit vectors in world coordinate system.
    w_p_w = np.array([ 0.0, 0.0, 0.0 ])
    w_w_x = np.array([ 1.0, 0.0, 0.0 ])
    w_w_y = np.array([ 0.0, 1.0, 0.0 ])
    w_w_z = np.array([ 0.0, 0.0, 1.0 ])

    # Convert to vectors - body.
    w_p_b = quat_to_vec3(w_p_b)
    w_v_x = quat_to_vec3(w_v_x)
    w_v_y = quat_to_vec3(w_v_y)
    w_v_z = quat_to_vec3(w_v_z)

    # Convert to vectors - camera.
    w_p_c = quat_to_vec3(w_p_c)
    w_u_x = quat_to_vec3(w_u_x)
    w_u_y = quat_to_vec3(w_u_y)
    w_u_z = quat_to_vec3(w_u_z)

    # Rotation printout.
    w_q_c = w_q_b * b_q_c
    c_q_b = b_q_c.conjugate()

    b_q_w = w_q_b.conjugate()
    test = b_q_w * w_q_c

    print("Camera to body:  {0}".format( \
        quat.as_euler_angles(b_q_c) * 180 / np.pi))
    print("Body to world:   {0}".format( \
        quat.as_euler_angles(w_q_b) * 180 / np.pi))
    print("Camera to world: {0}".format( \
        quat.as_euler_angles(w_q_c) * 180 / np.pi))
    print("Test:            {0}".format( \
        quat.as_euler_angles(test) * 180 / np.pi))

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1 = fig1.add_subplot(111, projection='3d')

    # World
    ax1.quiver(w_p_w[0], w_p_w[1], w_p_w[2], w_w_x[0], w_w_x[1], w_w_x[2], \
        color="r")
    ax1.quiver(w_p_w[0], w_p_w[1], w_p_w[2], w_w_y[0], w_w_y[1], w_w_y[2], \
        color="g")
    ax1.quiver(w_p_w[0], w_p_w[1], w_p_w[2], w_w_z[0], w_w_z[1], w_w_z[2], \
        color="b")

    # Body
    ax1.quiver(w_p_b[0], w_p_b[1], w_p_b[2], w_v_x[0], w_v_x[1], w_v_x[2], \
        color="r")
    ax1.quiver(w_p_b[0], w_p_b[1], w_p_b[2], w_v_y[0], w_v_y[1], w_v_y[2], \
        color="g")
    ax1.quiver(w_p_b[0], w_p_b[1], w_p_b[2], w_v_z[0], w_v_z[1], w_v_z[2], \
        color="b")

    # Camera
    ax1.quiver(w_p_c[0], w_p_c[1], w_p_c[2], w_u_x[0], w_u_x[1], w_u_x[2], \
        color="r")
    ax1.quiver(w_p_c[0], w_p_c[1], w_p_c[2], w_u_y[0], w_u_y[1], w_u_y[2], \
        color="g")
    ax1.quiver(w_p_c[0], w_p_c[1], w_p_c[2], w_u_z[0], w_u_z[1], w_u_z[2], \
        color="b")

    ax1.set_xlabel(r"$x_{w}$")
    ax1.set_ylabel(r"$y_{w}$")
    ax1.set_zlabel(r"$z_{w}$")
    ax1.set_title(r"World frame")
    ax1.set_xlim([ -10, 10 ])
    ax1.set_ylim([ -10, 10 ])
    ax1.set_zlim([ -10, 10 ])

    plt.show()

if __name__ == "__main__":
    main()
