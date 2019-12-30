# left_points, right_points
angles_tmp_idx = {
    "knee_angle": [(12, 13, 14),(9, 10, 11)],

    "ankle_angle": [(13, 14, 19),(10, 11, 22)],

    "hip_angle": [(5, 12, 13), (2, 9, 10)],

    "hip_shoulder_elbow_angle": [(6, 5, 12), (3, 2, 9)],
    
    "hip_shoulder_wrist_angle": [(7, 5, 12), (4, 2, 9)],

    "elbow_angle": [(5, 6, 7), (2, 3, 4)],

    "back_from_level": [(5, 12), (2, 9)],
    
    "forearm_from_level": [(6, 7), (3, 4)],
    
    "foot_from_level": [(14, 19), (11, 22)]
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


report_angle_dict = {
    "Ankle_Angle_Max": (angles_tmp_idx["ankle_angle"], "MAX", (90,100)),
    "Ankle_Angle_Min": (angles_tmp_idx["ankle_angle"], "MIN", (65,75)),
    "Ankle_Angle_Range": (angles_tmp_idx["ankle_angle"], "RANGE", (20,30)),
    "Ankle_Angle_Top": (angles_tmp_idx["ankle_angle"], "TOP", (None,None)),
    "Ankle_Angle_Bottom": (angles_tmp_idx["ankle_angle"], "BOTTOM", (90,100)),
    "Ankle_Angle_Forward": (angles_tmp_idx["ankle_angle"], "FORWARD", (None,None)),
    "Ankle_Angle_Rear": (angles_tmp_idx["ankle_angle"], "REAR", (None,None)),

    "Knee_Angle_Flexion": (angles_tmp_idx["knee_angle"], "MAX", (107,113)), # max
    "Knee_Angle_Extension": (angles_tmp_idx["knee_angle"], "MIN", (33,42)),  # min
    "Knee_Angle_Range": (angles_tmp_idx["knee_angle"], "RANGE", (70,75)),
   
    "Hip_Angle_Open": (angles_tmp_idx["hip_angle"], "MAX", (None,None)), # max
    "Hip_Angle_Closed": (angles_tmp_idx["hip_angle"], "MIN", (46,56)),  # min
    "Hip_Angle_Range": (angles_tmp_idx["hip_angle"], "RANGE", (40,45)),
  
    "Back_From_Level": (angles_tmp_idx["back_from_level"], "FLY", (20,35)),
    "Back_From_Level_Average": (angles_tmp_idx["back_from_level"], "AVERAGE", (20,35)),

    "Forearm_From_Level": (angles_tmp_idx["forearm_from_level"], "FLY", (None,None)),
    "Forearm_From_Level_Average": (angles_tmp_idx["forearm_from_level"], "AVERAGE", (None,None)),

    "Foot_From_Level": (angles_tmp_idx["foot_from_level"], "FLY", (None,None)),
    "Foot_From_Level_Average": (angles_tmp_idx["foot_from_level"], "AVERAGE", (None,None)),

    "Hip_Shoulder_Wrist": (angles_tmp_idx["hip_shoulder_wrist_angle"], "FLY", (None,None)),
    "Hip_Shoulder_Wrist_Average": (angles_tmp_idx["hip_shoulder_wrist_angle"], "AVERAGE", (None,None)),

    "Hip_Shoulder_Elbow": (angles_tmp_idx["hip_shoulder_elbow_angle"], "FLY", (None,None)),
    "Hip_Shoulder_Elbow_Average": (angles_tmp_idx["hip_shoulder_elbow_angle"], "AVERAGE", (None,None)),

    "Elbow_Angle": (angles_tmp_idx["hip_shoulder_elbow_angle"], "FLY", (70,80)),
    "Elbow_Angle_Average": (angles_tmp_idx["hip_shoulder_elbow_angle"], "AVERAGE", (70,80)),

    # Foot Float Angle
    # "Foot_Float_Angle_Min_left",
    # "Foot_Float_Angle_Max_left",
    # "Foot_Float_Angle_Mean_left",
    # "Foot_Float_Angle_Min_right",
    # "Foot_Float_Angle_Max_right",
    # "Foot_Float_Angle_Mean_right",


}
