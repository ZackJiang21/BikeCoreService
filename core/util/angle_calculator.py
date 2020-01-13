from core.config.constant import *
from core.util.util import *
from core.config.app_config import logger
import time
import cv2

class AngleCalculator:

    def __init__(self, width, height):
        t1 = time.time()
        self.angle_mode = ['2d', '3d'][0]

        self.idx = 1

        self.is_last_frame = False # only last frame we calculate range

        self.__initial_report_angles_with_none()
        self.__initial_report_angles_helper()

        self.__initial_report_distance_with_none()
        self.__initial_report_distance_helper()

        self.key_points_front = []
        self.key_points_left = []
        self.key_points_right = []

        # marker if not initialized
        self.knee_path_pic_color = (81, 62, 45) # BGR
        self.knee_path_pic = None
        self.left_knee_path_start_point = None
        self.right_knee_path_start_point = None
        self.knee_path_pic_crop_ratio = 2 # means final pic should be 1/ratio times of original from center
        self.frame_shape = (width, height, 3)

        print("*" * 50)
        print("Calculator initial time: {}".format(time.time() - t1))
        print("*" * 50)

        self.zero_time = t1

    def __initial_report_distance_with_none(self):
        self.report_distance = {}

        for name in distance_idx.keys():
            self.report_distance.update({name: None})

    def __initial_report_angles_with_none(self):
        self.report_angles = report_angle_dict

        for key, value in report_angle_dict.items():
            self.report_angles[key].update({"left": None,
                                            "right": None,
                                            "left_more_than_range": None,
                                            "left_less_than_range": None,
                                            "right_more_than_range": None,
                                            "right_less_than_range": None,
                                            "left_exceed_range": False,
                                            "right_exceed_range": False})

    def __initial_report_angles_helper(self):
        self.report_angles_helper = {}
        for key, item in report_angle_dict.items():
            if key.split("_")[-1] in ["Max", "Min","Top", "Bottom", "Forward", "Rear"]:
                self.report_angles_helper.update({key: [None, None]}) #left_value, right_value

    def __initial_report_distance_helper(self):
        self.__report_distance_helper = {}
        for key, value in distance_idx.items():
            if len(value) == 3:
                self.__report_distance_helper['{}_Min'.format(key)] = None
                self.__report_distance_helper['{}_Max'.format(key)] = None

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
            idxs_left, idxs_right = item["points"]
            points_left = [self.key_points_left[idx][:2] for idx in idxs_left]
            points_right = [self.key_points_right[idx][:2] for idx in idxs_right]
            if key == "Back_From_Level" and (None,None) not in points_right:
                a = 1

            if len(points_left) == 2:
                tmp_angle_left = horizen_angle(*points_left)
                tmp_angle_right = horizen_angle(*points_right)

            elif len(points_left) == 3:
                if self.angle_mode == '3d':
                    points_front = [self.key_points_front[idx][:2] for idx in idxs_left]
                    tmp_angle_left = angle_3d(*points_front, *points_left)
                    tmp_angle_right = angle_3d(*points_front, *points_right)

                elif self.angle_mode == '2d':
                    tmp_angle_left = angle_2d(*points_left)
                    tmp_angle_right = angle_2d(*points_right)

                    # knee angle exception
                    if key.startswith("Knee_Angle"):
                        tmp_angle_left = minus_with_none(180, tmp_angle_left)
                        tmp_angle_right = minus_with_none(180, tmp_angle_right)
                else:
                    logger.error('unknown angle mode')
                    tmp_angle_left = None
                    tmp_angle_right = None

            else:
                tmp_angle_left = None
                tmp_angle_right = None
                logger.error("error, unknown angle len")

            mode = key.split("_")[-1]
            basename = "_".join(key.split("_")[:-1])

            if mode in ["Max", "Flexion", "Open"]:
                self.report_angles[key]["left"] = max_with_none(self.report_angles[key]["left"], tmp_angle_left)
                self.report_angles[key]["right"] = max_with_none(self.report_angles[key]["right"], tmp_angle_right)

            elif mode in ["Min", "Extension", "Closed"]:
                self.report_angles[key]["left"] = min_with_none(self.report_angles[key]["left"], tmp_angle_left)
                self.report_angles[key]["right"] = min_with_none(self.report_angles[key]["right"], tmp_angle_right)

            elif mode == "Range":
                if self.is_last_frame:
                    max_key = "{}_Max".format(basename)
                    min_key = "{}_Min".format(basename)
                    self.report_angles[key]["left"] = minus_with_none(self.report_angles[max_key]["left"], self.report_angles[min_key]["left"])
                    self.report_angles[key]["right"] = minus_with_none(self.report_angles[max_key]["right"], self.report_angles[min_key]["right"])
                else:
                    self.report_angles[key]["left"] = None
                    self.report_angles[key]["right"] = None
            elif mode == "Top":
                if topper_than_with_none(self.key_points_left[19][1], self.report_angles_helper[key][0]):
                    self.report_angles_helper[key][0] = self.key_points_left[19][1]
                    self.report_angles[key]["left"] = tmp_angle_left

                if topper_than_with_none(self.key_points_right[22][1], self.report_angles_helper[key][1]):
                    self.report_angles_helper[key][1] = self.key_points_right[22][1]
                    self.report_angles[key]["right"] = tmp_angle_right

            elif mode == "Bottom":
                if bottomer_than_with_none(self.key_points_left[19][1], self.report_angles_helper[key][0]):
                    self.report_angles_helper[key][0] = self.key_points_left[19][1]
                    self.report_angles[key]["left"] = tmp_angle_left

                if bottomer_than_with_none(self.key_points_right[22][1], self.report_angles_helper[key][1]):
                    self.report_angles_helper[key][1] = self.key_points_right[22][1]
                    self.report_angles[key]["right"] = tmp_angle_right

            elif mode == "Forward":
                if forwarder_than_with_none(self.key_points_left[19][0], self.report_angles_helper[key][0]):
                    self.report_angles_helper[key][0] = self.key_points_left[19][1]
                    self.report_angles[key]["left"] = tmp_angle_left

                if forwarder_than_with_none_right(self.key_points_right[22][0], self.report_angles_helper[key][1]):
                    self.report_angles_helper[key][1] = self.key_points_right[22][1]
                    self.report_angles[key]["right"] = tmp_angle_right

            elif mode == "Rear":
                if rearer_than_with_none(self.key_points_left[19][0], self.report_angles_helper[key][0]):
                    self.report_angles_helper[key][0] = self.key_points_left[19][1]
                    self.report_angles[key]["left"] = tmp_angle_left

                if rearer_than_with_none_right(self.key_points_right[22][0], self.report_angles_helper[key][1]):
                    self.report_angles_helper[key][1] = self.key_points_right[22][1]
                    self.report_angles[key]["right"] = tmp_angle_right

            elif mode == "Average":
                self.report_angles[key]["left"] = calculate_average(self.report_angles[key]["left"], tmp_angle_left, self.idx)
                self.report_angles[key]["right"] = calculate_average(self.report_angles[key]["right"], tmp_angle_right, self.idx)

            else:
                self.report_angles[key]["left"] = tmp_angle_left
                self.report_angles[key]["right"] = tmp_angle_right

            # post process
            if self.report_angles[key]["left"] is not None:
                self.report_angles[key]["left"] = round(self.report_angles[key]["left"], 2)
            if self.report_angles[key]["right"] is not None:
                self.report_angles[key]["right"] = round(self.report_angles[key]["right"], 2)

    def __report_angles_alarm(self):
        for key, item in self.report_angles.items():

            range = item["good_range"]
            # no range data, no need to alarm
            if range == (None, None):
                continue

            for side in ["left", "right"]:

                # default we think there is no alarm, and will not update the exceed value
                item["{}_exceed_range".format(side)] = False

                side_angle = eval("item['{}']".format(side))

                if side_angle is not None:
                    if side_angle > range[1]:
                        item["{}_exceed_range".format(side)] = True
                        if item["{}_more_than_range".format(side)] is None or side_angle - range[1] > item["{}_more_than_range".format(side)]:
                            item["{}_more_than_range".format(side)] = round(side_angle - range[1], 2)
                    elif side_angle < range[0]:
                        item["{}_exceed_range".format(side)] = True
                        if item["{}_less_than_range".format(side)] is None or range[0] - side_angle >  abs(item["{}_less_than_range".format(side)]):
                            item["{}_less_than_range".format(side)] = - round((range[0] - side_angle), 2)

    def __update_knee_pic(self, key_points1, frame_shape):

        if self.knee_path_pic is None:
            self.knee_path_pic = np.zeros(frame_shape, np.uint8)
            for i in range(3):
                self.knee_path_pic[:,:,i] = self.knee_path_pic_color[i]

            # plot bike frame
            cv2.line(self.knee_path_pic,
                     (int(self.frame_shape[1]//2), int(self.frame_shape[0]//8*3)),
                     (int(self.frame_shape[1]//2), int(self.frame_shape[0]//8*5)),
                     color=(231, 136, 29),
                     thickness=3)

        for side, point_idx in [("left", 13), ("right", 10)]:
            if None not in key_points1[point_idx]:
                current_knee_point = (int(key_points1[point_idx][0]), int(key_points1[point_idx][1]))

                if eval("self.{}_knee_path_start_point".format(side)) is not None:
                    color = (0, 0, 255) if current_knee_point[1] > eval("self.{}_knee_path_start_point[1]".format(side)) else (0, 255, 0)

                    # down is red (0, 0 ,255), up is green (0, 255, 0) BGR
                    cv2.line(self.knee_path_pic, eval("self.{}_knee_path_start_point".format(side)), current_knee_point, color=color, thickness=2)

                exec("self.{}_knee_path_start_point = current_knee_point".format(side))

        cv2.imwrite("realtime_knee_path.png", self.knee_path_pic)

    def update_every_frame(self, key_points_front, key_points_right, key_points_left, is_last_frame):

        t1 = time.time()

        self.key_points_front = key_points_front
        self.key_points_left = key_points_left
        self.key_points_right = key_points_right

        self.is_last_frame = is_last_frame

        self.__update_report_angles()
        self.__report_angles_alarm()

        self.__update_knee_pic(key_points_front, self.frame_shape)

        self.__update_report_distance()
        for k, v in self.report_distance.items():
            if v is None:
                continue
            self.report_distance.update({k: round(float(v), 2)})

        # print("[{}] update time: {}".format(self.idx, time.time() - t1))
        # print("[{}] update fps: {}, actual fps: {}".format(self.idx, round(1 / (time.time() - t1), 1), round(self.idx/(time.time() - self.zero_time), 1)))
        self.idx += 1

