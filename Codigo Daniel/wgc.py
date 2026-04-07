import cv2
import mediapipe as mp
import pyautogui
import random
import time
import calculo_distancia as util
from pynput.mouse import Controller
import cursor_movement
import left_click
import right_click
import double_click
import screenshot

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
mouse = Controller()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85,
    max_num_hands=1
)

last_click_time = 0
click_cooldown = 0.5 
is_dragging = False
drag_start_time = 0
last_left_click_detected_time = 0


def detect_gesture(frame, landmark_list, processed):
    global last_click_time, is_dragging, drag_start_time, last_left_click_detected_time

    current_time = time.time()

    if len(landmark_list) >= 21:
        hand_landmarks = processed.multi_hand_landmarks[0]
        palm_center = cursor_movement.get_palm_center(hand_landmarks)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        left_clicking = left_click.is_left_click(landmark_list, thumb_index_dist, is_dragging)
        if left_clicking:
            last_left_click_detected_time = current_time
        right_clicking = right_click.is_right_click(landmark_list, thumb_index_dist)
        double_clicking = double_click.is_double_click(landmark_list, thumb_index_dist)
        screenshotting = screenshot.is_screenshot(landmark_list)
        
        any_click_intent = left_clicking or right_clicking or double_clicking or screenshotting

        index_is_straight = util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90
        
        is_actually_dragging = is_dragging and (current_time - drag_start_time > 0.25)
        if (index_is_straight and not any_click_intent and not is_dragging) or (is_actually_dragging and left_clicking):
            cursor_movement.move_mouse(palm_center)
        
        if left_clicking:
            if not is_dragging:
                left_click.hold_click(mouse)
                is_dragging = True
                drag_start_time = current_time
                
            if is_actually_dragging:
                cv2.putText(frame, "Dragging", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            if is_dragging:
                # 2 segundos para liberar dragging
                if current_time - last_left_click_detected_time > 0.2:
                    left_click.release_click(mouse)
                    is_dragging = False
                    last_click_time = current_time
                else:
                    if is_actually_dragging:
                        cv2.putText(frame, "Dragging", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if not is_dragging and current_time - last_click_time > click_cooldown:
                if right_clicking:
                    right_click.perform_click(mouse)
                    cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    last_click_time = current_time
                elif double_clicking:
                    double_click.perform_click()
                    cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    last_click_time = current_time
                elif screenshotting:
                    screenshot.take_screenshot()
                    cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    last_click_time = current_time
    else:
        # Sair drag click
        if is_dragging and current_time - last_left_click_detected_time > 0.2:
            left_click.release_click(mouse)
            is_dragging = False
            last_click_time = current_time

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0] 
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()