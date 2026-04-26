import calculo_distancia as util
import calibration_manager
import cursor_movement

prev_fingers_y = None

def detect_scroll(landmark_list):
    global prev_fingers_y
    cfg = calibration_manager.config.get("scroll", {})

    is_peace_sign = (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 55 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 55 and
            util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < cfg.get("ring_angle_max", 50) and
            util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < cfg.get("pinky_angle_max", 50)
    )

    is_frozen = cursor_movement.is_frozen(landmark_list)
    scroll_amount = 0

    if is_peace_sign and not is_frozen:
        current_fingers_y = (landmark_list[8][1] + landmark_list[12][1]) / 2.0
        
        if prev_fingers_y is not None:
            delta_y = current_fingers_y - prev_fingers_y
            
            if abs(delta_y) > 0.01:
                scroll_amount = int(-delta_y * 2500)
                prev_fingers_y = current_fingers_y
        else:
            prev_fingers_y = current_fingers_y
    else:
        prev_fingers_y = None
        
    return is_peace_sign, scroll_amount
