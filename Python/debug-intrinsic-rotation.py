import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use("./Styles/Scientific.mplstyle")

import numpy as np
import quaternion as quat

from utilities import quat_from_axis_angle, vec3_to_quat, quat_to_vec3

def main():
    alpha_x = 0.0
    alpha_y = 90.0 - 48.0
    alpha_z = 90.0

    q_x = quat_from_axis_angle(np.array([ 1.0, 0.0, 0.0]), \
        alpha_x  * np.pi / 180.0)
    q_y = quat_from_axis_angle(np.array([ 0.0, 1.0, 0.0]), \
        alpha_y  * np.pi / 180.0)
    q_z = quat_from_axis_angle(np.array([ 0.0, 0.0, 1.0]), \
        alpha_z * np.pi / 180.0)

    q_bc = q_x * q_y * q_z

    #q_bc = q_cb.conjugate() / ( np.norm(q_cb) * np.norm(q_cb) )

    # Point in camera coordinate system.
    p_c = np.array([ 1.0, 2.0, 3.0 ])
    v_cx = np.array([ 1.0, 0.0, 0.0 ])
    v_cy = np.array([ 0.0, 1.0, 0.0 ])
    v_cz = np.array([ 0.0, 0.0, 1.0 ])

    # Camera coordinate system unit vectors.
    v_cx = vec3_to_quat(v_cx)
    v_cy = vec3_to_quat(v_cy)
    v_cz = vec3_to_quat(v_cz)
    p_c = vec3_to_quat(p_c)

    # Rotate from camera to body.
    v_bx = q_bc * v_cx * q_bc.conjugate()
    v_by = q_bc * v_cy * q_bc.conjugate()
    v_bz = q_bc * v_cz * q_bc.conjugate()
    p_b = q_bc * p_c * q_bc.conjugate()

    # Extract vectors.
    v_bx = quat_to_vec3(v_bx)
    v_by = quat_to_vec3(v_by)
    v_bz = quat_to_vec3(v_bz)
    p_b = quat_to_vec3(p_b)

    print("Unit vector x: {0}".format(v_bx))
    print("Unit vector y: {0}".format(v_by))
    print("Unit vector z: {0}".format(v_bz))
    print("Point:         {0}".format(p_b))

    fig1, ax1 = plt.subplots(figsize=(8, 8))
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.quiver(0, 0, 0, 1, 0, 0, color="y", label="Body")
    ax1.quiver(0, 0, 0, 0, 1, 0, color="y")
    ax1.quiver(0, 0, 0, 0, 0, 1, color="y")
    ax1.quiver(0, 0, 0, v_bx[0], v_bx[1], v_bx[2], color="r", label=r"$x_{c}$")
    ax1.quiver(0, 0, 0, v_by[0], v_by[1], v_by[2], color="g", label=r"$y_{c}$")
    ax1.quiver(0, 0, 0, v_bz[0], v_bz[1], v_bz[2], color="b", label=r"$z_{c}$")
    ax1.scatter(p_b[0], p_b[1], p_b[2], label="Point")
    ax1.set_xlabel(r"$x_{b}$")
    ax1.set_ylabel(r"$y_{b}$")
    ax1.set_zlabel(r"$z_{b}$")
    ax1.set_title(r"Body frame")
    ax1.set_xlim([-5, 5])
    ax1.set_ylim([-5, 5])
    ax1.set_zlim([-5, 5])
    ax1.legend()

    plt.show()
if __name__ == "__main__":
    main()
