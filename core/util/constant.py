angles_tmp_idx = {
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

distance_idx = {
    "Knee_to_Foot_Forward_left": (13, 19, 'left', 'h'),
    "Knee_to_Foot_Forward_right": (10, 22, 'right', 'h'),

    "Knee_to_Foot_Lateral_left": (13, 19, 'front', 'h'),
    "Knee_to_Foot_Lateral_right": (10, 22, 'front', 'h'),

    "Hip_to_Foot_Lateral_left": (12, 19, 'front', 'h'),
    "Hip_to_Foot_Lateral_right": (9, 22, 'front', 'h'),

    "Hip_to_Wrist_Vertical_left": (12, 7, 'left', 'v'),
    "Hip_to_Wrist_Vertical_right": (9, 4, 'right', 'v'),

    "Hip_to_Wrist_Forward_left": (12, 7, 'left', 'h'),
    "Hip_to_Wrist_Forward_right": (9, 4, 'right', 'h'),

    "Hip_to_Elbow_Vertical_left": (12, 6, 'left', 'v'),
    "Hip_to_Elbow_Vertical_right": (9, 3, 'right', 'v'),

    "Hip_to_Elbow_Forward_left": (12, 6, 'left', 'h'),
    "Hip_to_Elbow_Forward_right": (9, 3, 'right', 'h'),

    "Shoulder_to_Wrist_Lateral_left": (5, 7, 'front', 'h'),
    "Shoulder_to_Wrist_Lateral_right": (2, 4, 'front', 'h'),

    # travel distance
    "Knee_Lateral_Travel_left": (13, 'front', 'h'),
    "Knee_Lateral_Travel_right": (10, 'front', 'h'),

    "Hip_Vertical_Travel_left": (12, 'left', 'v'),
    "Hip_Vertical_Travel_right": (9, 'right', 'v'),

    "Hip_Lateral_Travel_left": (12, 'front', 'v'),
    "Hip_Lateral_Travel_right": (9, 'front', 'v'),

    # length
    "Thigh_Length_left": (12, 13, 'left', 'd'),
    "Thigh_Length_right": (9, 10, 'right', 'd'),

    "Shin_Length_left": (13, 14, 'left', 'd'),
    "Shin_Length_right": (10, 11, 'right', 'd')
}

report_angle_names = [
    "Ankle_Angle_Max_left",
    "Ankle_Angle_Min_left",
    "Ankle_Angle_Range_left",
    "Ankle_Angle_Top_left",
    "Ankle_Angle_Bottom_left",
    "Ankle_Angle_Forward_left",
    "Ankle_Angle_Rear_left",

    "Knee_Angle_Flexion_left",  # max
    "Knee_Angle_Extension_left",  # min
    "Knee_Angle_Range_left",

    "Hip_Angle_Open_left",  # max
    "Hip_Angle_Closed_left",  # min
    "Hip_Angle_Range_left",

    "Back_From_Level_left",
    "Back_From_Level_Average_left",

    "Forearm_From_Level_left",
    "Forearm_From_Level_Average_left",

    "Foot_From_Level_left",
    "Foot_From_Level_Average_left",

    "Hip_Shoulder_Wrist_left",
    "Hip_Shoulder_Wrist_Average_left",

    "Hip_Shoulder_Elbow_left",
    "Hip_Shoulder_Elbow_Average_left",

    "Elbow_Angle_left",
    "Elbow_Angle_Average_left",

    # right angles
    "Ankle_Angle_Max_right",
    "Ankle_Angle_Min_right",
    "Ankle_Angle_Range_right",
    "Ankle_Angle_Top_right",
    "Ankle_Angle_Bottom_right",
    "Ankle_Angle_Forward_right",
    "Ankle_Angle_Rear_right",

    "Knee_Angle_Flexion_right",
    "Knee_Angle_Extension_right",
    "Knee_Angle_Range_right",

    "Hip_Angle_Open_right",
    "Hip_Angle_Closed_right",
    "Hip_Angle_Range_right",

    "Back_From_Level_right",
    "Back_From_Level_Average_right",

    "Forearm_From_Level_right",
    "Forearm_From_Level_Average_right",

    "Foot_From_Level_right",
    "Foot_From_Level_Average_right",

    "Hip_Shoulder_Wrist_right",
    "Hip_Shoulder_Wrist_Average_right",

    "Hip_Shoulder_Elbow_right",
    "Hip_Shoulder_Elbow_Average_right",

    "Elbow_Angle_right",
    "Elbow_Angle_Average_right",

    # Foot Float Angle
    "Foot_Float_Angle_Min_left",
    "Foot_Float_Angle_Max_left",
    "Foot_Float_Angle_Mean_left",
    "Foot_Float_Angle_Min_right",
    "Foot_Float_Angle_Max_right",
    "Foot_Float_Angle_Mean_right",

]
