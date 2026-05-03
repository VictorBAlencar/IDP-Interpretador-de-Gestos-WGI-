import numpy as np

def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    if angle > 180.0:
        angle = 360 - angle
    return angle

def get_hand_scale(landmark_list):
    """Returns the reference size of the hand (wrist to middle finger MCP)."""
    if len(landmark_list) < 10:
        return 1.0
    scale = get_raw_dist(landmark_list[0], landmark_list[9])
    return scale if scale > 0 else 1.0

def get_distance(landmark_list, idx1=4, idx2=5):
    """Returns distance between two landmarks, normalized by hand size."""
    if len(landmark_list) <= max(idx1, idx2):
        return 0 
    p1, p2 = landmark_list[idx1], landmark_list[idx2]
    scale = get_hand_scale(landmark_list)
    L = get_raw_dist(p1, p2) / scale
    return float(np.interp(L, [0, 2], [0, 1000]))

def get_raw_dist(p1, p2):
    """Returns Euclidean distance between two points in normalized space."""
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))