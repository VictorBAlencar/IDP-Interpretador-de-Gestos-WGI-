import calculo_distancia as util
from pynput.mouse import Button

def is_left_click(landmark_list, thumb_index_dist, is_dragging=False):
    if is_dragging:
        return (
                util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 160 and
                util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 40
        )
    else:
        return (
                util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
                util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
                thumb_index_dist > 50
        )

def hold_click(mouse):
    mouse.press(Button.left)

def release_click(mouse):
    mouse.release(Button.left)

def perform_click(mouse):
    mouse.press(Button.left)
    mouse.release(Button.left)