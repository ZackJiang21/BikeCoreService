# left_points, right_points
angles_tmp_idx = {
    "knee_angle": [(12, 13, 14), (9, 10, 11)],

    "ankle_angle": [(13, 14, 19), (10, 11, 22)],

    "hip_angle": [(5, 12, 13), (2, 9, 10)],

    "hip_shoulder_elbow_angle": [(6, 5, 12), (3, 2, 9)],
    
    "hip_shoulder_wrist_angle": [(7, 5, 12), (4, 2, 9)],

    "elbow_angle": [(5, 6, 7), (2, 3, 4)],

    "back_from_level": [(5, 12), (2, 9)],
    
    "forearm_from_level": [(6, 7), (3, 4)],
    
    "foot_from_level": [(14, 19), (11, 22)]
}

distance_dict = {
    "Knee_to_Foot_Forward": {
        "mode": "h",
        "points": {
            "left": {
                "side": "left",
                "index": (13, 19)
            },
            "right": {
                "side": "right",
                "index": (10, 22)
            }
        },
        "range": (50, 120)
    },
    "Knee_to_Foot_Lateral": {
        "mode": "h",
        "points": {
            "left": {
                "side": "front",
                "index": (13, 19)
            },
            "right": {
                "side": "front",
                "index": (10, 22)
            }
        },
    },
    "Hip_to_Foot_Lateral": {
        "mode": "h",
        "points": {
            "left": {
                "side": "front",
                "index": (12, 19)
            },
            "right": {
                "side": "front",
                "index": (9, 22)
            }
        },
    },
    "Hip_to_Wrist_Vertical": {
        "mode": "v",
        "points": {
            "left": {
                "side": "left",
                "index": (12, 7)
            },
            "right": {
                "side": "right",
                "index": (9, 4)
            }
        },
    },
    "Hip_to_Wrist_Forward": {
        "mode": "h",
        "points": {
            "left": {
                "side": "left",
                "index": (12, 7)
            },
            "right": {
                "side": "right",
                "index": (9, 4)
            }
        },
    },
    "Hip_to_Elbow_Vertical": {
        "mode": "v",
        "points": {
            "left": {
                "side": "left",
                "index": (12, 6)
            },
            "right": {
                "side": "right",
                "index": (9, 3)
            }
        },
    },
    "Hip_to_Elbow_Forward":  {
        "mode": "h",
        "points": {
            "left": {
                "side": "left",
                "index": (12, 6)
            },
            "right": {
                "side": "right",
                "index": (9, 3)
            }
        },
    },
    "Shoulder_to_Wrist_Lateral":  {
        "mode": "h",
        "points": {
            "left": {
                "side": "front",
                "index": (5, 7)
            },
            "right": {
                "side": "front",
                "index": (2, 4)
            }
        },
    },
    "Knee_Lateral_Travel": {
        "mode": "h",
        "points": {
            "left": {
                "side": "front",
                "index": (13,)
            },
            "right": {
                "side": "front",
                "index": (10,)
            }
        },
    },
    "Hip_Vertical_Travel": {
        "mode": "v",
        "points": {
            "left": {
                "side": "left",
                "index": (12,)
            },
            "right": {
                "side": "right",
                "index": (9,)
            }
        },
    },
    "Hip_Lateral_Travel": {
        "mode": "v",
        "points": {
            "left": {
                "side": "front",
                "index": (12,)
            },
            "right": {
                "side": "front",
                "index": (9,)
            }
        },
    },
    "Thigh_Length": {
        "mode": "d",
        "points": {
            "left": {
                "side": "left",
                "index": (12, 13)
            },
            "right": {
                "side": "right",
                "index": (9, 10)
            }
        },
    },
    "Shin_Length": {
        "mode": "d",
        "points": {
            "left": {
                "side": "left",
                "index": (13, 14)
            },
            "right": {
                "side": "right",
                "index": (10, 11)
            }
        },
    },
}

report_angle_dict = {
    "Ankle_Angle_Max": {"points": angles_tmp_idx["ankle_angle"], "mode": "MAX", "good_range": (90, 100), "display_name": "Ankle_Angle_Max"},
    "Ankle_Angle_Min": {"points": angles_tmp_idx["ankle_angle"], "mode": "MIN", "good_range": (65, 75), "display_name": "Ankle_Angle_Min"},
    "Ankle_Angle_Range": {"points": angles_tmp_idx["ankle_angle"], "mode": "RANGE", "good_range": (20, 30), "display_name": "Ankle_Angle_Range"},
    "Ankle_Angle_Top": {"points": angles_tmp_idx["ankle_angle"], "mode": "TOP", "good_range": (None, None), "display_name": "Ankle_Angle_Top"},
    "Ankle_Angle_Bottom": {"points": angles_tmp_idx["ankle_angle"], "mode": "BOTTOM", "good_range": (90, 100), "display_name": "Ankle_Angle_Bottom"},
    "Ankle_Angle_Forward": {"points": angles_tmp_idx["ankle_angle"], "mode": "FORWARD", "good_range": (None, None), "display_name": "Ankle_Angle_Forward"},
    "Ankle_Angle_Rear": {"points": angles_tmp_idx["ankle_angle"], "mode": "REAR", "good_range": (None, None), "display_name": "Ankle_Angle_Rear"},

    "Knee_Angle_Max": {"points": angles_tmp_idx["knee_angle"], "mode": "MAX", "good_range": (107, 113), "display_name": "Knee_Angle_Flexion"}, # max
    "Knee_Angle_Min": {"points": angles_tmp_idx["knee_angle"], "mode": "MIN", "good_range": (33, 42), "display_name": "Knee_Angle_Extension"},  # min
    "Knee_Angle_Range": {"points": angles_tmp_idx["knee_angle"], "mode": "RANGE", "good_range": (70, 75), "display_name": "Knee_Angle_Range"},
   
    "Hip_Angle_Max": {"points": angles_tmp_idx["hip_angle"], "mode": "MAX", "good_range": (None, None), "display_name": "Hip_Angle_Open"}, # max
    "Hip_Angle_Min": {"points": angles_tmp_idx["hip_angle"], "mode": "MIN", "good_range": (46, 56), "display_name": "Hip_Angle_Closed"},  # min
    "Hip_Angle_Range": {"points": angles_tmp_idx["hip_angle"], "mode": "RANGE", "good_range": (40, 45), "display_name": "Hip_Angle_Range"},
  
    "Back_From_Level": {"points": angles_tmp_idx["back_from_level"], "mode": "FLY", "good_range": (20, 35), "display_name": "Back_From_Level"},
    "Back_From_Level_Average": {"points": angles_tmp_idx["back_from_level"], "mode": "AVERAGE", "good_range": (20, 35), "display_name": "Back_From_Level_Average"},

    "Forearm_From_Level": {"points": angles_tmp_idx["forearm_from_level"], "mode": "FLY", "good_range": (None, None), "display_name": "Forearm_From_Level"},
    "Forearm_From_Level_Average": {"points": angles_tmp_idx["forearm_from_level"], "mode": "AVERAGE", "good_range": (None, None), "display_name": "Forearm_From_Level_Average"},

    "Foot_From_Level": {"points": angles_tmp_idx["foot_from_level"], "mode": "FLY", "good_range": (None, None), "display_name": "Foot_From_Level"},
    "Foot_From_Level_Average": {"points": angles_tmp_idx["foot_from_level"], "mode": "AVERAGE", "good_range": (None, None), "display_name": "Foot_From_Level_Average"},

    "Hip_Shoulder_Wrist": {"points": angles_tmp_idx["hip_shoulder_wrist_angle"], "mode": "FLY", "good_range": (None, None), "display_name": "Hip_Shoulder_Wrist"},
    "Hip_Shoulder_Wrist_Average": {"points": angles_tmp_idx["hip_shoulder_wrist_angle"], "mode": "AVERAGE", "good_range": (None, None), "display_name": "Hip_Shoulder_Wrist_Average"},

    "Hip_Shoulder_Elbow": {"points": angles_tmp_idx["hip_shoulder_elbow_angle"], "mode": "FLY", "good_range": (70, 80), "display_name": "Hip_Shoulder_Elbow"},
    "Hip_Shoulder_Elbow_Average": {"points": angles_tmp_idx["hip_shoulder_elbow_angle"], "mode": "AVERAGE", "good_range": (70, 80), "display_name": "Hip_Shoulder_Elbow_Average"},

    "Elbow_Angle": {"points": angles_tmp_idx["elbow_angle"], "mode": "FLY", "good_range": (None, None), "display_name": "Elbow_Angle"},
    "Elbow_Angle_Average": {"points": angles_tmp_idx["elbow_angle"], "mode": "AVERAGE", "good_range": (None, None), "display_name": "Elbow_Angle_Average"},

    # Foot Float Angle
    # "Foot_Float_Angle_Min_left",
    # "Foot_Float_Angle_Max_left",
    # "Foot_Float_Angle_Mean_left",
    # "Foot_Float_Angle_Min_right",
    # "Foot_Float_Angle_Max_right",
    # "Foot_Float_Angle_Mean_right",

}
