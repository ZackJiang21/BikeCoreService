angles_idx = {
    "knee_angle_left": (12, 13, 14),
    "knee_angle_right": (9, 10, 11),

    "ankle_angle_left": (13, 14, 19),
    "ankle_angle_right": (10, 11, 22),

    "hip_angle_left": (5, 12, 13),
    "hip_angle_right": (2, 9, 10),

    "hip_shoulder_elbow_angle_left": (6, 5, 12),
    "hip_shoulder_elbow_angle_right": (3, 2, 9),
    "hip_shoulder_wrist_angle_left": (7, 5, 12),
    "hip_shoulder_wrist_angle_right": (4, 2, 9),

    "elbow_angle_left": (5, 6, 7),
    "elbow_angle_right": (2, 3, 4),

    "back_from_level_left": (5, 12),
    "back_from_level_right": (2, 9),
    "forearm_from_level_left": (6, 7),
    "forearm_from_level_right": (3, 4),
    "foot_from_level_left": (14, 19),
    "foot_from_level_right": (11, 22)

}


# TODO
distance_idx = {
    "Knee_to_Foot_Forward_left": (13, 19, 'h'),
    "Knee_to_Foot_Forward_right": (10, 22, 'h')
}


def initial_report_angles():
    initial_angles = {}

    # left angles
    initial_angles["Ankle_Angle_Max_left"] = 0
    initial_angles["Ankle_Angle_Min_left"] = 360
    initial_angles["Ankle_Angle_Range_left"] = 0
    initial_angles["Ankle_Angle_Top_left"] = 0
    initial_angles["Ankle_Angle_Bottom_left"] = 0
    initial_angles["Ankle_Angle_Forward_left"] = 0
    initial_angles["Ankle_Angle_Rear_left"] = 0

    initial_angles["Knee_Angle_Flexion_left"] = 0 # max
    initial_angles["Knee_Angle_Extension_left"] = 360 # min
    initial_angles["Knee_Angle_Range_left"] = 0

    initial_angles["Hip_Angle_Open_left"] = 0 # max
    initial_angles["Hip_Angle_Closed_left"] = 360 # min
    initial_angles["Hip_Angle_Range_left"] = 0

    initial_angles["Back_From_Level_left"] = 0
    initial_angles["Forearm_From_Level_left"] = 0
    initial_angles["Foot_From_Level_left"] = 0

    initial_angles["Hip_Shoulder_Wrist_left"] = 0
    initial_angles["Hip_Shoulder_Elbow_left"] = 0

    initial_angles["Elbow_Angle_left"] = 0

    # right angles
    initial_angles["Ankle_Angle_Max_right"] = 0
    initial_angles["Ankle_Angle_Min_right"] = 360
    initial_angles["Ankle_Angle_Range_right"] = 0
    initial_angles["Ankle_Angle_Top_right"] = 0
    initial_angles["Ankle_Angle_Bottom_right"] = 0
    initial_angles["Ankle_Angle_Forward_right"] = 0
    initial_angles["Ankle_Angle_Rear_right"] = 0

    initial_angles["Knee_Angle_Flexion_right"] = 0
    initial_angles["Knee_Angle_Extension_right"] = 360
    initial_angles["Knee_Angle_Range_right"] = 0

    initial_angles["Hip_Angle_Open_right"] = 0
    initial_angles["Hip_Angle_Closed_right"] = 360
    initial_angles["Hip_Angle_Range_right"] = 0

    initial_angles["Back_From_Level_right"] = 0
    initial_angles["Forearm_From_Level_right"] = 0
    initial_angles["Foot_From_Level_right"] = 0

    initial_angles["Hip_Shoulder_Wrist_right"] = 0
    initial_angles["Hip_Shoulder_Elbow_right"] = 0

    initial_angles["Elbow_Angle_right"] = 0

    return initial_angles


def update_report_angles(key_points_left, key_points_left_pre, key_points_right, key_points_right_pre, angles_tmp,
                         report_angles):
    ############### left angles
    report_angles["Ankle_Angle_Min_left"] = min(report_angles["Ankle_Angle_Min_left"], angles_tmp["ankle_angle_left"])
    report_angles["Ankle_Angle_Max_left"] = max(report_angles["Ankle_Angle_Max_left"], angles_tmp["ankle_angle_left"])
    report_angles["Ankle_Angle_Range_left"] = report_angles["Ankle_Angle_Max_left"] - \
                                              report_angles["Ankle_Angle_Min_left"]

    report_angles["Ankle_Angle_Top_left"] = angles_tmp["ankle_angle_left"] \
        if len(key_points_left_pre) == 0 or key_points_left[19][1] < key_points_left_pre[19][1] \
        else report_angles["Ankle_Angle_Top_left"]
    report_angles["Ankle_Angle_Bottom_left"] = angles_tmp["ankle_angle_left"] \
        if len(key_points_left_pre) == 0 or key_points_left[19][1] > key_points_left_pre[19][1] \
        else report_angles["Ankle_Angle_Bottom_left"]
    report_angles["Ankle_Angle_Forward_left"] = angles_tmp["ankle_angle_left"] \
        if len(key_points_left_pre) == 0 or key_points_left[19][0] < key_points_left_pre[19][0] \
        else report_angles["Ankle_Angle_Forward_left"]
    report_angles["Ankle_Angle_Rear_left"] = angles_tmp["ankle_angle_left"] \
        if len(key_points_left_pre) == 0 or key_points_left[19][0] > key_points_left_pre[19][0] \
        else report_angles["Ankle_Angle_Rear_left"]

    report_angles["Knee_Angle_Flexion_left"] = max(report_angles["Knee_Angle_Flexion_left"],
                                                   angles_tmp["knee_angle_left"])
    report_angles["Knee_Angle_Extension_left"] = min(report_angles["Knee_Angle_Extension_left"],
                                                     angles_tmp["knee_angle_left"])
    report_angles["Knee_Angle_Range_left"] = report_angles["Knee_Angle_Flexion_left"] \
                                             - report_angles["Knee_Angle_Extension_left"]

    report_angles["Hip_Angle_Open_left"] = max(report_angles["Hip_Angle_Open_left"], angles_tmp["hip_angle_left"])
    report_angles["Hip_Angle_Closed_left"] = min(report_angles["Hip_Angle_Closed_left"], angles_tmp["hip_angle_left"])
    report_angles["Hip_Angle_Range_left"] = report_angles["Hip_Angle_Open_left"] - report_angles["Hip_Angle_Closed_left"]

    report_angles["Back_From_Level_left"] = angles_tmp["back_from_level_left"]
    report_angles["Forearm_From_Level_left"] = angles_tmp["forearm_from_level_left"]
    report_angles["Foot_From_Level_left"] = angles_tmp["foot_from_level_left"]

    report_angles["Hip_Shoulder_Wrist_left"] = angles_tmp["hip_shoulder_wrist_angle_left"]
    report_angles["Hip_Shoulder_Elbow_left"] = angles_tmp["hip_shoulder_elbow_angle_left"]

    report_angles["Elbow_Angle_left"] = angles_tmp["elbow_angle_left"]

    ############## right angles
    report_angles["Ankle_Angle_Min_right"] = min(report_angles["Ankle_Angle_Min_right"],
                                                 angles_tmp["ankle_angle_right"])
    report_angles["Ankle_Angle_Max_right"] = max(report_angles["Ankle_Angle_Max_right"],
                                                 angles_tmp["ankle_angle_right"])
    report_angles["Ankle_Angle_Range_right"] = report_angles["Ankle_Angle_Max_right"] \
                                               - report_angles["Ankle_Angle_Min_right"]

    report_angles["Ankle_Angle_Top_right"] = angles_tmp["ankle_angle_right"] \
        if len(key_points_right_pre) == 0 or key_points_right[19][1] < key_points_right_pre[19][1] \
        else report_angles["Ankle_Angle_Top_right"]
    report_angles["Ankle_Angle_Bottom_right"] = angles_tmp["ankle_angle_right"] \
        if len(key_points_right_pre) == 0 or key_points_right[19][1] > key_points_right_pre[19][1] \
        else report_angles["Ankle_Angle_Bottom_right"]
    # left and right has different meaning of Forward and Rear
    report_angles["Ankle_Angle_Forward_right"] = angles_tmp["ankle_angle_right"] \
        if len(key_points_right_pre) == 0 or key_points_right[19][0] > key_points_right_pre[19][0] \
        else report_angles["Ankle_Angle_Forward_right"]
    report_angles["Ankle_Angle_Rear_right"] = angles_tmp["ankle_angle_right"] \
        if len(key_points_right_pre) == 0 or key_points_right[19][0] < key_points_right_pre[19][0] \
        else report_angles["Ankle_Angle_Rear_right"]

    report_angles["Knee_Angle_Flexion_right"] = max(report_angles["Knee_Angle_Flexion_right"],
                                                    angles_tmp["knee_angle_right"])
    report_angles["Knee_Angle_Extension_right"] = min(report_angles["Knee_Angle_Extension_right"],
                                                      angles_tmp["knee_angle_right"])
    report_angles["Knee_Angle_Range_right"] = report_angles["Knee_Angle_Flexion_right"] - \
                                              report_angles["Knee_Angle_Extension_right"]

    report_angles["Hip_Angle_Open_right"] = max(report_angles["Hip_Angle_Open_right"], angles_tmp["hip_angle_right"])
    report_angles["Hip_Angle_Closed_right"] = min(report_angles["Hip_Angle_Closed_right"],
                                                  angles_tmp["hip_angle_right"])
    report_angles["Hip_Angle_Range_right"] = report_angles["Hip_Angle_Open_right"] - \
                                             report_angles["Hip_Angle_Closed_right"]

    report_angles["Back_From_Level_right"] = angles_tmp["back_from_level_right"]
    report_angles["Forearm_From_Level_right"] = angles_tmp["forearm_from_level_right"]
    report_angles["Foot_From_Level_right"] = angles_tmp["foot_from_level_right"]

    report_angles["Hip_Shoulder_Wrist_right"] = angles_tmp["hip_shoulder_wrist_angle_right"]
    report_angles["Hip_Shoulder_Elbow_right"] = angles_tmp["hip_shoulder_elbow_angle_right"]

    report_angles["Elbow_Angle_right"] = angles_tmp["elbow_angle_right"]
