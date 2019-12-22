from core.util.util import *
from core.util.angle_util import *


class AngleCalculator:

    def __init__(self):
        self.angles_tmp = {}
        self.report_angles = initial_report_angles()

        self.key_points_front_pre = []
        self.key_points_left_pre = []
        self.key_points_right_pre = []

        self.key_points_front = []
        self.key_points_left = []
        self.key_points_right = []

    def __update_angle_tmp(self):
        key_points_front = self.key_points_front
        key_points_right = self.key_points_right
        key_points_left = self.key_points_left

        self.angles_tmp = {}

        for key, value in angles_idx.items():

            if key.endswith("left"):
                key_points_side = key_points_left
            elif key.endswith("right"):
                key_points_side = key_points_right
            else:
                key_points_side = None
                print("error, unknown angle name")

            if len(value) == 3:

                start_point_side_plane, joint_point_side_plane, end_point_side_plane = [key_points_side[idx][:2] for idx
                                                                                        in
                                                                                        value]

                start_point_front_plane, joint_point_front_plane, end_point_front_plane = [key_points_front[idx][:2] for
                                                                                           idx
                                                                                           in value]

                angle = angle_3d(start_point_front_plane, joint_point_front_plane, end_point_front_plane,
                                 start_point_side_plane, joint_point_side_plane, end_point_side_plane)

            elif len(value) == 2:

                start_point, end_point = [key_points_side[idx][:2] for idx in value]

                angle = horizen_angle(start_point, end_point)

            else:
                angle = None
                print("error, unknown angle len")

            self.angles_tmp.update({key: angle})

    def __update_report_angles_use_angles_tmp(self):
        update_report_angles(self.key_points_left, self.key_points_left_pre,
                             self.key_points_right, self.key_points_right_pre,
                             self.angles_tmp, self.report_angles)

    def update_every_frame(self, key_points_front, key_points_right, key_points_left):
        self.key_points_front = key_points_front
        self.key_points_left = key_points_left
        self.key_points_right = key_points_right

        self.__update_angle_tmp()
        self.__update_report_angles_use_angles_tmp()

        self.key_points_front_pre = key_points_front
        self.key_points_left_pre = key_points_left
        self.key_points_right_pre = key_points_right
