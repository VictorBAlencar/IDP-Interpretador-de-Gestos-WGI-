import json
import os
import statistics

DB_FILE = "calibration.json"

# Default fallback values if the user hasn't calibrated yet
DEFAULT_CONFIG = {
    "right_click": {
        "mid_angle_max": 50,
        "idx_angle_min": 90,
        "thumb_index_dist_min": 50,
        "stability_std_max": 25
    },
    "left_click": {
        "idx_angle_max": 50,
        "mid_angle_min": 90,
        "idx_drag_angle_max": 110,
        "mid_drag_angle_min": 40,
        "thumb_index_dist_min": 50,
        "stability_std_max": 25
    },
    "double_click": {
        "trigger_angle_max": 50,
        "release_angle_min": 90,
        "thumb_index_dist_min": 50,
        "stability_std_max": 25
    },
    "scroll": {
        "idx_angle_min": 90,
        "mid_angle_min": 90,
        "ring_angle_max": 50,
        "pinky_angle_max": 50
    }
}

def load_config():
    if not os.path.exists(DB_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
        
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_CONFIG

def save_config(config_data):
    with open(DB_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)

def auto_calibrate(gesture_name, idx_raw_history, mid_raw_history):
    
    config = load_config()
    
    if gesture_name not in config:
        config[gesture_name] = {}
        
    config[gesture_name]["idx_angle_min"] = max(0, statistics.mean(idx_raw_history) - 15)
    config[gesture_name]["mid_angle_max"] = statistics.mean(mid_raw_history) + 15
    
    save_config(config)

config = load_config()