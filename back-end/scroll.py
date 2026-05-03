import calculo_distancia as util
import calibration_manager
import cursor_movement
import collections
import statistics

prev_hand_y = None

HISTORY_LENGTH = 5
idx_history = collections.deque(maxlen=HISTORY_LENGTH)
mid_history = collections.deque(maxlen=HISTORY_LENGTH)
ring_history = collections.deque(maxlen=HISTORY_LENGTH)
pinky_history = collections.deque(maxlen=HISTORY_LENGTH)
y_history = collections.deque(maxlen=HISTORY_LENGTH)

def detect_scroll(landmark_list):
    global prev_hand_y
    cfg = calibration_manager.config.get("scroll", {})

    idx_angle_raw = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8])
    mid_angle_raw = util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12])
    ring_angle_raw = util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16])
    pinky_angle_raw = util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20])
    

    current_y_raw = landmark_list[0][1]

    idx_history.append(idx_angle_raw)
    mid_history.append(mid_angle_raw)
    ring_history.append(ring_angle_raw)
    pinky_history.append(pinky_angle_raw)
    y_history.append(current_y_raw)
    
    if len(idx_history) < HISTORY_LENGTH:
        prev_hand_y = None
        return False, 0
        
    idx_angle = statistics.mean(idx_history)
    mid_angle = statistics.mean(mid_history)
    ring_angle = statistics.mean(ring_history)
    pinky_angle = statistics.mean(pinky_history)
    
    idx_std = statistics.stdev(idx_history)
    mid_std = statistics.stdev(mid_history)
    ring_std = statistics.stdev(ring_history)
    pinky_std = statistics.stdev(pinky_history)
    
    stability_max = cfg.get("stability_std_max", 35)
    
    is_stable = (idx_std < stability_max and mid_std < stability_max and
                 ring_std < stability_max and pinky_std < stability_max)

    is_peace_sign = (
            is_stable and
            idx_angle > cfg.get("idx_angle_min", 90) and
            mid_angle > cfg.get("mid_angle_min", 90) and
            ring_angle < cfg.get("ring_angle_max", 50) and
            pinky_angle < cfg.get("pinky_angle_max", 50)
    )

    scale = util.get_hand_scale(landmark_list)
    dist_8_12 = util.get_raw_dist(landmark_list[8], landmark_list[12]) / scale
    if dist_8_12 < 0.2:
        is_peace_sign = False

    is_frozen = cursor_movement.is_frozen(landmark_list)
    scroll_amount = 0

    if is_peace_sign and not is_frozen:

        current_hand_y = statistics.mean(y_history)
        
        if prev_hand_y is not None:
            delta_y = current_hand_y - prev_hand_y
            
            if abs(delta_y) > 0.005:
                scroll_amount = int(-delta_y * 3500)
                prev_hand_y = current_hand_y
        else:
            prev_hand_y = current_hand_y
    else:
        prev_hand_y = None
        
    return is_peace_sign, scroll_amount
