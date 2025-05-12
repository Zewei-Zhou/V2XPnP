


"""
Transformation utils
"""

import numpy as np


def x_to_world(pose, degree_flag=True):
    """
    The transformation matrix from x-coordinate system to carla world system

    Parameters
    ----------
    pose : list
        [x, y, z, roll, yaw, pitch]
    degree_flag : bool
        degree or radian for roll, yaw and pitch

    Returns
    -------
    matrix : np.ndarray
        The transformation matrix.
    """
    x, y, z, roll, yaw, pitch = pose[:]

    # unit change
    if degree_flag:
        yaw = np.radians(yaw)
        roll = np.radians(roll)
        pitch = np.radians(pitch)

    # used for rotation matrix
    c_y = np.cos(yaw)
    s_y = np.sin(yaw)
    c_r = np.cos(roll)
    s_r = np.sin(roll)
    c_p = np.cos(pitch)
    s_p = np.sin(pitch)

    matrix = np.identity(4)
    # translation matrix
    matrix[0, 3] = x
    matrix[1, 3] = y
    matrix[2, 3] = z

    # rotation matrix
    matrix[0, 0] = c_p * c_y
    matrix[0, 1] = c_y * s_p * s_r - s_y * c_r
    matrix[0, 2] = -c_y * s_p * c_r - s_y * s_r
    matrix[1, 0] = s_y * c_p
    matrix[1, 1] = s_y * s_p * s_r + c_y * c_r
    matrix[1, 2] = -s_y * s_p * c_r + c_y * s_r
    matrix[2, 0] = s_p
    matrix[2, 1] = -c_p * s_r
    matrix[2, 2] = c_p * c_r

    return matrix


def x1_to_x2(x1, x2, degree_flag=True):
    """
    Transformation matrix from x1 to x2.

    Parameters
    ----------
    x1 : list
        The pose of x1 under world coordinates.
    x2 : list
        The pose of x2 under world coordinates.
    degree_flag : bool

    Returns
    -------
    transformation_matrix : np.ndarray
        The transformation matrix.

    """
    x1_to_world = x_to_world(x1, degree_flag)
    world_to_x2 = world_to_x(x2, degree_flag)

    transformation_matrix = np.dot(world_to_x2, x1_to_world)
    return transformation_matrix


def world_to_x(pose, degree_flag=True):
    """
    Transformation matrix from world system to x-coordinate system.

    Parameters
    ----------
    pose : list
        [x, y, z, roll, yaw, pitch]
    degree_flag : bool

    Returns
    -------
    matrix : np.ndarray
        The transformation matrix.
    """

    transformation_matrix = \
        np.linalg.inv(x_to_world(pose, degree_flag))
    return transformation_matrix


def dist_to_continuous(p_dist, displacement_dist, res, downsample_rate):
    """
    Convert points discretized format to continuous space for BEV representation.
    Parameters
    ----------
    p_dist : numpy.array
        Points in discretized coorindates.

    displacement_dist : numpy.array
        Discretized coordinates of bottom left origin.

    res : float
        Discretization resolution.

    downsample_rate : int
        Dowmsamping rate.

    Returns
    -------
    p_continuous : numpy.array
        Points in continuous coorindates.

    """
    p_dist = np.copy(p_dist)
    p_dist = p_dist + displacement_dist
    p_continuous = p_dist * res * downsample_rate
    return p_continuous
