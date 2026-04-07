import calculo_distancia as util
import pyautogui
import random

def is_screenshot(landmark_list):
    # A Peace Sign (Index and Middle straight, Ring and Pinky bent) 
    # prevents clashing with double clicks and dragging gestures.
    return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
            util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) < 50
    )

def take_screenshot():
    im1 = pyautogui.screenshot()
    label = random.randint(1, 1000)
    im1.save(f'my_screenshot_{label}.png')