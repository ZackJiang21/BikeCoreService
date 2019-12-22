import math
import numpy as np

def distance_2d(start_point, end_point):
    assert type(start_point) == type(end_point) == tuple
    assert len(start_point) == len(end_point) == 2

    distance = math.sqrt((start_point[0] - end_point[0]) ** 2 + (start_point[1] - end_point[1]) ** 2)

    return distance


def distance_3d(start_point_plane1, end_point_plane1, start_point_plane2, end_point_plane2):
    assert type(start_point_plane1) == type(end_point_plane1) == type(start_point_plane2) == type(
        end_point_plane2) == tuple
    assert len(start_point_plane1) == len(end_point_plane1) == len(start_point_plane2) == len(end_point_plane2) == 2

    distance_plane1 = distance_2d(start_point_plane1, end_point_plane1)

    distance_plane2 = distance_2d(start_point_plane2, end_point_plane2)

    return math.sqrt(distance_plane1 ** 2 + distance_plane2 ** 2)


def angle_3d(start_point_front_plane, joint_point_front_plane, end_point_front_plane,
             start_point_side_plane, joint_point_side_plane, end_point_side_plane):
    assert type(start_point_front_plane) \
           == type(joint_point_front_plane) \
           == type(end_point_front_plane) \
           == type(start_point_side_plane) \
           == type(joint_point_side_plane) \
           == type(end_point_side_plane) \
           == tuple

    assert len(start_point_front_plane) \
           == len(joint_point_front_plane) \
           == len(end_point_front_plane) \
           == len(start_point_side_plane) \
           == len(joint_point_side_plane) \
           == len(end_point_side_plane) \
           == 2

    a_3d = distance_3d(joint_point_front_plane, start_point_front_plane, joint_point_side_plane, start_point_side_plane)
    b_3d = distance_3d(joint_point_front_plane, end_point_front_plane, joint_point_side_plane, end_point_side_plane)
    c_3d = distance_3d(start_point_front_plane, end_point_front_plane, start_point_side_plane, end_point_side_plane)

    return angle_use_side(a_3d, b_3d, c_3d)


def angle_2d(start_point, joint_point, end_point):
    assert type(start_point) == type(end_point) == tuple
    assert len(start_point) == len(end_point) == 2

    a = distance_2d(start_point, joint_point)

    b = distance_2d(end_point, joint_point)

    c = distance_2d(start_point, end_point)

    return angle_use_side(a, b, c)


def horizen_angle(start_point, end_point):
    assert type(start_point) == type(end_point) == tuple
    assert len(start_point) == len(end_point) == 2

    a = distance_2d(start_point, end_point)

    b = abs(start_point[0] - end_point[0])

    c = abs(start_point[1] - end_point[1])

    return angle_use_side(a, b, c)


def vertical_angle(start_point, end_point):
    return 90 - horizen_angle(start_point, end_point)


def angle_use_side(a, b, c):
    assert 0 not in [a, b, c]

    angle = np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)) * (180 / 3.141592653)

    return angle


