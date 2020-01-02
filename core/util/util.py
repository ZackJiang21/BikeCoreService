import math
import numpy as np

def common_elements(list1, list2):
    return [element for element in list1 if element in list2]

def distance_2d(start_point, end_point):
    assert len(start_point) == len(end_point) == 2
    if (None,None) in [start_point, end_point]:
        return None
    distance = math.sqrt((start_point[0] - end_point[0]) ** 2 + (start_point[1] - end_point[1]) ** 2)

    return distance


def distance_3d(start_point_plane1, end_point_plane1, start_point_plane2, end_point_plane2):
    assert len(start_point_plane1) == len(end_point_plane1) == len(start_point_plane2) == len(end_point_plane2) == 2
    if (None,None) in [start_point_plane1, end_point_plane1, start_point_plane2, end_point_plane2]:
        return None

    distance_plane1 = distance_2d(start_point_plane1, end_point_plane1)

    distance_plane2 = distance_2d(start_point_plane2, end_point_plane2)

    return math.sqrt(distance_plane1 ** 2 + distance_plane2 ** 2)


def angle_3d(start_point_front_plane, joint_point_front_plane, end_point_front_plane,
             start_point_side_plane, joint_point_side_plane, end_point_side_plane):
    assert len(start_point_front_plane) \
           == len(joint_point_front_plane) \
           == len(end_point_front_plane) \
           == len(start_point_side_plane) \
           == len(joint_point_side_plane) \
           == len(end_point_side_plane) \
           == 2

    # if any point is not detected, no need to calculate, return None
    if (None,None) in [start_point_front_plane, joint_point_front_plane, end_point_front_plane,
             start_point_side_plane, joint_point_side_plane, end_point_side_plane]:
        return None

    a_3d = distance_3d(joint_point_front_plane, start_point_front_plane, joint_point_side_plane, start_point_side_plane)
    b_3d = distance_3d(joint_point_front_plane, end_point_front_plane, joint_point_side_plane, end_point_side_plane)
    c_3d = distance_3d(start_point_front_plane, end_point_front_plane, start_point_side_plane, end_point_side_plane)

    return angle_use_side(a_3d, b_3d, c_3d)


def angle_2d(start_point, joint_point, end_point):
    assert len(start_point) == len(end_point) == 2

    # if any point is not detected, no need to calculate, return None
    if (None,None) in [start_point, joint_point, end_point]:
        return None

    a = distance_2d(start_point, joint_point)

    b = distance_2d(end_point, joint_point)

    c = distance_2d(start_point, end_point)

    return angle_use_side(a, b, c)


def horizen_angle(start_point, end_point):
    assert len(start_point) == len(end_point) == 2

    # if any point is not detected, no need to calculate, return None
    if (None,None)in [start_point, end_point]:
        return None

    a = distance_2d(start_point, end_point)

    b = abs(start_point[0] - end_point[0])

    c = abs(start_point[1] - end_point[1])

    return angle_use_side(a, b, c)


def vertical_angle(start_point, end_point):
    return 90 - horizen_angle(start_point, end_point)


def angle_use_side(a, b, c):

    # not a triangle
    if not (a + b >= c and a - b <= c):
        return None

    # only two points
    if 0 in [a,b]:
        return None

    return np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)) * (180 / 3.141592653)

def calculate_average(last_average, current, index):
    if current is None:
        return last_average
    return div_with_none(plus_with_none(mul_with_none(last_average, index - 1), current), index)

def max_with_none(a,b):
    if a is None:
        return b
    if b is None:
        return a
    return max(a,b)

def min_with_none(a,b):
    if a is None:
        return b
    if b is None:
        return a
    return min(a,b)

def minus_with_none(a,b):
    if None in (a, b):
        return None
    return a - b

def plus_with_none(a,b):
    if a is None:
        return b
    if b is None:
        return a
    return a + b

def mul_with_none(a,b):
    if None in (a, b):
        return None
    return a * b

def mod_with_none(a,b):
    if None in (a, b):
        return None
    return a // b

def div_with_none(a,b):
    if None in (a, b):
        return None
    return a / b

def less_than_with_none(a,b):
    if a is None:
        return True
    if b is None:
        return False
    return a < b

def bigger_than_with_none(a,b):
    return less_than_with_none(b,a)

def topper_than_with_none(a,b):
    if a is None:
        return False
    if b is None:
        return True
    return a < b

def bottomer_than_with_none(a,b):
    if a is None:
        return False
    if b is None:
        return True
    return a > b

def forwarder_than_with_none(a,b):
    if a is None:
        return False
    if b is None:
        return True
    return a < b

def rearer_than_with_none(a,b):
    if a is None:
        return False
    if b is None:
        return True
    return a > b

def forwarder_than_with_none_right(a,b):
    if a is None:
        return False
    if b is None:
        return True
    return a > b

def rearer_than_with_none_right(a,b):
    if a is None:
        return False
    if b is None:
        return True
    return a < b