import calculo_distancia as util
from pynput.mouse import Button

def is_right_click(landmark_list, thumb_index_dist):
    return (
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90  and
            thumb_index_dist > 50
    )

def perform_click(mouse):
    mouse.press(Button.right)
    mouse.release(Button.right)