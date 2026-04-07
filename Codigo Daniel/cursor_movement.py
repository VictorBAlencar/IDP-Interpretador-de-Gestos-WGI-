import pyautogui
import numpy as np
from pynput.mouse import Controller

mouse = Controller()

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0
smoothening = 5 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_palm_center(hand_landmarks):
    points = [0, 5, 9, 13, 17]
    avg_x = sum(hand_landmarks.landmark[i].x for i in points) / len(points)
    avg_y = sum(hand_landmarks.landmark[i].y for i in points) / len(points)
    return Point(avg_x, avg_y)

def move_mouse(palm_center):
    global prev_x, prev_y
    if palm_center is not None:
        boundary = 0.25 
        x = np.interp(palm_center.x, [boundary, 1 - boundary], [0, screen_width])
        y = np.interp(palm_center.y, [boundary, 1 - boundary], [0, screen_height])
        
        curr_x = prev_x + (x - prev_x) / smoothening
        curr_y = prev_y + (y - prev_y) / smoothening

        mouse.position = (curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y