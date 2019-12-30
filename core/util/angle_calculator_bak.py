from core.util.constant_bak import *
from core.util.util import *
from core.config.app_config import logger


class AngleCalculator:

    def __init__(self):
        self.angle_mode = ['2d', '3d'][0]

        self.idx = 1

        self.__initial_report_angles_with_none()
        self.__initial_report_angles_helper()

        self.__initial_report_distance_with_none()
        self.__initial_report_distance_helper()


        # self.__report_angle_helper = {'left_foot_edge_value': [None] * 4, 'right_foot_edge_value': [None] * 4}
        # left_foot_bottom_value, left_foot_forward_value, left_foot_rear_value
        # right_foot_bottom_value, right_foot_forward_value, right_foot_rear_value

        self.key_points_front = []
        self.key_points_left = []
        self.key_points_right = []





    def __initial_report_distance_with_none(self):
        self.report_distance = {}

        for name in distance_idx.keys():
            self.report_distance.update({name: None})

    def __initial_report_angles_with_none(self):
        self.report_angles = {}

        for name in report_angle_dict:
            self.report_angles.update({name: None})

    def __initial_report_angles_helper(self):
        self.report_angles_helper = {}
        for key, item in report_angle_dict.items():
            if item[1] in ["MAX", "MIN","TOP", "BOTTOM", "FORWARD", "REAR"]:
                self.report_angles_helper.update({key: [None, None]}) #left_value, right_value

    def __initial_report_distance_helper(self):
        self.__report_distance_helper = {}
        for key, value in distance_idx.items():
            if len(value) == 3:
                self.__report_distance_helper['{}_Min'.format(key)] = None
                self.__report_distance_helper['{}_Max'.format(key)] = None

    def __update_angle_tmp(self):
        key_points_front = self.key_points_front
        key_points_right = self.key_points_right
        key_points_left = self.key_points_left

        self.angles_tmp = {}

        for key, value in angles_tmp_idx.items():
            if key.endswith("left"):
                key_points_side = key_points_left
            elif key.endswith("right"):
                key_points_side = key_points_right
            else:
                key_points_side = None
                print("error, unknown angle name")

            if len(value) == 3:
                if self.angle_mode == '3d':
                    start_point_side_plane, joint_point_side_plane, end_point_side_plane = \
                        [key_points_side[idx][:2] for idx in value]

                    start_point_front_plane, joint_point_front_plane, end_point_front_plane = \
                        [key_points_front[idx][:2] for idx in value]

                    angle = angle_3d(start_point_front_plane, joint_point_front_plane, end_point_front_plane,
                                     start_point_side_plane, joint_point_side_plane, end_point_side_plane)
                elif self.angle_mode == '2d':
                    start_point_side_plane, joint_point_side_plane, end_point_side_plane = \
                        [key_points_side[idx][:2] for idx in value]
                    angle = angle_2d(start_point_side_plane, joint_point_side_plane, end_point_side_plane)
                else:
                    logger.error('unknown angle mode')
                    angle = None

            elif len(value) == 2:

                start_point, end_point = [key_points_side[idx][:2] for idx in value]

                angle = horizen_angle(start_point, end_point)

            else:
                angle = None
                logger.error("error, unknown angle len")

            self.angles_tmp.update({key: angle})

    def __update_report_distance(self):

        for key, value in distance_idx.items():

            frame = value[-2]
            mode = value[-1]
            if frame not in ['left', 'right', 'front']:
                logger.error('frame not valid')
                continue
            points = eval('self.key_points_{}'.format(frame))

            if mode not in ['h', 'v', 'd']:
                logger.error('mode not valid')
                continue

            if len(value) == 4:
                start_point = points[value[0]][:2]
                end_point = points[value[1]][:2]

                if mode == 'h':
                    distance = minus_with_none(start_point[0], end_point[0])
                elif mode == 'v':
                    distance = minus_with_none(start_point[1], end_point[1])
                elif mode == 'd':
                    distance = distance_2d(start_point, end_point)
                else:
                    logger.error("error, unknown distance mode")
                    distance = None

            elif len(value) == 3:
                point = points[value[0]][:2]

                if mode == 'h':
                    value = point[0]
                elif mode == 'v':
                    value = point[1]
                else:
                    logger.error("error, unknown distance mode for travel distance")
                    value = None

                self.__report_distance_helper["{}_Min".format(key)] = \
                    min_with_none(self.__report_distance_helper["{}_Min".format(key)], value)
                self.__report_distance_helper["{}_Max".format(key)] = \
                    max_with_none(self.__report_distance_helper["{}_Max".format(key)], value)
                distance = minus_with_none(self.__report_distance_helper["{}_Max".format(key)],
                                           self.__report_distance_helper["{}_Min".format(key)])

            else:
                logger.error("error, unknown distance parameter")
                distance = None

            self.report_distance.update({key: distance})

    def __update_report_angles(self):

        for key, item in report_angle_dict.items():
            idxs_left, idxs_right = item[0]
            points_left = [self.key_points_left[idx][:2] for idx in idxs_left]
            points_right = [self.key_points_right[idx][:2] for idx in idxs_left]

            if self.angle_mode == '3d':
                points_front = [self.key_points_front[idx][:2] for idx in idxs_left]
                tmp_angle_left = angle_3d(*points_front, *points_left)
                tmp_angle_right = angle_3d(*points_front, *points_right)

            elif self.angle_mode == '2d':
                tmp_angle_left = angle_2d(*points_left)
                tmp_angle_right = angle_2d(*points_right)
            else:
                logger.error('unknown angle mode')
                tmp_angle_left = None
                tmp_angle_right = None

            # if item[1] == "MAX":



    def __update_report_angles_with_none(self, key_points_left, key_points_right,
                                         angles_tmp, report_angles, index):
        # left angles
        report_angles["Ankle_Angle_Min_left"] = min_with_none(report_angles["Ankle_Angle_Min_left"],
                                                              angles_tmp["ankle_angle_left"])
        report_angles["Ankle_Angle_Max_left"] = max_with_none(report_angles["Ankle_Angle_Max_left"],
                                                              angles_tmp["ankle_angle_left"])
        report_angles["Ankle_Angle_Range_left"] = minus_with_none(report_angles["Ankle_Angle_Max_left"],
                                                                  report_angles["Ankle_Angle_Min_left"])

        if topper_than_with_none(key_points_left[19][1], self.__report_angle_helper['left_foot_edge_value'][0]):
            self.__report_angle_helper['left_foot_edge_value'][0] = key_points_left[19][1]
            report_angles["Ankle_Angle_Top_left"] = angles_tmp["ankle_angle_left"]

        if bottomer_than_with_none(key_points_left[19][1], self.__report_angle_helper['left_foot_edge_value'][1]):
            self.__report_angle_helper['left_foot_edge_value'][1] = key_points_left[19][1]
            report_angles["Ankle_Angle_Bottom_left"] = angles_tmp["ankle_angle_left"]

        if forwarder_than_with_none(key_points_left[19][0], self.__report_angle_helper['left_foot_edge_value'][2]):
            self.__report_angle_helper['left_foot_edge_value'][2] = key_points_left[19][0]
            report_angles["Ankle_Angle_Forward_left"] = angles_tmp["ankle_angle_left"]

        if rearer_than_with_none(key_points_left[19][0], self.__report_angle_helper['left_foot_edge_value'][3]):
            self.__report_angle_helper['left_foot_edge_value'][3] = key_points_left[19][0]
            report_angles["Ankle_Angle_Rear_left"] = angles_tmp["ankle_angle_left"]

        report_angles["Knee_Angle_Flexion_left"] = max_with_none(report_angles["Knee_Angle_Flexion_left"],
                                                                 angles_tmp["knee_angle_left"])
        report_angles["Knee_Angle_Extension_left"] = min_with_none(report_angles["Knee_Angle_Extension_left"],
                                                                   angles_tmp["knee_angle_left"])
        report_angles["Knee_Angle_Range_left"] = minus_with_none(report_angles["Knee_Angle_Flexion_left"],
                                                                 report_angles["Knee_Angle_Extension_left"])

        report_angles["Hip_Angle_Open_left"] = max_with_none(report_angles["Hip_Angle_Open_left"],
                                                             angles_tmp["hip_angle_left"])
        report_angles["Hip_Angle_Closed_left"] = min_with_none(report_angles["Hip_Angle_Closed_left"],
                                                               angles_tmp["hip_angle_left"])
        report_angles["Hip_Angle_Range_left"] = minus_with_none(report_angles["Hip_Angle_Open_left"],
                                                                report_angles["Hip_Angle_Closed_left"])

        report_angles["Back_From_Level_left"] = angles_tmp["back_from_level_left"]

        report_angles["Back_From_Level_Average_left"] = calculate_average(report_angles["Back_From_Level_Average_left"],
                                                                          angles_tmp["back_from_level_left"], index)

        report_angles["Forearm_From_Level_left"] = angles_tmp["forearm_from_level_left"]
        report_angles["Forearm_From_Level_Average_left"] = calculate_average(
            report_angles["Forearm_From_Level_Average_left"], angles_tmp["forearm_from_level_left"], index)

        report_angles["Foot_From_Level_left"] = angles_tmp["foot_from_level_left"]
        report_angles["Foot_From_Level_Average_left"] = calculate_average(report_angles["Foot_From_Level_Average_left"],
                                                                          angles_tmp["foot_from_level_left"], index)

        report_angles["Hip_Shoulder_Wrist_left"] = angles_tmp["hip_shoulder_wrist_angle_left"]
        report_angles["Hip_Shoulder_Wrist_Average_left"] = calculate_average(
            report_angles["Hip_Shoulder_Wrist_Average_left"], angles_tmp["hip_shoulder_wrist_angle_left"], index)

        report_angles["Hip_Shoulder_Elbow_left"] = angles_tmp["hip_shoulder_elbow_angle_left"]
        report_angles["Hip_Shoulder_Elbow_Average_left"] = calculate_average(
            report_angles["Hip_Shoulder_Elbow_Average_left"], angles_tmp["hip_shoulder_elbow_angle_left"], index)

        report_angles["Elbow_Angle_left"] = angles_tmp["elbow_angle_left"]
        report_angles["Elbow_Angle_Average_left"] = calculate_average(report_angles["Elbow_Angle_Average_left"],
                                                                      angles_tmp["elbow_angle_left"], index)

        # right angles

        report_angles["Ankle_Angle_Min_right"] = min_with_none(report_angles["Ankle_Angle_Min_right"],
                                                               angles_tmp["ankle_angle_right"])
        report_angles["Ankle_Angle_Max_right"] = max_with_none(report_angles["Ankle_Angle_Max_right"],
                                                               angles_tmp["ankle_angle_right"])
        report_angles["Ankle_Angle_Range_right"] = minus_with_none(report_angles["Ankle_Angle_Max_right"],
                                                                   report_angles["Ankle_Angle_Min_right"])

        if topper_than_with_none(key_points_right[22][1], self.__report_angle_helper['right_foot_edge_value'][0]):
            self.__report_angle_helper['right_foot_edge_value'][0] = key_points_right[22][1]
            report_angles["Ankle_Angle_Top_right"] = angles_tmp["ankle_angle_right"]

        if bottomer_than_with_none(key_points_right[22][1], self.__report_angle_helper['right_foot_edge_value'][1]):
            self.__report_angle_helper['right_foot_edge_value'][1] = key_points_right[22][1]
            report_angles["Ankle_Angle_Bottom_right"] = angles_tmp["ankle_angle_right"]

        if forwarder_than_with_none_right(key_points_right[22][0],
                                          self.__report_angle_helper['right_foot_edge_value'][2]):
            self.__report_angle_helper['right_foot_edge_value'][2] = key_points_right[22][0]
            report_angles["Ankle_Angle_Forward_right"] = angles_tmp["ankle_angle_right"]

        if rearer_than_with_none_right(key_points_right[22][0], self.__report_angle_helper['right_foot_edge_value'][3]):
            self.__report_angle_helper['right_foot_edge_value'][3] = key_points_right[22][0]
            report_angles["Ankle_Angle_Rear_right"] = angles_tmp["ankle_angle_right"]

        report_angles["Knee_Angle_Flexion_right"] = max_with_none(report_angles["Knee_Angle_Flexion_right"],
                                                                  angles_tmp["knee_angle_right"])
        report_angles["Knee_Angle_Extension_right"] = min_with_none(report_angles["Knee_Angle_Extension_right"],
                                                                    angles_tmp["knee_angle_right"])
        report_angles["Knee_Angle_Range_right"] = minus_with_none(report_angles["Knee_Angle_Flexion_right"],
                                                                  report_angles["Knee_Angle_Extension_right"])

        report_angles["Hip_Angle_Open_right"] = max_with_none(report_angles["Hip_Angle_Open_right"],
                                                              angles_tmp["hip_angle_right"])
        report_angles["Hip_Angle_Closed_right"] = min_with_none(report_angles["Hip_Angle_Closed_right"],
                                                                angles_tmp["hip_angle_right"])
        report_angles["Hip_Angle_Range_right"] = minus_with_none(report_angles["Hip_Angle_Open_right"],
                                                                 report_angles["Hip_Angle_Closed_right"])

        report_angles["Back_From_Level_right"] = angles_tmp["back_from_level_right"]
        report_angles["Back_From_Level_Average_right"] = calculate_average(
            report_angles["Back_From_Level_Average_right"], angles_tmp["back_from_level_right"], index)

        report_angles["Forearm_From_Level_right"] = angles_tmp["forearm_from_level_right"]
        report_angles["Forearm_From_Level_Average_right"] = calculate_average(
            report_angles["Forearm_From_Level_Average_right"], angles_tmp["forearm_from_level_right"], index)

        report_angles["Foot_From_Level_right"] = angles_tmp["foot_from_level_right"]
        report_angles["Foot_From_Level_Average_right"] = calculate_average(
            report_angles["Foot_From_Level_Average_right"], angles_tmp["foot_from_level_right"], index)

        report_angles["Hip_Shoulder_Wrist_right"] = angles_tmp["hip_shoulder_wrist_angle_right"]
        report_angles["Hip_Shoulder_Wrist_Average_right"] = calculate_average(
            report_angles["Hip_Shoulder_Wrist_Average_right"], angles_tmp["hip_shoulder_wrist_angle_right"], index)

        report_angles["Hip_Shoulder_Elbow_right"] = angles_tmp["hip_shoulder_elbow_angle_right"]
        report_angles["Hip_Shoulder_Elbow_Average_right"] = calculate_average(
            report_angles["Hip_Shoulder_Elbow_Average_right"], angles_tmp["hip_shoulder_elbow_angle_right"], index)

        report_angles["Elbow_Angle_right"] = angles_tmp["elbow_angle_right"]
        report_angles["Elbow_Angle_Average_right"] = calculate_average(report_angles["Elbow_Angle_Average_right"],
                                                                       angles_tmp["elbow_angle_right"], index)

    def update_every_frame(self, key_points_front, key_points_right, key_points_left):
        self.key_points_front = key_points_front
        self.key_points_left = key_points_left
        self.key_points_right = key_points_right


        self.__update_report_angles()

        # angle float set to 2 wei xiao shu
        for k, v in self.report_angles.items():
            if v is None:
                continue
            self.report_angles.update({k: round(float(v), 2)})

        self.__update_report_distance()
        for k, v in self.report_distance.items():
            if v is None:
                continue
            self.report_distance.update({k: round(float(v), 2)})

        self.idx += 1
